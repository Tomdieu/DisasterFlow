FROM python:3.10.13-slim-bullseye

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory to /app
WORKDIR /emergency_responder

COPY requirements.txt /emergency_responder/requirements.txt


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libgeos-dev \
    libproj-dev \
    gdal-bin \
    libsqlite3-mod-spatialite \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . .

EXPOSE 8002

RUN python manage.py makemigrations && python ./manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')" && python manage.py migrate