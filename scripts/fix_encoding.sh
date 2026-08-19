#!/bin/bash
set -e

echo "1. Recreating database with utf8mb4..."
mariadb -e "DROP DATABASE IF EXISTS django_fondation; CREATE DATABASE django_fondation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; GRANT ALL PRIVILEGES ON django_fondation.* TO 'django_user'@'localhost'; FLUSH PRIVILEGES;"

echo "2. Importing SQL with utf8mb4..."
mariadb --default-character-set=utf8mb4 -u django_user -pFondationSecurePass2026! django_fondation < /var/www/django-fondation/django_fondation.sql

echo "3. Running migrations..."
cd /var/www/django-fondation
./venv/bin/python manage.py migrate

echo "4. Restarting service..."
systemctl restart django-fondation

echo "5. Checking encoding in database..."
mariadb -u django_user -pFondationSecurePass2026! django_fondation -e "SELECT id, title, title_fr FROM core_contentitem LIMIT 5;"
