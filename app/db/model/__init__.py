from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.sql import func

from .. import db


class Physician(db.Model):
    __tablename__ = 'physician'
    eid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, eid, ssn):
        self.eid = eid
        self.ssn = ssn

    def __repr__(self):
        return f'Physician({self.eid}, {self.ssn})'


class Clinic(db.Model):
    __tablename__ = 'clinic'
    eid = db.Column(db.Integer, primary_key=True)
    clinic_name = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    chief_id = db.Column(db.Integer, ForeignKey(Physician.id), nullable=False, unique=False)

    chief = relationship('Physician', foreign_keys='Clinic.chief_id')

    def __init__(self, eid, clinic_name, street, city, state, zip, chief_id):
        self.eid = eid
        self.clinic_name = clinic_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.chief_id = chief_id

    def address(self):
        return self.street + " " + self.city + " " + self.state + " " + self.zip

    def __repr__(self):
        return f'Clinic({self.eid}, {self.clinic_name}, {self.address()}, {self.chief_id})'


class Nurse(db.Model):
    __tablename__ = 'nurse'
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, eid, ssn):
        self.eid = eid
        self.ssn = ssn

    def __repr__(self):
        return f'Nurse({self.eid}, {self.ssn})'

class Patient(db.Model):
    __tablename__ = 'patient'
    pid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, ssn):
        self.pid = pid
        self.ssn = ssn

    def __repr__(self):
        return f'Patient({self.pid}, {self.ssn})'