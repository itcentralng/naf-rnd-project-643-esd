from app import ma
from app.vehiclelog.model import *

class VehiclelogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehiclelog
        exclude = ('is_deleted',)