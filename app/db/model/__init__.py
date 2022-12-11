from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, aliased

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
    clinic_id = db.Column(db.Integer, primary_key=True)
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
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

    def __init__(self, eid, ssn):
        self.eid = eid
        self.ssn = ssn

    def __repr__(self):
        return f'Nurse({self.eid}, {self.ssn})'

class Patient(db.Model):
    __tablename__ = 'patient'
    pid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, ssn):
        self.pid = pid
        self.ssn = ssn

    def __repr__(self):
        return f'Patient({self.pid}, {self.ssn})'

class Consultation(db.Model):
    __tablename__ = 'consultation'
    consultation_id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __init__(self, consultation_id, eid, pid, date, time):
        self.consultation_id = consultation_id
        self.eid = eid
        self.pid = pid
        self.date = date
        self.time = time

    def __repr__(self):
        return f'Consultation{self.consultation_id}, {self.eid}, {self.pid}, {self.date}, {self.time})'

class Physician_Schedule(db.Model):
    __tablename__ = 'staff_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, schedule_id, eid, date, start_time, end_time):
        self.schedule_id = schedule_id
        self.eid = eid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Nurse_Schedule(db.Model):
    __tablename__ = 'staff_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, schedule_id, eid, date, start_time, end_time):
        self.schedule_id = schedule_id
        self.eid = eid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Surgeon_Schedule(db.Model):
    __tablename__ = 'staff_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, schedule_id, eid, date, start_time, end_time):
        self.schedule_id = schedule_id
        self.eid = eid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class SupportStaff_Schedule(db.Model):
    __tablename__ = 'staff_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, schedule_id, eid, date, start_time, end_time):
        self.schedule_id = schedule_id
        self.eid = eid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Bed(db.Model):
    __tablename__ = 'bed'
    pid = db.Column(db.Integer, primary_key=True)
    wing = db.Column(db.String, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    bed = db.Column(db.String, nullable=False)

    def __init__(self, pid, wing, room, bed):
        self.pid = pid
        self.wing = wing
        self.room = room
        self.bed = bed

class Inpatient(db.Model):
    __tablename__ = 'inpatient'
    pid = db.Column(db.Integer, primary_key=True)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    bed_id = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, check_in, check_out, bed_id):
        self.pid = pid
        self.check_in = check_in
        self.check_out = check_out
        self.bed_id = bed_id

class Nurse_Inpatient(db.Model):
    __tablename__ = 'inpatient'
    pid = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, eid):
        self.pid = pid
        self.eid = eid