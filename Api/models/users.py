from mongoengine import *
from settings import db
import datetime

class User(Document):
    Username         =     StringField(max_length=20, required=True, unique=True)
    First_name       =     StringField(max_length=20)
    Last_name        =     StringField(max_length=20)
    Age 	         = 	   IntField(default=20)
    Sex		         =     StringField(choices=('Male','Female'), default='Male')
    Email            =     EmailField(max_length=50, required=True, unique=True)
    Phone            =     StringField(max_length=15)
    Country          =     StringField(max_length=20)
    Interest         =     ListField(required=True)
    Profile_picture  =     StringField(max_length=500)
    Password         =     StringField(max_length=128, required=True)
    Genre_history    =     ListField(StringField())
    Deleted          =     BooleanField(default=False)


    #def __repr__(self):
    #    return '<Review %r:%r>' % (self.Movie_name, self.Body)

