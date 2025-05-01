import sqlite3
import os

# Chemin vers le fichier de base de données SQLite
db_path = os.path.join(os.path.dirname(__file__), 'app.db')

print(f"Tentative d'accès à la base de données: {db_path}")

try:
    # Vérifier si le fichier existe
    if not os.path.exists(db_path):
        print(f"ERREUR: Le fichier de base de données n'existe pas à l'emplacement: {db_path}")
    else:
        print(f"Le fichier de base de données existe et sa taille est de: {os.path.getsize(db_path)} octets")
        
        # Connexion directe à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table users existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("ERREUR: La table 'users' n'existe pas dans la base de données!")
        else:
            # Récupérer tous les utilisateurs
            cursor.execute("SELECT id, email, firstname, lastname, is_admin, token_balance FROM users")
            users = cursor.fetchall()
            
            if not users:
                print("Aucun utilisateur trouvé dans la base de données!")
            else:
                print(f"=== {len(users)} Utilisateurs enregistrés ===")
                for user in users:
                    print(f"ID: {user[0]} | Email: {user[1]} | Nom: {user[2]} {user[3]} | Admin: {user[4]} | Jetons: {user[5]}")
        
        conn.close()
except Exception as e:
    print(f"ERREUR: {e}")
    import traceback
    traceback.print_exc()

print("Fin du script.")