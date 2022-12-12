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
            unit_add = model.Unit(unit=form.data.unit, eid=last_id+1)
            new_address = model.Address(eid=last_id,
                                        street=form.data.street,
                                        city=form.data.city,
                                        state=form.data.state,
                                        zip=form.data.zip)
            new_gender = model.Gender(eid=last_id, gender=form.data.gender)
            new_salary = model.Salary(eid=last_id, salary=form.data.salary)
            session.add(new_nurse)
            session.add(unit_add)
            session.add(new_address)
            session.add(new_gender)
            session.add(new_salary)
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
            # Delete from Nurse table
            nurse_table = session.query(model.Nurse).filter(model.Nurse.eid==form.data.eid)
            # Delete from Unit table
            unit_table = session.query(model.Nurse_Unit).filter(model.Nurse_Unit.eid==form.data.eid)
            # Delete patient association
            patients = session.query(model.Nurse_Assign_Inpatient).\
                filter(model.Nurse_Assign_Inpatient.eid==form.data.eid)
            patients.update({model.Inpatient.eid : -1})
            # Delete from Salary table
            salary = session.query(model.Salary).filter(model.Salary.eid==form.data.eid)
            # Delete from Address table
            address = session.query(model.Address).filter(model.Address.eid==form.data.eid)
            # Delete from Gender table
            gender = session.query(model.Gender).filter(model.Gender.eid == form.data.eid)
            session.delete(nurse_table)
            session.delete(unit_table)
            session.delete(salary)
            session.delete(address)
            session.delete(gender)
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