#!/bin/bash

# Collect static files
echo "Collect static files"
python ./transcendence/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python ./transcendence/manage.py makemigrations
python ./transcendence/manage.py migrate

python ./transcendence/manage.py createsuperuser --username=admin --email=admin@example.com --noinput

# Start server
echo "Starting server"
python ./transcendence/manage.py runserver 0.0.0.0:8000