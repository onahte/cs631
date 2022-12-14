import os

from flask import Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, event
# from sqlalchemy_utils import database_exists, create_database
#from flask_migrate import Migrate
# import psycopg2
import pandas as pd

from .. import config

db = SQLAlchemy()
#migrate = Migrate()
database = Blueprint('database', __name__, )
URL = config.Config.SQLALCHEMY_DATABASE_URI
engine = create_engine(URL)


def init_db():

    '''
    '''
    with engine.connect() as connection:
        db.drop_all()
        db.create_all()
    '''
    '''
    '''This is a list of all our tables. 
        Order the list by putting tables w/ no Foreign Keys first '''
    '''
    '''
    tables = ['address', 'allergy', 'physician', 'bed', 'nurse',
            'patient', 'clinic', 'consultation', 'contract', 'corporate',
            'gender', 'illness', 'inpatient', 'medical_data', 'medication',
            'nurse_assign_surgery', 'nurse_assign_inpatient', 'nurse_schedule',
            'own', 'skill_possessed', 'prescription', 'salary', 'skill',
            'surgery_schedule', 'staff', 'surgeon', 'surgery',
            'work', 'physician_schedule', 'staff_schedule', 'nurse_unit']
    for table in tables:
       populate_table(table)
    '''
    '''
    '''
    Foreign Key error occurs when implementing:
    for filename in os.listdir(current_app.config['CSV_DIR']):
        basename, extension = os.path.splitext(filename)
    '''
    '''
    '''
    connection.close()
    engine.dispose()
    '''
    '''
    '''
    try:
        connection = psycopg2.connect(URL)
        print("ElephantSQL connection successful")
    except:
        print("Database not connected")

    if not database_exists(URL):
        print("Creating database...")
        create_database(URL)
    '''
'''
'''
def populate_table(table):
    filename = table + '.csv'
    filepath = os.path.join(current_app.config['CSV_DIR'], filename)
    data = pd.read_csv(filepath)
    data.to_sql(table, engine, if_exists='append', index=False)
'''
'''