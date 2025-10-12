from flask import Blueprint, render_template, request, redirect, url_for, session
from .forms import EditEvent
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Event

editbp = Blueprint('edit', __name__, template_folder='templates')

@editbp.route('/edit/<int:eventid>', methods=['GET', 'POST'])
def edit(eventid):
    event = Event.query.get_or_404(eventid)
    form = EditEvent(obj=event)  

    if form.validate_on_submit():
        event.artist = form.artist.data
        event.startTime = form.startTime.data 
        event.date = form.date.data
        event.location = form.location.data
        event.country = form.country.data
        event.title=form.title.data
        event.description=form.description.data
        event.tags = form.tags.data
        event.normalAvail = form.normalAvail.data
        event.normalPrice = form.normalPrice.data
        event.vipAvail = form.vipAvail.data
        event.vipPrice = form.vipPrice.data
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('edit.html', form=form, title='Edit')


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
