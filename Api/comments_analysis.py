from textblob import TextBlob
import json
import math
from models import Reviews
from rating_calculation import *

def sentiment(sentence):
    analysis = TextBlob(sentence)
    polarity = list(analysis.sentiment)[0]
    if polarity>0:
        return {'polarity':(polarity*100),
                'sense':'positive'}
    elif polarity<0:
        return {'polarity':(-1*polarity*100),
                'sense':'negative'}
    else:
        return {'polarity':polarity,
                'sense':'neutral'}

def update_movie_review(movie_name, sentence, review_author='Pankaj Gupta'):
    try:
        analysis = TextBlob(sentence)
        polarity = list(analysis.sentiment)[0]
        if(polarity>0):
            review = Reviews(Movie_name=movie_name, Body=sentence, Polarity=(polarity*100), Sense='positive', Review_author=review_author)
            review.save()
        elif(polarity<0):
            review = Reviews(Movie_name=movie_name, Body=sentence, Polarity=(-1*polarity*100), Sense='negative', Review_author=review_author)
            review.save()
        else:
            review = Reviews(Movie_name=movie_name, Body=sentence, Polarity=polarity, Sense='neutral', Review_author=review_author)
            review.save()
        print('Successfully updated')
        return {'Success': True}
    except:
        print('Something went wrong in updating reviews in DB')
        return {'Success': False}


def get_movie_reviews(movie_name,offset=0,limit=10):
    positive_reviews=[]
    negative_reviews=[]
    neutral_reviews=[]
    reviews = Reviews.objects(Movie_name=movie_name)

    for review in reviews:
        d={}
        d['sentence']=review.Body
        d['polarity']=review.Polarity
        if review.Sense == 'positive':
            positive_reviews.append(d)
        elif review.Sense == 'neutral':
            neutral_reviews.append(d)
        else:
            negative_reviews.append(d)

    positive_reviews = sorted(positive_reviews, key=lambda k: k['polarity'], reverse=True)
    negative_reviews = sorted(negative_reviews, key=lambda k: k['polarity'], reverse=True)
    #rating = calculate_rating(positive_reviews,negative_reviews)
    #print  rating
    return positive_reviews,neutral_reviews,negative_reviews
