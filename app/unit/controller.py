from flask import Blueprint, request, redirect, render_template
from app.route_guard import auth_required

from app.unit.model import *
from app.unit.schema import *
from app.location.model import Location
from app.command.model import Command

bp = Blueprint('unit', __name__)

@bp.post('/unit')
def create_unit():
    name = request.form.get('name')
    location = request.form.get('location')
    command = request.form.get('command')
    Unit.create(name, location, command)
    return {'message':'Unit added successfully!'}, 201

@bp.get('/units')
def add_unit():
    locations = Location.get_all()
    commands = Command.get_all()
    units = Unit.get_all()
    return render_template('units.html', locations=locations, commands=commands, units=units)

@bp.put('/unit/<int:id>')
@auth_required()
def update_unit(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    name = request.json.get('name')
    unit.update(name)
    return UnitSchema().dump(unit), 200

@bp.delete('/unit/<int:id>')
@auth_required()
def delete_unit(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    unit.delete()
    return {'message': 'Unit deleted successfully'}, 200

@bp.get('/units')
@auth_required()
def get_units():
    units = Unit.get_all()
    return UnitSchema(many=True).dump(units), 200