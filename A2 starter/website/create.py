from flask import Blueprint, render_template, request, redirect, url_for
from .forms import CreateEvent


createbp = Blueprint('create', __name__, template_folder='templates')


@createbp.route('/create')
def create():
    print('Method type: ', request.method)
    form = CreateEvent()
    if form.validate_on_submit():
        print('Successfully created new travel destination')
        return redirect(url_for('create.create'))
    return render_template('create.html', form=form)
