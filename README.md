<!-- filepath: c:\Users\mrpan\Documents\VS CODE\Auction Eleven\README.md -->

# Auction Eleven

Plateforme d'enchères en ligne développée avec Flask.

## Fonctionnalités

- Système d'authentification des utilisateurs
- Gestion des enchères en temps réel
- Interface responsive et moderne
- Système de jetons pour les enchères

## Technologies utilisées

- Flask (Python)
- SQLite
- Bootstrap 5
- JavaScript

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/KingRandAlThor/auction-eleven.git

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py
```

## 2. Problème avec le fichier app.py sur PythonAnywhere

D'après le code que vous avez partagé, il semble que votre fichier app.py utilise une variable `basedir` qui n'est peut-être pas définie dans le contexte WSGI. Vous devez vous assurer que le fichier app.py contient toutes les importations et définitions nécessaires.

Sur PythonAnywhere, dans la console Bash, vérifiez le contenu de votre app.py :

```bash
cd ~/mysite
cat [app.py](http://_vscodecontentref_/2)
