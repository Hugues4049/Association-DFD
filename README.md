# 🌍 Dreams Family of Development (DFD)

Site web officiel de l'association **DFD** – une organisation engagée dans le développement communautaire, l'aide sociale et l'éducation.

---

## 🚀 Fonctionnalités principales

- 🎥 Bannière vidéo d'accueil
- 🧾 Présentation des projets et des campagnes de dons
- 📬 Formulaire de contact avec envoi d'e-mail sécurisé
- 📚 Section blog, documents, partenaires
- 📱 Design responsive (adapté aux mobiles)
- 📦 Prêt pour le déploiement avec `.env` sécurisé

---

## 🛠️ Technologies utilisées

- **Django** 5.x (backend)
- **HTML / CSS** (frontend)
- **JavaScript** (léger)
- **Python Decouple** (gestion des variables d’environnement)
- **SMTP** (pour l’envoi d’e-mails)
- **Render.com** (option de déploiement)

---

## ⚙️ Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/tonutilisateur/dfd-site.git
cd dfd-site

# 2. Créer un environnement virtuel
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sous Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer les migrations
python manage.py migrate

# 5. Lancer le serveur
python manage.py runserver

---
🔐 Configuration .env
Créer un fichier .env à la racine :

SECRET_KEY=ta-cle-secrete
DEBUG=True
EMAIL_HOST_USER=tonemail@gmail.com
EMAIL_HOST_PASSWORD=mot-de-passe-application
ALLOWED_HOSTS=127.0.0.1,localhost

---
✉️ Envoi d'e-mails
Le formulaire de contact utilise Gmail (SMTP) pour envoyer les messages.
Pour cela, tu dois générer un mot de passe d’application Gmail :
https://myaccount.google.com/apppasswords

---
🧑‍💻 Auteur
Roland #4049.

Projet pour l'association Dreams Family of Development
