FROM python:3.8-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends locales locales-all git curl python3-dev build-essential gnupg2 libmagic1 python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info wget cabextract && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python && \
    cd /usr/local/bin && \
    ln -s /etc/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN wget https://gist.githubusercontent.com/maxwelleite/913b6775e4e408daa904566eb375b090/raw/ttf-ms-tahoma-installer.sh -q -O - | bash

# Copy in the config files:
COPY pyproject.toml poetry.lock ./
# Install only dependencies:
RUN poetry install --no-root --no-dev

# Copy in everything else and install:
COPY . .

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080
# ENV ENV_TYPE staging
# Setting this ensures print statements and log messages
# promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE
ENV PYTHONDONTWRITEBYTECODE 1

ARG ENV_GCP_SECRET_NAME 
ENV ENV_GCP_SECRET_NAME=$ENV_GCP_SECRET_NAME

ARG ENV_TYPE
ENV ENV_TYPE=$ENV_TYPE

RUN ENV_TYPE=$ENV_TYPE COLLECT_STATIC=1 python manage.py collectstatic --noinput

# Gunicorn as app server
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 descartapp.wsgi:application
