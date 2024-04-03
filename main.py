import sys
sys.dont_write_bytecode = True

from app import app
from app.user.model import User

from flask import render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, logout_user

#Flask Login Setup
LOGINMANAGER = LoginManager()
LOGINMANAGER.init_app(app)
LOGINMANAGER.login_view = 'index'

#Loading Teachers to Flask-Login
@LOGINMANAGER.user_loader
def load_user(_user):
    '''
    Queries and loads all users from the db module.
    '''
    #Getting all users from the database
    user = User.query.get(_user)
    return user

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/dashboard')

@app.route('/health')
def health():
    # TODO do some checks here to confirm everything works
    return {'status':'OK'}, 200

if __name__ == '__main__':
    app.run(debug=True)