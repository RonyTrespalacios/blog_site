# Usar una imagen base de Python 3.9
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requisitos y luego instalarlos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Especificar el comando por defecto que se ejecutará en el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]