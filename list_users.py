from app import app, db
from models import User
import sys

print("Début du script de liste d'utilisateurs...")

try:
    with app.app_context():
        print("Accès à la base de données...")
        users = User.query.all()
        
        if not users:
            print("Aucun utilisateur trouvé dans la base de données!")
        else:
            print(f"=== {len(users)} Utilisateurs enregistrés ===")
            for user in users:
                print(f"ID: {user.id} | Email: {user.email} | Nom: {user.firstname} {user.lastname} | Admin: {user.is_admin} | Jetons: {user.token_balance}")
except Exception as e:
    print(f"ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("Fin du script.")