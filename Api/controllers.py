from settings import *
import comments_analysis, rating_calculation
import text_summarization
from models import Reviews, Movies, User
from mongoengine.queryset import DO_NOTHING,DoesNotExist,InvalidQueryError,\
                                 MultipleObjectsReturned, NotUniqueError, OperationError

####### Comments controllers ########
#Like,Dislike feature in comments section

def new_movie_review(movie_id, body, review_author='Pankaj Gupta'):
    try:
        comments_analysis.update_movie_review(movie_id=movie_id,sentence=body,review_author=review_author)
        rating = reviews_rating(movie_id=movie_id)
        movie = Movies.objects(id=movie_id)
        movie.update(Rating=rating)
        movie.update(Reviews_rating=rating)
        return {"Success":True}
    except:
        raise DoesNotExist("Movie does not exist.")

def update_movie_review(review_id, movie_id=None, body=None, timestamp=None, deleted=None, review_author=None):
    try:
        review = Reviews.objects(id=review_id)
        if movie_id:
            review.update(Movie_id=movie_id)

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
        raise InvalidQueryError("Check for details")

def top_movie_reviews(movie_id,offset=0,limit=10):
    try:
        positive_reviews,neutral_reviews,negative_reviews = comments_analysis.get_movie_reviews(movie_id=movie_id)
        if len(positive_reviews)==0 and len(neutral_reviews)==0 and len(negative_reviews)==0:
            return {'Body': 'No reviews'}

        return {'Success':True,
                'positive_reviews':positive_reviews,
                'neutral_reviews':neutral_reviews,
                'negative_reviews':negative_reviews
               }
    except:
        raise DoesNotExist("Movie does not exist")

def reviews_rating(movie_id):
    try:
        positive_reviews,neutral_reviews,negative_reviews = comments_analysis.get_movie_reviews(movie_id=movie_id)
        rating = rating_calculation.calculate_rating(positive_reviews=positive_reviews,negative_reviews=negative_reviews)
        return rating
        # {'Success':True,
        # 'Rating':rating}
    except:
        raise DoesNotExist("Movie does not exist")

def review_summarization(movie_id):
    try:
        positive_reviews = Reviews.objects(Movie_id=movie_id, Sense='positive').order_by('-Polarity')
        negative_reviews = Reviews.objects(Movie_id=movie_id, Sense='negative').order_by('Polarity')
        neutral_reviews = Reviews.objects(Movie_id=movie_id, Sense='neutral')
        positive_string=""
        negative_string=""
        neutral_string=""
        for review in positive_reviews:
            positive_string+=(review.Body+" ")
        for review in negative_reviews:
            negative_string+=(review.Body+" ")
        for review in neutral_reviews:
            neutral_string+=(review.Body+" ")

        positive_summ = text_summarization.summarize(text=positive_string)
        negative_summ = text_summarization.summarize(text=negative_string)
        neutral_summ = text_summarization.summarize(text=neutral_string)
        return {
                "positive_key_reviews":positive_summ,
                "negative_key_reviews":negative_summ,
                "neutral_key_reviews":neutral_summ
        }
    except:
        raise InvalidQueryError("Summary cannot be generated")

#### Movies controllers ######

def new_movie(movie_name, year, description, cover_picture, genre, cast, directors, created_by='Pankaj Gupta'):
    try:
        movie = Movies(Movie_name=movie_name, Created_by=created_by, Year=year, Description=description,
                       Cover_picture=cover_picture, Genre=genre, Cast=cast, Directors=directors)
        movie.save()
        return {'Success':True}
    except:
        raise InvalidQueryError("Check for movie details")

def edit_movie(movie_id, movie_name=None, created_by=None, year=None, description=None, cover_picture=None,
               genre=None, rating=None, reviews_rating=None, user_rating=None, social_rating=None, deleted=None,
               cast=None, directors=None):
    
    try:
        movie = Movies.objects(id=movie_id)
        if movie_name:
            movie.update(Movie_name=movie_name)
        if created_by:
            movie.update(Created_by=created_by)
        if year:
            movie.update(Year=year)
        if description:
            movie.update(Description=description)
        if cover_picture:
            movie.update(Cover_picture=cover_picture)
        if rating:
            movie.update(Rating=rating)
        if reviews_rating:
            movie.update(Reviews_rating=reviews_rating)
        if user_rating:
            movie.update(User_rating=user_rating)
        if social_rating:
            movie.update(Social_rating=social_rating)
        if deleted:
            movie.update(Deleted=deleted)
        if cast:
            movie.update(Cast=cast)

        return {'Success':True}

    except:
        raise DoesNotExist("Movie does not exist")

def get_movie_details(movie_id, offset, limit):
    try:
        movie = Movies.objects(id=movie_id).first()
        return {
                'id':            movie_id,
                'movie_name':    movie.Movie_name,
                'genre':         movie.Genre,
                'description':   movie.Description,
                'cover_picture': movie.Cover_picture,
                'rating':        movie.Rating,
                'cast':          movie.Cast,
                'directors':     movie.Directors
            }
    except:
        raise DoesNotExist("Movie does not exist")


def get_movies(offset,limit):
    try:
        movies = Movies.objects.all()
        movie_list=[]
        for movie in movies:
            movie_data={}
            movie_data['id']=str(movie.id)
            movie_data['movie_name']=movie.Movie_name
            movie_data['genre']=movie.Genre
            movie_data['description']=movie.Description
            movie_data['cover_picture']=movie.Cover_picture
            movie_data['rating']=movie.Rating
            movie_data['cast']=movie.Cast
            movie_data['directors']=movie.Directors

            movie_list.append(movie_data)

        return {'movie_list':movie_list}

    except:
        raise InvalidQueryError("Movies not available")

def get_recommendation(user_id):
    user = User.objects(id=user_id).first()
    user_interest = user.Interest
    movies = Movies.objects(Genre__in=user_interest).order_by('-Rating')
    movie_list=[]
    for movie in movies:
        movie_detail={}
        movie_detail["Movie_name"]=movie.Movie_name
        movie_detail["Rating"]=movie.Rating
        movie_detail["Genre"]=movie.Genre
        movie_list.append(movie_detail)

    return {"movie_list":movie_list,"user_interest":user.Interest}

def new_user(username, password, email, first_name, last_name, interest):
    if User.objects(Username=username).first():
        raise InvalidQueryError("User already exists.")
    if User.objects(Email=email).first():
        raise InvalidQueryError("User already exists.")

    try:
        user = User(Username=username, Password=password, Email=email,
                    First_name=first_name, Last_name=last_name, Interest=interest)
        user.save()
        return {"Success":True}
    except:
        raise InvalidQueryError("Error in creating user.")

