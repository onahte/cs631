import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5

from .simple_pages import simple_pages
from .db import database, db, migrate, init_db
from .patient import patient
from .staff import staff

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
    app.register_blueprint(staff)

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        init_db()

    return app