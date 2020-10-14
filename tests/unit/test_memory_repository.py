from datetime import date, datetime
from typing import List

import pytest
from movie.domain.user import User
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.review import Review, make_review

from movie.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('bmarshall7688')
    assert user == User('bmarshall7688', 'cLQ^C#oFXloS')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_articles = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 Articles.
    assert number_of_articles == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie( 1001, 'A Movie', 2014, 'Blah blah blah blah','Director',121,'6.9','69')
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(1001) is movie

Movie( 1, 'Guardians of the Galaxy', 2014, 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.','James Gunn',121,'8.1','76')
def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Movie has expected reviews.
    review_three = [review for review in movie.reviews if review.review == 'Eh, it was ok'][
        0]

    assert review_three.user.user_name == 'kilic20'



def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1001)
    assert movie is None


def test_repository_can_retrieve_movie_by_rank(in_memory_repo):
    movie = in_memory_repo.get_movie_by_rank(2)

    assert movie[0].title == 'Prometheus'


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Nine Lives'


def test_repository_returns_rank_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(6)
    previous_rank = in_memory_repo.get_rank_of_previous_movie(movie)

    assert previous_rank == 5


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_rank = in_memory_repo.get_rank_of_previous_movie(movie)

    assert previous_rank is None


def test_repository_returns_rank_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    next_rank = in_memory_repo.get_rank_of_next_movie(movie)

    assert next_rank == 4


def test_repository_returns_none_when_there_are_no_subsequent_articles(in_memory_repo):
    movie = in_memory_repo.get_movie(1000)
    next_rank = in_memory_repo.get_rank_of_next_movie(movie)

    assert next_rank is None


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('kilic20')
    movie = in_memory_repo.get_movie(2)
    review = make_review("Meh, could be better", user, movie)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "Meh, could be better", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 1



