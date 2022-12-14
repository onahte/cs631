from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..db.model import *
from ..forms import *


surgeon = Blueprint('surgeon', __name__, template_folder='templates', url_prefix='/surgeon')

@surgeon.route('/remove_surgeon', methods=['POST','GET'])
def remove_surgeon():
    form = remove_staff_form()
    if form.validate_on_submit():
        db.session.query(model.Salary).filter_by(pid=form.pid.data).delete()
        db.session.query(model.Address).filter_by(pid=form.pid.data).delete()
        db.session.query(model.Gender).filter_by(pid=form.pid.data).delete()
        db.session.query(model.Surgeon).filter_by(pid=form.pid.data).delete()
        db.session.commit()
        return redirect(url_for('staff._staff'))
    return render_template('remove_surgeon.html', form=form)