from app import db
from app.user.model import User
from app.vehicle.model import Vehicleallocation
from helpers.sms import SMS

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    mileage_limit = db.Column(db.Integer)
    current_mileage = db.Column(db.Integer)
    status = db.Column(db.String, default='active')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, vehicle_id=None, mileage_limit=None, current_mileage=None, status=None):
        self.vehicle_id = vehicle_id or self.vehicle_id
        self.mileage_limit = mileage_limit or self.mileage_limit
        self.current_mileage = current_mileage or self.current_mileage
        self.status = status or self.status
        self.trigger_alert()
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()
    
    def trigger_alert(self):
        if self.current_mileage >= self.mileage_limit and self.status == 'active':
            allocation = Vehicleallocation.get_by_vehicle_id(self.vehicle_id)
            users = User.get_all_by_unit_id(allocation.unit_id)
            message = f"This is to notify you that the current mileage on the vehicle - {allocation.vehicle.make} {allocation.vehicle.model} {allocation.vehicle.year} has reached {self.current_mileage} and needs to be serviced!"
            sms = SMS()
            for user in users:
                if user.role == 'mto' and user.phone:
                    sms.send(user.phone, message)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_by_vehicle_id(cls, vehicle_id):
        return cls.query.filter_by(vehicle_id=vehicle_id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, vehicle_id, mileage_limit, current_mileage, status):
        alert = cls.get_by_vehicle_id(vehicle_id)
        if not alert:
            alert = cls(vehicle_id=vehicle_id, mileage_limit=mileage_limit, current_mileage=current_mileage, status=status)
            alert.save()
        alert.update(vehicle_id, mileage_limit, current_mileage, status)
        return alert