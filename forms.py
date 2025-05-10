from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
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

class AuctionCreateForm(FlaskForm):
    # Informations produit
    product_name = StringField('Nom du produit', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    market_price = DecimalField('Prix du marché (€)', validators=[DataRequired(), NumberRange(min=1)])
    
    # Image du produit
    product_image = FileField('Image du produit', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images uniquement (JPG, JPEG, PNG)')
    ])
    
    # Paramètres de l'enchère
    duration = SelectField('Durée de l\'enchère', choices=[
        ('3', '3 jours'),
        ('7', '7 jours'),
        ('14', '14 jours')
    ], validators=[DataRequired()])
    
    tokens_required = IntegerField('Jetons requis pour participer', 
                                  validators=[DataRequired(), NumberRange(min=1, max=10)])
    
    submit = SubmitField('Créer l\'enchère')

class CreateAuctionForm(FlaskForm):
    product_name = StringField('Nom du produit', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    market_price = DecimalField('Prix estimé (€)', validators=[DataRequired(), NumberRange(min=1)])
    image = FileField('Image du produit', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images uniquement')])
    duration = SelectField('Durée', choices=[('3', '3 jours'), ('7', '7 jours'), ('14', '14 jours')], default='7')
    tokens_required = IntegerField('Jetons requis', validators=[DataRequired(), NumberRange(min=1, max=10)], default=1)
    submit = SubmitField('Mettre en vente')