from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


patient = Blueprint('patient', __name__, template_folder='templates', url_prefix='/patient')
Session = sessionmaker(bind=engine)
session = Session()

@patient.route('/', methods=['POST','GET'])
def patient():
    form = patient_options_form()
    if form.validate_on_submit():
        option = form.options.data
        if option == 'View Patient Data':
            return redirect(url_for('patient.view_patient'))
        elif option == 'Add New Patient':
            return redirect(url_for('patient.add_patient'))
        elif option == 'Check Previous Diagnosis':
            return redirect(url_for('patient.diag_history_patient'))
        elif option == 'Schedule Appointment':
            return redirect(url_for('patient.schedule_appointment'))
        elif option == 'View Past Appointments':
            return redirect(url_for('patient.view_appointment'))

    return render_template('patient.html', form=form)

@patient.route('/view_patient', methods=['POST','GET'])
def view_patient():
    form = query_patient_form()
    patient_data = None
    if form.validate_on_submit():
        ssn = form.ssn.data
        patient_data = model.Patient.query.filter_by(ssn=ssn)
        patient_diag = model.MedicalData.query(query=patient.ssn.data)
        patient_allergy = model.Allergy.query(query=patient.ssn.data)
    return render_template('view_patient.html',
                           form=form,
                           data=patient_data,
                           data2=patient_diag,
                           data3=patient_allergy)

@patient.route('/add_patient', methods=['POST','GET'])
def add_patient():
    form = add_patient_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            new_patient = form.data
            new_patient_id = model.Patient.query(func.max(model.Patient.id)) + 1
            new_patient = model.Patient(pid=new_patient_id,
                                        ssn=new_patient.ssn,
                                        name=new_patient.name,
                                        street=new_patient.street,
                                        city=new_patient.city,
                                        state=new_patient.state,
                                        zip=new_patient.zip)
            session.add(new_patient)
            session.commit()
            flash('Successfully Added New Patient')
            connection.close()
        engine.dispose()
        return redirect(url_for('patient.patient'))
    return render_template('add_patient.html', form=form)

@patient.route('/diag_history_patient', methods=['POST','GET'])
def diag_history_patient():
    form = query_patient_form()
    if form.validate_on_submit():
        patient = form.data
        with engine.connect() as connection:
            patient_query = session.query(model.Patient)
            patient_data = patient_query.filter(model.Patient.ssn==patient.ssn)
            patient_diag = patient_query.filter(model.MedicalData.ssn==patient.ssn)
            patient_consult = patient_query.filter(model.Consultation.ssn==patient.ssn)
            connection.close()
        engine.dispose()
        return render_template('diag_history_patient.html',
                               data=patient_data,
                               data2=patient_diag,
                               data3=patient_consult)
    return render_template('diag_history_patient.html', form=form)

@patient.route('/schedule_appt_patient', methods=['POST','GET'])
def schedule_appt_patient():
    form = schedule_appt_patient_form()
    if form.validate_on_submit():
        appt = form.data
        with engine.connect() as connection:
            physician_avail = session.query(Consultation).filter(model.Consultation.eid==appt.eid,
                                                                 model.Consultation.date==appt.date,
                                                                 model.Consultation.time==appt.time)
            if physician_avail != None:
                flash(f'Physician {appt.eid} has a scheduling conflict. Please try another time.')
                return redirect('schedule_appt_patient.html', form=form)
            pid = session.query(Patient).filter(Patient.ssn==appt.ssn)
            if pid == None:
                flash('Patient not in database. Please add patient.')
                return redirect(url_for('add_patient', form=add_patient_form))
            appt.pid = pid.pid
            appt.consultation_id = session.query(func.max(model.Patient.id)) + 1
            session.add(appt)
            session.commit()
            flash('Successfully Scheduled Appointment')
        connection.close()
        engine.dispose()
        return redirect(url_for('patient.patient'))
    return render_template('schedule_appt_patient.html', form=form)


'''
    if selected_form.validate_on_submit():
        v = model.Patient.query(query=selected_form.query.data)
        db.session.add(v)
        db.session.commit()
        flash('Thank you for your query')

The applications should minimally cover:
 Patient management
o Insert a new patient
o View patient information
o Schedule an appointment with a Doctor 
o Check previous diagnoses and illnesses 

'''