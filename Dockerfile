# Imagen base ligera de Python 3.13
FROM python:3.13-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Variables de entorno recomendadas para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Instalar dependencias del sistema si fueran necesarias (compatibilidad con Pillow, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente completo
COPY . .

# Crear carpetas para archivos de medios si no existen
RUN mkdir -p /app/files/imagenes

# Puerto expuesto por el contenedor
EXPOSE 8000

# Comando por defecto: aplicar migraciones y levantar servidor de desarrollo
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
