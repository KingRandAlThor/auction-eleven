from app import app, db
from models import Auction, Bid, Product
from datetime import datetime, timedelta

with app.app_context():
    # 1. Réinitialiser les enchères existantes
    print("Réinitialisation des enchères...")
    
    # 1.1 Supprimer toutes les enchères existantes
    Bid.query.delete()
    
    # 1.2 Mettre à jour les dates des enchères (7 jours à partir de maintenant)
    now = datetime.utcnow()
    end_date = now + timedelta(days=7)
    
    auctions = Auction.query.all()
    for auction in auctions:
        auction.start_date = now
        auction.end_date = end_date
        auction.status = 'active'
        auction.winner_id = None
        auction.winning_price = None
    
    # 2. Vérifier les prix de marché des produits
    products = Product.query.all()
    for product in products:
        if not product.market_price or product.market_price <= 0:
            product.market_price = 100.0  # Prix par défaut
    
    # 3. Sauvegarder les modifications
    db.session.commit()
    
    print(f"✅ {len(auctions)} enchères réinitialisées avec succès!")
    print(f"✅ {len(products)} produits vérifiés!")