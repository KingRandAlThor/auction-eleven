from app import app, db
from models import User, Product, Auction, Bid

with app.app_context():
    # Vérifier les utilisateurs
    users = User.query.all()
    print(f"Nombre d'utilisateurs : {len(users)}")
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}")
    
    # Vérifier les produits
    products = Product.query.all()
    print(f"\nNombre de produits : {len(products)}")
    for product in products:
        print(f"ID: {product.id}, Nom: {product.name}")
    
    # Vérifier les enchères
    auctions = Auction.query.all()
    print(f"\nNombre d'enchères : {len(auctions)}")
    for auction in auctions:
        print(f"ID: {auction.id}, Produit: {auction.product_id}, Statut: {auction.status}")
        # Vérifier si le produit existe
        if not Product.query.get(auction.product_id):
            print(f"  ERREUR: Le produit {auction.product_id} n'existe pas!")
    
    # Vérifier les enchères actives
    active_auctions = Auction.query.filter_by(status='active').all()
    print(f"\nNombre d'enchères actives : {len(active_auctions)}")