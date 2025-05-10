from __future__ import annotations
from app import app, db
from models import Product, Auction
import os
from PIL import Image  # Vous avez déjà installé pillow

with app.app_context():
    # 1. Créer le dossier des images s'il n'existe pas
    images_folder = os.path.join(app.static_folder, 'images', 'products')
    os.makedirs(images_folder, exist_ok=True)
    
    # 2. Créer une image par défaut si nécessaire
    default_image_path = os.path.join(images_folder, 'default.jpg')
    if not os.path.exists(default_image_path):
        # Créer une image grise simple
        img = Image.new('RGB', (400, 300), color=(200, 200, 200))
        img.save(default_image_path)
        print(f"Image par défaut créée: {default_image_path}")
    
    # 3. Vérifier toutes les images de produits
    products = Product.query.all()
    print(f"Vérification de {len(products)} produits...")
    
    fixed_count = 0
    for product in products:
        print(f"\nProduit: {product.name}")
        print(f"  Image actuelle: {product.image_url}")
        
        # Vérifier si l'image existe
        image_path = product.image_url
        if image_path.startswith('/static/'):
            # Enlever le préfixe '/static/'
            relative_path = image_path[8:]
            full_path = os.path.join(app.static_folder, relative_path)
        else:
            # Si le chemin ne commence pas par /static/, supposer qu'il est relatif à static
            full_path = os.path.join(app.static_folder, image_path)
            
        exists = os.path.exists(full_path)
        print(f"  Chemin complet: {full_path}")
        print(f"  Existe: {exists}")
        
        # Corriger le chemin si l'image n'existe pas
        if not exists:
            new_path = '/static/images/products/default.jpg'
            product.image_url = new_path
            fixed_count += 1
            print(f"  → Corrigé vers: {new_path}")
    
    # Sauvegarder les modifications
    if fixed_count > 0:
        db.session.commit()
        print(f"\n{fixed_count} images corrigées avec succès!")
    else:
        print("\nAucune image n'avait besoin d'être corrigée.")

with app.app_context():
    # Correction spécifique pour le produit "Dimitre"
    dimitre = Product.query.filter(Product.name.like('%Dimitre%')).first()
    if dimitre:
        print(f"\nProduit spécifique trouvé: {dimitre.name}")
        print(f"  Image actuelle: {dimitre.image_url}")
        
        # Forcer la mise à jour de l'image
        dimitre.image_url = '/static/images/products/default.jpg'
        db.session.commit()
        print("  → Image corrigée avec succès!")

with app.app_context():
    # Correction spécifique pour les chemins de fichiers problématiques
    products_with_phone = Product.query.filter(Product.image_url.like('%phone.jpg')).all()
    for product in products_with_phone:
        # Créer une copie de phone.jpg dans static/images/products
        source_path = os.path.join(app.static_folder, 'images/products/phone.jpg')
        if os.path.exists(source_path):
            # Copier l'image vers le chemin relatif static/images/products
            import shutil
            shutil.copy(source_path, os.path.join(app.static_folder, 'images/products/phone.jpg'))
            print(f"Image phone.jpg copiée avec succès!")