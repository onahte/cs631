import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5

from .db import database, db, migrate, init_db
from .clinic import clinic
from .patient import patient
from .physician import physician
from .surgeon import surgeon
from .nurse import nurse
from .staff import staff
from .inpatient import inpatient

def create_app():
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")

    csrf = CSRFProtect(app)
    bootstrap = Bootstrap5(app)

    app.register_blueprint(simple_pages)
    app.register_blueprint(database)
    app.register_blueprint(patient)
    app.register_blueprint(physician)
    app.register_blueprint(surgeon)
    app.register_blueprint(nurse)
    app.register_blueprint(staff)
    app.register_blueprint(inpatient)

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        init_db()

    return app