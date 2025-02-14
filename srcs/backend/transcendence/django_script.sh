#!/bin/bash

# Collect static files
echo "Collect static files"
python ./transcendence/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python ./transcendence/manage.py makemigrations
python ./transcendence/manage.py migrate

python ./transcendence/manage.py createsuperuser --username=admin --email=admin@example.com --noinput


mkdir -p certs
if [ ! -f "certs/cert.pem" ]; then
    openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
    echo "✅ Certificat auto-signé généré."
fi


# Start server
echo "Starting server"
#python ./transcendence/manage.py runserver 0.0.0.0:8000
python ./transcendence/manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:8000