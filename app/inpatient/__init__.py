from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func, distinct
from ..db import db, model, engine
from ..forms import *


inpatient = Blueprint('inpatient', __name__, template_folder='templates', url_prefix='/inpatient')

@inpatient.route('/', methods=['POST','GET'])
def _inpatient():
    form = inpatient_option_form()
    if form.validate_on_submit():
        choice = form.inpatient.data
        if choice == 'Check-in':
            return redirect(url_for('inpatient.checkin'))
        elif choice == 'View Surgery':
            return redirect(url_for('inpatient.view_options'))
        elif choice == 'Schedule Surgery':
            return redirect(url_for('inpatient.schedule_surgery'))
        elif choice == 'Reassign Nurse/Physician':
            return redirect(url_for('inpatient.reassign'))
        elif choice == 'Check-out':
            return redirect(url_for('inpatient.checkout'))
    return render_template('inpatient.html', form=form)

@inpatient.route('/checkin', methods=['POST', 'GET'])
def checkin():
    avail_beds = show_beds()
    blue_wing, green_wing = show_nurses()
    nurses = [blue_wing, green_wing]
    form = inpatient_checkin_form()
    physicians = show_physician()
    patients_checkedin = db.session.query(model.Inpatient).all()
    if form.validate_on_submit():
        new_bed = model.Bed(pid=form.pid.data,
                            wing=form.wing.data,
                            room=form.room.data,
                            bed=form.bed.data)
        inpatient_checkin = model.Inpatient(pid=form.pid.data,
                                            check_in_date=form.check_in_date.data,
                                            check_in_time=form.check_in_time.data,
                                            check_out_date=form.check_in_date.data,
                                            check_out_time=form.check_in_time.data,
                                            eid=form.eid.data)
        if form.nurse_eid.data:
            nurse_assign = model.Nurse_Assign_Inpatient(pid=form.pid.data,
                                                        eid=form.nurse_eid.data)
            session.add(nurse_assign)
        db.session.add(new_bed)
        db.session.add(inpatient_checkin)
        db.session.commit()
        flash(f'Patient was assigned to physician: {form.eid.data} wing: {form.wing.data} '
              f'room: {form.room.data} bed: {form.bed.data}.')
        return redirect(url_for('inpatient._inpatient'))
    return render_template('checkin.html', beds=avail_beds, nurses=nurses, physicians=physicians,
                           form=form, patients_checkedin=patients_checkedin)

def show_beds():
    beds_green_first = 120
    beds_green_last = 125
    beds_blue_first = 130
    beds_blue_last = 140
    avail_beds = []
    for i in range(beds_green_first, beds_green_last + 1):
        if db.session.query(model.Bed).filter_by(wing='Green', room=i, bed='A').first() is None:
            temp = ['Green', i, 'A']
            avail_beds.append(temp)
        if db.session.query(model.Bed).filter_by(wing='Green', room=i, bed='B').first() is None:
            temp = ['Green', i, 'B']
            avail_beds.append(temp)
    for j in range(beds_blue_first, beds_blue_last + 1):
        if db.session.query(model.Bed).filter_by(wing='Blue', room=j, bed='A').first() is None:
            temp = ['Blue', j, 'A']
            avail_beds.append(temp)
        if db.session.query(model.Bed).filter_by(wing='Blue', room=j, bed='B').first() is None:
            temp = ['Blue', j, 'B']
            avail_beds.append(temp)
    return avail_beds

def show_nurses():
    nurses = db.session.query(model.Nurse_Unit)
    blue_wing = nurses.filter_by(wing='Blue').all()
    green_wing = nurses.filter_by(wing='Green').all()
    return blue_wing, green_wing

def show_physician():
    physicians = model.Inpatient.query.with_entities(model.Inpatient.eid,
                                                    func.count(model.Inpatient.eid)).group_by(model.Inpatient.eid).all()
    return physicians

@inpatient.route('/view_options', methods=['POST', 'GET'])
def view_options():
    form = view_surgery_form()
    if form.validate_on_submit():
        if form.view_surgery_by.data == 'Theatre':
            return redirect(url_for('inpatient.view_by_theatre'))
        elif form.view_surgery_by.data == 'Surgeon':
            return redirect(url_for('inpatient.view_by_surgeon'))
        elif form.view_surgery_by.data == 'Patient':
            return redirect(url_for('inpatient.view_by_patient'))
    return render_template('view_options.html', form=form)

@inpatient.route('/view_by_theatre', methods=['POST', 'GET'])
def view_by_theatre():
    form = view_by_theatre_form()
    view_by = f'Theatre {form.theatre.data}'
    if form.validate_on_submit():
        surgery = None
        if form.theatre.data == '1001':
           surgery = model.SurgerySchedule.query.filter_by(theatre=1001).all()
        else:
           surgery = model.SurgerySchedule.query.filter_by(theatre=1002).all()
        return render_template('view_surgery.html', view_by=view_by, surgery=surgery)
    return render_template('view_by_theatre.html', form=form)

@inpatient.route('/view_by_surgeon', methods=['POST', 'GET'])
def view_by_surgeon():
    form = view_by_surgeon_form()
    view_by = f'Surgeon {form.surgeon.data}'
    surgeons = model.SurgerySchedule.query.with_entities(model.SurgerySchedule.eid).distinct()
    if form.validate_on_submit():
        surgery = model.SurgerySchedule.query.filter_by(eid=form.surgeon.data).all()
        return render_template('view_surgery.html', view_by=view_by, surgery=surgery)
    return render_template('view_by_surgeon.html', form=form, surgeons = surgeons)

@inpatient.route('/view_by_patient', methods=['POST', 'GET'])
def view_by_patient():
    form = view_by_patient_form()
    view_by = f'Patient {form.patient.data}'
    patient = db.session.query(distinct(model.SurgerySchedule.pid)).all()
    if form.validate_on_submit():
        surgery = model.SurgerySchedule.query.filter_by(pid=form.patient.data).all()
        return render_template('view_surgery.html', view_by=view_by, surgery=surgery)
    return render_template('view_by_patient.html', form=form, patient=patient)

@inpatient.route('/schedule_surgery', methods=['POST', 'GET'])
def schedule_surgery():
    form = schedule_surgery_form()
    surgery_code = db.session.query(model.Surgery).all()
    if form.validate_on_submit():
        last_scheduled = db.session.query(func.max(model.SurgerySchedule.schedule_id)).first()[0] + 1
        new_surgery = model.SurgerySchedule(schedule_id=last_scheduled,
                                            surgery_code=form.surgery_code.data,
                                            eid=form.eid.data,
                                            pid=form.pid.data,
                                            theatre=form.theatre.data,
                                            date=form.date.data,
                                            time=form.time.data)
        db.session.add(new_surgery)
        flash(f'Surgery {new_surgery.schedule_id} successfully scheduled.')
        return redirect(url_for('inpatient._inpatient'))
    return render_template('schedule_surgery.html', form=form, surgery_code=surgery_code)

@inpatient.route('/reassign', methods=['POST', 'GET'])
def reassign():
    form = reassign_staff_form()
    role = form.staff.data
    nurses = db.session.query(model.Nurse).all()
    physicians = db.session.query(model.Physician).all()
    if form.validate_on_submit():
        if role == 'Nurse':
            db.session.query(model.Nurse_Assign_Inpatient).filter_by(pid=form.pid.data).update({model.Nurse_Assign_Inpatient.eid : form.eid.data})
        db.session.query(model.Inpatient).filter_by(pid=form.pid.data).update({model.Inpatient.eid : form.eid.data})
        db.session.commit()
        flash(f'{form.staff.data} reassigned.')
        return redirect(url_for('inpatient._inpatient'))
    return render_template('reassign.html', form=form, role=role, nurses=nurses, physicians=physicians)

@inpatient.route('/checkout', methods=['POST', 'GET'])
def checkout():
    form = query_patient_form()
    patients_checkedin = db.session.query(model.Inpatient).all()
    if form.validate_on_submit():
        patient = db.session.query(model.Inpatient).filter_by(pid=form.pid.data).delete()
        nurse = db.session.query(model.Nurse_Assign_Inpatient).filter_by(pid=form.pid.data).delete()
        bed = db.session.query(model.Bed).filter_by(pid=form.pid.data).delete()
        db.session.commit()
        flash(f'Patient {form.pid.data} successfully checked out.')
        return redirect(url_for('inpatient._inpatient'))
    return render_template('checkout.html', form=form, patients_checkedin=patients_checkedin)


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