#!/usr/bin/env bash
set -e

echo "========================================="
echo " Starting Automated Deployment for Django"
echo " Date: $(date)"
echo "========================================="

# 1. Aller dans le répertoire du projet
PROJECT_DIR="${1:-/var/www/django-fondation}"
cd "$PROJECT_DIR"

# 2. Récupérer la dernière version depuis GitHub
echo "-> Fetching latest changes from Git (main)..."
git fetch origin main
git reset --hard origin/main

# 3. Activer l'environnement virtuel
if [ -d "venv" ]; then
    echo "-> Activating virtual environment (venv)..."
    source venv/bin/activate
elif [ -d "../venv" ]; then
    echo "-> Activating virtual environment (../venv)..."
    source ../venv/bin/activate
else
    echo "-> Creating new virtual environment in venv..."
    python3 -m venv venv
    source venv/bin/activate
fi

# 4. Installer / Mettre à jour les dépendances
echo "-> Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Appliquer les migrations de la base de données
echo "-> Running database migrations..."
python manage.py migrate --noinput

# 6. Rassembler les fichiers statiques
echo "-> Collecting static files..."
python manage.py collectstatic --noinput

# 7. Compiler les traductions (si gettext est disponible)
if command -v msgfmt >/dev/null 2>&1; then
    echo "-> Compiling translation messages..."
    python manage.py compilemessages || true
fi

# 8. Redémarrer le service Gunicorn / Django
echo "-> Restarting Gunicorn service..."
sudo systemctl restart django-fondation || sudo systemctl restart gunicorn

echo "========================================="
echo " Deployment Completed Successfully! 🚀"
echo "========================================="
