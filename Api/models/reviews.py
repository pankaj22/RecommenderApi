from mongoengine import *
from settings import db
import datetime

class Reviews(Document):
    Body      		=     StringField(max_length=500, required=True)
    Timestamp 		=     DateTimeField(default= datetime.datetime.now())
    Deleted   		=     BooleanField(default=False, required=True)
    Review_author 	= 	  StringField(required=True, default='Pankaj Gupta')
    Movie_id 		=     StringField(required=True)
    Polarity 		=     FloatField(required=True)
    Sense  			=     StringField(choices=('positive','neutral','negative'),required=True)

    #def __repr__(self):
    #    return '<Review %r:%r>' % (self.Movie_name, self.Body)

