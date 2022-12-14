from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..db.model import *
from ..forms import *


staff = Blueprint('staff', __name__, template_folder='templates', url_prefix='/staff')

@staff.route('/', methods=['POST', 'GET'])
def _staff():
    form = staff_options_form()
    if form.validate_on_submit():
        option = form.options.data
        role = form.role.data
        if option == 'Add':
            if role == 'Nurse':
                return redirect(url_for('nurse.add_nurse'))
            else:
                return redirect(url_for('staff.add_staff', role=role))
        elif option == 'Remove':
            if role == 'Physician':
                return redirect(url_for('physician.remove_physician'))
            elif role == 'Nurse':
                return redirect(url_for('nurse.remove_nurse'))
            elif role == 'Surgeon':
                return redirect(url_for('surgeon.remove_surgeon'))
            elif role == 'Support Staff':
                return redirect(url_for('staff.remove_staff'))
        elif option == 'Schedule':
            if role == 'Surgeon':
                flash('Surgeons are scheduled by surgery scheduler and not by shift scheduler. Please try again.')
                return redirect(url_for('staff._staff'))
            return redirect(url_for('staff.schedule_staff', role=role))
        elif option == 'View Staff by Type':
            return redirect(url_for('staff.view_staff', role=role))
    return render_template('staff.html', form=form)


@staff.route('/view_staff/<role>', methods=['POST', 'GET'])
def view_staff(role):
    staff = None
    if role == 'Physician':
        staff = db.session.query(model.Physician)
    elif role == 'Nurse':
        staff = db.session.query(model.Nurse)
    elif role == 'Surgeon':
        staff = db.session.query(model.Surgeon)
    elif role == 'Support Staff':
        staff = db.session.query(model.Nurse)
    return render_template('view_staff.html', role=role, data=staff)


@staff.route('/add_staff/<role>', methods=['POST', 'GET'])
def add_staff(role):
    form = add_staff_form()
    if form.validate_on_submit():
        dept = model.Physician
        if role == 'Support Staff':
            dept = model.Support_Staff
        last_id = db.session.query(func.max(dept.eid)).first()[0] + 1
        new_staff = dept(eid=last_id,
                         ssn=form.ssn.data,
                         name=form.name.data)
        new_address = model.Address(eid=last_id,
                                    street=form.street.data,
                                    city=form.city.data,
                                    state=form.state.data,
                                    zip=form.zip.data)
        new_gender = model.Gender(eid=last_id, gender=form.gender.data)
        new_salary = model.Salary(eid=last_id, salary=form.salary.data)
        db.session.add(new_staff)
        db.session.add(new_address)
        db.session.add(new_gender)
        db.session.add(new_salary)
        db.session.commit()
        flash(f'Successfully Added {form.name.data} as New {role}')
        return redirect(url_for('staff._staff'))
    return render_template('add_staff.html', form=form, role=role)


@staff.route('/schedule_staff/<role>', methods=['POST', 'GET'])
def schedule_staff(role):
    form = schedule_shift_form()
    if form.validate_on_submit():
        dept = model.Physician
        schedule = model.Physician_Schedule
        if role == 'Nurse':
            dept = model.Nurse
            schedule = model.Nurse_Schedule
        elif role == 'Support Staff':
            dept = model.Staff
            schedule = model.SupportStaff_Schedule

        st = form.start_time.data
        et = form.end_time.data
        dept_db = db.session.query(dept).filter_by(eid=form.eid.data)
        if dept_db == None:
            flash(f'There is no employee by that EID in this department. Please try again.')
            return redirect(url_for('staff.schedule_staff'))
        shifts = db.session.query(schedule).filter_by(eid=form.eid.data, date=form.date.data).all()
        if shifts:
            for shift in shifts:
                shst = shift.start_time
                shet = shift.end_time
                if shift.date == form.date.data and \
                        (st == shst or et == shet or (st < shst and et > shst) or (st < shet and et > shet)):
                    flash(f'{role} {form.eid.data} is already scheduled for a shift at that time.')
                    return redirect(url_for('staff.schedule_staff', role=role))
        new_id = db.session.query(func.max(schedule.schedule_id)).first()[0] + 1
        new_shift = schedule(schedule_id=new_id, eid=form.eid.data, date=form.date.data,
                             start_time=form.start_time.data, end_time=form.end_time.data)
        db.session.add(new_shift)
        db.session.commit()
        flash(f'{role} {form.eid.data} has been scheduled for a shift on {form.date.data}.'
              f'\nStart: {form.start_time.data}  \nEnd: {form.end_time.data}')
        return redirect(url_for('staff._staff'))
    return render_template('schedule_staff.html', form=form, role=role)


'''
??? Medical staff management
xo Add/remove a staff member
xo View staff member per job type 
xo Schedule job shift 
o Staff salary range $25,000 to $300,000
'''
