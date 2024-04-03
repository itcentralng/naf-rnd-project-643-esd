from app import ma
from app.vehicle.model import *

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        exclude = ('is_deleted',)

class VehicleAllocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicleallocation
        exclude = ('is_deleted',)
    vehicle = ma.Nested('VehicleSchema')