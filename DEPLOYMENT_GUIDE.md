# 🚀 Guide Complet de Déploiement Django & CI/CD Automatique

Ce guide vous accompagne pour déployer votre projet Django sur votre VPS (**fondation.sdbo.ma**) et activer le **déploiement automatique à chaque `git push`** via GitHub Actions.

---

## 📋 Table des Matières
1. [Étape 1 : Initialiser et Pousser sur GitHub](#1-initialiser-et-pousser-sur-github)
2. [Étape 2 : Préparer le Serveur VPS Linux (Ubuntu / Debian)](#2-préparer-le-serveur-vps-linux)
3. [Étape 3 : Configurer les GitHub Secrets (CI/CD)](#3-configurer-les-github-secrets)
4. [Étape 4 : Tester le Déploiement Automatique](#4-tester-le-déploiement-automatique)

---

## 1. Initialiser et Pousser sur GitHub

1. Créez un nouveau dépôt vide sur votre compte [GitHub](https://github.com/new) (nommé par exemple `django-fondation`), sans cocher README ni .gitignore (ils sont déjà prêts dans votre projet).
2. Dans votre terminal local (dans le dossier `c:\Projects\django-fondation`), exécutez :

```bash
# Vérifier l'état et ajouter les fichiers
git init
git branch -M main
git add .
git commit -m "feat: initial commit - Django configuration and CI/CD setup"

# Lier à votre dépôt GitHub
git remote add origin git@github.com:othmanbakkali/fondation.git
git push -u origin main
```

---

## 2. Préparer le Serveur VPS Linux

Connectez-vous à votre serveur VPS en SSH :
```bash
ssh root@198.199.75.86
# ou si votre utilisateur est ubuntu :
# ssh ubuntu@198.199.75.86
```

### A. Installer les paquets requis
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git nginx mysql-server certbot python3-certbot-nginx libmysqlclient-dev pkg-config build-essential
```

### B. Cloner le projet dans `/var/www/django-fondation`
```bash
sudo mkdir -p /var/www/django-fondation
sudo chown -R $USER:$USER /var/www/django-fondation

# Cloner votre dépôt
git clone https://github.com/othmanbakkali/fondation.git /var/www/django-fondation
cd /var/www/django-fondation

# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

### C. Configurer les variables d'environnement (.env)
```bash
cp .env.example .env
nano .env
```
Renseignez les vraies informations de production :
- `DEBUG=False`
- `SECRET_KEY=votre_cle_secrete_ultra_securisee`
- `ALLOWED_HOSTS=fondation.sdbo.ma,www.fondation.sdbo.ma,127.0.0.1,localhost`
- `CSRF_TRUSTED_ORIGINS=https://fondation.sdbo.ma,http://fondation.sdbo.ma`
- `DB_NAME=django_fondation`
- `DB_USER=django_user`
- `DB_PASSWORD=mot_de_passe_mysql`
- `DB_HOST=127.0.0.1`

### D. Importer la Base de Données et Collecter les Statiques
```bash
# Si la base MySQL n'est pas encore créée :
sudo mysql -e "CREATE DATABASE IF NOT EXISTS django_fondation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'django_user'@'localhost' IDENTIFIED BY 'mot_de_passe_mysql';"
sudo mysql -e "GRANT ALL PRIVILEGES ON django_fondation.* TO 'django_user'@'localhost'; FLUSH PRIVILEGES;"

# Importer vos données initiales depuis le fichier SQL :
mysql -u django_user -p django_fondation < django_fondation.sql

# Exécuter les migrations et collectstatic
python manage.py migrate
python manage.py collectstatic --noinput
```

### E. Activer le Service Systemd (Gunicorn)
```bash
# Copier le fichier de service
sudo cp systemd/django-fondation.service /etc/systemd/system/django-fondation.service

# Ajuster l'utilisateur si nécessaire dans le fichier de service
# Recharger et démarrer
sudo systemctl daemon-reload
sudo systemctl start django-fondation
sudo systemctl enable django-fondation

# Vérifier le statut
sudo systemctl status django-fondation
```

### F. Configurer Nginx et le Certificat SSL HTTPS
```bash
# Copier la configuration Nginx
sudo cp nginx/fondation.sdbo.ma.conf /etc/nginx/sites-available/fondation.sdbo.ma
sudo ln -s /etc/nginx/sites-available/fondation.sdbo.ma /etc/nginx/sites-enabled/

# Tester la configuration Nginx
sudo nginx -t

# Redémarrer Nginx
sudo systemctl restart nginx

# Installer le certificat SSL HTTPS gratuit Let's Encrypt
sudo certbot --nginx -d fondation.sdbo.ma -d www.fondation.sdbo.ma
```

### G. Autoriser le redémarrage sans mot de passe pour le CI/CD
Pour permettre à GitHub Actions de redémarrer Gunicorn lors du déploiement automatique :
```bash
sudo visudo
```
Ajoutez cette ligne tout en bas (remplacez `ubuntu` par votre nom d'utilisateur SSH) :
```text
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart django-fondation, /bin/systemctl reload django-fondation
```

---

## 3. Configurer les GitHub Secrets

Sur votre page de dépôt GitHub :
1. Allez dans **Settings** > **Secrets and variables** > **Actions**.
2. Cliquez sur **New repository secret** et ajoutez :

| Nom du Secret | Description | Exemple de Valeur |
|---|---|---|
| `SERVER_HOST` | IP ou nom de domaine du VPS | `fondation.sdbo.ma` |
| `SERVER_USER` | Utilisateur SSH de connexion | `ubuntu` ou `root` |
| `SSH_PRIVATE_KEY` | Votre clé privée SSH (le contenu complet de `~/.ssh/id_ed25519` ou `~/.ssh/id_rsa`) | `-----BEGIN OPENSSH PRIVATE KEY----- ...` |
| `SERVER_PORT` | Port SSH (optionnel, 22 par défaut) | `22` |
| `PROJECT_PATH` | Chemin du projet sur le serveur | `/var/www/django-fondation` |

---

## 4. Tester le Déploiement Automatique 🚀

Dès que vos secrets sont configurés :
1. Effectuez n'importe quelle modification dans votre code en local.
2. Poussez vers GitHub :
   ```bash
   git add .
   git commit -m "test: test auto deployment"
   git push origin main
   ```
3. Rendez-vous sur l'onglet **Actions** de votre dépôt GitHub : vous verrez le workflow s'exécuter en quelques secondes.
4. Votre site sur **https://fondation.sdbo.ma** est automatiquement mis à jour sans coupure !
