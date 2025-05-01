from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, IntegerField, TextAreaField, SelectField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError
from models import User

class LoginForm(FlaskForm):
    """Formulaire de connexion utilisateur"""
    email = StringField('Email', validators=[
        DataRequired(message="L'email est requis"), 
        Email(message="Veuillez entrer un email valide")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message="Le mot de passe est requis")
    ])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    """Formulaire d'inscription utilisateur"""
    firstname = StringField('Prénom', validators=[
        DataRequired(message="Le prénom est requis"), 
        Length(min=2, max=50, message="Le prénom doit comporter entre 2 et 50 caractères")
    ])
    lastname = StringField('Nom', validators=[
        DataRequired(message="Le nom est requis"), 
        Length(min=2, max=50, message="Le nom doit comporter entre 2 et 50 caractères")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="L'email est requis"), 
        Email(message="Veuillez entrer un email valide")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message="Le mot de passe est requis"), 
        Length(min=6, message='Le mot de passe doit comporter au moins 6 caractères')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(message="La confirmation du mot de passe est requise"), 
        EqualTo('password', message='Les mots de passe doivent correspondre')
    ])
    submit = SubmitField('S\'inscrire')
    
    def validate_email(self, email):
        """Vérifie si l'email est déjà utilisé"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé. Veuillez en choisir un autre.')

class BidForm(FlaskForm):
    """Formulaire pour soumettre une enchère"""
    amount = DecimalField('Votre prix (€)', validators=[
        DataRequired(message="Le prix est requis"),
        NumberRange(min=0.01, message='Le prix doit être positif')
    ])
    submit = SubmitField('Proposer ce prix')
    
    def validate_price(self, price):
        """Vérifie que le prix est au centime près"""
        if round(price.data, 2) != price.data:
            raise ValidationError('Le prix doit être au centime près (deux décimales maximum)')

# Formulaires additionnels qui pourraient être utiles

class ProductForm(FlaskForm):
    """Formulaire pour ajouter/modifier un produit (pour l'administration)"""
    name = StringField('Nom du produit', validators=[DataRequired()])
    description = TextAreaField('Description')
    market_price = FloatField('Prix du marché', validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField('URL de l\'image')
    is_active = BooleanField('Actif')
    submit = SubmitField('Enregistrer')

class AuctionForm(FlaskForm):
    """Formulaire pour créer/modifier une enchère (pour l'administration)"""
    product_id = SelectField('Produit', coerce=int, validators=[DataRequired()])
    start_date = StringField('Date de début', validators=[DataRequired()])
    end_date = StringField('Date de fin', validators=[DataRequired()])
    tokens_required = IntegerField('Jetons requis par mise', validators=[
        DataRequired(),
        NumberRange(min=1, message='Au moins 1 jeton est requis')
    ])
    status = SelectField('Statut', choices=[
        ('scheduled', 'Programmée'),
        ('active', 'Active'),
        ('ended', 'Terminée')
    ])
    submit = SubmitField('Enregistrer')