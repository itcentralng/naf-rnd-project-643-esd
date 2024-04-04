from flask import Blueprint, request
from app.route_guard import auth_required

from app.alert.model import *
from app.alert.schema import *

bp = Blueprint('alert', __name__)

@bp.post('/alert')
@auth_required()
def create_alert():
    vehicle_id = request.json.get('vehicle_id')
    mileage_limit = request.json.get('mileage_limit')
    current_mileage = request.json.get('current_mileage')
    status = request.json.get('status')
    alert = Alert.create(vehicle_id, mileage_limit, current_mileage, status)
    return AlertSchema().dump(alert), 201

@bp.get('/alert/<int:id>')
@auth_required()
def get_alert(id):
    alert = Alert.get_by_id(id)
    if alert is None:
        return {'message': 'Alert not found'}, 404
    return AlertSchema().dump(alert), 200

@bp.put('/alert/<int:id>')
@auth_required()
def update_alert(id):
    alert = Alert.get_by_id(id)
    if alert is None:
        return {'message': 'Alert not found'}, 404
    vehicle_id = request.json.get('vehicle_id')
    mileage_limit = request.json.get('mileage_limit')
    current_mileage = request.json.get('current_mileage')
    status = request.json.get('status')
    alert.update(vehicle_id, mileage_limit, current_mileage, status)
    return AlertSchema().dump(alert), 200

@bp.delete('/alert/<int:id>')
@auth_required()
def delete_alert(id):
    alert = Alert.get_by_id(id)
    if alert is None:
        return {'message': 'Alert not found'}, 404
    alert.delete()
    return {'message': 'Alert deleted successfully'}, 200

@bp.get('/alerts')
@auth_required()
def get_alerts():
    alerts = Alert.get_all()
    return AlertSchema(many=True).dump(alerts), 200