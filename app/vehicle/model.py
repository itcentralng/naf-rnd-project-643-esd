from app import db
from sqlalchemy import func

from app.unit.model import Unit

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allocation = db.relationship('Vehicleallocation', viewonly=True)
    lifespan = db.Column(db.Integer)
    make = db.Column(db.String)
    model = db.Column(db.String)
    type = db.Column(db.String)
    trim = db.Column(db.String)
    year = db.Column(db.Integer)
    chassis_no = db.Column(db.String)
    engine_no = db.Column(db.String)
    supplier = db.Column(db.String)
    contract_reference = db.Column(db.String)
    date = db.Column(db.DateTime)
    remarks = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, lifespan=None, make=None, model=None, type=None, trim=None, year=None, chassis_no=None, engine_no=None, supplier=None, contract_reference=None, date=None, remarks=None):
        self.lifespan = lifespan or self.lifespan
        self.make = make or self.make
        self.model = model or self.model
        self.type = type or self.type
        self.trim = trim or self.trim
        self.year = year or self.year
        self.chassis_no = chassis_no or self.chassis_no
        self.engine_no = engine_no or self.engine_no
        self.supplier = supplier or self.supplier
        self.contract_reference = contract_reference or self.contract_reference
        self.date = date or self.date
        self.remarks = remarks or self.remarks
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    def remaining_life(self):
        difference = db.session.query(func.strftime('%Y', func.date('now')) - func.strftime('%Y', self.date)).scalar()
        return self.lifespan - difference
    

    @classmethod
    def get_by_make_model_year(cls, make, model, year):
        result = db.session.query(Vehicle.type, func.count()).filter(
        Vehicle.make.ilike(f'%{make}%'),
        Vehicle.model.ilike(f'%{model}%'),
        Vehicle.year == year,
        ).group_by(Vehicle.type).all()

        print(result)

        # Format the result as desired
        return [(row[0], row[1]) for row in result]


    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.is_deleted==False, ~cls.allocation.any()).all()
    
    @classmethod
    def create(cls, lifespan, make, model, type, trim, year, chassis_no, engine_no, supplier, contract_reference, date, remarks):
        vehicle = cls(lifespan=lifespan, make=make, model=model, type=type, trim=trim, year=year, chassis_no=chassis_no, engine_no=engine_no, supplier=supplier, contract_reference=contract_reference, date=date, remarks=remarks)
        vehicle.save()
        return vehicle

class Vehicleallocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle = db.relationship('Vehicle')
    unit = db.relationship('Unit', primaryjoin="Vehicleallocation.unit_id == Unit.id")
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    loosing_unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    status = db.Column(db.String, default='pending')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = db.func.now()
        db.session.commit()
    
    def accept(self):
        if self.status == 'pending':
            self.status = 'active'
        else:
            self.status = 'pending'
        self.update()
    
    def reject(self):
        self.status = 'rejected'
        self.update()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_by_unit_id_vehicle_id_active(cls, unit_id, vehicle_id):
        return cls.query.filter_by(unit_id=unit_id, vehicle_id=vehicle_id, is_deleted=False, status='active').first()
    
    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(is_deleted=False, status='active').all()
    
    @classmethod
    def get_by_unit_id_make_model_year(cls, make='', model='', year=0, unit_id=None):
        result = db.session.query(Unit.name, func.count(Vehicle.id)).join(Vehicleallocation, Vehicleallocation.unit_id == Unit.id).join(Vehicle, Vehicle.id == Vehicleallocation.vehicle_id)
        if unit_id:
            result = result.filter(Vehicleallocation.unit_id == unit_id)
        if make:
            result = result.filter(Vehicle.make.ilike(f'%{make}%'))
        if model:
            result = result.filter(Vehicle.model.ilike(f'%{model}%'))
        if year:
            result = result.filter(Vehicle.year == year)

        return result.group_by(Unit.name).all()
    
    @classmethod
    def get_by_unit_id_make_model_year_unstructured(cls, make='', model='', year=0, unit_id=None):
        result = db.session.query(Vehicleallocation).join(Vehicle, Vehicle.id == Vehicleallocation.vehicle_id)
        if unit_id:
            result = result.filter(Vehicleallocation.unit_id == unit_id)
        if make:
            result = result.filter(Vehicle.make.ilike(f'%{make}%'))
        if model:
            result = result.filter(Vehicle.model.ilike(f'%{model}%'))
        if year:
            result = result.filter(Vehicle.year == year)

        return result.all()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.is_deleted==False, cls.status!='inactive').all()
    
    @classmethod
    def get_all_by_unit_id(cls, unit_id):
        return cls.query.filter(cls.is_deleted==False, cls.unit_id==unit_id, cls.status=='active').all()
    
    @classmethod
    def get_all_by_pending_loosing_unit_id(cls, unit_id):
        return cls.query.filter(cls.is_deleted==False, cls.status=='reallocated', cls.loosing_unit_id==unit_id).all()
    
    @classmethod
    def get_all_unaccepted_by_unit_id(cls, unit_id):
        return cls.query.filter(cls.is_deleted==False, cls.status=='pending', cls.unit_id==unit_id).all()
    
    @classmethod
    def get_by_vehicle_id(cls, vehicle_id):
        return cls.query.filter(cls.is_deleted==False, cls.vehicle_id==vehicle_id).first()
    
    @classmethod
    def create(cls, vehicle_id, unit_id):
        allocation = cls.get_by_vehicle_id(vehicle_id)
        if not allocation:
            allocation = cls(vehicle_id=vehicle_id, unit_id=unit_id)
            allocation.save()
        if allocation.unit_id != unit_id and (allocation.status == 'active' or allocation.status == 'rejected'):
            allocation.status = 'reallocated'
            allocation.loosing_unit_id = allocation.unit_id
            allocation.unit_id = unit_id
            allocation.update()
        return allocation