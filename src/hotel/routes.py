from flask import jsonify, request, Blueprint
from .models import Chambre, Reservation, Client
from datetime import datetime
from .database import db
main = Blueprint('main', __name__)

@main.route('/api/chambres/disponibles', methods=['GET'])
def rechercher_chambres_disponibles():
    data = request.get_json()
    date_arrivee = data['date_arrivee']
    date_depart = data['date_depart']
    
    if not date_arrivee or not date_depart:
        return jsonify({'message': 'Les dates de début et de fin sont requises.'}), 400
    try:
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d')
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Format de date invalide. Utilisez YYYY-MM-DD.'}), 400
    if date_arrivee >= date_depart:
        return jsonify({'message': 'La date de départ doit être postérieure à la date d\'arrivée.'}), 400
    chambres_disponibles = []
    chambres_occupees = Reservation.query.filter(
        (Reservation.date_arrivee < date_depart) &
        (Reservation.date_depart > date_arrivee)
    ).with_entities(Reservation.id_chambre)

    for chambre in Chambre.query.all():
        if chambre.id not in [r.id_chambre for r in chambres_occupees]:
            chambres_disponibles.append({
                'id': chambre.id,
                'numero': chambre.numero,
                'type': chambre.type,
                'prix': float(chambre.prix)
            })

    return jsonify(chambres_disponibles), 200

@main.route('/api/chambres', methods=['POST'])
def ajouter_chambre():
    data = request.get_json()

    if 'numero' not in data or 'type' not in data or 'prix' not in data:
        return jsonify({'success': False, 'message': 'Tous les champs sont requis.'}), 400

    nouvelle_chambre = Chambre(numero=data['numero'], type=data['type'], prix=data['prix'])

    db.session.add(nouvelle_chambre)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre ajoutée avec succès.'}), 201

@main.route('/api/chambres/<int:id>', methods=['PUT'])
def modifier_chambre(id):
    data = request.get_json()

    chambre = Chambre.query.get(id)
    if chambre is None:
        return jsonify({'success': False, 'message': 'Chambre non trouvée.'}), 404

    if 'numero' in data:
        chambre.numero = data['numero']
    if 'type' in data:
        chambre.type = data['type']
    if 'prix' in data:
        chambre.prix = data['prix']

    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre mise à jour avec succès.'}), 200

@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def supprimer_chambre(id):
    chambre = Chambre.query.get(id)
    if chambre is None:
        return jsonify({'success': False, 'message': 'Chambre non trouvée.'}), 404

    db.session.delete(chambre)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre supprimée avec succès.'}), 200

@main.route('/api/reservations', methods=['POST'])
def creer_reservation():
    data = request.get_json()
    
    if 'id_client' not in data or 'id_chambre' not in data or 'date_arrivee' not in data or 'date_depart' not in data:
        return jsonify({'success': False, 'message': 'Tous les champs sont requis.'}), 400

    try:
        date_arrivee = datetime.strptime(data['date_arrivee'], '%Y-%m-%d')
        date_depart = datetime.strptime(data['date_depart'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'success': False, 'message': 'Format de date invalide. Utilisez YYYY-MM-DD.'}), 400

    chambre = Chambre.query.get(data['id_chambre'])
    if chambre is None:
        return jsonify({'success': False, 'message': 'Chambre non trouvée.'}), 404

    reservations_existantes = Reservation.query.filter(
        (Reservation.id_chambre == data['id_chambre']) &
        ((Reservation.date_arrivee < date_depart) & (Reservation.date_depart > date_arrivee))
    ).all()

    if reservations_existantes:
        return jsonify({'success': False, 'message': 'La chambre est déjà réservée pour les dates spécifiées.'}), 400

    nouvelle_reservation = Reservation(
        id_client=data['id_client'],
        id_chambre=data['id_chambre'],
        date_arrivee=date_arrivee,
        date_depart=date_depart,
        statut='confirmée'
    )

    db.session.add(nouvelle_reservation)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Réservation créée avec succès.'}), 201

@main.route('/api/clients', methods=['POST'])
def ajouter_client():
    data = request.get_json()

    if 'nom' not in data or 'email' not in data:
        return jsonify({'success': False, 'message': 'Tous les champs sont requis.'}), 400

    nouveau_client = Client(nom=data['nom'], email=data['email'])

    db.session.add(nouveau_client)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Client ajouté avec succès.'}), 201

@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def annuler_reservation(id):
    reservation = Reservation.query.get(id)
    if reservation is None:
        return jsonify({'success': False, 'message': 'Réservation non trouvée.'}), 404

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Réservation annulée avec succès.'}), 200


