
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db=SQLAlchemy()

def get_uuid():
    return uuid4().hex

class user(db.Model):
    __tablename__="users"
    id=db.Column(db.String(255),primary_key=True,unique=True,default=get_uuid)
    email=db.Column(db.String(255),unique=True)
    password=db.Column(db.Text,nullable=False)
    name=db.Column(db.Text,nullable=False)
    phone_number=db.Column(db.String(255))
    gender=db.Column(db.Text)

class coupon(db.Model):
    __tablename__="Coupons_ind"
    index= db.Column(db.String(255),primary_key=True,unique=True)
    merchant_title =db.Column(db.String(255))         
    offer_title=db.Column(db.String(255))           
    description=db.Column(db.String(255))            
    coupon_code=db.Column(db.String(255))            
    verified=db.Column(db.String(255))           
    region=db.Column(db.String(255)) 
    title_logo=db.Column(db.String(255))
    type_of_voucher=db.Column(db.String(255))       


class coupon_user(db.Model):
    __tablename__="coupon_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(255),unique=False,nullable=False)
    offer_title=db.Column(db.String(255))
    coupon_code=db.Column(db.String(255)) 
    category=db.Column(db.String(255),nullable=False)
    points_earned=db.Column(db.Integer,nullable=False)

