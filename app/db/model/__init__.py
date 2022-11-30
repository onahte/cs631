from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.sql import func

from .. import db


class Physician(db.Model):
    __tablename__ = 'physician'
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, id, ssn):
        self.id = id
        self.ssn = ssn

    def __repr__(self):
        return f'Physician({self.id}, {self.ssn})'


class Clinic(db.Model):
    __tablename__ = 'clinic'
    id = db.Column(db.Integer, primary_key=True)
    clinic_name = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    chief_id = db.Column(db.Integer, ForeignKey(Physician.id), nullable=False, unique=False)

    chief = relationship('Physician', foreign_keys='Clinic.chief_id')

    def __init__(self, id, clinic_name, street, city, state, zip, chief_id):
        self.id = id
        self.clinic_name = clinic_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.chief_id = chief_id

    def address(self):
        return self.street + " " + self.city + " " + self.state + " " + self.zip

    def __repr__(self):
        return f'Clinic({self.id}, {self.clinic_name}, {self.address()}, {self.chief_id})'


class Nurse(db.Model):
    __tablename__ = 'nurse'
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, id, ssn):
        self.id = id
        self.ssn = ssn

    def __repr__(self):
        return f'Nurse({self.id}, {self.ssn})'

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, id, ssn):
        self.id = id
        self.ssn = ssn

    def __repr__(self):
        return f'Patient({self.id}, {self.ssn})'