# Paso 1: Usar una imagen base oficial de Python.
# python:3.9-slim es una buena opción porque es ligera.
FROM python:3.9-slim

# Paso 2: Establecer el directorio de trabajo dentro del contenedor.
# Todo lo que hagamos de ahora en adelante será dentro de esta carpeta.
WORKDIR /app

# Paso 3: Isntalamos Tesseract-ocr y el idioma español del mismo.
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libgl1-mesa-glx \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Paso 4: Copiar el archivo de dependencias
COPY requirements.txt .

# Paso 5: Instalar las dependencias.

RUN pip install --no-cache-dir -r requirements.txt

# Paso 6: Copiar todos los archivos de tu proyecto al directorio de trabajo del contenedor.
COPY . .

# Paso 7: Exponer el puerto que usa Streamlit.
EXPOSE 8501

# Paso 8: El comando para ejecutar la aplicación cuando el contenedor se inicie.
# Se usa --server.address=0.0.0.0 para que Streamlit sea accesible desde fuera del contenedor.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
