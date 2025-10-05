from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment
from .forms import CommentForm

detailsbp = Blueprint('details', __name__, url_prefix='/details')

@detailsbp.route('/<id>/comment', methods = ['GET', 'POST'])
def comment(id):
  # here the form is created  form = CommentForm()
  form = CommentForm()
  if form.validate_on_submit():	#this is true only in case of POST method
    print(f"The following comment has been posted: {form.text.data}")
  # notice the signature of url_for
  return redirect(url_for('details.show', id=1))

def get_event():
    