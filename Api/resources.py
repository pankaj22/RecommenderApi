import sys
import flask
import flask_restful
from flask_restful import reqparse
from flask import request
from flask_restful import Resource
import controllers
import json
from flask_restful import abort
import traceback
import datetime
from mongoengine.queryset import DO_NOTHING,DoesNotExist,InvalidQueryError,\
                                 MultipleObjectsReturned, NotUniqueError, OperationError

internal_server_error_message = "Something went wrong. Please try again in a few seconds"


####### Movie comments resources #########
class New_Movie_Review(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('body', required=True, type=str, location='json')
    post_parser.add_argument('review_author', default=None, location='json')

    def post(self, movie_id):
        '''
            Creating new movie review
        '''
        args = self.post_parser.parse_args()
        try:
            return controllers.new_movie_review(movie_id=movie_id,
                                                body=args['body'],
                                                review_author=args['review_author'])

        except DoesNotExist as e:
            abort(400, message=str(e))
        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)


class Edit_Review(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('movie_id', type=str, location='json')
    post_parser.add_argument('body', type=str, location='json')
    post_parser.add_argument('review_author', default=None, location='json')
    post_parser.add_argument('timestamp', default=datetime.datetime.now(), location='json')
    post_parser.add_argument('deleted', default=False, location='json')

    def post(self,review_id):
        '''
            Editing movie review
        '''
        args = self.post_parser.parse_args()
        try:
            return controllers.update_movie_review(review_id=review_id,
                                                   movie_name=args['movie_name'],
                                                   body=args['body'],
                                                   review_author=args['review_author'],
                                                   timestamp=args['timestamp'],
                                                   deleted=args['deleted'])

        except DoesNotExist as e:
            abort(400, message=str(e))
        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)

class Get_Movie_Reviews(Resource):
    get_parser = reqparse.RequestParser()
    #get_parser.add_argument('movie_name', required=True, type=str, location='args')
    get_parser.add_argument('offset', type=int, location='args')
    get_parser.add_argument('limit', type=int, location='args')

    def get(self, movie_id):
        '''
          retreving movie review
        '''
        args = self.get_parser.parse_args()
        try:
            return controllers.top_movie_reviews(movie_name=args['movie_name'],
                                                 offset=args['offset'],
                                                 limit=args['limit'])

        except DoesNotExist as e:
            abort(400, message=str(e))
        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)

class Review_Summarization(Resource):
    get_parser = reqparse.RequestParser()
    def get(self, movie_id):
        '''
            Summarization of movie reviews
        '''
        try:
            return controllers.review_summarization(movie_id=movie_id)

        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)

####### Movie resources ########

class New_Movie(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('movie_name', required=True, type=str, location='json')
    post_parser.add_argument('year', type=int, location='json')
    post_parser.add_argument('description', type=str, default=None, location='json')
    post_parser.add_argument('cover_picture', type=str, default=None, location='json')
    post_parser.add_argument('genre', type=list, default=None, location='json')
    post_parser.add_argument('cast', type=list, default=None, location='json')
    post_parser.add_argument('directors', type=list, default=None, location='json')

    def post(self):
        '''
            Creating new movie
        '''
        args = self.post_parser.parse_args()
        try:
            return controllers.new_movie(movie_name=args['movie_name'],
                                         year=args['year'],
                                         description=args['description'],
                                         cover_picture=args['cover_picture'],
                                         genre=args['genre'],
                                         cast=args['cast'],
                                         directors=args['directors'])


        except DoesNotExist as e:
            abort(400, message=str(e))
        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)

class Edit_Movie(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('movie_name', type=str, location='json')
    post_parser.add_argument('year', type=str, location='json')
    post_parser.add_argument('description', type=str, default=None, location='json')
    post_parser.add_argument('genre', type=str, default=None, location='json')
    post_parser.add_argument('cast', type=list, default=None, location='json')
    post_parser.add_argument('directors', type=list, default=None, location='json')
    post_parser.add_argument('cover_picture', type=str, default=None, location='json')
    post_parser.add_argument('created_by', type=str, default=None, location='json')
    post_parser.add_argument('reviews_rating', type=float, default=None, location='json')
    post_parser.add_argument('user_rating', type=float, default=None, location='json')
    post_parser.add_argument('social_rating', type=float, default=None, location='json')
    post_parser.add_argument('deleted', type=bool, default=None, location='json')


    def post(self, movie_id):
        '''
            updating new movie
        '''
        args = self.post_parser.parse_args()
        try:
            return controllers.edit_movie(movie_id=movie_id,
                                         movie_name=args['movie_name'],
                                         year=args['year'],
                                         description=args['description'],
                                         genre=args['genre'],
                                         cast=args['cast'],
                                         directors=args['directors'],
                                         created_by=args['created_by'],
                                         reviews_rating=args['reviews_rating'],
                                         user_rating=args['user_rating'],
                                         social_rating=args['social_rating'],
                                         deleted=args['deleted'],
                                         cover_picture=args['cover_picture'])


        except DoesNotExist as e:
            abort(400, message=str(e))
        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)


class Get_Movie_Details(Resource):
    get_parser = reqparse.RequestParser()
    #get_parser.add_argument('movie_name', required=True, type=str, location='args')
    get_parser.add_argument('offset', type=int, default=0, location='args')
    get_parser.add_argument('limit', type=int, default=10, location='args')

    def get(self, movie_id):
        '''
          retreving movie details
        '''
        args = self.get_parser.parse_args()
        try:
            return controllers.get_movie_details(movie_id=movie_id,
                                                 offset=args['offset'],
                                                 limit=args['limit'])

        except DoesNotExist as e:
            abort(400, message=str(e))
        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)

class Get_Movies(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('offset', type=int, default=0, location='args')
    get_parser.add_argument('limit', type=int, default=10, location='args')

    def get(self):
        '''
          retreving all movies details
        '''
        args = self.get_parser.parse_args()
        try:
            return controllers.get_movies(offset=args['offset'],
                                          limit=args['limit'])

        except DoesNotExist as e:
            abort(400, message=str(e))
        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)

class Get_Recommendation(Resource):
    get_parser = reqparse.RequestParser()
    def get(self, user_id):
        '''
            Recommendation of users
        '''
        try:
            return controllers.get_recommendation(user_id=user_id)

        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)


class New_User(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('username', type=str, required=True, location='json')
    post_parser.add_argument('password', type=str, required=True, location='json')
    post_parser.add_argument('email', type=str, required=True, location='json')
    post_parser.add_argument('first_name', type=str, default=None, location='json')
    post_parser.add_argument('last_name', type=str, default=None, location='json')
    post_parser.add_argument('interest', type=list, default=None, location='json')


    def post(self):
        '''
            new user
        '''
        args = self.post_parser.parse_args()
        try:
            return controllers.new_user(username=args['username'],
                                          password=args['password'],
                                          email=args['email'],
                                          first_name=args['first_name'],
                                          last_name=args['last_name'],
                                          interest=args['interest']
                                        )


        except InvalidQueryError as e:
            abort(400, message=str(e))
        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)