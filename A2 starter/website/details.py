from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment
from .forms import OrderForm, CommentForm

detailsbp = Blueprint('details', __name__, url_prefix='/details')

@detailsbp.route("/")
def index():
    return render_template('order_details.html')

@detailsbp.route('/event-details', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    return render_template('details.html', form=form)

#@detailsbp.route('/<id>/comment', methods = ['GET', 'POST'])
#def comment(id):
  # form created for comment section
  #form = CommentForm()
  #if form.validate_on_submit():	#this is true only in case of POST method
    #print(f"The following comment has been posted: {form.text.data}")
  #sreturn redirect(url_for('details.show', id=id))

