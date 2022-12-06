from flask import Blueprint, render_template

simple_pages = Blueprint('simple_pages', __name__, template_folder='templates')

@simple_pages.route('/')
@simple_pages.route('/index')
def index():
    return render_template('index.html')

