from datetime import datetime
from flask import Blueprint, request
from app.route_guard import auth_required

from app.vehiclelog.model import *
from app.vehiclelog.schema import *

bp = Blueprint('vehiclelog', __name__)

@bp.post('/vehiclelog/<int:vehicle_id>')
def create_vehiclelog(vehicle_id):
    mileage = request.form.get('mileage', type=int)
    type = request.form.get('type')
    description = request.form.get('description')
    date = request.form.get('date')
    date = datetime.fromisoformat(date) if date else datetime.now()
    vehiclelog = Vehiclelog.create(vehicle_id, mileage, type, description, date)
    return VehiclelogSchema().dump(vehiclelog), 201

@bp.get('/vehiclelog/<int:id>')
def get_vehiclelog(id):
    vehiclelog = Vehiclelog.get_by_id(id)
    if vehiclelog is None:
        return {'message': 'Vehiclelog not found'}, 404
    return VehiclelogSchema().dump(vehiclelog), 200

@bp.put('/vehiclelog/<int:id>')
def update_vehiclelog(id):
    vehiclelog = Vehiclelog.get_by_id(id)
    if vehiclelog is None:
        return {'message': 'Vehiclelog not found'}, 404
    vehicle_id = request.form.get('vehicle_id')
    mileage = request.form.get('mileage')
    type = request.form.get('type')
    description = request.form.get('description')
    vehiclelog.update(vehicle_id, mileage, type, description)
    return VehiclelogSchema().dump(vehiclelog), 200

@bp.delete('/vehiclelog/<int:id>')
def delete_vehiclelog(id):
    vehiclelog = Vehiclelog.get_by_id(id)
    if vehiclelog is None:
        return {'message': 'Vehiclelog not found'}, 404
    vehiclelog.delete()
    return {'message': 'Vehiclelog deleted successfully'}, 200

@bp.get('/vehiclelogs')
def get_vehiclelogs():
    vehiclelogs = Vehiclelog.get_all()
    return VehiclelogSchema(many=True).dump(vehiclelogs), 200