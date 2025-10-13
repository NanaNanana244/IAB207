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
    
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data.strip()
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.username==user_name))
        
        if user is None:
            # Add error under username field
            login_form.user_name.errors.append('Incorrect user name')
        elif not check_password_hash(user.password_hash, password):
            # Add error under password field
            login_form.password.errors.append('Incorrect password')
        else:
            # Login successful
            session['user_id'] = user.userid
            login_user(user)
            nextp = request.args.get('next')
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
    
    return render_template('login.html', form=login_form, heading='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data) 
        user_name = form.username.data.strip()
        email = (form.email.data).strip()
        name = (form.name.data).strip()
        phoneNo = (form.phoneNo.data).strip()

        # Check if the username already exists
        existing_user = db.session.scalar(db.select(User).where(User.username == user_name))
        if existing_user:
            # Add error under username field instead of flash
            form.username.errors.append('Username already exists. Please choose a different one.')
            return render_template('register.html', form=form, title='Register')
        
        # Check if the email already exists
        existing_email = db.session.scalar(db.select(User).where(User.email == email))
        if existing_email:
            form.email.errors.append('Email address already registered. Please log in directly.')
            return render_template('register.html', form=form, title='Register')
        
        userAdd = User(name=name,
                    username=user_name, 
                    email=email,
                    phoneNo=phoneNo,
                    password_hash=password_hash)
        # add the object to the db session
        db.session.add(userAdd)
        # commit to the database
        db.session.commit()
        print('success')
        login_user(userAdd)
        session['user_id'] = userAdd.userid
        # Always end with redirect when form is valid
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form, title='Register')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


