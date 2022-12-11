from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from ..db import db, model, engine
from ..forms import *


inpatient = Blueprint('inpatient', __name__, template_folder='templates', url_prefix='/inpatient')
Session = sessionmaker(bind=engine)
session = Session()

@inpatient.route('/', methods=['POST','GET'])
def inpatient():
    form = inpatient_option_form()
    if form.validate_on_submit():
        input = form.data.inpatient
        if input == 'Check Available/Assign Room/Bed':
            return redirect(url_for('assign_bed', ssn=form.data.ssn))
        elif input == 'Assign Physician':
            return redirect(url_for('assign_physician', ssn=form.data.ssn))
        elif input == 'Assign Nurse':
            return redirect(url_for('assign_nurse', ssn=form.data.ssn))
        elif input == 'View Scheduled Surgery':
            return redirect(url_for('view_surgery', ssn=form.data.ssn))
        elif input == 'Schedule Surgery':
            return redirect(url_for('schedule_surgery', ssn=form.data.ssn))
    return render_template('inpatient.html', form=form)

@inpatient.route('/bed_assign<int:ssn>', methods=['POST', 'GET'])
def bed_assign(ssn):
    beds_green_first = 120
    beds_green_last = 125
    beds_blue_first = 130
    beds_blue_last = 140
    avail_beds = []
    with engine.connect() as connection:
        for i in range(beds_green_first, beds_green_last + 1):
            bedA = session.query(model.Bed).filter(model.Bed.wing=='Green',
                                                         model.Bed.room==i,
                                                         model.Bed.bed=='A')
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
    form = select_bed_form()
    if form.validate_on_submit():
        with engine.connect() as connection:
            bed_reservation = model.Inpatient(pid=form.data.pid,
                                              check_in=datetime.date.now(),
                                              wing=form.data.wing,
                                              room=form.data.room,
                                              bed=form.data.bed,
                                              )
    return render_template('bed_assign.html', data=avail_beds)

'''
 In-patient management
o Check for available room/bed
o Assign/remove a patent to a room/bed
o Assign/remove a doctor to a patient
o Assign/remove a nurse to a patient
o View scheduled surgery per room and per day
o View scheduled surgery per surgeon and per day
o View scheduled surgery per patient
o Book a surgery


o No two physicians can prescribe the same medication to the same patient. 
'''