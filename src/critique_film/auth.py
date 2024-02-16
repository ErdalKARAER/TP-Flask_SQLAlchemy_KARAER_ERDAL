from flask import Blueprint, flash, url_for, render_template, redirect
from .forms import InscriptionForm, LoginForm
from .models import Utilisateur
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from flask_login import login_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    # Définir les actions pour inscrire un utilisateur
    form = InscriptionForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.mot_de_passe.data)

        # logique pour entrer l'utilisateur dans la BDD
        new_user = Utilisateur(
            nom=form.nom.data,
            email=form.email.data,
            mot_de_passe_hash = hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html')
    return render_template('inscription.html', form=form)


@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.mot_de_passe_hash, form.mot_de_passe.data):
            login_user(user, remember=True)
            flash("Connecté!")
            flash(current_user.email)
            return redirect(url_for('main.index'))
        else:
            # afficher mot de passe incorrect
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('connexion.html', form=form)