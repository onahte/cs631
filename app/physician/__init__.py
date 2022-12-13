from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


physician = Blueprint('physician', __name__, template_folder='templates', url_prefix='/physician')
Session = sessionmaker(bind=engine)
session = Session()

@physician.route('/', methods=['POST', 'GET'])
def _physician():
    form = physician_options_form()
    if form.validate_on_submit():
        if form.option.data == 'View Schedule':
            return redirect(url_for('physician_schedule'))
        elif form.option.data == 'Remove':
            return redirect(url_for('remove_physician'))
    return render_template('physician.html', form=form)

@physician.route('/physician_schedule', methods=['POST','GET'])
def physician_schedule():
    form = physician_view_schedule_form()
    if form.validate_on_submit():
        schedule = None
        with engine.connect as connection:
            schedule = session.query(model.Consultation).filter(model.Consultation.eid==form.eid.data,
                                                                model.Consultation.date==form.date.data)
        connection.close()
        engine.dispose()
        return redirect(url_for('view_schedule'), data=schedule)
    return render_template('physician_schedule.html', form=form)

@physician.route('/remove_physician', methods=['POST','GET'])
def remove_physician():
    form = remove_staff_form()
    if form.validate_on_submit():
        eid = form.eid.data
        with engine.connect() as connection:
            # Remove from Physician table
            physician = session.query(model.Physician).filter(model.Physician.eid==eid)
            # Remove from Prescription table
            script = session.query(model.Precription).filter(model.Prescription.eid==eid)
            # Remove patient assignment
            patient_assign = session.query(model.Inpatient).filter(model.Inpatient.physician_eid == eid)
            # Remove from schedule
            schedule = session.query(model.Physician_Schedule).filter(model.Physician_Schedule.eid == eid)
            # Reassign patients to chief of staff
            clinic = session.query(model.Clinic)
            chief = clinic.chief_id
            consultation = session.query(model.Consultation).filter(model.Consultation.eid==eid)
            consultation.update({model.Consultation.eid : chief})
            # Delete from Salary table
            salary = session.query(model.Salary).filter(model.Salary.eid == eid)
            # Delete from Address table
            address = session.query(model.Address).filter(model.Address.eid == eid)
            # Delete from Gender table
            gender = session.query(model.Gender).filter(model.Gender.eid == eid)
            flash(f'Physician {eid} successfully removed from system.')
            flash(f"Physician {eid}'s patients have been transferred to {chief}.")
            session.delete(physician)
            if script:
                session.delete(script)
            if patient_assign:
                session.delete(patient_assign)
            if schedule:
                session.delete(schedule)
            session.delete(salary)
            session.delete(address)
            session.delete(gender)
            session.commit()
            connection.close()
        engine.dispose()
        return redirect(url_for('physician.physician'))
    return render_template('physician.html', form=form)


'''
xo View scheduled per doctor and per day
xo If a physician leaves the clinic, temporarily assign the physician’s patients to the
    clinic’s chief of staff
xo If a physician leaves the clinic, all prescriptions prescribed by that physician
    should also be removed because this information is also retained in the archives.
'''