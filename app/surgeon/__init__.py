from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..db.model import *
from ..forms import *


surgeon = Blueprint('surgeon', __name__, template_folder='templates', url_prefix='/surgeon')
Session = sessionmaker(bind=engine)
session = Session()


@surgeon.route('/remove_surgeon', methods=['POST','GET'])
def remove_surgeon():
    form = remove_staff_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            # Remove from Salary
            salary = session.query(model.Salary).filter_by(pid=form.pid.data)
            # Remove from Address
            address = session.query(model.Address).filter_by(pid=form.pid.data)
            # Remove from Gender
            gender = session.query(model.Gender).filter_by(pid=form.pid.data)
            # Remove from Surgeon
            surgeon = session.query(model.Surgeon).filter_by(pid=form.pid.data)
            session.delete(salary)
            session.delete(address)
            session.delete(gender)
            session.delete(surgeon)
            session.commit()
            connection.close()
        engine.dispose()
        return redirect(url_for('staff.staff'))
    return render_template('remove_surgeon.html', form=form)