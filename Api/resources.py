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
internal_server_error_message = "Something went wrong. Please try again in a few seconds"

class New_Movie_Review(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('movie_name', required=True, type=str, location='json')
    post_parser.add_argument('body', required=True, type=str, location='json')
    post_parser.add_argument('review_author', default=None, location='json')

    def post(self):
        '''
            Creating new movie review
        '''
        args = self.post_parser.parse_args()
        try:
            return controllers.new_movie_review(movie_name=args['movie_name'],
                                                body=args['body'],
                                                review_author=args['review_author'])

        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)


class Edit_Review(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('movie_name', type=str, location='json')
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


        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)

class Get_Movie_Reviews(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('movie_name', required=True, type=str, location='args')
    get_parser.add_argument('offset', type=int, location='args')
    get_parser.add_argument('limit', type=int, location='args')

    def get(self):
        '''
          retreving movie review
        '''
        args = self.get_parser.parse_args()
        try:
            return controllers.top_movie_reviews(movie_name=args['movie_name'],
                                                 offset=args['offset'],
                                                 limit=args['limit'])


        except Exception as e:
            print traceback.format_exc(e)
            abort(500, message=internal_server_error_message)