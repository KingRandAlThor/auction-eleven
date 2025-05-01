from app import app, db
from models import Auction, Product
from datetime import datetime

with app.app_context():
    # Vérifier toutes les enchères
    all_auctions = Auction.query.all()
    print(f"Nombre total d'enchères : {len(all_auctions)}")
    
    # Vérifier les enchères actives
    active_auctions = Auction.query.filter_by(status='active').all()
    print(f"Nombre d'enchères actives : {len(active_auctions)}")
    
    # Si aucune enchère active, mettre à jour quelques enchères
    if len(active_auctions) == 0 and len(all_auctions) > 0:
        print("Mise à jour des enchères pour les rendre actives...")
        for auction in all_auctions[:3]:  # Prendre les 3 premières
            auction.status = 'active'
            # S'assurer que la date de fin est dans le futur
            now = datetime.utcnow()
            if auction.end_date < now:
                auction.end_date = datetime(now.year, now.month, now.day + 3)  # +3 jours
            print(f"Enchère ID {auction.id} mise à jour")
        
        db.session.commit()
        print("Mises à jour terminées")