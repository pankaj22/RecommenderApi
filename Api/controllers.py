import comments_analysis
import rating_calculation
from models import Reviews
from settings import *

####### Comments controllers ########
#Like,Dislike feature in comments section

def new_movie_review(movie_name, body, review_author='Pankaj Gupta'):
    return comments_analysis.update_movie_review(movie_name=movie_name,sentence=body,review_author=review_author)

def update_movie_review(review_id, movie_name=None, body=None, timestamp=None, deleted=None, review_author=None):
    try:
        review = Reviews.objects(id=review_id)
        if movie_name:
            review.update(Movie_name=movie_name)

        if body:
            review.update(Body=body)
            analysis = comments_analysis.sentiment(sentence=body)
            review.update(Polarity=analysis['polarity'])
            review.update(Sense=analysis['sense'])

        if timestamp:
            review.update(Timestamp=timestamp)

        if deleted:
            review.update(Deleted=deleted)

        if review_author:
            review.update(Review_author=review_author)

        return {'Success':True}

    except:
        return {'Success':False}

def top_movie_reviews(movie_name,offset=0,limit=10):
    try:
        positive_reviews,neutral_reviews,negative_reviews = comments_analysis.get_movie_reviews(movie_name=movie_name)
        if len(positive_reviews)==0 and len(neutral_reviews)==0 and len(negative_reviews)==0:
            return {'Body': 'No reviews'}

        return {'Success':True,
                'positive_reviews':positive_reviews,
                'neutral_reviews':neutral_reviews,
                'negative_reviews':negative_reviews
               }
    except:
        return {'Success':False}

def reviews_rating(movie_name):
    try:
        positive_reviews,neutral_reviews,negative_reviews = comments_analysis.get_movie_reviews(movie_name=movie_name)
        rating = rating_calculation.calculate_rating(positive_reviews=positive_reviews,negative_reviews=negative_reviews)
        return {'Success':True,
                'Rating':rating
               }
    except:
        return {'Success':False}
