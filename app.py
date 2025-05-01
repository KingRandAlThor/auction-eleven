# Extrait de app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime, timedelta
import os
import sys

# Ajouter le répertoire courant au chemin Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'une-cle-secrete-difficile-a-deviner'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max
app.config['DEBUG'] = True

# Initialisation des extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Injecter la date actuelle dans tous les templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Fonction de chargement de l'utilisateur
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Importez les routes à la fin pour éviter les importations circulaires
from app_routes import *