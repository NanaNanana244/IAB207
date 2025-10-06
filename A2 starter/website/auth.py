from flask import Blueprint, flash, render_template, request, url_for, redirect, session
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.username==user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next')
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('login.html', form=login_form, heading='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        userAdd = User(name=form.name.data,
                    username=form.username.data, 
                    email=form.email.data,
                    phoneNo=form.phoneNo.data,
                    password_hash=password_hash)
        # add the object to the db session
        db.session.add(userAdd)
        # commit to the database
        db.session.commit()
        print('success')
        session['user_id'] = userAdd.userid
        # Always end with redirect when form is valid
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form, title='Register')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

