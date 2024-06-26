from flask import Blueprint, g, request, flash, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_login import login_user

from app.user.model import User
from app.user.schema import UserSchema
from app.route_guard import auth_required
bp = Blueprint('user', __name__, template_folder='templates')

@bp.post('/login')
def login():
    email = request.form.get('username')
    password = request.form.get('password')

    user = User.get_by_email(email)
    
    if user is None:
        flash("User not found")
        return redirect('/')
    if not user.check_password(password):
        flash("Wrong password")
        return redirect('/')
    login_user(user)
    if 'next' in request.args:
        return redirect(request.args['next'])
    return redirect('/dashboard')

@bp.patch('/reset-password')
@auth_required()
def reset_password():
    new_password = request.form.get('password')
    if not new_password:
        return {'message': 'Password is required'}, 400
    elif len(new_password) < 6:
        return {'message': 'Password must be at least 6 characters'}, 400
    g.user.reset_password(new_password)
    return {'message': 'Password updated successfully'}, 200
    

@bp.post('/personnel/<int:unit_id>')
def register(unit_id):
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    role = request.form.get('role', 'mto')
    user = User.get_by_email(email)
    if user is not None:
        return {'message': 'User already exists'}, 400
    user = User.create(name, phone, email, password, role, unit_id)
    if user is not None:
        return {'message': 'User created'}, 201
    return {'message': 'User not created'}, 400

@bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    user = User.get_by_id(get_jwt_identity())
    # generate token
    access_token = user.generate_refreshed_access_token()
    return {"status": "success", "message": "Request processed succesfully", 'access_token': access_token}, 200