from app import db
from app.alert.model import Alert
from app.vehicle.model import Vehicle

class Vehiclelog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    mileage = db.Column(db.Integer)
    type = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, default=db.func.now())
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, vehicle_id=None, mileage=None, type=None, description=None, date=None):
        self.vehicle_id = vehicle_id or self.vehicle_id
        self.mileage = mileage or self.mileage
        self.type = type or self.type
        self.description = description or self.description
        self.date = date or self.date
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_by_vehicle_id(cls, vehicle_id):
        return cls.query.filter_by(is_deleted=False, vehicle_id=vehicle_id).all()
    
    @classmethod
    def create(cls, vehicle_id, mileage, type, description, date):
        vehiclelog = cls(vehicle_id=vehicle_id, mileage=mileage, type=type, description=description, date=date)
        vehiclelog.save()
        vehicle = Vehicle.get_by_id(vehicle_id)
        alert = Alert.get_by_vehicle_id(vehicle_id)
        vehicle.mileage = vehicle.mileage or 0
        vehicle.mileage += mileage
        vehicle.update()
        
        alert.current_mileage = alert.current_mileage or 0
        alert.current_mileage += mileage
        alert.update()
        return vehiclelog