from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# App Config
app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
JWTManager(app)

# Celery
from app.celery import make_celery
celery = make_celery(app)

# Database
from config import secret
app.secret_key = secret
migrate = Migrate(app, db)


# Controllers
from app.user.controller import bp as user_bp
app.register_blueprint(user_bp)
from app.vehicle.controller import bp as vehicle_bp
app.register_blueprint(vehicle_bp)
from app.dashboard.controller import bp as dashboard_bp
app.register_blueprint(dashboard_bp)
from app.unit.controller import bp as unit_bp
app.register_blueprint(unit_bp)
from app.location.controller import bp as location_bp
app.register_blueprint(location_bp)
from app.command.controller import bp as command_bp
app.register_blueprint(command_bp)
from app.vehiclelog.controller import bp as vehiclelog_bp
app.register_blueprint(vehiclelog_bp)
from app.alert.controller import bp as alert_bp
app.register_blueprint(alert_bp)

# Error handlers
# from .error_handlers import *