from flask import Blueprint, render_template, url_for, redirect, flash
from ..db import db, model
from .forms import query_form


simple_pages = Blueprint('simple_pages', __name__, template_folder='templates')


@simple_pages.route('/', methods=['POST', 'GET', 'DELETE'])
def index():
    qform = query_form()
    if qform.validate_on_submit():
        q = model.Clinic.query(query=qform.query.data)
        db.session.add(q)
        db.session.commit()
        flash('Thank you for your RSVP')
        #return redirect(url_for('simple_pages.success'))
    return render_template('index.html', form=qform)




