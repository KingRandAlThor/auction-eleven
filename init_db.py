from app import app, db
from models import User, Product, Auction, Bid, TokenPack, TokenTransaction
from datetime import datetime, timedelta
import os

# Créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()
    
    # Vérifier si l'admin existe déjà
    admin = User.query.filter_by(email='admin@example.com').first()
    
    if not admin:
        # Créer un utilisateur admin
        admin = User(
            firstname='Admin',
            lastname='System',
            email='admin@example.com',
            token_balance=100,
            is_admin=True,
            registration_date=datetime.utcnow()
        )
        admin.set_password('adminpass')
        db.session.add(admin)
        
    # Ajouter d'autres données seulement si nécessaire
    if TokenPack.query.count() == 0:
        # Créer des packs de jetons
        token_packs = [
            TokenPack(name='Pack Débutant', quantity=10, price_euros=5.99, description='Idéal pour commencer'),
            TokenPack(name='Pack Standard', quantity=25, price_euros=12.99, description='Le meilleur rapport qualité-prix'),
            TokenPack(name='Pack Premium', quantity=50, price_euros=19.99, description='Pour les enchérisseurs réguliers'),
            TokenPack(name='Pack VIP', quantity=100, price_euros=34.99, description='Pour les passionnés d\'enchères')
        ]
        db.session.add_all(token_packs)
    
    # Ajouter des produits et enchères seulement si nécessaire
    if Product.query.count() == 0:
        # Créer des produits exemple
        products = [
            Product(
                name='Smartphone Dernière Génération',
                description='Le tout dernier smartphone avec écran AMOLED, processeur ultra-rapide et appareil photo de qualité professionnelle.',
                image_url='images/products/phone.jpg',
                market_price=899.99,
                created_by=1  # Admin user
            ),
            Product(
                name='Télévision 4K Smart TV',
                description='Télévision 4K avec une image époustouflante, son surround et toutes les applications de streaming intégrées.',
                image_url='images/products/tv.jpg',
                market_price=1299.99,
                created_by=1  # Admin user
            ),
            Product(
                name='Casque Audio Sans Fil',
                description='Casque bluetooth avec réduction de bruit active, son haute-fidélité et autonomie exceptionnelle.',
                image_url='images/products/headphones.jpg',
                market_price=349.99,
                created_by=1  # Admin user
            )
        ]
        db.session.add_all(products)
        db.session.flush()  # Pour obtenir les IDs des produits
        
        # Créer des enchères actives
        now = datetime.utcnow()
        auctions = [
            Auction(
                product_id=1,  # Smartphone
                start_date=now - timedelta(days=1),
                end_date=now + timedelta(days=6),
                tokens_required=1,
                status='active'
            ),
            Auction(
                product_id=2,  # TV
                start_date=now - timedelta(days=2),
                end_date=now + timedelta(days=3),
                tokens_required=2,
                status='active'
            ),
            Auction(
                product_id=3,  # Casque
                start_date=now - timedelta(hours=12),
                end_date=now + timedelta(hours=12),
                tokens_required=1,
                status='active'
            )
        ]
        db.session.add_all(auctions)
    
    db.session.commit()
    print("Base de données initialisée avec succès!")