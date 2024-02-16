from flask import Blueprint, render_template, redirect, url_for
from .forms import  AjoutFilmForm, CritiqueForm, LoginForm
from .models import  Film, Critique
from flask_login import login_required
from .database import db
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')





@main.route('/ajouter-film', methods=['GET', 'POST'])
@login_required
def ajouter_film():
    form = AjoutFilmForm()
    if form.validate_on_submit():
        new_film = Film(
            titre = form.titre.data,
            realisateur = form.realisateur.data,
            annee_sortie = form.annee_sortie.data,
            genre = form.genre.data
        )
        db.session.add(new_film)
        db.session.commit()
        return render_template('index.html')
    return render_template('ajouter-film.html', form=form)

@main.route('/film/<int:id>')
def film_detail(id):
    film = Film.query.get_or_404(id)
    return render_template('afficher-film.html', film=film)

@main.route('/films')
def films():
    films = Film.query.all()
    return render_template('films.html', films=films)


@main.route('/film/<int:id>/critique', methods=['GET', 'POST'])
@login_required
def ajouter_critique(id):
    form = CritiqueForm()
    film = Film.query.get_or_404(id)
    if form.validate_on_submit():
        critique = Critique(contenu=form.contenu.data, film=film)
        db.session.add(critique)
        db.session.commit()
        return redirect(url_for('main.film_detail', id=id))
    return render_template('ajouter_critique.html', film=film, form=form)

