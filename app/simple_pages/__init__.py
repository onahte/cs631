from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from ..db import db, model, engine
from .forms import *


simple_pages = Blueprint('simple_pages', __name__, template_folder='templates')
Session = sessionmaker(bind=engine)
session = Session()

@simple_pages.route('/patient', methods=['POST','GET'])
def patient():
    form = patient_options_form()
    if form.validate_on_submit():
        option = form.options.data
        if option == 'View Patient Data':
            return redirect(url_for('simple_pages.view_patient'))
        elif option == 'Add New Patient':
            return redirect(url_for('simple_pages.add_patient'))
        elif option == 'Check Previous Diagnosis':
            return redirect(url_for('simple_pages.diag_history_patient'))
        elif option == 'Schedule Appointment':
            return redirect(url_for('simple_pages.schedule_appointment'))
        elif option == 'View Past Appointments':
            return redirect(url_for('simple_pages.view_appointment'))

    return render_template('patient.html', form=form)

@simple_pages.route('/patient/view_patient', methods=['POST','GET'])
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

@simple_pages.route('/patient/add_patient', methods=['POST','GET'])
def add_patient():
    form = add_patient_form()
    new_patient = None
    if form.validate_on_submit():
        new_patient = form.data
        new_patient = Patient(name=new_patient.name, ssn=new_patient.ssn, street=new_patient.street,
                              city=new_patient.city, state=new_patient.state)
        with engine.connect() as connection:
            session.add(new_patient)
            session.commit()
        flash('Successfully Added New Patient')
        connection.close()
        engine.dispose()
        return redirect(url_for('simple_pages.patient'))
    return render_template('add_patient.html', form=form)


@simple_pages.route('/patient/diag_history_patient', methods=['POST','GET'])
def diag_history_patient():
    form = query_patient_form()
    patient = None
    if form.validate_on_submit():
        patient = form.data
        with engine.connect() as connection:
            patient_query = session.query(Patient)
            patient_data = patient_query.filter(Patient.ssn==patient.ssn)
            patient_diag = patient_query.filter(MedicalData.ssn==patient.ssn)
            patient_consult = patient_query.filter(ConsultationReceived.ssn==patient.ssn)
        connection.close()
        engine.dispose()
        return render_template('diag_history_patient.html',
                               data=patient_data,
                               data2=patient_diag,
                               data3=patient_consult)
    return render_template('diag_history_patient.html', form=form)

@simple_pages.route('/patient/schedule_appt_patient', methods=['POST','GET'])
def schedule_appt_patient():
    form = schedule_appt_patient_form()
    appt = None
    if form.validate_on_submit():
        appt = form.data
        appt = Consultation(ssn=appt.ssn, time=appt.time)
        with engine.connect() as connection:
            session.add(appt)
            session.commit()
        flash('Successfully Scheduled Appointment')
        connection.close()
        engine.dispose()
        return redirect(url_for('simple_pages.patient'))
    return render_template('schedule_appt_patient.html', form=form)


@simple_pages.route('/')
@simple_pages.route('/index')
def index():
    return render_template('index.html')


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
o View scheduled per doctor and per day
 In-patient management
o Check for available room/bed
o Assign/remove a patent to a room/bed
o Assign/remove a doctor to a patient
o Assign/remove a nurse to a patient
o View scheduled surgery per room and per day
o View scheduled surgery per surgeon and per day
o Book a surgery
o View scheduled surgery per patient
 Medical staff management
o Add/remove a stuff member
o View stuff member per job type o Schedule job shift
'''

