from mongoengine import *
from settings import db
import datetime

class Movies(Document):
    Movie_name      =     StringField(max_length=50, required=True)
    Created_by      =     StringField(max_length=50, default='Pankaj Gupta')
    Year            =     IntField()
    Genre           =     ListField(StringField())
    Description     =     StringField(max_length=1000)
    Cover_picture   =     StringField(max_length=500)
    Rating          =     FloatField(default=0)
    Reviews_rating  =     FloatField(default=0)
    User_rating     =     FloatField(default=0)
    Social_rating   =     FloatField(default=0)
    User_rating_list=     ListField(FloatField())
    Cast            =     ListField(StringField())
    Directors       =     ListField(StringField())
    Deleted         =     BooleanField(default=False)
    Created_at      =     DateTimeField(default=datetime.datetime.now())


    #def __repr__(self):
    #    return '<Review %r:%r>' % (self.Movie_name, self.Body)

