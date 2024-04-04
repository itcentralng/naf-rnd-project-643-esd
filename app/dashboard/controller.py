from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from app.route_guard import auth_required

from app.dashboard.model import *
from app.dashboard.schema import *
from app.unit.model import Unit
from app.vehicle.model import Vehicle, Vehicleallocation

bp = Blueprint('dashboard', __name__)

@bp.get('/dashboard')
@login_required
def view_dashboard():
    if current_user.role == 'admin':
        unallocated = Vehicle.get_all()
        allocated = Vehicleallocation.get_all()
        units = Unit.get_all()
        return render_template('admin-dashboard.html', unallocated=unallocated, allocated=allocated, units=units)
    allocated = Vehicleallocation.get_all_by_unit_id(current_user.unit_id)
    serviceable = [i for i in allocated if i.vehicle.service == 'Serviceable']
    unserviceable = [i for i in allocated if i.vehicle.service == 'Unserviceable']
    ber = [i for i in allocated if i.vehicle.service == 'Beyond Economic Repairs']
    return render_template('mto-dashboard.html', allocated=allocated, ber=ber, serviceable=serviceable, unserviceable=unserviceable)