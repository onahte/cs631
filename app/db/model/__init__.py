from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, aliased

from .. import db


class Address(db.Model):
    __tablename__ = 'address'
    eid = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

    def __init__(self, eid, street, city, state, zip):
        self.eid = eid
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def address(self):
        return self.street + " " + self.city + " " + self.state + " " + self.zip

    def __repr__(self):
        return f'Address({self.eid}, {self.address()})'


class Allergy(db.Model):
    __tablename__ = 'allergy'
    allergy_code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    medical_code = db.Column(db.Integer, nullable=False)

    def __init__(self, allergy_code, name, medical_code):
        self.allergy_code = allergy_code
        self.name = name
        self.medical_code = medical_code

    def __repr__(self):
        return f'Allergy({self.allergy_code}, {self.name}, {self.medical_code})'

class Physician(db.Model):
    __tablename__ = 'physician'
    eid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.BIGINT, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, eid, ssn, name):
        self.eid = eid
        self.ssn = ssn
        self.name = name

    def __repr__(self):
        return f'Physician({self.eid}, {self.ssn}, {self.name})'

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

class Clinic(db.Model):
    __tablename__ = 'clinic'
    cid = db.Column(db.Integer, primary_key=True)
    clinic_name = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.BIGINT, nullable=False)
    chief_id = db.Column(db.Integer, ForeignKey(Physician.eid), nullable=False, unique=False)

    chief = relationship('Physician', foreign_keys='Clinic.chief_id')

    def __init__(self, cid, clinic_name, street, city, state, zip, chief_id):
        self.cid = cid
        self.clinic_name = clinic_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.chief_id = chief_id

    def address(self):
        return self.street + " " + self.city + " " + self.state + " " + self.zip

    def __repr__(self):
        return f'Clinic({self.cid}, {self.clinic_name}, {self.address()}, {self.chief_id})'

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


class Contract(db.Model):
    __tablename__ = 'contract'
    eid = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)

    def __init__(self, eid, rate, start, end):
        self.eid = eid
        self.rate = rate
        self.start = start
        self.end = end

    def __repr__(self):
        return f'Contract({self.eid}, {self.rate}, {self.start}, {self.end})'


class Corporate(db.Model):
    __tablename__ = 'corporate'
    corporate_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip = db.Column(db.BIGINT, nullable=False)

    def __init__(self, corporate_id, name, street, city, state, zip):
        self.corporate_id = corporate_id
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def address(self):
        return self.street + " " + self.city + " " + self.state + " " + self.zip

    def __repr__(self):
        return f'Corporate({self.corporate_id}, {self.name} {self.address()})'


class Gender(db.Model):
    __tablename__ = 'gender'
    eid = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.CHAR(1), nullable=False)

    def __init__(self, eid, gender):
        self.eid = eid
        self.gender = gender

    def __repr__(self):
        return f'Gender({self.eid}, {self.gender})'


class Illness(db.Model):
    __tablename__ = 'illness'
    illness_code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    medical_code = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, illness_code, name, medical_code):
        self.illness_code = illness_code
        self.name = name
        self.medical_code = medical_code

    def __repr__(self):
        return f'Illness({self.illness_code}, {self.name}, {self.medical_code})'

class Inpatient(db.Model):
    __tablename__ = 'inpatient'
    pid = db.Column(db.Integer, primary_key=True)
    check_in_date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.Time, nullable=False)
    check_out_date = db.Column(db.Date)
    check_out_time = db.Column(db.Time)
    eid = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, check_in_date, check_in_time, check_out_date, check_out_time, physician_eid):
        self.pid = pid
        self.check_in_date = check_in_date
        self.check_in_time = check_in_time
        self.check_out_date = check_out_date
        self.check_out_time = check_out_time
        self.eid = eid

class Medical_Data(db.Model):
    __tablename__ = 'medical_data'
    pid = db.Column(db.Integer, primary_key=True)
    total_cholesterol = db.Column(db.Integer, nullable=False)
    HDL = db.Column(db.Integer, nullable=False)
    triglyceride = db.Column(db.Integer, nullable=False)
    LDL = db.Column(db.Integer, nullable=False)
    sugar_level = db.Column(db.Integer, nullable=False)
    blood_type = db.Column(db.String, nullable=False)
    heart_disease_risk = db.Column(db.String, nullable=False)

    def __init__(self, pid, total_cholesterol, HDL, triglyceride, LDL, sugar_level, blood_type,
                 heart_disease_risk):
        self.pid = pid
        self.total_cholesterol = total_cholesterol
        self.HDL = HDL
        self.triglyceride = triglyceride
        self.LDL = LDL
        self.sugar_level = sugar_level
        self.blood_type = blood_type
        self.heart_disease_risk = heart_disease_risk

    def __repr__(self):
        return f'Medicaldata({self.medical_code}, {self.pid}, {self.total_cholesterol}, {self.HDL}, ' \
               f'{self.triglyceride} {self.LDL}, {self.sugar_level}, {self.blood_type}, {self.heart_disease_risk})'


class Medication(db.Model):
    __tablename__ = 'medication'
    medication_code = db.Column(db.Integer, primary_key=True)
    unit_cost = db.Column(db.Integer, nullable=False)
    year_date_usage = db.Column(db.String, nullable=False)
    inventory_quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, medication_code, unit_cost, year_date_usage, inventory_quantity, order_date, name):
        self.medication_code = medication_code
        self.unit_cost = unit_cost
        self.year_date_usage = year_date_usage
        self.inventory_quantity = inventory_quantity
        self.order_date = order_date
        self.name = name

    def __repr__(self):
        return f'Medication({self.medication_code}, {self.unit_cost}, {self.year_date_usage}, ' \
               f'{self.inventory_quantity}, {self.order_date}, {self.name})'


class Nurse(db.Model):
    __tablename__ = 'nurse'
    eid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.BIGINT, nullable=False, unique=True)
    grade = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, eid, ssn, grade, name):
        self.eid = eid
        self.ssn = ssn
        self.grade = grade
        self.name = name

    def __repr__(self):
        return f'Nurse({self.eid}, {self.ssn}, {self.grade}, {self.name})'


class Nurse_Assign_Surgery(db.Model):
    __tablename__ = 'nurse_assign_surgery'
    eid = db.Column(db.Integer, primary_key=True)
    surgery_code = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, eid, surgery_code):
        self.eid = eid
        self.surgery_code = surgery_code

    def __repr__(self):
        return f'Assign({self.eid}, {self.surgery_code})'

class Nurse_Assign_Inpatient(db.Model):
    __tablename__ = 'nurse_assign_inpatient'
    pid = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, eid):
        self.pid = pid
        self.eid = eid

class Nurse_Schedule(db.Model):
    __tablename__ = 'nurse_schedule'
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

class Nurse_Unit(db.Model):
    __tablename__ = 'nurse_unit'
    eid = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, nullable=False)
    wing = db.Column(db.String(10), nullable=False)

    def __init__(self, eid, unit):
        self.eid = eid
        self.unit = unit

class Own(db.Model):
    __tablename__ = 'own'
    own_id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    corporate_id = db.Column(db.Integer)
    eid = db.Column(db.Integer)
    percent_own = db.Column(db.Integer)

    def __init__(self, cid, owner_id, percent_own):
        self.cid = cid
        self.owner_id = owner_id
        self.percent_own = percent_own

    def __repr__(self):
        return f'Own({self.cid}, {self.corporate_id}, {self.eid}, {self.percent_own})'

class Patient(db.Model):
    __tablename__ = 'patient'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    ssn = db.Column(db.BIGINT, nullable=False, unique=True)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.CHAR(1), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.BIGINT, nullable=False)
    number = db.Column(db.BIGINT, nullable=False)
    eid = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, ssn, name, street, city, state, zip, dob, gender, number, eid):
        self.pid = pid
        self.ssn = ssn
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.dob = dob
        self.gender = gender
        self.number = number
        self.eid = eid

    def __repr__(self):
        return f'Patient({self.pid}, {self.ssn})'

class Physician_Schedule(db.Model):
    __tablename__ = 'physician_schedule'
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

class Prescription(db.Model):
    __tablename__ = 'prescription'
    prescription_id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)
    medication_code = db.Column(db.Integer, nullable=False)
    dosage = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    interaction = db.Column(db.String, nullable=False)
    medical_code = db.Column(db.Integer, nullable=False)

    def __init__(self, prescription_id, eid, medication_code, dosage, frequency, interaction, medical_code):
        self.prescription_id = prescription_id
        self.eid = eid
        self.medication_code = medication_code
        self.dosage = dosage
        self.frequency = frequency
        self.interaction = interaction
        self.medical_code = medical_code

    def __repr__(self):
        return f'Prescription({self.prescription_id}, {self.eid}, {self.medication_code}, ' \
               f'{self.dosage}, {self.frequency}, {self.interaction}, {self.medical_code})'


class Salary(db.Model):
    __tablename__ = 'salary'
    eid = db.Column(db.Integer, nullable=False, primary_key=True)
    salary = db.Column(db.Integer, nullable=False)

    def __init__(self, salary, eid):
        self.salary = salary
        self.eid = eid

    def __repr__(self):
        return f'Salary({self.salary}, {self.eid})'

class Skill_Possessed(db.Model):
    __tablename__ = 'skill_possessed'
    eid = db.Column(db.Integer, primary_key=True, unique=False)
    skill_code = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, eid, skill_code):
        self.eid = eid
        self.skill_code = skill_code

    def __repr__(self):
        return f'possess({self.eid}, {self.skill_code})'

class SurgerySchedule (db.Model):
    __tablename__ = 'surgery_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    surgery_code = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    eid = db.Column(db.Integer, nullable=False)
    theatre = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __init__(self, schedule_id, surgery_code, pid, eid, theatre, date, time):
        self.schedule_id = schedule_id
        self.surgery_code = surgery_code
        self.pid = pid
        self.eid = eid
        self.theatre = theatre
        self.date = date
        self.time = time

    def __repr__(self):
        return f'Schedule({self.schedule_id}, {self.surgery_code}, {self.pid}, ' \
               f'{self.eid}, {self.theatre}, {self.date}, {self.time})'

class Skill(db.Model):
    __tablename__ = 'skill'
    skill_code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __init__(self, skill_code, description):
        self.skill_code = skill_code
        self.description = description

    def __repr__(self):
        return f'Skill({self.skill_code}, {self.description})'

class Staff(db.Model):
    __tablename__ = 'staff'
    eid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.BIGINT, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, eid, ssn, name):
        self.eid = eid
        self.ssn = ssn
        self.name = name

    def __repr__(self):
        return f'Staff({self.eid}, {self.ssn}, {self.name})'

class Surgeon(db.Model):
    __tablename__ = 'surgeon'
    eid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.BIGINT, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, eid, ssn, name):
        self.eid = eid
        self.ssn = ssn
        self.name = name

    def __repr__(self):
        return f'Surgeon({self.eid}, {self.ssn}, {self.name})'

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

class Surgery(db.Model):
    __tablename__ = 'surgery'
    surgery_code = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    skill_code = db.Column(db.Integer, nullable=False)
    special_needs = db.Column(db.String, nullable=False)
    anatomical_location = db.Column(db.String, nullable=False)
    rarity = db.Column(db.String, nullable=False)

    def __init__(self, surgery_code, type, skill_code, special_needs, anatomical_location, rarity):
        self.surgery_code = surgery_code
        self.type = type
        self.skill_code = skill_code
        self.special_needs = special_needs
        self.anatomical_location = anatomical_location
        self.rarity = rarity

    def __repr__(self):
        return f'Surgery({self.surgery_code}, {self.type}, {self.skill_code}, {self.special_needs}, ' \
               f'{self.anatomical_location}, {self.rarity})'


'''
class Works_At_Clinic(db.Model):
    __tablename__ = 'work'
    cid = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.Integer, nullable=False)

    def __init__(self, cid, eid):
        self.cid = cid
        self.eid = eid

    def __repr__(self):
        return f'Work({self.cid}, {self.eid})'
'''
