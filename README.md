# Fondation - Plateforme Web & Dashboard

Plateforme web multilingue (Français, Arabe, Anglais) avec espace public et tableau de bord d'administration pour la Fondation.

## 🌐 Déploiement Production
- **URL du site** : [https://fondation.sdbo.ma](https://fondation.sdbo.ma)
- **CI/CD** : Déploiement automatique sur chaque push vers la branche `main` via GitHub Actions.

## 🚀 Démarrage Rapide en Local

### 1. Cloner le projet
```bash
git clone git@github.com:othmanbakkali/fondation.git
cd fondation
```

### 2. Créer l'environnement virtuel et installer les dépendances
```bash
python -m venv venv
# Windows :
.\venv\Scripts\activate
# Linux/macOS :
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration des variables d'environnement
```bash
cp .env.example .env
```

### 4. Lancer les migrations et le serveur de développement
```bash
python manage.py migrate
python manage.py runserver
```

## 📖 Déploiement sur le Serveur VPS
Consultez le guide complet : [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
