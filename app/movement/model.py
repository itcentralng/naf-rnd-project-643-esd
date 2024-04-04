from app import db
from app.alert.model import Alert
from app.vehicle.model import Vehicle

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    date = db.Column(db.DateTime)
    driver = db.Column(db.String)
    starting_point = db.Column(db.String)
    mileage = db.Column(db.Integer)
    destination = db.Column(db.String)
    remarks = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, date=None, driver=None, starting_point=None, mileage=None, destination=None, remarks=None):
        self.date = date or self.date
        self.driver = driver or self.driver
        self.starting_point = starting_point or self.starting_point
        self.mileage = mileage or self.mileage
        self.destination = destination or self.destination
        self.remarks = remarks or self.remarks
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
    def create(cls, vehicle_id, date, driver, starting_point, mileage, destination, remarks):
        movement = cls(vehicle_id=vehicle_id, date=date, driver=driver, starting_point=starting_point, mileage=mileage, destination=destination, remarks=remarks)
        movement.save()

        vehicle = Vehicle.get_by_id(vehicle_id)
        alert = Alert.get_by_vehicle_id(vehicle_id)
        vehicle.mileage = vehicle.mileage or 0
        vehicle.mileage += mileage
        vehicle.update()
        
        alert.current_mileage = alert.current_mileage or 0
        alert.current_mileage += mileage
        alert.update()
        return movement