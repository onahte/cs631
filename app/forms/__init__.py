import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Length, NumberRange
from wtforms.fields import SelectField, IntegerField, StringField, SubmitField, RadioField, DateField, TimeField
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
    ssn = IntegerField('SSN', validators=[DataRequired()])
    gender = SelectField('Gender', choices=['M', 'F'], validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city =  StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=state_dropdown, validators=[DataRequired()])
    zip = IntegerField('Zip', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    eid = IntegerField('Physician EID', validators=[DataRequired()])
    submit = SubmitField('Submit')
'''
    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")
        with engine.connect() as connection:
            ssn_query = session.query(model.Patient).filter(model.Patient.ssn==ssn)
            if ssn:
                raise ValidationError("There is already a patient with that SSN.")
            connection.close()
        engine.dispose()
'''
class schedule_appt_patient_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Physician ID', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField("Submit")

class physician_options_form(FlaskForm):
    option = SelectField('Options', choices=[('View Schedule', 'View Schedule'), ('Remove','Remove Physician')],
                         validators=[DataRequired()])
    submit = SubmitField('Submit')

class physician_view_schedule_form(FlaskForm):
    eid = IntegerField('Physician EID', validators=[DataRequired()])
    date = DateField('Date', format='%m/%d/%Y', validators=[DataRequired()])
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
    ssn = IntegerField('SSN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city =  StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=state_dropdown, validators=[DataRequired()])
    gender = SelectField('Gender', choices=['M', 'F'], validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_salary(self, salary):
        if salary < 25000 or salary > 300000:
           raise ValidationError(f"Salary must be greater than 25,000 and less than 300,000.")
'''
    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")
        with engine.connect() as connection:
            ssn_query = session.query(model.Physician).filter(model.Physician.ssn==ssn)
            if ssn:
                raise ValidationError("There is already a physician with that SSN.")
            connection.close()
        engine.dispose()
'''
class add_nurse_form(FlaskForm):
    grade_option = ['CNA', 'LPN', 'RN', 'APRN']
    unit_option = [1,2,3,4,5,6,7]
    ssn = IntegerField('SSN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    grade = SelectField(choices=grade_option, validators=[DataRequired()])
    unit = SelectField(choices=unit_option, validators=[DataRequired()])
    gender = SelectField('Gender', choices=['M', 'F'], validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_salary(self, salary):
        if salary < 25000 or salary > 300000:
           raise ValidationError(f"Salary must be greater than 25,000 and less than 300,000.")
'''
    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")
'''

class remove_staff_form(FlaskForm):
    eid = IntegerField('EID', validators=[DataRequired()])
    submit = SubmitField("Submit")


class schedule_shift_form(FlaskForm):
    role = SelectField(choices=role_selection, validators=[DataRequired()])
    eid = IntegerField('EID', validators=[DataRequired()])
    date = DateField('Date', format='%m/%d/%Y', validators=[DataRequired()])
    start_time = TimeField('Start Time', formate='%H:%M', validators=[DataRequired()])
    end_time = TimeField('End Time', formate='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_date(self, date):
        if date < datetime.date.now():
            raise ValidationError(f"You cannot schedule a shift in passed date.")

    def validate_time(self, start_time, end_time):
        if start_time > end_time:
            raise ValidationError("Shift end time must be after start time.")

class inpatient_option_form(FlaskForm):
    inpatient_options = ['Check-in','View/Schedule Surgery', 'Reassign Nurse/Physician', 'Check-out']
    inpatient = SelectField('InPatient Options', choices=inpatient_options, validators=[DataRequired()])
    submit = SubmitField('Submit')

class inpatient_checkin_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    wing = SelectField('Wing', choices=['Blue', 'Green'], validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    bed = SelectField('Bed', choices=['A', 'B'], validators=[DataRequired()])
    check_in_date = DateField('Check In Date', format='%Y-%m-%d')
    check_in_time = TimeField('Check In Time', format='%H:%M')
    nurse_eid = IntegerField('Nurse')
    eid = IntegerField('Physician', validators=[DataRequired()])
    submit = SubmitField('Submit')

class assign_staff_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class view_surgery_form(FlaskForm):
    view_surgery_by = SelectField('View Surgery By', choices=[('Theatre','Theatre'), ('Surgeon','Surgeon'),
                                                              ('Patient','Patient')],
                                  render_kw={'onchange': "myFunction()"})
    options = IntegerField('ID')
    date = DateField('Date (Leave blank if query is by patient)', format='%H:%M')
    submit = SubmitField('Submit')

class schedule_surgery_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Surgeon ID', validators=[DataRequired()])
    surgery_code = IntegerField('Surgery Code', validators=[DataRequired()])
    theatre = IntegerField('Theatre', validators=[DataRequired()])
    date = DateField('Date', format='%m/%d/%Y', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')

class reassign_staff_form(FlaskForm):
    staff = SelectField('Staff Type', choices=[('Physician','Physician'), ('Nurse','Nurse')], validators=[DataRequired()])
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    eid = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
