from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import *


class query_form(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    submit = SubmitField("Submit")
