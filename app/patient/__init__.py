from flask import Blueprint, render_template, url_for, redirect, flash, request
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


patient = Blueprint('patient', __name__, template_folder='templates', url_prefix='/patient')

@patient.route('/patient', methods=['POST','GET'])
def _patient():
    form = patient_options_form()
    if form.validate_on_submit():
        option = form.options.data
        if option == 'View Patient Data':
            return redirect(url_for('patient.view_patient'))
        elif option == 'Add New Patient':
            return redirect(url_for('patient.add_patient'))
        elif option == 'Check Previous Diagnosis':
            return redirect(url_for('patient.diag_history'))
        elif option == 'Schedule Appointment':
            return redirect(url_for('patient.schedule_appt'))
        elif option == 'View Past Appointments':
            return redirect(url_for('patient.view_appointment'))
    return render_template('patient.html', form=form)

@patient.route('/view_patient', methods=['POST','GET'])
def view_patient():
    form = query_patient_form()
    patient = db.session.query(model.Patient).all()
    if form.validate_on_submit():
        pid = form.pid.data
        patient_data = model.Patient.query.get(pid)
        patient_diag = model.Medical_Data.query.get(pid)
        return render_template('view_patient_data.html', data=patient_data, data2=patient_diag)
    return render_template('view_patient.html', form=form, patient=patient)

@patient.route('/patient/view_patient_data/<data>/<data2>', methods=['POST','GET'])
def view_patient_data(data, data2):
    return render_template('view_patient_data.html', data=data, data2=data2)

@patient.route('/add_patient', methods=['POST','GET'])
def add_patient():
    form = add_patient_form()
    physicians = db.session.query(model.Physician).all()
    if form.validate_on_submit():
        # Add patient to Patient table
        new_patient_id = db.session.query(func.max(model.Patient.pid)).first()[0] + 1
        new_patient = model.Patient(pid=new_patient_id,
                                    ssn=form.ssn.data,
                                    gender=form.gender.data,
                                    dob=form.dob.data,
                                    name=form.name.data,
                                    street=form.street.data,
                                    city=form.city.data,
                                    state=form.state.data,
                                    zip=form.zip.data,
                                    number=form.phone.data,
                                    eid=form.eid.data)
        db.session.add(new_patient)
        db.session.commit()
        flash(f'Successfully Added New Patient {new_patient_id}')
        return redirect(url_for('patient._patient'))
    return render_template('add_patient.html', form=form, physicians=physicians)

@patient.route('/diag_history', methods=['POST','GET'])
def diag_history():
    form = query_patient_form()
    if form.validate_on_submit():
        patient_data = model.Patient.query.get(form.pid.data)
        patient_diag = model.Medical_Data.query.get(form.pid.data)
        patient_consult = model.Consultation.query.get(form.pid.data)
        return render_template('view_diag_history.html',
                               data=patient_data,
                               data2=patient_diag,
                               data3=patient_consult)
    return render_template('diag_history.html', form=form)

@patient.route('/schedule_appt', methods=['POST','GET'])
def schedule_appt():
    form = schedule_appt_patient_form()
    if form.validate_on_submit():
        physician = model.Patient.query.get(form.pid.data)
        physician_avail = model.Consultation.query.filter_by(eid=physician.eid,
                                                            date=form.date.data,
                                                            time=form.time.data).first()
        if physician_avail != None:
            flash(f'Specified time is not available. Please try another time.')
            return redirect(url_for('patient.schedule_appt', form=form))
        new_appt_id = db.session.query(func.max(model.Consultation.consultation_id)).first()[0] + 1
        new_appt = model.Consultation(consultation_id=new_appt_id,
                                      eid=physician.eid,
                                      pid=form.pid.data,
                                      date=form.date.data,
                                      time=form.time.data)
        db.session.add(new_appt)
        db.session.commit()
        flash('Successfully Scheduled Appointment')
        return redirect(url_for('patient._patient'))
    return render_template('schedule_appt.html', form=form)

@patient.route('/view_appointment', methods=['POST','GET'])
def view_appointment():
    form = query_patient_form()
    patient = db.session.query(model.Patient).all()
    if form.validate_on_submit():
        pid = form.pid.data
        patient_data = db.session.query(model.Consultation).filter_by(pid=form.pid.data)
        return render_template('view_appointment_data.html', pid=pid, data=patient_data)
    return render_template('view_appointment.html', form=form, patient=patient)

'''
 Patient management
xo Insert a new patient
xo View patient information
xo Schedule an appointment with a Doctor 
xo Check previous diagnoses and illnesses 
'''