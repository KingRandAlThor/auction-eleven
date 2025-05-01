from itsdangerous import URLSafeTimedSerializer
from app import app

def generate_confirmation_token(email):
    """Génère un token de confirmation basé sur l'email"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirmation-salt')

def confirm_token(token, expiration=3600):
    """Vérifie un token de confirmation et retourne l'email associé"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='email-confirmation-salt',
            max_age=expiration
        )
        return email
    except:
        return None