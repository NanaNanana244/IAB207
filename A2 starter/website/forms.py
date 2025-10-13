from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, FileField, DecimalField, IntegerField, SubmitField, TimeField, DateField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#this is the registration form
class RegisterForm(FlaskForm):
    username=StringField("User Name", validators=[InputRequired()])
    name=StringField("Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phoneNo=DecimalField("Phone Number", validators=[InputRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

#event creation
class CreateEvent(FlaskForm):
    def validate_eventdate(form, field):
        print("Validating date:", field.data)
        if field.data < date.today():
            raise ValidationError('The date cannot be in the past.')
    title = StringField('Enter event name', [InputRequired()])
    artist = StringField('Enter artist/group name', [InputRequired()])
    image = FileField('Event Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    eventdate = DateField('Enter the date of event', validators=[InputRequired(), validate_eventdate])
    startTime = TimeField('Enter the starting time of event', [InputRequired()])
    location = StringField('Enter venue name', [InputRequired()])
    country = StringField('Enter country (Spelling must be correct)', [InputRequired()]) 
    status = StringField()
    normalPrice = DecimalField('Enter normal ticket price', [InputRequired()])
    vipPrice = DecimalField('Enter VIP ticket price', [InputRequired()])
    normalAvail = IntegerField('Enter number of normal tickets', [InputRequired()])
    vipAvail = IntegerField('Enter number of VIP tickets', [InputRequired()])
    description = TextAreaField('Enter event description', [InputRequired()])
    tags = TextAreaField('Enter keywords to help users find this event. Examples: genre, common mispellings, band members, popular songs, etc.')
    submit = SubmitField('Submit')

class EditEvent(FlaskForm):
    def validate_eventdate(form, field):
        print("Validating date:", field.data)
        if field.data < date.today():
            raise ValidationError('The date cannot be in the past.')
    title = StringField('Enter event name')
    artist = StringField('Enter artist/group name')
    image = FileField('Event Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    date = DateField('Enter the date of event', validators=validate_eventdate)
    startTime = TimeField('Enter the starting time of event')
    location = StringField('Enter venue name')
    country = StringField('Enter country (Spelling must be correct)') 
    normalPrice = DecimalField('Enter normal ticket price')
    vipPrice = DecimalField('Enter VIP ticket price')
    normalAvail = DecimalField('Enter number of normal tickets')
    vipAvail = DecimalField('Enter number of VIP tickets')
    status = StringField('Event Status')
    description = TextAreaField('Enter event description')
    tags = TextAreaField('Enter keywords to help users find this event. Examples: genre, common mispellings, band members, popular songs, etc.')
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




