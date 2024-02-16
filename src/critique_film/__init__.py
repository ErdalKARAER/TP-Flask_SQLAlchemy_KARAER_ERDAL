from flask import Flask
from flask_migrate import Migrate
from .models import Utilisateur
from flask_login import LoginManager
from .database import db 


migrate = Migrate()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@<domaine|ip>:<port>/<database>'
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db/critiques_de_films'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.connexion'

    return app


