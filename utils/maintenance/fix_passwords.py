# Créez un fichier fix_passwords.py
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Trouver tous les utilisateurs
    users = User.query.all()
    updated_count = 0
    
    for user in users:
        # Vérifier si le mot de passe utilise scrypt
        if user.password_hash and user.password_hash.startswith('scrypt'):
            # Définir un nouveau mot de passe en utilisant pbkdf2
            user.password_hash = generate_password_hash(
                'password123',  # Mot de passe par défaut
                method='pbkdf2:sha256'
            )
            updated_count += 1
            print(f"Mot de passe mis à jour pour: {user.email}")
    
    if updated_count > 0:
        db.session.commit()
        print(f"{updated_count} mots de passe mis à jour avec succès!")
    else:
        print("Aucun mot de passe n'a besoin d'être mis à jour.")