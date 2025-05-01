from app import app, db
from models import Product, Auction

with app.app_context():
    products = Product.query.all()
    print(f"Vérification des images pour {len(products)} produits...")
    
    updates_needed = False
    
    # Dictionnaire des images par défaut par type de produit
    default_images = {
        'phone': '/static/images/products/phone.jpg',
        'tv': '/static/images/products/tv.jpg',
        'headphones': '/static/images/products/headphones.jpg',
        'default': '/static/images/products/default.jpg'
    }
    
    for product in products:
        print(f"Produit ID: {product.id}, Nom: {product.name}")
        print(f"  Image actuelle: {product.image_url}")
        
        # Vérifier si l'image est vide ou None
        if not product.image_url:
            # Déterminer l'image par défaut basée sur le nom du produit
            image_url = None
            name_lower = product.name.lower()
            
            if 'phone' in name_lower or 'smartphone' in name_lower:
                image_url = default_images['phone']
            elif 'tv' in name_lower or 'télé' in name_lower:
                image_url = default_images['tv']
            elif 'casque' in name_lower or 'headphone' in name_lower:
                image_url = default_images['headphones']
            else:
                image_url = default_images['default']
            
            product.image_url = image_url
            updates_needed = True
            print(f"  ⚠️ Image corrigée à: {product.image_url}")
        
        # S'assurer que les chemins commencent par /static/
        elif not product.image_url.startswith('/static/'):
            product.image_url = '/static/images/products/' + product.image_url.split('/')[-1]
            updates_needed = True
            print(f"  ⚠️ Chemin corrigé à: {product.image_url}")
        
        print("  ---")
    
    if updates_needed:
        db.session.commit()
        print("✅ Corrections enregistrées dans la base de données")
    else:
        print("✅ Aucune correction nécessaire")