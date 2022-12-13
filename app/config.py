import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = '4xfd{Hxxe5<we95p0bf9WWeu4x96e59236xne1O<!oe976xckswa0pp9fRqqu11nmx8'
    SESSION_COOKIE_SECURE = True
    USER = "kisdjrmq"
    PW = "DsSJegBQVqGvc3f2GFapEcQpqLFPBgRf"
    PORT = "5432"
    POSTGRES_URI = "newarkmedicalassociates.caglylxbhcpl.us-east-1.rds.amazonaws.com"
    #POSTGRES_URI = "peanut.db.elephantsql.com"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + PW + "@" + POSTGRES_URI + "/" + USER
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_DIR = os.path.join(BASE_DIR, 'static/uploads')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
