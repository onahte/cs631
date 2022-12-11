from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..db.model import *
from ..forms import *


nurse = Blueprint('nurse', __name__, template_folder='templates', url_prefix='/nurse')
Session = sessionmaker(bind=engine)
session = Session()

@nurse.route('/add_nurse', methods=['POST','GET'])
def add_nurse():
    form = add_nurse_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            last_id = session.query(func.max(model.Nurse.eid))
            new_nurse = model.Nurse(eid=last_id+1,
                                    ssn=form.data.ssn,
                                    name=form.data.name,
                                    grade=form.data.grade)
            session.add(new_nurse)
            unit_add = model.Unit(unit=form.data.unit, eid=last_id+1)
            session.add(unit_add)
            session.commit()
            flash(f'Successfully Added New Nurse')
            connection.close()
        engine.dispose()
        return redirect(url_for('staff.staff'))
    return render_template('add_nurse.html', form=form)

@nurse.route('/remove_nurse', method=['POST','GET'])
def remove_nurse():
    form = remove_staff_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            n = session.query(model.Nurse).filter(model.Nurse.eid==form.data.eid)
            session.delete(n)
            n = session.query(model.Unit).filter(model.Unit.eid==form.data.eid)
            session.delete(n)
            patients = session.query(model.Inpatient).filter(model.Inpatient.eid==form.data.eid)
            patients.update({model.Inpatient.eid : -1})
            session.commit()
            connection.close()
            flash('Nurse successfully removed.')
        engine.dispose()
        return redirect(url_for('staff.staff'))
    return render_template('remove_nurse.html', form=form)

'''
xo If a nurse leaves the clinic, temporarily remove the association of all in-patients 
    previously attended to by that nurse in order to allow these patients to be 
    transferred to another nurse at a later time
'''