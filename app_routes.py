from flask import render_template, redirect, url_for, flash, request, jsonify, session
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from app import app, db
from models import User, Product, Auction, Bid, TokenPack, TokenTransaction
from forms import LoginForm, RegisterForm, BidForm, AuctionCreateForm, CreateAuctionForm
import os
from werkzeug.utils import secure_filename

# Route principale - page d'accueil
@app.route('/')
def index():
    active_auctions = Auction.query.filter_by(status='active').order_by(Auction.end_date).limit(6).all()
    featured_auctions = active_auctions[:3]  # Les 3 premiers pour la section vedette
    auctions = active_auctions[3:] if len(active_auctions) > 3 else []  # Le reste pour la section supplémentaire
    
    return render_template('index.html', featured_auctions=featured_auctions, auctions=auctions)

# Route pour la liste des enchères
@app.route('/auctions')
def auctions():
    # Récupérer toutes les enchères actives, ordonnées par date de fin
    active_auctions = Auction.query.filter_by(status='active').order_by(Auction.end_date).all()
    now = datetime.utcnow()
    
    print(f"Nombre d'enchères trouvées : {len(active_auctions)}")
    for auction in active_auctions:
        print(f"Enchère ID: {auction.id}, Produit: {auction.product.name if auction.product else 'Non défini'}")
    
    return render_template('auctions.html', auctions=active_auctions, now=now)

# Route pour le détail d'une enchère
@app.route('/auction/<int:auction_id>')
def auction_detail(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    
    # Calculer le temps restant pour l'enchère
    now = datetime.utcnow()
    time_left = auction.end_date - now if auction.end_date > now else timedelta(0)
    
    return render_template('auction_detail.html', auction=auction, time_left=time_left, now=now)

# Route pour la connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
    
    return render_template('login.html', form=form)

# Route pour l'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Initialiser le formulaire mais ne pas l'utiliser pour la validation
    form = RegisterForm()
    
    if request.method == 'POST':
        print("\n=== TENTATIVE D'INSCRIPTION ===")
        try:
            # Récupérer les données manuellement
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            
            print(f"Données reçues: {firstname}, {lastname}, {email}")
            
            # Validation manuelle
            if not all([firstname, lastname, email, password]):
                flash('Tous les champs sont obligatoires.', 'danger')
                return render_template('register.html', form=form)
            
            # Vérifier si l'email existe déjà
            if User.query.filter_by(email=email).first():
                flash('Cette adresse email est déjà utilisée.', 'danger')
                return render_template('register.html', form=form)
            
            # Créer le nouvel utilisateur
            user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                token_balance=5,
                registration_date=datetime.utcnow()
            )
            
            # Définir le mot de passe
            print("Définition du mot de passe...")
            user.password_hash = generate_password_hash(password)
            
            # Ajouter à la base de données
            print("Ajout à la session DB...")
            db.session.add(user)
            
            print("Commit de la transaction...")
            db.session.commit()
            
            print(f"✅ Utilisateur {email} enregistré avec succès!")
            flash('Votre compte a été créé avec succès!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Une erreur est survenue lors de la création du compte.', 'danger')
    
    return render_template('register.html', form=form)

# Ajouter cette route simplifiée
@app.route('/register-simple', methods=['GET', 'POST'])
def register_simple():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            firstname = request.form.get('firstname', '')
            lastname = request.form.get('lastname', '')
            email = request.form.get('email', '')
            password = request.form.get('password', '')
            
            # Validation basique
            if not firstname or not lastname or not email or not password:
                flash('Tous les champs sont obligatoires', 'danger')
                return render_template('register_simple.html')
            
            # Vérifier si l'email existe déjà
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Cet email est déjà utilisé', 'danger')
                return render_template('register_simple.html')
            
            # Créer un nouvel utilisateur
            user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password_hash=generate_password_hash(password),
                token_balance=5,
                registration_date=datetime.utcnow()
            )
            
            # Enregistrer dans la base de données
            db.session.add(user)
            db.session.commit()
            
            # Message de succès
            flash('Votre compte a été créé avec succès!', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"ERREUR INSCRIPTION: {str(e)}")
            flash('Une erreur est survenue lors de la création du compte', 'danger')
    
    return render_template('register_simple.html')

# Route pour la déconnexion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route pour le profil utilisateur
@app.route('/profile')
@login_required
def profile():
    # Code du profil...
    return render_template('profile.html')

# Route pour les jetons (achat)
@app.route('/tokens')
@login_required
def tokens():
    token_packs = TokenPack.query.filter_by(is_active=True).all()
    return render_template('tokens.html', token_packs=token_packs)

# Route pour l'achat de jetons
@app.route('/buy_tokens/<int:pack_id>', methods=['POST'])
@login_required
def buy_tokens(pack_id):
    # Code d'achat de jetons...
    return redirect(url_for('tokens'))

# Route pour mes enchères
@app.route('/my_bids')
@login_required
def my_bids():
    # Code pour mes enchères...
    return render_template('my_bids.html')

# Ajouter cette route pour les enchères via API
@app.route('/api/bids', methods=['POST'])
@login_required
def api_place_bid():
    data = request.json
    auction_id = data.get('auction_id')
    price = data.get('price')
    
    if not auction_id or not price:
        return jsonify({'success': False, 'message': 'Données manquantes'})
    
    try:
        price = float(price)
    except ValueError:
        return jsonify({'success': False, 'message': 'Prix invalide'})
    
    auction = Auction.query.get_or_404(auction_id)
    
    # Vérifier si l'enchère est active
    now = datetime.utcnow()
    if auction.end_date < now:
        return jsonify({'success': False, 'message': 'Cette enchère est terminée'})
    
    # Vérifier si l'utilisateur a assez de jetons
    if current_user.token_balance < auction.tokens_required:
        return jsonify({'success': False, 'message': 'Vous n\'avez pas assez de jetons'})
    
    # Créer une nouvelle enchère
    bid = Bid(
        auction_id=auction_id,
        user_id=current_user.id,
        price=price,
        tokens_used=auction.tokens_required
    )
    
    # Déduire les jetons
    current_user.token_balance -= auction.tokens_required
    
    # Créer une transaction
    transaction = TokenTransaction(
        user_id=current_user.id,
        quantity=-auction.tokens_required,
        type='bid',
        bid_id=bid.id  # Sera rempli après commit
    )
    
    db.session.add(bid)
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Votre enchère a été placée avec succès!',
        'new_balance': current_user.token_balance
    })

# Première occurrence (à commenter ou supprimer)
# @app.route('/bids', methods=['POST'])
# def place_bid():
#     # Ancien code...

# Deuxième occurrence (à conserver)
@app.route('/bids', methods=['POST'])
@login_required
def place_bid():
    auction_id = request.form.get('auction_id', type=int)
    amount = request.form.get('amount', type=float)  # Vous recevez toujours 'amount' du formulaire
    
    # Validation de base
    if not auction_id or not amount:
        return jsonify({'success': False, 'message': 'Données d\'enchère invalides'}), 400
    
    # Récupérer l'enchère
    auction = Auction.query.get_or_404(auction_id)
    
    # Vérifier si l'enchère est toujours active
    now = datetime.utcnow()
    if auction.end_date <= now:
        return jsonify({'success': False, 'message': 'Cette enchère est terminée'}), 400
    
    # Vérifier si l'utilisateur a assez de jetons
    if current_user.token_balance < auction.tokens_required:
        return jsonify({'success': False, 'message': f'Vous avez besoin de {auction.tokens_required} jetons pour participer'}), 400
    
    # Ne garder QUE cette vérification pour les enchères inversées
    lowest_bid = Bid.query.filter_by(auction_id=auction_id).order_by(Bid.price.asc()).first()  # MODIFIÉ: price
    
    if lowest_bid:
        max_allowed = lowest_bid.price - 0.01  # MODIFIÉ: price
        if amount >= lowest_bid.price:  # MODIFIÉ: price
            return jsonify({'success': False, 'message': f'Votre enchère doit être inférieure à {lowest_bid.price:.2f}€'}), 400
    else:
        # Première enchère: max 90% du prix du marché
        product_price = auction.product.market_price or 100.0
        max_allowed = round(product_price * 0.9, 2)
        if amount > max_allowed:
            return jsonify({'success': False, 'message': f'Votre première enchère doit être inférieure à {max_allowed:.2f}€'}), 400
    
    # Créer l'enchère
    try:
        bid = Bid(
            user_id=current_user.id,
            auction_id=auction_id,
            price=amount,  # MODIFIÉ: utiliser price au lieu de amount
            bid_date=now  # Utiliser bid_date ou placed_at selon votre modèle
        )
        
        # Déduire les jetons
        current_user.token_balance -= auction.tokens_required
        
        # Enregistrer les changements
        db.session.add(bid)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Enchère de {amount:.2f}€ placée avec succès',
            'new_amount': amount,
            'new_balance': current_user.token_balance
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erreur: {str(e)}'}), 500

# @app.route('/confirm/<token>')
# def confirm_email(token):
#     from utils import confirm_token
    
#     try:
#         email = confirm_token(token)
#     except:
#         flash('Le lien de confirmation est invalide ou a expiré.', 'danger')
#         return redirect(url_for('login'))
    
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         flash('Utilisateur non trouvé.', 'danger')
#         return redirect(url_for('login'))
    
#     if user.is_confirmed:
#         flash('Votre compte est déjà confirmé. Veuillez vous connecter.', 'info')
#     else:
#         user.is_confirmed = True
#         user.confirmation_token = None  # Effacer le token après confirmation
#         db.session.commit()
#         flash('Votre compte a été confirmé avec succès! Vous pouvez maintenant vous connecter.', 'success')
    
#     return redirect(url_for('login'))

# @app.route('/resend-confirmation')
# def resend_confirmation():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
    
#     return render_template('resend_confirmation.html')

# @app.route('/resend-confirmation', methods=['POST'])
# def resend_confirmation_post():
#     email = request.form.get('email')
#     if not email:
#         flash('Veuillez fournir votre adresse email.', 'danger')
#         return redirect(url_for('resend_confirmation'))
    
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         # Ne pas indiquer que l'utilisateur n'existe pas pour des raisons de sécurité
#         flash('Si votre email est enregistré, un nouveau lien de confirmation a été envoyé.', 'info')
#         return redirect(url_for('login'))
    
#     if user.is_confirmed:
#         flash('Votre compte est déjà confirmé. Veuillez vous connecter.', 'info')
#         return redirect(url_for('login'))
    
#     # Envoyer un nouvel email de confirmation
#     try:
#         send_confirmation_email(user)
#         flash('Un nouveau lien de confirmation a été envoyé à votre adresse email.', 'success')
#     except:
#         flash('Une erreur est survenue lors de l\'envoi de l\'email. Veuillez réessayer plus tard.', 'danger')
    
#     return redirect(url_for('login'))

@app.route('/create-auction', methods=['GET', 'POST'])
@login_required
def create_auction():
    form = CreateAuctionForm()
    
    if form.validate_on_submit():
        # Gestion de l'image
        image_path = 'images/products/default.jpg'
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # Créer le dossier s'il n'existe pas
            os.makedirs(os.path.join(app.static_folder, 'images/products'), exist_ok=True)
            # Sauvegarder l'image
            form.image.data.save(os.path.join(app.static_folder, 'images/products', filename))
            image_path = f'images/products/{filename}'
        
        # Créer le produit
        product = Product(
            name=form.product_name.data,
            description=form.description.data,
            image_url=image_path,
            market_price=form.market_price.data,
            created_by=current_user.id,
            created_at=datetime.utcnow(),
            is_active=True
        )
        db.session.add(product)
        db.session.flush()  # Pour obtenir l'ID
        
        # Créer l'enchère
        duration = int(form.duration.data)
        now = datetime.utcnow()
        
        auction = Auction(
            product_id=product.id,
            start_date=now,
            end_date=now + timedelta(days=duration),
            tokens_required=form.tokens_required.data,
            status='active'
        )
        db.session.add(auction)
        db.session.commit()
        
        flash('Votre produit a été mis aux enchères avec succès!', 'success')
        return redirect(url_for('auction_detail', auction_id=auction.id))
    
    return render_template('create_auction.html', form=form, title="Vendre un produit")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Ajouter cette nouvelle route à app_routes.py
@app.route('/api/auction/<int:auction_id>/min-bid', methods=['GET'])
def get_min_bid(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    
    # Vérifier si l'enchère est active
    now = datetime.utcnow()
    if auction.end_date <= now:
        return jsonify({'success': False, 'message': 'Cette enchère est terminée'}), 400
    
    # Trouver l'enchère la plus basse actuelle - MODIFIÉ: price au lieu de amount
    lowest_bid = Bid.query.filter_by(auction_id=auction_id).order_by(Bid.price.asc()).first()
    
    # Prix minimum autorisé
    if lowest_bid:
        min_bid = lowest_bid.price - 0.01  # MODIFIÉ: price au lieu de amount
        min_bid = round(min_bid, 2)
    else:
        # Première enchère: 90% du prix du marché
        product_price = auction.product.market_price or 100.0
        min_bid = round(product_price * 0.9, 2)
    
    return jsonify({
        'success': True,
        'min_bid': min_bid,
        'formatted_min_bid': f"{min_bid:.2f}€"
    })

@app.route('/api/auction/<int:auction_id>/max-bid', methods=['GET'])
def get_max_bid(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    
    # Vérifier si l'enchère est active
    now = datetime.utcnow()
    if auction.end_date <= now:
        return jsonify({'success': False, 'message': 'Cette enchère est terminée'}), 400
    
    # Trouver l'enchère la plus basse actuelle
    lowest_bid = Bid.query.filter_by(auction_id=auction_id).order_by(Bid.amount.asc()).first()
    
    # Prix maximum autorisé (1 centime de moins que l'enchère actuelle)
    if lowest_bid:
        max_bid = lowest_bid.amount - 0.01
    else:
        # Première enchère: 90% du prix du marché
        max_bid = auction.product.market_price * 0.9
        
    max_bid = round(max_bid, 2)  # Arrondir à 2 décimales
    
    return jsonify({
        'success': True,
        'max_bid': max_bid,
        'formatted_max_bid': f"{max_bid:.2f}€"
    })