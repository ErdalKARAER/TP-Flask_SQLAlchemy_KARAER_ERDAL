from flask import jsonify, request, Blueprint
from .models import Chambre, Reservation, Client
from datetime import datetime
from .database import db
main = Blueprint('main', __name__)

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

@main.route('/api/chambres', methods=['POST'])
def ajouter_chambre():
    # Récupérer les données de la requête
    data = request.get_json()

    # Vérifier si toutes les données nécessaires sont fournies
    if 'numero' not in data or 'type' not in data or 'prix' not in data:
        return jsonify({'success': False, 'message': 'Tous les champs sont requis.'}), 400

    # Créer une nouvelle instance de Chambre
    nouvelle_chambre = Chambre(numero=data['numero'], type=data['type'], prix=data['prix'])

    # Ajouter la nouvelle chambre à la base de données
    db.session.add(nouvelle_chambre)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre ajoutée avec succès.'}), 201

@main.route('/api/chambres/<int:id>', methods=['PUT'])
def modifier_chambre(id):
    # Récupérer les données de la requête
    data = request.get_json()

    # Vérifier si la chambre existe
    chambre = Chambre.query.get(id)
    if chambre is None:
        return jsonify({'success': False, 'message': 'Chambre non trouvée.'}), 404

    # Mettre à jour les informations de la chambre
    if 'numero' in data:
        chambre.numero = data['numero']
    if 'type' in data:
        chambre.type = data['type']
    if 'prix' in data:
        chambre.prix = data['prix']

    # Enregistrer les modifications dans la base de données
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre mise à jour avec succès.'}), 200

@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def supprimer_chambre(id):
    # Vérifier si la chambre existe
    chambre = Chambre.query.get(id)
    if chambre is None:
        return jsonify({'success': False, 'message': 'Chambre non trouvée.'}), 404

    # Supprimer la chambre de la base de données
    db.session.delete(chambre)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre supprimée avec succès.'}), 200

@main.route('/api/reservations', methods=['POST'])
def creer_reservation():
    # Récupérer les données de la requête
    data = request.get_json()

    # Vérifier si toutes les données nécessaires sont fournies
    if 'id_client' not in data or 'id_chambre' not in data or 'date_arrivee' not in data or 'date_depart' not in data:
        return jsonify({'success': False, 'message': 'Tous les champs sont requis.'}), 400

    # Convertir les dates en objets datetime
    try:
        date_arrivee = datetime.strptime(data['date_arrivee'], '%Y-%m-%d')
        date_depart = datetime.strptime(data['date_depart'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'success': False, 'message': 'Format de date invalide. Utilisez YYYY-MM-DD.'}), 400

    # Vérifier la disponibilité de la chambre pour les dates demandées
    chambre = Chambre.query.get(data['id_chambre'])
    if chambre is None:
        return jsonify({'success': False, 'message': 'Chambre non trouvée.'}), 404

    reservations_existantes = Reservation.query.filter(
        (Reservation.id_chambre == data['id_chambre']) &
        ((Reservation.date_arrivee < date_depart) & (Reservation.date_depart > date_arrivee))
    ).all()

    if reservations_existantes:
        return jsonify({'success': False, 'message': 'La chambre est déjà réservée pour les dates spécifiées.'}), 400

    # Créer une nouvelle instance de Réservation
    nouvelle_reservation = Reservation(
        id_client=data['id_client'],
        id_chambre=data['id_chambre'],
        date_arrivee=date_arrivee,
        date_depart=date_depart
    )

    # Ajouter la nouvelle réservation à la base de données
    db.session.add(nouvelle_reservation)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Réservation créée avec succès.'}), 201

@main.route('/api/clients', methods=['POST'])
def ajouter_client():
    # Récupérer les données de la requête
    data = request.get_json()

    # Vérifier si toutes les données nécessaires sont fournies
    if 'nom' not in data or 'email' not in data:
        return jsonify({'success': False, 'message': 'Tous les champs sont requis.'}), 400

    # Créer une nouvelle instance de Client
    nouveau_client = Client(nom=data['nom'], email=data['email'])

    # Ajouter le nouveau client à la base de données
    db.session.add(nouveau_client)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Client ajouté avec succès.'}), 201



