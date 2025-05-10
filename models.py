from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

# Modèle utilisateur
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    token_balance = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relations
    products = db.relationship('Product', backref='creator', lazy='dynamic')
    bids = db.relationship('Bid', backref='user', lazy='dynamic')
    transactions = db.relationship('TokenTransaction', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Set the password hash for the user."""
        try:
            self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            return True
        except Exception as e:
            print(f"Erreur lors de la définition du mot de passe: {str(e)}")
            return False
        
    def check_password(self, password):
        """Vérifier le mot de passe de l'utilisateur."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


# Modèle produit
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    market_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations
    auctions = db.relationship('Auction', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.name}>'


# Modèle enchère
class Auction(db.Model):
    __tablename__ = 'auctions'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    tokens_required = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='pending')  # pending, active, ended
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    winning_price = db.Column(db.Float)
    
    # Relations
    bids = db.relationship('Bid', backref='auction', lazy='dynamic')
    winner = db.relationship('User', foreign_keys=[winner_id])
    
    def __repr__(self):
        return f'<Auction {self.id} - {self.product.name}>'


# Modèle enchère utilisateur
class Bid(db.Model):
    __tablename__ = 'bids'
    
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)  # MODIFIÉ: price au lieu de amount
    bid_date = db.Column(db.DateTime, default=datetime.utcnow)
    tokens_used = db.Column(db.Integer, default=1)
    is_winning = db.Column(db.Boolean, default=False)
    is_refunded = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Bid {self.id} - {self.price}€>'


# Modèle pack de jetons
class TokenPack(db.Model):
    __tablename__ = 'token_packs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_euros = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations
    transactions = db.relationship('TokenTransaction', backref='pack', lazy='dynamic')
    
    def __repr__(self):
        return f'<TokenPack {self.name} - {self.quantity} tokens>'


# Modèle transaction de jetons
class TokenTransaction(db.Model):
    __tablename__ = 'token_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # purchase, bid, refund, welcome
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    price_euros = db.Column(db.Float)
    pack_id = db.Column(db.Integer, db.ForeignKey('token_packs.id'))
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id'))
    
    # Relations
    bid = db.relationship('Bid', foreign_keys=[bid_id])
    
    def __repr__(self):
        return f'<TokenTransaction {self.id} - {self.type} {self.quantity} tokens>'