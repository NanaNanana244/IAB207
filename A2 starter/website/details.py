from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Comment
from .forms import OrderForm, CommentForm

detailsbp = Blueprint('details', __name__, url_prefix='/details')


@detailsbp.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    return render_template('event_details/details.html', form=form)



