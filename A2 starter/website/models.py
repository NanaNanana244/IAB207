from . import db
from sqlalchemy import Time
from flask_login import UserMixin
from datetime import datetime, date
#users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False) 
    phoneNo = db.Column(db.String(20), index=True, nullable=False) 
    
    comments = db.relationship('Comment', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
   
    def get_id(self):
        return str(self.userid)
    
    def __repr__(self):
        return f'<User {self.username}>'
    #events
class Event(db.Model):
    __tablename__ = 'event'
    eventid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
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
    normalAvail = db.Column(db.Integer, index=True, nullable=False) 
    vipAvail = db.Column(db.Integer, index=True, nullable=False)   
    normalPrice = db.Column(db.Numeric(10,2), index=True, nullable=False)  
    vipPrice = db.Column(db.Numeric(10,2), index=True, nullable=False)    
    comments = db.relationship('Comment', backref='event', lazy=True)
    orders = db.relationship('Order', backref='event', lazy=True)
    
    def update_status(self):
        """Update event status based on date and ticket availability"""
        # Check if event date has passed
        if self.date < date.today():
            self.status = 'Inactive'
        # Check if all tickets are sold out (and event hasn't passed)
        elif self.normalAvail == 0 and self.vipAvail == 0:
            self.status = 'Sold out'  
        # Event is in future with tickets available
        else:
            # Only update if not Available or Cancelled
            if self.status not in ['Available', 'Cancelled']:  
                self.status = 'Available'
        
    def __repr__(self):
        return f'<Event {self.title}>'
#comments
class Comment(db.Model):
    __tablename__ = 'comment'
    commentid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey('event.eventid'))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    comment = db.Column(db.String(255), index=True, nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.commentid}>'
#orders
class Order(db.Model):
    __tablename__ = 'order'
    orderid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    eventid = db.Column(db.Integer, db.ForeignKey('event.eventid'))
    normalQty = db.Column(db.Integer, index=True, nullable=True)
    vipQty = db.Column(db.Integer, index=True, nullable=True)
    totalPrice = db.Column(db.Numeric(10,2), index=True, nullable=False)
    timeBooked = db.Column(db.DateTime, index=True, nullable=False)

    def __repr__(self):

        return f'<Order {self.orderid}>'
