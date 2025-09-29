from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DecimalField, SubmitField, TimeField, DateField, PasswordField
from wtforms.validators import InputRequired, length, EqualTo, Email

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

class CreateEvent(FlaskForm):
#event creation
    title = StringField('Enter event name', [InputRequired()])
    image = FileField('Enter image that you would like to use', [InputRequired()])
    date = DateField('Enter the date of event', [InputRequired()])
    time = TimeField('Enter the starting time of event', [InputRequired()])
    venue = StringField('Enter venue name', [InputRequired()])
    normalPrice = DecimalField('Enter normal ticket price', [InputRequired()])
    vipPrice = DecimalField('Enter VIP ticket price', [InputRequired()])
    normalAvail = DecimalField('Enter number of normal tickets', [InputRequired()])
    vipAvail = DecimalField('Enter number of VIP tickets', [InputRequired()])
    description = TextAreaField('Enter event description', [InputRequired()])
    submit = SubmitField('Submit')


