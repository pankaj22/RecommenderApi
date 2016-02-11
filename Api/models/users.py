from mongoengine import *
from settings import db
import datetime


class Genre_list(EmbeddedDocument):
    Genre     =     StringField(max_length=50)
    Count     =     IntField(default=0)

class User(Document):
    Username         =     StringField(max_length=20, required=True, unique=True)
    First_name       =     StringField(max_length=20)
    Last_name        =     StringField(max_length=20)
    Age 	         = 	   IntField(default=20)
    Sex		         =     StringField(choices=('Male','Female'), required=True)
    Email            =     EmailField()
    Phone            =     StringField(max_length=15)
    Country          =     StringField(max_length=20)
    Interest         =     ListField(required=True)
    Profile_picture  =     StringField(max_length=500)
    Password         =     StringField(max_length=128, required=True)
    Genre_history    =     ListField(EmbeddedDocumentField('Genre_list'))
    Deleted          =     BooleanField(default=False, required=True)


    #def __repr__(self):
    #    return '<Review %r:%r>' % (self.Movie_name, self.Body)

