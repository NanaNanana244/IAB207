from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, FileField, DecimalField, SubmitField, TimeField, DateField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email

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
    artist = StringField('Enter artist/group name', [InputRequired()])
    image = FileField('Event Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    date = DateField('Enter the date of event', [InputRequired()])
    startTime = TimeField('Enter the starting time of event', [InputRequired()])
    location = StringField('Enter venue name', [InputRequired()])
    normalPrice = DecimalField('Enter normal ticket price', [InputRequired()])
    vipPrice = DecimalField('Enter VIP ticket price', [InputRequired()])
    normalAvail = DecimalField('Enter number of normal tickets', [InputRequired()])
    vipAvail = DecimalField('Enter number of VIP tickets', [InputRequired()])
    description = TextAreaField('Enter event description', [InputRequired()])
    tags = TextAreaField('Enter any words that will be helpful for users to search. This could include: genre, common mispellings, band members, popular songs etc.')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
#create comments
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')


class OrderForm(FlaskForm):
#creates order
    ticType = SelectField('Select Ticket Type', validators = [InputRequired()], choices = [('normTicket', 'Normal Ticket (Price: $200)'), ('vipticket', 'VIP Ticket (Price $300)')])
    numTickets = StringField("How many tickets?", validators = [InputRequired()])
    submit = SubmitField('Submit')
    

