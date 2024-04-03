from app import ma
from app.command.model import *

class CommandSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Command
        exclude = ('is_deleted',)