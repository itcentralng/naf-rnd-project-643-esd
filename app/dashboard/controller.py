from flask import Blueprint, request, render_template
from flask_login import login_required
from app.route_guard import auth_required

from app.dashboard.model import *
from app.dashboard.schema import *

bp = Blueprint('dashboard', __name__)

@bp.get('/dashboard')
@login_required
def view_dashboard():
    return render_template('dashboard.html')