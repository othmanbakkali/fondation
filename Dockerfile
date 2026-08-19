# Dockerfile pour Django Production
FROM python:3.11-slim

# Eviter l'écriture de fichiers .pyc et activer le mode non-bufferisé pour les logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système pour MySQL et compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le code du projet
COPY . /app/

# Exposer le port gunicorn
EXPOSE 8000

# Commande par défaut pour lancer gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "config.wsgi:application"]
