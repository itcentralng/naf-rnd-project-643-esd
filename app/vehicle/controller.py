from flask import Blueprint, request, render_template
from app.route_guard import auth_required

from datetime import datetime

from app.unit.model import Unit
from app.vehicle.model import *
from app.vehicle.schema import *

bp = Blueprint('vehicle', __name__)

@bp.post('/vehicle')
def create_vehicle():
    lifespan = request.form.get('lifespan')
    make = request.form.get('make')
    model = request.form.get('model')
    type = request.form.get('type')
    trim = request.form.get('trim')
    year = request.form.get('year')
    chassis_no = request.form.get('chassis_no')
    engine_no = request.form.get('engine_no')
    supplier = request.form.get('supplier')
    contract_reference = request.form.get('contract_reference')
    date = request.form.get('date')
    date = datetime.fromisoformat(date) if date else datetime.now()
    remarks = request.form.get('remark')
    vehicle = Vehicle.create(lifespan, make, model, type, trim, year, chassis_no, engine_no, supplier, contract_reference, date, remarks)
    return VehicleSchema().dump(vehicle), 201

@bp.get('/vehicle/<int:id>')
def get_vehicle(id):
    vehicle = Vehicle.get_by_id(id)
    if vehicle is None:
        return {'message': 'Vehicle not found'}, 404
    units = Unit.get_all()
    return render_template('single-vehicle.html', vehicle=vehicle, units=units)

@bp.post('/vehicle/allocate/<int:id>')
def allocate_vehicle(id):
    vehicle = Vehicle.get_by_id(id)
    unit_id = request.form.get('unit_id')
    if vehicle is None:
        return {'message': 'Vehicle not found'}, 404
    Vehicleallocation.create(id, unit_id)
    return {'message':'Vehicle allocated successfully!'}

@bp.put('/vehicle/<int:id>')
def update_vehicle(id):
    vehicle = Vehicle.get_by_id(id)
    if vehicle is None:
        return {'message': 'Vehicle not found'}, 404
    lifespan = request.form.get('lifespan')
    make = request.form.get('make')
    model = request.form.get('model')
    type = request.form.get('type')
    trim = request.form.get('trim')
    year = request.form.get('year')
    chassis_no = request.form.get('chassis_no')
    engine_no = request.form.get('engine_no')
    supplier = request.form.get('supplier')
    contract_reference = request.form.get('contract_reference')
    date = request.form.get('date')
    remarks = request.form.get('remark')
    vehicle.update(lifespan, make, model, type, trim, year, chassis_no, engine_no, supplier, contract_reference, date, remarks)
    return VehicleSchema().dump(vehicle), 200

@bp.delete('/vehicle/<int:id>')
def delete_vehicle(id):
    vehicle = Vehicle.get_by_id(id)
    if vehicle is None:
        return {'message': 'Vehicle not found'}, 404
    vehicle.delete()
    return {'message': 'Vehicle deleted successfully'}, 200

@bp.get('/vehicles')
def get_vehicles():
    unallocated = Vehicle.get_all()
    allocated = Vehicleallocation.get_all()
    return render_template('vehicles.html', allocated=allocated, unallocated=unallocated)