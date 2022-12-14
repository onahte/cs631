from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..db.model import *
from ..forms import *


nurse = Blueprint('nurse', __name__, template_folder='templates', url_prefix='/nurse')

@nurse.route('/add_nurse', methods=['POST', 'GET'])
def add_nurse():
    form = add_nurse_form()
    if form.validate_on_submit():
        new_id = db.session.query(func.max(model.Nurse.eid)).first()[0] + 1
        new_nurse = model.Nurse(eid=new_id,
                                ssn=form.ssn.data,
                                name=form.name.data,
                                grade=form.grade.data)
        unit_add = model.Nurse_Unit(unit=form.unit.data, eid=new_id)
        new_address = model.Address(eid=new_id,
                                    street=form.street.data,
                                    city=form.city.data,
                                    state=form.state.data,
                                    zip=form.zip.data)
        new_gender = model.Gender(eid=new_id, gender=form.gender.data)
        new_salary = model.Salary(eid=new_id, salary=form.salary.data)
        db.session.add(new_nurse)
        db.session.add(unit_add)
        db.session.add(new_address)
        db.session.add(new_gender)
        db.session.add(new_salary)
        db.session.commit()
        flash(f'Successfully Added New Nurse')
        return redirect(url_for('staff._staff'))
    return render_template('add_nurse.html', form=form)


@nurse.route('/remove_nurse', methods=['POST', 'GET'])
def remove_nurse():
    form = remove_staff_form()
    nurses = db.session.query(model.Nurse).all()
    if form.validate_on_submit():
        db.session.query(model.Nurse).filter_by(eid=form.eid.data).delete()
        db.session.query(model.Nurse_Unit).filter_by(eid=form.eid.data).delete()
        db.session.query(model.Nurse_Assign_Inpatient).filter_by(eid=form.eid.data).update({model.Inpatient.eid: -1})
        db.session.query(model.Salary).filter_by(eid=form.eid.data).delete()
        db.session.query(model.Address).filter_by(eid=form.eid.data).delete()
        db.session.query(model.Gender).filter_by(eid=form.eid.data).delete()
        db.session.commit()
        flash('Nurse successfully removed.')
        return redirect(url_for('staff._staff'))
    return render_template('remove_nurse.html', form=form, nurses=nurses)


'''
xo If a nurse leaves the clinic, temporarily remove the association of all in-patients 
    previously attended to by that nurse in order to allow these patients to be 
    transferred to another nurse at a later time
'''
