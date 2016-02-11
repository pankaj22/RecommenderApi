from settings import app,api
from resources import *

#Comments Urls

api.add_resource(New_Movie_Review, '/review/new')
api.add_resource(Edit_Review, '/review/edit/<review_id>')
api.add_resource(Get_Movie_Reviews, '/reviews/get')

if __name__ == '__main__':
    app.run('127.0.0.1', 8000)