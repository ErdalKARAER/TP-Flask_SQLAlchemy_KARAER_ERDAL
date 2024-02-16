from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email

class InscriptionForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()]) 
    email = EmailField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()]) 
    submit = SubmitField('Inscription')


class AjoutFilmForm(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    realisateur = StringField('Réalisateur')
    annee_sortie = IntegerField('Année de sortie')
    genre = StringField('genre')
    submit = SubmitField('Submit')

class CritiqueForm(FlaskForm):
    contenu = TextAreaField('Critique', validators=[DataRequired()])
    submit = SubmitField('Publier')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de Passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')