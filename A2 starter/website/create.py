from flask import Blueprint, render_template, request, redirect, url_for, session
from .forms import CreateEvent
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Event

createbp = Blueprint('create', __name__, template_folder='templates')


@createbp.route('/create', methods=['GET', 'POST'])
def create():
    print('Method type: ', request.method)
    form = CreateEvent()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        user_id = session.get('user_id')
        eventAdd = Event(userid= user_id,
                         artist=form.artist.data,
                      startTime=form.startTime.data, 
                      date=form.eventdate.data,
                      location=form.location.data,
                      country=form.country.data,
                      title=form.title.data,
                      description=form.description.data,
                      image = db_file_path,
                      tags=form.tags.data,
                      normalAvail=form.normalAvail.data,
                      normalPrice=form.normalPrice.data,
                      vipAvail=form.vipAvail.data,
                      vipPrice=form.vipPrice.data)
        # add the object to the db session
        db.session.add(eventAdd)
        # commit to the database
        db.session.commit()
        print('success')
        # Always end with redirect when form is valid
        return redirect(url_for('main.index'))
    else:
        print("Form errors:", form.errors)

    return render_template('create.html', form=form, title = 'Create')

def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image/uploads',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/uploads/' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path
