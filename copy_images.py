import os
import shutil
from app import app

def ensure_image_exists(source_path, dest_path):
    if os.path.exists(source_path) and not os.path.exists(dest_path):
        # Créer le répertoire de destination si nécessaire
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        # Copier l'image
        shutil.copy(source_path, dest_path)
        print(f"Image copiée: {dest_path}")
    elif not os.path.exists(source_path):
        print(f"Image source introuvable: {source_path}")

with app.app_context():
    static_folder = app.static_folder
    
    # Copier les images essentielles dans tous les emplacements possibles
    image_files = ['phone.jpg', 'tv.jpg', 'headphones.jpg', 'default.jpg']
    
    for image in image_files:
        # Vérifier différentes sources possibles
        source_paths = [
            os.path.join(static_folder, f'images/products/{image}'),
            os.path.join(static_folder, image)
        ]
        
        # Définir différentes destinations possibles
        dest_paths = [
            os.path.join(static_folder, f'images/products/{image}'),
            os.path.join(static_folder, f'static/images/products/{image}'),
            os.path.join(static_folder, f'{image}')
        ]
        
        # Trouver une source valide
        valid_source = None
        for src in source_paths:
            if os.path.exists(src):
                valid_source = src
                break
        
        if valid_source:
            # Copier vers toutes les destinations
            for dest in dest_paths:
                ensure_image_exists(valid_source, dest)
        else:
            print(f"Aucune source valide trouvée pour {image}")