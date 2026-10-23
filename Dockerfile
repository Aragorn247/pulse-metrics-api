# Usamos una imagen oficial y ligera de Python
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Definimos el PYTHONPATH para que Python reconozca siempre los módulos raíz
ENV PYTHONPATH=/app

# Instalamos dependencias del sistema necesarias para compilar paquetes si hiciese falta
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del proyecto
COPY . .

# Exponemos el puerto de FastAPI
EXPOSE 8000