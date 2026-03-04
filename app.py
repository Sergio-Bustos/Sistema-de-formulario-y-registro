# Registro de Contacto - Backend

# Este archivo es el servidor principal de la aplicación. Se encarga de
# recibir los datos del formulario, guardarlos en la base de datos, y
# también de mostrarlos cuando se necesiten consultar.
#
# Tiene tres rutas:
#   /              → carga el formulario HTML en el navegador
#   /formulario    → recibe los datos del formulario y los guarda (POST)
#   /ver-contactos → devuelve todos los contactos registrados (GET)
#
# El frontend manda los datos como JSON usando fetch, así que acá
# se usa request.get_json() en vez de request.form para leerlos.
# La base de datos es PostgreSQL y los contactos se guardan en la tabla "contactos".
# Versión: 2.0


# Importaciones necesarias para que todo funcione
from flask import Flask, jsonify, render_template, request
import psycopg2                              # Es el conector que nos permite hablar con PostgreSQL
from psycopg2.extras import RealDictCursor   # Con esto los resultados de las consultas llegan como diccionarios, no como tuplas
from datetime import datetime                # Lo tenemos disponible por si en algún momento necesitamos trabajar con fechas


# Creamos la instancia principal de Flask, que es básicamente la aplicación
app = Flask(__name__)


# Datos de conexión a la base de datos
# Si cambias el entorno (producción, staging, etc.) este es el lugar donde hay que actualizar las credenciales
DB_CONFIG = {
    'host':     'localhost',
    'database': 'diseño',
    'user':     'postgres',
    'password': '123456',
    'port':     5432
}


def conectar_bd():
    """
    Intenta conectarse a la base de datos usando los datos de DB_CONFIG.
    Si la conexión falla por cualquier motivo, imprime el error en consola
    y devuelve None para que quien llame a esta función sepa que algo salió mal.
    """
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"[ERROR] Conexión a la base de datos fallida: {e}")
        return None


@app.route('/')
def inicio():
    """
    Esta es la ruta raíz. Cuando alguien entra a la aplicación por primera vez,
    lo que hace es servir el formulario HTML que está en templates/index.html.
    Nada más, simple y directo.
    """
    return render_template('index.html')


@app.route('/formulario', methods=['POST'])
def guardar_contacto():
    """
    Aquí llegan los datos del formulario cuando el usuario le da clic a "enviar".
    El frontend los manda como JSON mediante fetch, así que los leemos con get_json().

    Lo que esperamos recibir en el cuerpo de la petición:
        {
            "nombre":    "...",
            "apellido":  "...",
            "direccion": "...",
            "telefono":  "...",
            "correo":    "...",
            "mensaje":   "..."   <- este es opcional
        }

    Si todo sale bien devuelve un JSON con el id del nuevo contacto y código 201.
    Si algo falla (datos inválidos, problema de conexión, etc.) devuelve un error descriptivo.
    """
    conexion = None   # Iniciamos en None para poder cerrar de forma segura en el bloque finally
    cursor   = None

    try:
        # Intentamos leer el cuerpo como JSON. Con silent=True no explota si el body viene mal formado,
        # simplemente devuelve None y lo manejamos nosotros en el siguiente if
        datos = request.get_json(silent=True)

        if datos is None:
            # Si llegamos acá, el cliente mandó algo que no era JSON válido
            return jsonify({'error': 'El cuerpo de la petición debe ser JSON válido'}), 400

        # Sacamos cada campo del JSON y le quitamos los espacios de los extremos con strip()
        # Si un campo no viene en el JSON, get() devuelve una cadena vacía por defecto
        nombre    = datos.get('nombre',    '').strip()
        apellido  = datos.get('apellido',  '').strip()
        direccion = datos.get('direccion', '').strip()
        telefono  = datos.get('telefono',  '').strip()
        correo    = datos.get('correo',    '').strip()
        mensaje   = datos.get('mensaje',   '').strip()

        # Validamos que al menos nombre y correo vengan llenos, ya que son los campos mínimos obligatorios
        if not nombre or not correo:
            return jsonify({'error': 'Nombre y correo son obligatorios'}), 400

        # Abrimos la conexión a la base de datos
        conexion = conectar_bd()
        if conexion is None:
            # Si no pudimos conectar, no tiene sentido seguir
            return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500

        # Creamos el cursor y ejecutamos el INSERT
        # El RETURNING id al final nos devuelve directamente el id que PostgreSQL le asignó al nuevo registro
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO contactos (nombre, apellido, direccion, telefono, correo, mensaje)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (nombre, apellido, direccion, telefono, correo, mensaje))

        # fetchone() trae la primera (y única) fila que retornó el RETURNING, y [0] saca el id de ahí
        contacto_id = cursor.fetchone()[0]

        # Confirmamos la transacción para que el INSERT quede guardado de verdad
        conexion.commit()

        # Todo salió bien, devolvemos el mensaje de éxito junto con el id del nuevo contacto
        return jsonify({
            'mensaje': 'Contacto guardado exitosamente',
            'id': contacto_id
        }), 201

    except Exception as e:
        # Si llegamos acá es porque algo inesperado pasó durante el proceso
        print(f"[ERROR] No se pudo guardar el contacto: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

    finally:
        # Esto se ejecuta siempre, sin importar si hubo error o no
        # Cerramos el cursor y la conexión para no dejar recursos colgados
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


@app.route('/ver-contactos', methods=['GET'])
def ver_contactos():
    """
    Devuelve todos los contactos que hay en la base de datos.
    Los trae ordenados del más reciente al más antiguo usando la columna 'creado'.
    Cada contacto viene como un objeto JSON con todos sus campos.
    """
    conexion = None
    cursor   = None

    try:
        # Conectamos a la base de datos
        conexion = conectar_bd()
        if conexion is None:
            return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500

        # Usamos RealDictCursor para que cada fila llegue como un diccionario del tipo {'nombre': 'Juan', ...}
        # En lugar de una tupla como ('Juan', ...) que sería más difícil de trabajar
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, nombre, apellido, direccion, telefono, correo, mensaje, creado
            FROM contactos
            ORDER BY creado DESC;
        """)
        contactos = cursor.fetchall()

        # La columna 'creado' viene como objeto datetime de Python, así que la convertimos
        # a un string legible con el formato YYYY-MM-DD HH:MM:SS para que el JSON lo pueda serializar
        for contacto in contactos:
            if contacto['creado']:
                contacto['creado'] = contacto['creado'].strftime('%Y-%m-%d %H:%M:%S')

        # Devolvemos la lista completa de contactos como JSON
        return jsonify(contactos), 200

    except Exception as e:
        print(f"[ERROR] No se pudieron obtener los contactos: {e}")
        return jsonify({'error': 'Error al obtener contactos'}), 500

    finally:
        # Igual que en la ruta anterior, cerramos todo siempre
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


# Punto de entrada cuando ejecutamos el archivo directamente con python app.py
# debug=True activa el modo de desarrollo (recarga automática, mensajes de error detallados)
# host='0.0.0.0' hace que el servidor sea accesible desde otras máquinas en la red, no solo desde localhost
if __name__ == '__main__':
    print("Iniciando servidor Flask en http://localhost:5000 ...")
    app.run(debug=True, host='0.0.0.0', port=5000)