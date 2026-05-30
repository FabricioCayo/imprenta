#!/usr/bin/env bash
# Render build script - se ejecuta al desplegar el codigo

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
