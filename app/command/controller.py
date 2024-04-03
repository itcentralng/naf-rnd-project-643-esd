from flask import Blueprint, request
from app.route_guard import auth_required

from app.command.model import *
from app.command.schema import *

bp = Blueprint('command', __name__)

@bp.post('/command')
@auth_required()
def create_command():
    name = request.json.get('name')
    command = Command.create(name)
    return CommandSchema().dump(command), 201

@bp.get('/command/<int:id>')
@auth_required()
def get_command(id):
    command = Command.get_by_id(id)
    if command is None:
        return {'message': 'Command not found'}, 404
    return CommandSchema().dump(command), 200

@bp.put('/command/<int:id>')
@auth_required()
def update_command(id):
    command = Command.get_by_id(id)
    if command is None:
        return {'message': 'Command not found'}, 404
    name = request.json.get('name')
    command.update(name)
    return CommandSchema().dump(command), 200

@bp.delete('/command/<int:id>')
@auth_required()
def delete_command(id):
    command = Command.get_by_id(id)
    if command is None:
        return {'message': 'Command not found'}, 404
    command.delete()
    return {'message': 'Command deleted successfully'}, 200

@bp.get('/commands')
@auth_required()
def get_commands():
    commands = Command.get_all()
    return CommandSchema(many=True).dump(commands), 200