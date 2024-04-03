from flask import Blueprint, request
from app.route_guard import auth_required

from app.location.model import *
from app.location.schema import *

bp = Blueprint('location', __name__)

@bp.post('/location')
@auth_required()
def create_location():
    name = request.json.get('name')
    location = Location.create(name)
    return LocationSchema().dump(location), 201

@bp.get('/location/<int:id>')
@auth_required()
def get_location(id):
    location = Location.get_by_id(id)
    if location is None:
        return {'message': 'Location not found'}, 404
    return LocationSchema().dump(location), 200

@bp.put('/location/<int:id>')
@auth_required()
def update_location(id):
    location = Location.get_by_id(id)
    if location is None:
        return {'message': 'Location not found'}, 404
    name = request.json.get('name')
    location.update(name)
    return LocationSchema().dump(location), 200

@bp.delete('/location/<int:id>')
@auth_required()
def delete_location(id):
    location = Location.get_by_id(id)
    if location is None:
        return {'message': 'Location not found'}, 404
    location.delete()
    return {'message': 'Location deleted successfully'}, 200

@bp.get('/locations')
@auth_required()
def get_locations():
    locations = Location.get_all()
    return LocationSchema(many=True).dump(locations), 200