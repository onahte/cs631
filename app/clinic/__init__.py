from flask import Blueprint, render_template

clinic = Blueprint('clinic', __name__, template_folder='templates')

@clinic.route('/')
@clinic.route('/index')
def index():
    return render_template('index.html')

