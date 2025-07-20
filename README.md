# Extractor y Gestor de Datos de Escrituras
Este proyecto es una aplicación robusta para la extracción, edición y gestión de datos clave de escrituras mediante una combinación de OCR avanzado (Tesseract) y procesamiento de lenguaje natural con Inteligencia Artificial (OpenAI). Los datos extraídos se almacenan de forma local en una base de datos MongoDB y se presentan a través de una interfaz interactiva desarrollada con Streamlit, facilitando la consulta y edición.

## Características Principales
### Extracción Inteligente de Datos:

Utiliza Pytesseract para realizar un Reconocimiento Óptico de Caracteres (OCR) de alta precisión sobre las imágenes de las escrituras.

Implementa LangChain y OpenAI para procesar el texto extraído, identificar y estructurar los datos relevantes en un formato Pydantic predefinido, asegurando consistencia y facilidad de uso.

### Gestión de Datos Local:

Almacena todos los datos extraídos y editados en una base de datos MongoDB local, garantizando la persistencia y disponibilidad de la información.

### Interfaz de Usuario Intuitiva via Streamlit:

Ofrece una aplicación web simple y fácil de usar, construida con Streamlit, que permite interactuar con el sistema sin necesidad de conocimientos técnicos avanzados.

### Consulta por Número de Carpeta:

Permite a los usuarios buscar y recuperar datos de escrituras específicas utilizando un número de carpeta asignado, agilizando el acceso a la información.

### Edición de Datos Extraídos:

Ofrece la funcionalidad de editar los datos extraídos directamente desde la interfaz de Streamlit, permitiendo corregir errores de OCR o ajustar la información según sea necesario.

## Tecnologías Utilizadas
- Python 3.9+
- Tesseract OCR
- Streamlit
- Pytesseract
- LangChain
- OpenAI API
- PyMongo (para interacción con MongoDB)
- Pydantic
- Docker & Docker Compose

## Configuración y Ejecución Local
Para poner en marcha esta aplicación en tu máquina, solo necesitas tener Docker Desktop (o el motor de Docker y Docker Compose CLI) instalado.

### Clonar el Repositorio:

```Bash
git clone https://github.com/bjrompal/escrituras-analizador.git
cd escrituras-analizador
```

### Configurar Variables de Entorno:

Este proyecto utiliza una clave de API de OpenAI para el procesamiento de lenguaje natural.

Crea un archivo llamado .env en la raíz del proyecto (al mismo nivel que docker-compose.yml) y añade tus variables.

Puedes usar el archivo .env.example como guía:

```Bash
cp .env.example .env
```

Edita el archivo .env y rellena tu clave de OpenAI:

¡Importante! El archivo .env está en .gitignore para asegurar que tus claves secretas nunca se suban a GitHub.

## Iniciar la Aplicación con Docker Compose:

Desde la raíz del proyecto, ejecuta el siguiente comando. Esto construirá la imagen de tu aplicación, descargará la imagen de MongoDB y levantará ambos servicios.

```bash
docker-compose up --build
```

La primera vez tardará un poco más ya que Docker necesita descargar las imágenes base e instalar todas las dependencias.

## Acceder a la Aplicación:

Una vez que los contenedores estén en funcionamiento, la aplicación Streamlit estará accesible en tu navegador web.

Abre tu navegador y ve a: http://localhost:8501 (o el puerto que hayas configurado si lo modificaste).

📄 Licencia
Este proyecto está bajo la Licencia MIT. 

