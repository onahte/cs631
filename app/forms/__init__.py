from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import *

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
    ssn = IntegerField('SSN', validators=[DataRequired()])
    time = DateTimeField('time', validators=[DataRequired()], format='%Y=%m-%d')
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