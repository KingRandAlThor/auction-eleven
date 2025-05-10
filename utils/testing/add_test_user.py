from app import app, db
from models import User
from datetime import datetime
import traceback

with app.app_context():
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email="test@example.com").first()
        if existing_user:
            print(f"L'utilisateur test@example.com existe déjà (ID: {existing_user.id})")
        else:
            # Créer un nouvel utilisateur de test
            new_user = User(
                firstname="Test",
                lastname="User",
                email="test@example.com",
                token_balance=10,
                registration_date=datetime.utcnow()
            )
            new_user.set_password("password123")
            
            # Ajouter et valider
            db.session.add(new_user)
            db.session.commit()
            
            print(f"Utilisateur test@example.com créé avec succès (ID: {new_user.id})")
    except Exception as e:
        db.session.rollback()
        print(f"ERREUR: {e}")
        traceback.print_exc()