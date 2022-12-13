from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


inpatient = Blueprint('inpatient', __name__, template_folder='templates', url_prefix='/inpatient')
Session = sessionmaker(bind=engine)
session = Session()

@inpatient.route('/', methods=['POST','GET'])
def _inpatient():
    form = inpatient_option_form()
    if form.validate_on_submit():
        input = form.inpatient.data
        if input == 'Check-in':
            return redirect(url_for('inpatient.assign_bed'))
        elif input == 'View/Schedule Surgery':
            return redirect(url_for('inpatient.schedule_surgery'))
        elif input == 'Reassign Nurse or Physician':
            return redirect(url_for('inpatient.reassign'))
        elif input == 'Check-out':
            return redirect(url_for('check-out'))
    return render_template('inpatient.html', form=form)

@inpatient.route('/checkin', methods=['POST', 'GET'])
def checkin():
    avail_beds = show_beds()
    blue_wing, green_wing = show_nurses()
    nurses = [blue_wing, green_wing]
    form = inpatient_checkin_form()
    physicians = show_physician()
    if form.validate_on_submit():
        with engine.connect() as connection:
            # Assign Bed
            bed_reservation = session.query(model.Bed).filter_by(wing=form.wing.data,
                                                                room=form.room.data,
                                                                bed=form.bed.data)
            inpatient_checkin = model.Inpatient(pid=form.pid.data,
                                                check_in_date=form.check_in_date,
                                                check_in_time=form.check_in_time,
                                                check_out_date=None,
                                                check_out_time=None,
                                                bed_id=bed_reservation,
                                                eid=form.eid.data)

            nurse_assign = model.Nurse_Assign_Inpatient(pid=form.pid.data, eid=form.nurse_eid.data)
            session.add(inpatient_checkin)
            session.add(nurse_assign)
            session.commit()
            connection.close()
            flash(f'Patient was assigned to physician: {form.physician_eid.data} wing: {form.wing.data} '
                  f'room: {form.room.data} bed: {form.bed.data}.')
        engine.dispose()
        return redirect(url_for('inpatient'))
    return render_template('checkin.html', beds=avail_beds, nurses=nurses, physicians=physicians, form=form)

def show_beds():
    beds_green_first = 120
    beds_green_last = 125
    beds_blue_first = 130
    beds_blue_last = 140
    avail_beds = []
    with engine.connect() as connection:
        for i in range(beds_green_first, beds_green_last + 1):
            bedA = session.query(model.Bed).filter(model.Bed.wing == 'Green',
                                                   model.Bed.room == i,
                                                   model.Bed.bed == 'A')
            if not bedA:
                temp = ['Green', i, 'A']
                avail_beds.append(temp)
        for i in range(beds_blue_first, beds_blue_last + 1):
            bedB = session.query(model.Bed).filter(model.Bed.wing == 'Green',
                                                   model.Bed.room == i,
                                                   model.Bed.bed == 'B')
            if not bedB:
                temp = ['Green', i, 'B']
                avail_beds.append(temp)
        connection.close()
    engine.dispose()
    return avail_beds

def show_nurses():
    blue_wing = None
    green_wing = None
    with engine.connect() as connection:
        nurses = session.query(model.Nurse_Unit)
        blue_wing = nurses.filter_by(wing = 'Blue')
        green_wing = nurses.filter_by(wing = 'Green')
        session.commit()
        connection.close()
    engine.dispose()
    return blue_wing, green_wing

def show_physician():
    patient_count = {}
    with engine.connect() as connection:
        physicians = session.query(func.count(model.Inpatient.physician_eid) < 21)
        for physician in physicians:
            if patient_count.has_key(physician.physician_eid):
                patient_count[physician.physician_eid] = patient_count.get(physician.physician_eid) + 1
            else:
                patient_count[physician.physician_eid] = 1
        connection.close()
    engine.dispose()
    return patient_count

@inpatient.route('/view_options', methods=['POST', 'GET'])
def view_options():
    form = view_surgery_form()
    if form.validate_on_submit():
        if form.view_surgery_by.data == 'Theatre' or form.view_surgery_by.data == 'Surgeon':
            surgery = None
            view_by = form.view_surgery_by.data.lower()
            with engine.connect() as connection:
                surgery = session.query(model.SurgerySchedule).filter(model.SurgerySchedule.date==form.date.data,
                                                                      model.SurgerySchedule.view_by==form.options.data)
                connection.close()
            engine.dispose()
            if surgery == None:
                flash('There is no surgery by the provided criteria.')
                return redirect(url_for('view_surgery'))
            return redirect(url_for('surgery'), data=surgery, view_by=view_by)
        elif form.view_surgery_by.data == 'Patient':
            surgery = None
            with engine.connect() as connection:
                surgery = session.query(model.SurgerySchedule).filter(model.SurgerySchedule.pid==form.pid.data)
                connection.close()
            engine.dispose()
            if surgery == None:
                flash('There is no surgery by the provided criteria.')
                return redirect(url_for('view_options'))
            return redirect(url_for('view_surgery'), surgery=surgery, view_by=view_by)
    return render_template('view_options.html', form=form)

@inpatient.route('/schedule_surgery', methods=['POST', 'GET'])
def schedule_surgery():
    form = schedule_surgery_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            last_scheduled = session.query(session.query(func.max(model.SurgerySchedule.schedule_id)))
            new_surgery = model.SurgerySchedule(schedule_id=last_scheduled  + 1,
                                                surgery_code=form.surgery_code.data,
                                                eid=form.eid.data,
                                                pid=form.pid.data,
                                                theatre=form.theatre.data,
                                                date=form.date.data,
                                                time=form.time.data)
            session.add(new_surgery)
            flash(f'Surgery successfully {new_surgery.schedule_id} scheduled.')
            connection.close()
        engine.dispose()
        return redirect(url_for('inpatient._inpatient'))
    return render_template('schedule_surgery.html', form=form)

@inpatient.route('/reassign', methods=['POST', 'GET'])
def reassign():
    form = reassign_staff_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            if form.staff.data == 'Nurse':
                assignment = session.query(model.Nurse_Assign_Inpatient).filter_by(pid=form.pid.data)
                model.Nurse_Assign_Inpatient.update({assignment.eid : form.eid.data})
            patient = session.query(model.Inpatient).filter_by(pid=form.pid.data)
            model.Inpatient.update({patient.eid : form.eid.data})
            session.commit()
            flash(f'{form.staff.data} reassigned.')
            return redirect(url_for('inpatient'))
        engine.dispose()
    return render_template('reassign.html', form=form)

@inpatient.route('/checkout', methods=['POST', 'GET'])
def checkout():
    form = query_patient_form()
    if form.validate_on_submit():
       with engine.connect() as connection:
            patient = session.query(model.Inpatient).filter_by(pid=form.pid.data)
            nurse = session.query(model.Nurse_Assign_Inpatient).filter_by(pid=form.pid.data)
            bed = session.query(model.Bed).filter_by(pid=form.pid.data)
            session.delete(patient)
            session.delete(nurse)
            session.commit()
            connection.close()
            flash(f'Patient {form.pid.data} successfully checked out.')
       engine.dispose()
       return redirect(url_for('inpatient'))
    return render_template('checkout.html', form=form)


'''
 In-patient management
xo Check for available room/bed
xo Assign/remove a patent to a room/bed
xo Assign/remove a doctor to a patient
xo Assign/remove a nurse to a patient
xo View scheduled surgery per room and per day
xo View scheduled surgery per surgeon and per day
xo View scheduled surgery per patient
xo Book a surgery
o No two physicians can prescribe the same medication to the same patient. 
'''