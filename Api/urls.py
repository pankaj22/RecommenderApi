from settings import app,api
from resources import *

#Comments Urls

api.add_resource(New_Movie_Review, '/review/new/<movie_id>')
api.add_resource(Edit_Review, '/review/edit/<review_id>')
api.add_resource(Get_Movie_Reviews, '/reviews/get/<movie_id>')
api.add_resource(New_Movie, '/movie/new')
api.add_resource(Edit_Movie, '/movie/edit/<movie_id>')
api.add_resource(Get_Movie_Details, '/movie/get/<movie_id>')
api.add_resource(Get_Movies, '/movies/get')
api.add_resource(Get_Recommendation, '/movies/recommendations/<user_id>')
api.add_resource(Review_Summarization, '/reviews/summarization/<movie_id>')
api.add_resource(New_User, '/new/user')


if __name__ == '__main__':
    app.run('127.0.0.1', 8000)
