from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


patient = Blueprint('patient', __name__, template_folder='templates', url_prefix='/patient')
Session = sessionmaker(bind=engine)
session = Session()

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
            return redirect(url_for('patient.diag_history_patient'))
        elif option == 'Schedule Appointment':
            return redirect(url_for('patient.schedule_appointment'))
        elif option == 'View Past Appointments':
            return redirect(url_for('view_appointment'))
    return render_template('patient.html', form=form)

@patient.route('/view_patient', methods=['POST','GET'])
def view_patient():
    form = query_patient_form()
    if form.validate_on_submit():
        pid = form.pid.data
        with engine.connect() as connection:
            patient_data = session.query(model.Patient).filter_by(pid=pid)
            patient_diag = session.query(model.Medical_Data).filter_by(pid=pid)
        return redirect(url_for('patient.view_patient_data', data=patient_data, data2=patient_diag))
    return render_template('view_patient.html', form=form)

@patient.route('/patient/view_patient_data/<data>/<data2>', methods=['POST','GET'])
def view_patient_data(data, data2):
    return render_template('view_patient_data.html', data=data, data2=data2)

@patient.route('/add_patient', methods=['POST','GET'])
def add_patient():
    form = add_patient_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            # Add patient to Patient table
            new_patient_id = session.query(func.max(model.Patient.pid)) + 1
            new_patient = model.Patient(pid=new_patient_id,
                                        ssn=form.ssn.data,
                                        name=form.name.data,
                                        street=form.street.data,
                                        city=form.city.data,
                                        state=form.state.data,
                                        zip=form.zip.data,
                                        number=form.phone.data)
            # Auto assign physician and enter into Physician_Assign_Patient table
            physicians = session.query(model.Physician).distinct()
            assigned = None
            all_assigned = []
            for physician in physicians:
                assignments = session.query(model.Physician_Assign_Patient).count()
                if assignments > 19:
                    continue
                if assignments == 0:
                    assigned = physician.eid
                    break
                temp = [physician.eid, assignments]
                all_assigned.append(temp)
            if not assigned:
                assigned = min(all_assigned)[1]
            assigned_physician = model.Physician_Assign_Patient(eid=assigned[0], pid=new_patient_id)
            session.add(new_patient)
            session.add(assigned_physician)
            session.commit()
            flash('Successfully Added New Patient')
            connection.close()
        engine.dispose()
        return redirect(url_for('patient._patient'))
    return render_template('add_patient.html', form=form)

@patient.route('/diag_history', methods=['POST','GET'])
def diag_history():
    form = query_patient_form()
    if form.validate_on_submit():
        patient_data = None
        patient_diag = None
        patient_consult = None
        with engine.connect() as connection:
            patient_query = session.query(model.Patient)
            patient_data = patient_query.filter(model.Patient.pid==form.pid.data)
            patient_diag = patient_query.filter(model.Medical_Data.pid==form.pid.data)
            patient_consult = patient_query.filter(model.Consultation.pid==form.pid.data)
            connection.close()
        engine.dispose()
        return render_template('view_diag_history.html',
                               data=patient_data,
                               data2=patient_diag,
                               data3=patient_consult)
    return render_template('diag_history.html', form=form)

@patient.route('/schedule_appt', methods=['POST','GET'])
def schedule_appt():
    form = schedule_appt_patient_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            physician = session.query(model.Physician_Assign_Patient).\
                filter(model.Physician_Assign_Patient.pid==form.pid.data)
            physician_avail = session.query(model.Consultation).filter(model.Consultation.eid==physician.eid,
                                                                 model.Consultation.date==form.date.data,
                                                                 model.Consultation.time==form.time.data)
            if physician_avail != None:
                flash(f'Specified time is not available. Please try another time.')
                return redirect('schedule_appt.html', form=form)
            new_appt = model.Consultation(eid=physician.eid,
                                          pid=form.pid.data,
                                          date=form.date.data,
                                          time=form.time.data)
            session.add(new_appt)
            session.commit()
            flash('Successfully Scheduled Appointment')
        connection.close()
        engine.dispose()
        return redirect(url_for('patient._patient'))
    return render_template('schedule_appt.html', form=form)


'''
 Patient management
xo Insert a new patient
xo View patient information
xo Schedule an appointment with a Doctor 
xo Check previous diagnoses and illnesses 
'''