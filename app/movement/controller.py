from datetime import datetime
from flask import Blueprint, request
from app.route_guard import auth_required

from app.movement.model import *
from app.movement.schema import *

bp = Blueprint('movement', __name__)

@bp.post('/movement/<int:vehicle_id>')
def create_movement(vehicle_id):
    date = request.form.get('date')
    date = datetime.fromisoformat(date) if date else datetime.now()
    driver = request.form.get('driver')
    starting_point = request.form.get('starting_point')
    mileage = request.form.get('mileage', type=int)
    destination = request.form.get('destination')
    remarks = request.form.get('remarks')
    movement = Movement.create(vehicle_id, date, driver, starting_point, mileage, destination, remarks)
    return MovementSchema().dump(movement), 201

@bp.get('/movement/<int:id>')
def get_movement(id):
    movement = Movement.get_by_id(id)
    if movement is None:
        return {'message': 'Movement not found'}, 404
    return MovementSchema().dump(movement), 200

@bp.put('/movement/<int:id>')
def update_movement(id):
    movement = Movement.get_by_id(id)
    if movement is None:
        return {'message': 'Movement not found'}, 404
    date = request.form.get('date')
    driver = request.form.get('driver')
    starting_point = request.form.get('starting_point')
    mileage = request.form.get('mileage', type=int)
    destination = request.form.get('destination')
    remarks = request.form.get('remarks')
    movement.update(date, driver, starting_point, mileage, destination, remarks)
    return MovementSchema().dump(movement), 200

@bp.delete('/movement/<int:id>')
def delete_movement(id):
    movement = Movement.get_by_id(id)
    if movement is None:
        return {'message': 'Movement not found'}, 404
    movement.delete()
    return {'message': 'Movement deleted successfully'}, 200

@bp.get('/movements')
def get_movements():
    movements = Movement.get_all()
    return MovementSchema(many=True).dump(movements), 200