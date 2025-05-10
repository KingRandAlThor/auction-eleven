from app import app, db
from models import Auction, Product
from datetime import datetime, timedelta

with app.app_context():
    # Récupérer toutes les enchères
    auctions = Auction.query.all()
    print(f"Vérification de {len(auctions)} enchères...")
    
    updates_needed = False
    
    for auction in auctions:
        # Afficher les données actuelles
        print(f"Enchère ID: {auction.id}")
        print(f"  Produit: {auction.product.name if auction.product else 'Non défini'}")
        
        # Utiliser getattr pour vérifier les attributs de manière sécurisée
        # et afficher les champs qui existent réellement
        print(f"  Prix actuel: {getattr(auction, 'current_price', 'N/A')}")
        print(f"  Date de début: {getattr(auction, 'start_date', 'N/A')}")
        print(f"  Date de fin: {getattr(auction, 'end_date', 'N/A')}")
        print(f"  Statut: {getattr(auction, 'status', 'N/A')}")
        
        # Corriger le prix actuel s'il est None
        if hasattr(auction, 'current_price') and auction.current_price is None:
            # Si un champ initial_price ou base_price existe, l'utiliser comme valeur de repli
            if hasattr(auction, 'initial_price') and auction.initial_price is not None:
                auction.current_price = auction.initial_price
            elif hasattr(auction, 'base_price') and auction.base_price is not None:
                auction.current_price = auction.base_price
            else:
                auction.current_price = 100  # Valeur par défaut
            
            updates_needed = True
            print(f"  ⚠️ Prix actuel corrigé à: {auction.current_price}")
        
        # Vérifier et corriger le statut
        if hasattr(auction, 'status'):
            if auction.status not in ['active', 'completed', 'cancelled']:
                auction.status = 'active'
                updates_needed = True
                print(f"  ⚠️ Statut corrigé à: {auction.status}")
        
        # Vérifier les dates
        now = datetime.utcnow()
        
        if hasattr(auction, 'end_date'):
            if auction.end_date is None or auction.end_date < now:
                auction.end_date = now + timedelta(days=7)
                updates_needed = True
                print(f"  ⚠️ Date de fin corrigée à: {auction.end_date}")
        
        if hasattr(auction, 'start_date'):
            if auction.start_date is None:
                auction.start_date = now
                updates_needed = True
                print(f"  ⚠️ Date de début corrigée à: {auction.start_date}")
        
        print("  ---")
    
    # Sauvegarder les modifications si nécessaire
    if updates_needed:
        db.session.commit()
        print("✅ Corrections enregistrées dans la base de données")
    else:
        print("✅ Aucune correction nécessaire")