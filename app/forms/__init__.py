import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Length, NumberRange
from wtforms.fields import SelectField, IntegerField, StringField, SubmitField, RadioField
from wtforms.fields.html5 import DateField, Time
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
    ssn = IntegerField('SSN', validators=[DataRequired()])
    submit = SubmitField("Submit")

class add_patient_form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ssn = IntegerField('SSN', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city =  StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=state_dropdown, validators=[DataRequired()])
    add = SubmitField("Add")
    submit = SubmitField('Submit')

    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")
        with engine.connect() as connection:
            ssn_query = session.query(model.Patient).filter(model.Patient.ssn==ssn)
            if ssn:
                raise ValidationError("There is already a patient with that SSN.")
            connection.close()
        engine.dispose()

class schedule_appt_patient_form(FlaskForm):
    physician_select = []
    curr_yr = datetime.now().year
    yr_select = [curr_yr, curr_yr+1, curr_yr+2]
    with engine.connect() as connection:
        physician_list = session.query(model.Physician)
        for p in physician_list:
            physician_select.append(p.eid)
        connection.close()
        engine.dispose()
    ssn = IntegerField('Patient SSN', validators=[DataRequired()])
    #year = SelectField('Year', choices=yr_select, validators=[DataRequired()])
    #month = SelectField('Month', choices=month_select, validators=[DataRequired()])
    #day = StringField('Day', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.date.now())
    time = Time('Time', validators=[DataRequired()], format='%hr:%min')
    eid = SelectField('Physician', choices=physician_select, validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")


class physician_view_schedule_form(FlaskForm):
    eid = IntegerField('Physician EID', validators=[DataRequired])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.now())
    submit = SubmitField('Submit')

class staff_options_form(FlaskForm):
    option_selection = ['Add', 'Remove', 'Schedule', 'View']
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
    salary = IntegerField('Salary', validators=[DataRequired])
    submit = SubmitField("Submit")

    def validate_salary(self, salary):
        if salary < 25000 or salary > 300000:
           raise ValidationError(f"Salary must be greater than 25,000 and less than 300,000.")

    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")
        with engine.connect() as connection:
            ssn_query = session.query(model.Physician).filter(model.Physician.ssn==ssn)
            if ssn:
                raise ValidationError("There is already a physician with that SSN.")
            connection.close()
        engine.dispose()

class add_nurse_form(FlaskForm):
    grade_option = ['CNA', 'LPN', 'RN', 'APRN']
    unit_option = [1,2,3,4,5,6,7]
    ssn = IntegerField('SSN', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    grade = SelectField(choices=grade_option, validators=[DataRequired()])
    unit = SelectField(choices=unit_option, validators=[DataRequired()])
    gender = SelectField('Gender', choices=['M', 'F'], validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired])
    submit = SubmitField("Submit")

    def validate_salary(self, salary):
        if salary < 25000 or salary > 300000:
           raise ValidationError(f"Salary must be greater than 25,000 and less than 300,000.")

    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")


class remove_staff_form(FlaskForm):
    eid = IntegerField('EID', validators=[DataRequired()])
    submit = SubmitField("Submit")

class view_physician(FlaskForm):
    ssn = IntegerField('SSN', validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")

class schedule_shift_form(FlaskForm):
    role = SelectField(choices=role_selection, validators=[DataRequired()])
    eid = IntegerField('EID', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.now())
    start_time = Time('Start Time', formate='%H:%M')
    end_time = Time('End Time', formate='%H:%M')
    submit = SubmitField('Submit')

    def validate_date(self, date):
        if date < datetime.date.now():
            raise ValidationError(f"You cannot schedule a shift in passed date.")

    def validate_time(self, start_time, end_time):
        if start_time > end_time:
            raise ValidationError("Shift end time must be after start time.")

class inpatient_option_form(FlaskForm):
    inpatient_options = ['Check Available Room/Bed', 'Assign Room/Bed', 'Assign Physician',
                         'Assign Nurse', 'View Scheduled Surgery', 'Book Surgery']
    inpatient = SelectField('InPatient Options', choices=inpatient_options, validators=[DataRequired])
    ssn = IntegerField('SSN', validators=[DataRequired])
    submit = SubmitField('Submit')

    def validate_ssn(self, ssn):
        if len(ssn) != 9:
            raise ValidationError("SSN must be 9 digits.")
        with engine.connect() as connection:
            ssn_query = session.query(model.Patient).filter(model.Patient.ssn==ssn)
            if ssn is None:
                raise ValidationError("There is no patient by that SSN. Please check your entry or first add patient via Add Patient page")
            connection.close()
        engine.dispose()

class select_bed_form(FlaskForm):
    pid = IntegerField('Patient ID', validators=[DataRequired()])
    wing = RadioField('Wing', choices=['Blue', 'Green'], validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
    bed = RadioField('Bed', choices=['A', 'B'], validators=[DataRequired()])
    submit = SubmitField('Submit')

class view_surgery_per_room_form(FlaskForm):

class view_surgery_per_surgeon_form(FlaskForm):

class view_surgery_per_patient_form(FlaskForm):

#'View Scheduled Surgery Per Day Per Room','View Schedule Surgery Per Day Per Surgeon'