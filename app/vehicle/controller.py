from flask import Blueprint, request, render_template
from app.alert.model import Alert
from app.movement.model import Movement
from app.route_guard import auth_required
from flask_login import current_user

from datetime import datetime

from app.unit.model import Unit
from app.vehicle.model import *
from app.vehicle.schema import *
from app.vehiclelog.model import Vehiclelog
from helpers.color_maker import make_color
from helpers.csv import get_vehicles_from_csv

bp = Blueprint('vehicle', __name__)

@bp.post('/vehicle')
def create_vehicle():
    mileage = request.form.get('mileage', type=int)
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
    vehicle = Vehicle.create(mileage, lifespan, make, model, type, trim, year, chassis_no, engine_no, supplier, contract_reference, date, remarks)
    return VehicleSchema().dump(vehicle), 201

@bp.post('/vehicle/bulk/<int:unit_id>')
def create_bulk_vehicles_unit(unit_id):
    file = request.files.get('file')
    data = get_vehicles_from_csv(file)
    for item in data:
        make, model, type, trim, year, lifespan, mileage, chassis_no, engine_no, supplier, contract_reference, date, remarks = item
        if make and date:
            date = datetime.strptime(date, "%m/%d/%Y")
            vehicle = Vehicle.create(mileage, lifespan, make, model, type, trim, year, chassis_no, engine_no, supplier, contract_reference, date, remarks)
            allocation = Vehicleallocation.create(vehicle.id, unit_id)
            allocation.accept()
    return {"message":"Vehicles added successfully!"}

@bp.post('/vehicle/bulk')
def create_bulk_vehicles():
    file = request.files.get('file')
    data = get_vehicles_from_csv(file)
    for item in data:
        make, model, type, trim, year, lifespan, mileage, chassis_no, engine_no, supplier, contract_reference, date, remarks = item
        if make and date:
            date = datetime.strptime(date, "%m/%d/%Y")
            Vehicle.create(mileage, lifespan, make, model, type, trim, year, chassis_no, engine_no, supplier, contract_reference, date, remarks)
    return {"message":"Vehicles added successfully!"}

@bp.get('/vehicle/<int:id>')
def get_vehicle(id):
    vehicle = Vehicle.get_by_id(id)
    if vehicle is None:
        return {'message': 'Vehicle not found'}, 404
    if current_user.role == 'admin':
        units = Unit.get_all()
        return render_template('admin-single-vehicle.html', vehicle=vehicle, units=units)
    maintenance = [
        "Reactive",
        "Preventive",
        "Predictive",
        "Proactive",
        "Conditioning Monitoring"
    ]
    logs = Vehiclelog.get_by_vehicle_id(id)
    movements = Movement.get_by_vehicle_id(id)
    alert = Alert.get_by_vehicle_id(id)
    return render_template('mto-single-vehicle.html', vehicle=vehicle, maintenance=maintenance, logs=logs, alert=alert, movements=movements)

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
    mileage = request.form.get('mileage', type=int)
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
    vehicle.update(mileage, lifespan, make, model, type, trim, year, chassis_no, engine_no, supplier, contract_reference, date, remarks)
    return VehicleSchema().dump(vehicle), 200

@bp.delete('/vehicle/<int:id>')
def delete_vehicle(id):
    vehicle = Vehicle.get_by_id(id)
    if vehicle is None:
        return {'message': 'Vehicle not found'}, 404
    vehicle.delete()
    return {'message': 'Vehicle deleted successfully'}, 200

@bp.patch('/vehicle/accept/<int:id>')
def accept_vehicle(id):
    allocation = Vehicleallocation.get_by_id(id)
    if allocation is None:
        return {'message': 'Allocation not found'}, 404
    allocation.accept()
    return {'message': 'Allocation accepted successfully'}, 200

@bp.patch('/vehicle/reject/<int:id>')
def reject_vehicle(id):
    allocation = Vehicleallocation.get_by_id(id)
    if allocation is None:
        return {'message': 'Allocation not found'}, 404
    allocation.reject()
    return {'message': 'Allocation rejected successfully'}, 200

@bp.get('/vehicles')
def get_vehicles():
    if current_user.role == 'admin':
        unallocated = Vehicle.get_all()
        allocated = Vehicleallocation.get_all()
        return render_template('admin-vehicles.html', allocated=allocated, unallocated=unallocated)
    allocated = Vehicleallocation.get_all_by_unit_id(current_user.unit_id)
    unit = Unit.get_by_id(current_user.unit_id)
    return render_template('mto-vehicles.html', allocated=allocated, unit=unit)

@bp.get('/statistics')
def get_vehicles_statistics():
    if current_user.role == 'admin':
        units = Unit.get_all()
        return render_template('admin-statistics.html', units=units)
    unit = Unit.get_by_id(current_user.unit_id)
    return render_template('mto-statistics.html', unit=unit)

@bp.post('/statistics/data')
def get_vehicles_statistics_data():
    make = request.form.get('make', '')
    model = request.form.get('model', '')
    year = request.form.get('year', '')
    unit_id = request.form.get('unit_id')

    allocations = Vehicleallocation.get_by_unit_id_make_model_year(make, model, year, unit_id)
    
    labels = [allocation[0] for allocation in allocations]
    data = [allocation[1] for allocation in allocations]
    colors = make_color(len(allocations))

    return {
        "labels":labels,
        "data":data,
        "colors":colors,
    }

@bp.get('/statistics/table')
def get_vehicles_statistics_table():
    make = request.args.get('make', '')
    model = request.args.get('model', '')
    year = request.args.get('year', '')
    unit_id = request.args.get('unit_id')

    allocations = Vehicleallocation.get_by_unit_id_make_model_year_unstructured(make, model, year, unit_id)

    return {
        'data': [[
            allocation.vehicle.make,
            allocation.vehicle.model,
            allocation.vehicle.type,
            allocation.vehicle.chassis_no,
            allocation.vehicle.engine_no,
            allocation.vehicle.year,
            allocation.vehicle.lifespan,
            allocation.vehicle.remaining_life(),
            allocation.unit.name,
            ] for allocation in allocations]
        }

@bp.get('/requests')
def get_reallocation_vehicle_request():
    reallocations = Vehicleallocation.get_all_by_pending_loosing_unit_id(current_user.unit_id)
    allocations = Vehicleallocation.get_all_unaccepted_by_unit_id(current_user.unit_id)
    return render_template('requests.html', reallocations=reallocations, allocations=allocations)