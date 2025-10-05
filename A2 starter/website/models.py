from . import db
from sqlalchemy import Time
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True) #PK
    username = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    phoneNo = db.Column(db.Integer,index=True, nullable=False)

    #places where there are FKs from this table
    db.relationship('comment', backref='user')
   # db.relationship('event', backref='user') #MUST BE CHANGED WHEN LOGIN IS SORTED
    db.relationship('order', backref='user')

class Event(db.Model):
    __tablename__ = 'event'
    eventid = db.Column(db.Integer,db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    db.Column(db.Integer, nullable=False, default=1) #MUST BE CHANGED TO THE FK
    artist = db.Column(db.String(100), index=True, nullable=False)
    startTime = db.Column(db.Time, index=True, nullable=False)
    location = db.Column(db.String(100), index=True, nullable=False)
    country = db.Column(db.String(100), index=True, nullable=False)  
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(255), index=True, nullable=False)
    image = db.Column(db.String(100), index=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Active')
    tags = db.Column(db.String(255), index=True, nullable=True)

    db.relationship('comment', backref='events')
    db.relationship('order', backref='events')

class Comment(db.Model):
    __tablename__ = 'comment'
    commentid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey('event.eventid'))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    username = db.Column(db.String(100), db.ForeignKey('user.username'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    comment = db.Column(db.String(255), index=True, nullable=False)


class Order(db.Model):
    __tablename__ = 'order'
    orderid = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    eventid = db.Column(db.Integer, db.ForeignKey('event.eventid'))
    price = db.Column(db.Integer, index=True, nullable=False)
    timeBooked = db.Column(db.DateTime, index=True, nullable=False)
