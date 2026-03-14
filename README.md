<div align="center">

# 📋 Registro de Contacto — Flask + PostgreSQL

**Aplicación web fullstack de registro de contactos con backend en Python**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Fetch_API-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/API/Fetch_API)
[![HTML5](https://img.shields.io/badge/HTML5-Jinja2-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://jinja.palletsprojects.com/)

> Proyecto educativo que demuestra cómo construir un servidor web en Python con **Flask + Jinja2**,  
> conectar una base de datos **PostgreSQL**, y comunicar frontend y backend de forma asíncrona con **Fetch API**.

</div>

---

## 🧠 ¿Qué hace esta aplicación?

Permite registrar y consultar contactos a través de un formulario web. El frontend envía los datos de forma asíncrona (sin recargar la página) y el backend los valida, guarda en PostgreSQL y responde con JSON.

**Flujo completo:**

```
Usuario llena el formulario
        ↓
Fetch API envía JSON al servidor (POST /formulario)
        ↓
Flask valida los datos y ejecuta INSERT en PostgreSQL
        ↓
Servidor responde con { mensaje, id } → código 201
        ↓
El formulario muestra alerta de éxito y se limpia
```

---

## 🛣️ Rutas de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Sirve el formulario HTML (`index.html`) |
| `POST` | `/formulario` | Recibe datos JSON y guarda el contacto en la BD |
| `GET` | `/ver-contactos` | Devuelve todos los contactos ordenados por fecha |

---

## 📦 Estructura del proyecto

```
registro-contacto/
│
├── app.py               # Servidor Flask — rutas, lógica y conexión a PostgreSQL
├── requirements.txt     # Dependencias Python del proyecto
├── README.md            # Documentación
│
├── templates/
│   └── index.html       # Formulario HTML con Fetch API integrado
│
└── static/
    └── styles.css       # Estilos del formulario
```

---

## ⚙️ Tecnologías utilizadas

| Área | Tecnología | Uso |
|------|------------|-----|
| Backend | Python + Flask | Servidor web y manejo de rutas |
| Templates | Jinja2 | Renderizado del HTML desde Flask |
| Base de datos | PostgreSQL | Almacenamiento de contactos |
| Conector BD | psycopg2 | Driver Python para PostgreSQL |
| Frontend | HTML5 + CSS3 | Estructura y estilos del formulario |
| Comunicación | Fetch API (JS) | Envío asíncrono sin recargar la página |

---

## 🗄️ Esquema de la base de datos

```sql
CREATE TABLE contactos (
    id        SERIAL PRIMARY KEY,
    nombre    VARCHAR(100) NOT NULL,
    apellido  VARCHAR(100),
    direccion VARCHAR(200),
    telefono  VARCHAR(20),
    correo    VARCHAR(150) NOT NULL,
    mensaje   TEXT,
    creado    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Instalación y puesta en marcha

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/registro-contacto.git
cd registro-contacto
```

### 2. Crear y activar el entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> Si no tienes `requirements.txt`, instala manualmente:
> ```bash
> pip install flask psycopg2-binary
> ```

### 4. Configurar la base de datos

Abre `app.py` y ajusta las credenciales de conexión:

```python
DB_CONFIG = {
    'host':     'localhost',
    'database': 'diseño',     # ← nombre de tu base de datos
    'user':     'postgres',   # ← tu usuario
    'password': '123456',     # ← tu contraseña
    'port':     5432
}
```

Luego crea la tabla ejecutando el SQL del esquema de arriba en tu cliente PostgreSQL (pgAdmin, DBeaver o `psql`).

### 5. Ejecutar el servidor

```bash
python app.py
```

### 6. Abrir en el navegador

```
http://localhost:5000
```

---

## 🔌 Ejemplo de uso — Fetch API

El formulario usa `fetch` para enviar los datos como JSON al backend:

```javascript
const respuesta = await fetch('/formulario', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ nombre, apellido, correo, ... })
});

const resultado = await respuesta.json();
// { mensaje: 'Contacto guardado exitosamente', id: 5 }
```

---

## 📡 Respuestas de la API

**POST `/formulario`** — éxito:
```json
{
    "mensaje": "Contacto guardado exitosamente",
    "id": 5
}
```
**Código:** `201 Created`

---

**POST `/formulario`** — error de validación:
```json
{
    "error": "Nombre y correo son obligatorios"
}
```
**Código:** `400 Bad Request`

---

**GET `/ver-contactos`** — respuesta:
```json
[
    {
        "id": 5,
        "nombre": "Juan",
        "apellido": "Pérez",
        "correo": "juan@ejemplo.com",
        "telefono": "3001234567",
        "direccion": "Calle 10 # 5-20",
        "mensaje": "Hola, me interesa el servicio",
        "creado": "2025-03-14 10:30:00"
    }
]
```
**Código:** `200 OK`

---

## 📌 Estado del proyecto

| Funcionalidad | Estado |
|---------------|--------|
| Formulario HTML | ✅ Completo |
| Envío asíncrono con Fetch | ✅ Completo |
| Validación de campos | ✅ Completo |
| Guardado en PostgreSQL | ✅ Completo |
| Consulta de contactos (`/ver-contactos`) | ✅ Completo |
| Alerta de éxito / error | ✅ Completa |
| Manejo de errores en backend | ✅ Completo |
| Variables de entorno (`.env`) | 🔧 Pendiente |
| Autenticación / panel de admin | 🔧 Pendiente |

---

## 💡 Conceptos que aprenderás con este proyecto

- Crear un servidor web con **Flask** y definir rutas `GET` / `POST`
- Renderizar plantillas HTML con **Jinja2**
- Conectar Python a **PostgreSQL** usando `psycopg2`
- Recibir y procesar datos **JSON** en el backend con `request.get_json()`
- Usar `RealDictCursor` para recibir resultados como diccionarios
- Comunicar frontend y backend de forma **asíncrona** con **Fetch API**
- Manejar errores y responder con **códigos HTTP** apropiados (`201`, `400`, `500`)

---

<div align="center">
  Hecho con 🐍 + 🐘 · Proyecto educativo fullstack · 2025
</div>
