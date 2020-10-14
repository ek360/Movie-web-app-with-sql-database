from typing import List, Iterable

from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie
from movie.domain.actor import Actor
from movie.domain.genre import Genre
from movie.domain.director import Director
from movie.domain.review import make_review

class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_rank, review_text, username, repo):
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentArticleException
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    comment = make_review(review_text, user, movie)
    repo.add_review(comment)

def get_first_movie(repo):
    movie = repo.get_first_movie()
    return movie_to_dict(movie)

def get_last_movie(repo):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)

def get_movie(movie_rank: int,repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    return movie_to_dict(movie)

def get_movie_by_rank(rank,repo):

    movie = repo.get_movie_by_rank(rank)


    movies_ranked = []
    next_movie = previous_movie = None

    if len(movie) > 0:
        previous_movie = repo.get_rank_of_previous_movie(movie[0])
        next_movie = repo.get_rank_of_next_movie(movie[0])

        movies_ranked = movies_to_dict(movie)
    return movies_ranked, previous_movie, next_movie

def get_review_for_movie(rank,repo):
    movie = repo.get_movie(rank)

    if movie is None:
        raise NonExistentArticleException
    return reviews_to_dict(movie.reviews)

def movie_to_dict(movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'year': movie.year,
        'description': movie.description,
        'director': movie.director,
        "runtime": movie.runtime_minutes,
        "rating": movie.rating,
        "metascore": movie.metascore,
        "reviews": reviews_to_dict(movie.reviews)}
    return movie_dict

def movies_to_dict(movies):
    return [movie_to_dict(movie) for movie in movies]

def review_to_dict(review):
    review_dict = {
        'username': review.user.user_name,
        'movie_rank': review.movie.rank,
        'review_text': review.review,
        'timestamp': review.timestamp
    }
    return review_dict

def reviews_to_dict(reviews):
    return[review_to_dict(review) for review in reviews]