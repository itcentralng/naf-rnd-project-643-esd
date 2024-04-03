from app import ma
from app.location.model import *

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        exclude = ('is_deleted',)