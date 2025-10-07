from . import db
from sqlalchemy import Time
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    username = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    phoneNo = db.Column(db.Integer, index=True, nullable=False)

    # Add this property for Flask-Login
    @property
    def id(self):
        return self.userid

    # Relationships - SPECIFY FOREIGN KEYS
    comments = db.relationship('Comment', backref='user', foreign_keys='Comment.userid')
    events = db.relationship('Event', backref='user')
    orders = db.relationship('Order', backref='user', foreign_keys='Order.userid')

class Comment(db.Model):
    __tablename__ = 'comment'
    commentid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey('event.eventid'))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))  # This is the main foreign key
    username = db.Column(db.String(100), db.ForeignKey('user.username'))  # This causes the ambiguity
    created_at = db.Column(db.DateTime, default=datetime.now())
    comment = db.Column(db.String(255), index=True, nullable=False)
    
class Event(db.Model):
    __tablename__ = 'event'
    eventid = db.Column(db.Integer,db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    artist = db.Column(db.String(100), index=True, nullable=False)
    startTime = db.Column(db.Time, index=True, nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)
    location = db.Column(db.String(100), index=True, nullable=False)
    country = db.Column(db.String(100), index=True, nullable=False)  
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(255), index=True, nullable=False)
    image = db.Column(db.String(100), index=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Active')
    tags = db.Column(db.String(255), index=True, nullable=True)
    country = db.Column(db.String(100), index=True, nullable=False)
    normalAvail = db.Column(db.Float, index=True, nullable=False)
    vipAvail = db.Column(db.Float, index=True, nullable=False)
    normalPrice = db.Column(db.Float, index=True, nullable=False)
    vipPrice = db.Column(db.Float, index=True, nullable=False)

    comments = db.relationship('Comment', backref='event', lazy=True)
    orders = db.relationship('Order', backref='event', lazy=True)
    
    def __repr__(self):
        return f'<Event {self.title}>'

class Order(db.Model):
    __tablename__ = 'order'
    orderid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    eventid = db.Column(db.Integer, db.ForeignKey('event.eventid'))
    normalQty = db.Column(db.Integer, nullable=True)
    vipQty = db.Column(db.Integer, nullable=True)
    totalPrice = db.Column(db.Float, nullable=False)
    timeBooked = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Order {self.orderid}>'

