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

from app import app, db
from models import Auction
import inspect

with app.app_context():
    # Afficher les attributs de la classe Auction
    print("Attributs du modèle Auction:")
    for attr_name in dir(Auction):
        if not attr_name.startswith('_') and not callable(getattr(Auction, attr_name)):
            print(f"- {attr_name}")
    
    # Afficher les colonnes de la table
    print("\nColonnes de la table Auction:")
    for column in Auction.__table__.columns:
        print(f"- {column.name} (type: {column.type})")
    
    # Créer un exemple d'enchère
    print("\nTest de création d'enchère:")
    try:
        auction_dict = {col.name: None for col in Auction.__table__.columns 
                       if col.name != 'id'}
        print(f"Paramètres à utiliser: {auction_dict}")
    except Exception as e:
        print(f"Erreur: {e}")

@app.before_first_request
def create_admin_account():
    try:
        # Vérifier si l'admin existe déjà
        admin = User.query.filter_by(email="superadmin@auction11.com").first()
        if not admin:
            # Créer le compte administrateur
            admin = User(
                firstname="SUPER",
                lastname="ADMIN",
                email="superadmin@auction11.com",
                password_hash=generate_password_hash("WebCestCool", method='pbkdf2:sha256'),
                token_balance=999,  # Beaucoup de jetons
                registration_date=datetime.utcnow(),
                is_admin=True  # Définir comme administrateur
            )
            db.session.add(admin)
            db.session.commit()
            print("Compte administrateur créé avec succès!")
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la création du compte admin: {e}")