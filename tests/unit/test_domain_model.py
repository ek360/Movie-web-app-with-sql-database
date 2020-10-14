from datetime import date

from movie.domain.user import User
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.review import Review, make_review

import pytest


@pytest.fixture()
def movie():
    return Movie( 1, 'Guardians of the Galaxy', 2014, 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.','James Gunn',121,'8.1','76')


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.rank == 1
    assert movie.title == 'Guardians of the Galaxy'
    assert movie.description == 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'
    assert movie.director == 'James Gunn'
    assert movie.runtime_minutes == 121
    assert movie.rating == '8.1'
    assert movie.metascore == '76'


def test_movie_less_than_operator():
    movie1 = Movie(
        1, None, 2000, None, None, None, None, None
    )

    movie2 = Movie(
        2, None, 2000, None, None, None, None, None
    )

    assert movie1 < movie2


def test_make_review_establishes_relationships(movie, user):
    review_text = 'The movie was recommended to me by a friend who saw the reviews and somehow believed those. Huge mistake.'
    review = make_review(review_text, user, movie)

    # Check that the User object knows about the Review.
    assert review in user.reviews

    # Check that the Review knows about the User.
    assert review.user is user

    # Check that Movie knows about the Review.
    assert review in movie.reviews

    # Check that the Review knows about the Movie.
    assert review.movie is movie



