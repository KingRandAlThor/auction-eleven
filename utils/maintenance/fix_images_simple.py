# Créez fix_images_simple.py
import os
import shutil

# Chemin vers le dossier static
static_folder = os.path.join(os.path.dirname(__file__), 'static')

def ensure_image_exists(source_path, dest_path):
    if os.path.exists(source_path) and not os.path.exists(dest_path):
        # Créer le répertoire de destination si nécessaire
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        # Copier l'image
        shutil.copy(source_path, dest_path)
        print(f"Image copiée: {dest_path}")
    elif not os.path.exists(source_path):
        print(f"Image source introuvable: {source_path}")

# Créer les dossiers nécessaires
os.makedirs(os.path.join(static_folder, 'images/products'), exist_ok=True)
os.makedirs(os.path.join(static_folder, 'static/images/products'), exist_ok=True)

# Images à traiter
image_files = ['phone.jpg', 'tv.jpg', 'headphones.jpg', 'default.jpg']

for image in image_files:
    # Trouver une source valide
    source_paths = [
        os.path.join(static_folder, f'images/products/{image}'),
        os.path.join(static_folder, image)
    ]
    
    valid_source = None
    for src in source_paths:
        if os.path.exists(src):
            valid_source = src
            print(f"Source trouvée: {src}")
            break
    
    if valid_source:
        # Destinations à créer
        destinations = [
            os.path.join(static_folder, f'images/products/{image}'),
            os.path.join(static_folder, f'static/images/products/{image}')
        ]
        
        # Copier vers toutes les destinations
        for dest in destinations:
            ensure_image_exists(valid_source, dest)
    else:
        print(f"⚠️ Aucune source valide trouvée pour {image}")