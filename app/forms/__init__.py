import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import *
from sqlalchemy.orm import sessionmaker
from ..db import db, model, engine

Session = sessionmaker(bind=engine)
session = Session()

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

class schedule_appt_patient_form(FlaskForm):
    with engine.connect() as connection:
        physician_list = session.query(Physician)
        connection.close()
        engine.dispose()
    physician_select = []
    physician_select_id = []
    for physician in physician_list:
        physician_select.append(physician.name)
        physician_select_id.append(physician.eid)
    month_select = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    curr_yr = datetime.now().year
    yr_select = [curr_yr, curr_yr+1, curr_yr+2]
    ssn = IntegerField('Patient SSN', validators=[DataRequired()])
    year = SelectField('Year', choices=yr_select, validators=[DataRequired()])
    month = SelectField('Month', choices=month_select, validators=[DataRequired()])
    day = DateTimeField('Day', validators=[DataRequired()])
    time = DateTimeField('Time', validators=[DataRequired()])
    submit = SubmitField("Submit")


class staff_role_options_form(FlaskForm):
    option_selection = ['Physician', 'Nurse', 'Surgeon', 'Support Staff']
    options = SelectField(choices=option_selection, validators=[DataRequired()])
    submit = SubmitField("Submit")

class staff_options_form(FlaskForm):
    option_selection = ['Add/Remove', 'Schedule', 'View']
    options = SelectField(choices=option_selection, validators=[DataRequired()])
    submit = SubmitField("Submit")

class add_staff(FlaskForm):
    option_selection = ['Physician', 'Nurse', 'Surgeon', 'Support Staff']
    options = SelectField(choices=option_selection, validators=[DataRequired()])
    ssn = IntegerField('SSN', validators=[DataRequired()])
    submit = SubmitField("Submit")

class view_physician(FlaskForm):
    ssn = IntegerField('SSN', validators=[DataRequired()])
    submit = SubmitField("Submit")