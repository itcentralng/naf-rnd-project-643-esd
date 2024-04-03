from flask import Blueprint, request, redirect, render_template
from app.route_guard import auth_required

from app.unit.model import *
from app.unit.schema import *
from app.location.model import Location
from app.command.model import Command
from app.user.model import User

bp = Blueprint('unit', __name__)

@bp.post('/unit')
def create_unit():
    name = request.form.get('name')
    location = request.form.get('location')
    command = request.form.get('command')
    Unit.create(name, location, command)
    return {'message':'Unit added successfully!'}, 201

@bp.get('/units')
def get_all_units():
    locations = Location.get_all()
    commands = Command.get_all()
    units = Unit.get_all()
    return render_template('units.html', locations=locations, commands=commands, units=units)

@bp.get('/unit/<int:id>')
def single_unit(id):
    unit = Unit.get_by_id(id)
    personnels = User.get_all_by_unit_id(id)
    locations = Location.get_all()
    commands = Command.get_all()
    return render_template('single-unit.html', unit=unit, personnels=personnels, locations=locations, commands=commands)

@bp.put('/unit/<int:id>')
def update_unit(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    name = request.form.get('name')
    location = request.form.get('location')
    command = request.form.get('command')
    unit.update(name, location, command)
    return UnitSchema().dump(unit), 200

@bp.delete('/unit/<int:id>')
def delete_unit(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    unit.delete()
    return {'message': 'Unit deleted successfully'}, 200