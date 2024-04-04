from app import ma
from app.alert.model import *

class AlertSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Alert
        exclude = ('is_deleted',)