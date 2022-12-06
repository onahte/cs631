from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from ..db import db, model, engine
from ..forms import *


staff = Blueprint('staff', __name__, template_folder='templates')
Session = sessionmaker(bind=engine)
session = Session()


@staff.route('/staff', methods=['POST','GET'])
def staff():
    form = staff_options_form()
    if form.validate_on_submit():
        option = form.options.data
        if option == 'Add/Remove':
            return redirect(url_for('staff.addremove'))
        elif option == 'Schedule':
            return redirect(url_for('staff.schedule'))
        elif option == 'View':
            return redirect(url_for('staff.select'))

    return render_template('staff.html', form=form)

@staff.route('/staff/select', methods=['POST','GET'])
def select():
    form = staff_role_options_form()
    if form.validate_on_submit():
        option = form.options.data
        if option == 'Physician':
            return redirect(url_for('staff.physician'))
        elif option == 'Nurse':
            return redirect(url_for('staff.nurse'))
        elif option == 'Surgeon':
            return redirect(url_for('staff.surgeon'))
        elif option == 'Support Staff':
            return redirect(url_for('staff.support'))

    return render_template('staff_view.html', form=form)

@staff.route('/staff/add_staff', methods=['POST','GET'])
def add_staff():
    form = add_staff_form()
    staff_query = None
    if form.validate_on_submit():
        option = form.options.data
        if option == 'Physician':
            return redirect(url_for('staff.physician'))
        with engine.connect() as connection:
            last_id = session.query(func.max(Patient.id))
            new_patient = form.data
            new_patient = Patient(id=last_id + 1, name=new_patient.name, ssn=new_patient.ssn, street=new_patient.street,
                                  city=new_patient.city, state=new_patient.state, zip=new_patient.zip)
            session.add(new_patient)
            session.commit()
        flash('Successfully Added New Patient')
        connection.close()
        engine.dispose()
        return redirect(url_for('simple_pages.patient'))
    return render_template('add_patient.html', form=form)



@physician.route('/staff/physician', methods=['POST','GET'])
def physician():
    form = query_physician_form()
    physician = None
    if form.validate_on_submit():
        ssn = form.ssn.data
        physician_data = model.Physician.query.filter_by(ssn=ssn)
    return render_template('view_physician.html',
                           form=form,
                           data=physician_data)




@staff.route('/staff/diag_history_patient', methods=['POST','GET'])
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

@staff.route('/staff/schedule_shift', methods=['POST','GET'])
def schedule_shift():
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


'''

    if selected_form.validate_on_submit():
        v = model.Patient.query(query=selected_form.query.data)
        db.session.add(v)
        db.session.commit()
        flash('Thank you for your query')

The applications should minimally cover:
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
o Add/remove a staff member
o View staff member per job type 
o Schedule job shift
'''