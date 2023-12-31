FROM python:3.10.13-slim-bullseye

EXPOSE 8001

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a virtual environment
RUN python -m venv /opt/venv


# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /alert_service

COPY requirements.txt /alert_service/requirements.txt

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

RUN python manage.py makemigrations && python ./manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')" && python manage.py migrate

# Collect static files
# RUN /opt/venv/bin/python manage.py collectstatic --noinput

# CMD ["python","manage.py","runserver","0.0.0.0:8001"]