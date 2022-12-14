from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, NumberRange
from wtforms.fields import SelectField, IntegerField, StringField, SubmitField, DateField, TimeField
from sqlalchemy.orm import sessionmaker
from ..db import db, model, engine

Session = sessionmaker(bind=engine)
session = Session()

month_select = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
role_selection = ['Physician', 'Nurse', 'Surgeon', 'Support Staff']
state_dropdown = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
                  'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
                  'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
                  'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

class patient_options_form(FlaskForm):
    option_selection = ['View Patient Data', 'Add New Patient', 'Check Previous Diagnosis',
                        'Schedule Appointment', 'View Past Appointments']
    options = SelectField(choices=option_selection, validators=[DataRequired()])
    submit = SubmitField("Submit")

class query_patient_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    submit = SubmitField("Submit")

class add_patient_form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ssn = StringField('SSN', validators=[DataRequired()])
    gender = SelectField('Gender', choices=['M', 'F'], validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city =  StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=state_dropdown, validators=[DataRequired()])
    zip = StringField('Zip', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    eid = IntegerField('Physician EID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class schedule_appt_patient_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Physician ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField("Submit")

class physician_options_form(FlaskForm):
    option = SelectField('Options', choices=[('View Schedule', 'View Schedule'), ('Remove','Remove Physician')],
                         validators=[DataRequired()])
    submit = SubmitField('Submit')

class physician_view_schedule_form(FlaskForm):
    eid = IntegerField('Physician EID', validators=[DataRequired()])
    date = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

class staff_options_form(FlaskForm):
    option_selection = ['Add', 'Remove', 'Schedule', 'View Staff by Type']
    options = SelectField(choices=option_selection, validators=[DataRequired()])
    role = SelectField(choices=role_selection, validators=[DataRequired()])
    submit = SubmitField("Submit")

class staff_type_form(FlaskForm):
    options = SelectField(choices=role_selection, validators=[DataRequired()])
    submit = SubmitField('Submit')

class add_staff_form(FlaskForm):
    ssn = StringField('SSN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city =  StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=state_dropdown, validators=[DataRequired()])
    zip = StringField('Zip Code', validators=[DataRequired()])
    gender = SelectField('Gender', choices=['M', 'F'], validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(), NumberRange(25000, 300000)])
    submit = SubmitField("Submit")

class add_nurse_form(FlaskForm):
    grade_option = ['CNA', 'LPN', 'RN', 'APRN']
    unit_option = [1,2,3,4,5,6,7]
    ssn = StringField('SSN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    grade = SelectField(choices=grade_option, validators=[DataRequired()])
    unit = SelectField(choices=unit_option, validators=[DataRequired()])
    gender = SelectField('Gender', choices=['M', 'F'], validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(), NumberRange(25000, 300000)])
    submit = SubmitField("Submit")


class remove_staff_form(FlaskForm):
    eid = IntegerField('EID', validators=[DataRequired()])
    submit = SubmitField("Submit")


class schedule_shift_form(FlaskForm):
    eid = IntegerField('EID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_date(self, date):
        if date.data < datetime.now().date():
            raise ValidationError(f"You cannot schedule a shift in passed date.")

    def validate_time(self, start_time, end_time):
        if start_time.data > end_time.data:
            raise ValidationError("Shift end time must be after start time.")

class inpatient_option_form(FlaskForm):
    inpatient_options = ['Check-in','View Surgery', 'Schedule Surgery', 'Reassign Nurse/Physician', 'Check-out']
    inpatient = SelectField('Inpatient Options', choices=inpatient_options, validators=[DataRequired()])
    submit = SubmitField('Submit')

class inpatient_checkin_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    wing = SelectField('Wing', choices=['Blue', 'Green'], validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    bed = SelectField('Bed', choices=['A', 'B'], validators=[DataRequired()])
    check_in_date = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    check_in_time = TimeField('Check In Time')
    nurse_eid = IntegerField('Nurse')
    eid = IntegerField('Physician', validators=[DataRequired()])
    submit = SubmitField('Submit')

class assign_staff_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class view_surgery_form(FlaskForm):
    view_surgery_by = SelectField('View Surgery By', choices=[('Theatre','Theatre'), ('Surgeon','Surgeon'),
                                                              ('Patient','Patient')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class view_by_theatre_form(FlaskForm):
    theatre = SelectField('Surgery Theatre', choices=[1001, 1002], validators=[DataRequired()])
    submit = SubmitField('Submit')

class view_by_surgeon_form(FlaskForm):
    surgeon = IntegerField('Surgeons', validators=[DataRequired()])
    submit = SubmitField('Submit')

class view_by_patient_form(FlaskForm):
    patient = IntegerField('Patient', validators=[DataRequired()])
    submit = SubmitField('Submit')

class schedule_surgery_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Surgeon ID', validators=[DataRequired()])
    surgery_code = IntegerField('Surgery Code', validators=[DataRequired()])
    theatre = IntegerField('Theatre', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')

class reassign_staff_form(FlaskForm):
    staff = SelectField('Staff Type', choices=[('Physician','Physician'), ('Nurse','Nurse')], validators=[DataRequired()])
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
