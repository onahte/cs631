from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


physician = Blueprint('physician', __name__, template_folder='templates', url_prefix='/physician')

@physician.route('/', methods=['POST', 'GET'])
def _physician():
    form = physician_options_form()
    if form.validate_on_submit():
        if form.option.data == 'View Schedule':
            return redirect(url_for('physician.physician_schedule'))
        elif form.option.data == 'Remove':
            return redirect(url_for('physician.remove_physician'))
    return render_template('physician.html', form=form)

@physician.route('/physician_schedule', methods=['POST','GET'])
def physician_schedule():
    form = physician_view_schedule_form()
    if form.validate_on_submit():
        schedule = session.query(model.Consultation).filter_by(eid=form.eid.data, date=form.date.data)
        return redirect(url_for('view_schedule'), data=schedule)
    return render_template('physician_schedule.html', form=form)

@physician.route('/remove_physician', methods=['POST','GET'])
def remove_physician():
    form = remove_staff_form()
    physicians = db.session.query(model.Physician).all()
    if form.validate_on_submit():
        eid = form.eid.data
        db.session.query(model.Physician).filter_by(eid=eid).delete()
        db.session.query(model.Prescription).filter_by(eid=eid).delete()
        db.session.query(model.Inpatient).filter_by(eid=eid).delete()
        db.session.query(model.Physician_Schedule).filter_by(eid=eid).delete()
        chief = db.session.query(model.Clinic.chief_id).first()[0]
        db.session.query(model.Consultation).filter_by(eid=eid).update({model.Consultation.eid: chief})
        db.session.query(model.Salary).filter_by(eid=eid).delete()
        db.session.query(model.Address).filter_by(eid=eid).delete()
        db.session.query(model.Gender).filter_by(eid=eid).delete()
        flash(f'Physician {eid} successfully removed from system.')
        flash(f"Physician {eid}'s patients have been transferred to {chief}.")
        db.session.commit()
        return redirect(url_for('staff._staff'))
    return render_template('remove_physician.html', form=form, physicians=physicians)


'''
xo View scheduled per doctor and per day
xo If a physician leaves the clinic, temporarily assign the physician’s patients to the
    clinic’s chief of staff
xo If a physician leaves the clinic, all prescriptions prescribed by that physician
    should also be removed because this information is also retained in the archives.
'''