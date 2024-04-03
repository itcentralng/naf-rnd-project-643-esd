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
    unallocated = Vehicle.get_all()
    allocated = Vehicleallocation.get_all()
    units = Unit.get_all()
    return render_template('mto-dashboard.html', unallocated=unallocated, allocated=allocated, units=units)