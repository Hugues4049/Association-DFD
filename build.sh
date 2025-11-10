#!/usr/bin/env bash
# build.sh

set -o errexit  # Arrête le script en cas d'erreur

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --no-input

# Appliquer les migrations
python manage.py migrate
