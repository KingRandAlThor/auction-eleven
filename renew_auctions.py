from app import app, db
from models import Auction, Product
from datetime import datetime, timedelta

with app.app_context():
    # Trouver toutes les enchères
    auctions = Auction.query.all()
    print(f"Nombre total d'enchères: {len(auctions)}")
    
    renewed_count = 0
    now = datetime.utcnow()
    
    # Renouveler toutes les enchères
    for auction in auctions:
        product = Product.query.get(auction.product_id)
        old_status = auction.status
        
        # Mettre à jour l'enchère
        auction.start_date = now
        auction.end_date = now + timedelta(days=7)  # Nouvelle fin dans 7 jours
        auction.status = 'active'
        
        # Réinitialiser le gagnant si nécessaire
        if hasattr(auction, 'winner_id') and auction.winner_id:
            auction.winner_id = None
        
        if hasattr(auction, 'winning_price'):
            auction.winning_price = None
        
        # Afficher le changement
        product_name = product.name if product else f"ID: {auction.product_id}"
        print(f"Enchère #{auction.id} - {product_name}: {old_status} → active")
        renewed_count += 1
    
    # Sauvegarder les changements
    db.session.commit()
    print(f"\n{renewed_count} enchères ont été relancées avec succès!")
    print(f"Les enchères sont maintenant actives jusqu'au {now + timedelta(days=7)}")