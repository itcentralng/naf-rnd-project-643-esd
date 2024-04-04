from app import ma
from app.movement.model import *

class MovementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movement
        exclude = ('is_deleted',)