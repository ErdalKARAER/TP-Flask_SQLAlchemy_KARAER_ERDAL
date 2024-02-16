from .database import db
from datetime import datetime
from flask_login import UserMixin

class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    reservations = db.relationship('Reservation', backref='client', lazy=True)
    

class Chambre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    type = db.Column(db.String(100))
    prix =  db.Column(db.Integer)
    reservations = db.relationship('Reservation', backref='chambre', lazy=True)



class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_arrivee = db.Column(db.DateTime, default=datetime.utcnow)
    date_depart = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(100))
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    id_chambre = db.Column(db.Integer, db.ForeignKey('chambre.id'), nullable=False)
