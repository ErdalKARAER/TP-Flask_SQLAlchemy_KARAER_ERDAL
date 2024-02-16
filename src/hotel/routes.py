from flask import jsonify, request, Blueprint
from .models import Chambre, Reservation
from datetime import datetime
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# Endpoint pour rechercher les chambres disponibles
@main.route('/api/chambres/disponibles', methods=['GET'])
def rechercher_chambres_disponibles():
    # Récupérer les paramètres de la requête
    date_arrivee = request.args.get('date_arrivee')
    date_depart = request.args.get('date_depart')

    # Vérifier que les paramètres sont fournis
    if not date_arrivee or not date_depart:
        return jsonify({'message': 'Les dates de début et de fin sont requises.'}), 400

    # Convertir les dates en objets datetime
    try:
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d')
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Format de date invalide. Utilisez YYYY-MM-DD.'}), 400

    # Vérifier que la date de début est antérieure à la date de fin
    if date_arrivee >= date_depart:
        return jsonify({'message': 'La date de départ doit être postérieure à la date d\'arrivée.'}), 400

    # Rechercher les chambres disponibles pour les dates spécifiées
    chambres_disponibles = []
    chambres_occupees = Reservation.query.filter(
        (Reservation.date_arrivee < date_depart) &
        (Reservation.date_depart > date_arrivee)
    ).values('id_chambre')

    for chambre in Chambre.query.all():
        if chambre.id not in [r.id_chambre for r in chambres_occupees]:
            chambres_disponibles.append({
                'id': chambre.id,
                'numero': chambre.numero,
                'type': chambre.type,
                'prix': float(chambre.prix)
            })

    return jsonify(chambres_disponibles), 200


