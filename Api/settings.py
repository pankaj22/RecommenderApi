from flask import Flask
from mongoengine import *
from flask_restful import *

# app initialization
app = Flask(__name__)
app.debug = True
api = Api(app)
# db initialization
db = 'recmongo'
connect(db)


