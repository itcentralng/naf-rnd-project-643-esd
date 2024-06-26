from flask import Blueprint, request
from app.route_guard import auth_required

from app.alert.model import *
from app.alert.schema import *

bp = Blueprint('alert', __name__)

@bp.post('/alert/<int:vehicle_id>')
def create_alert(vehicle_id):
    mileage_limit = request.form.get('mileage_limit')
    current_mileage = request.form.get('current_mileage')
    status = request.form.get('status')
    alert = Alert.create(vehicle_id, mileage_limit, current_mileage, status)
    return AlertSchema().dump(alert), 201

@bp.get('/alert/<int:id>')
def get_alert(id):
    alert = Alert.get_by_id(id)
    if alert is None:
        return {'message': 'Alert not found'}, 404
    return AlertSchema().dump(alert), 200

@bp.put('/alert/<int:id>')
def update_alert(id):
    alert = Alert.get_by_id(id)
    if alert is None:
        return {'message': 'Alert not found'}, 404
    vehicle_id = request.form.get('vehicle_id')
    mileage_limit = request.form.get('mileage_limit')
    current_mileage = request.form.get('current_mileage')
    status = request.form.get('status')
    alert.update(vehicle_id, mileage_limit, current_mileage, status)
    return AlertSchema().dump(alert), 200

@bp.delete('/alert/<int:id>')
def delete_alert(id):
    alert = Alert.get_by_id(id)
    if alert is None:
        return {'message': 'Alert not found'}, 404
    alert.delete()
    return {'message': 'Alert deleted successfully'}, 200

@bp.get('/alerts')
def get_alerts():
    alerts = Alert.get_all()
    return AlertSchema(many=True).dump(alerts), 200