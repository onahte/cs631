from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


patient = Blueprint('physician', __name__, template_folder='templates', url_prefix='/physician')
Session = sessionmaker(bind=engine)
session = Session()

@physician.route('/', methods=['POST','GET'])
def physician():
    form = physician_view_schedule_form()
    if form.validate_on_submit():
        schedule = None
        with engine.connect as connection:
            schedule = session.query(model.Consultation).filter(model.Consultation.eid==form.eid,
                                                                model.Consultation.date==form.date)
        connection.close()
        engine.dispose()
        return redirect(url_for('physician.physician_schedule'), data=schedule)
    return render_template('physician.html', form=form)

@physician.route('/remove_physician', methods=['POST','GET'])
def remove_physician():
    form = remove_staff_form()
    if form.validate_on_submit():
        eid = form.data.eid
        with engine.connect() as connection:
            p = session.query(model.Physician).filter(model.Physician.eid==eid)
            session.delete(p)
            p = session.query(model.Precription).filter(model.Prescription.eid==eid)
            session.delete(p)
            clinic = session.query(model.Clinic)
            chief = clinic.chief_id
            consultation = session.query(model.Consultation).filter(model.Consultation.eid==eid)
            consultation.update({model.Consultation.eid : chief})
            flash(f'Physician {eid} successfully removed from system.')
            flash(f"Physician {eid}'s patients have been transferred to {chief}.")
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