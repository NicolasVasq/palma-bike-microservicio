# Imagen base ligera de Python 3.13 sobre Alpine Linux
FROM python:3.13-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Variables de entorno recomendadas para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Instalar dependencias del sistema necesarias para compilar Pillow y otros paquetes
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    && apk add --no-cache \
    curl \
    libjpeg-turbo \
    zlib

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente completo
COPY . .

# Crear carpetas para archivos de medios si no existen
RUN mkdir -p /app/files/imagenes

# Limpiar dependencias de compilación para reducir superficie de ataque
RUN apk del .build-deps

# Puerto expuesto por el contenedor
EXPOSE 8000

# Comando por defecto: aplicar migraciones y levantar servidor de desarrollo
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
