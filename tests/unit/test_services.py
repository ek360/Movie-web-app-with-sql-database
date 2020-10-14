from datetime import date

import pytest

from movie.authentication.services import AuthenticationException
from movie.movies import services as movie_services
from movie.authentication import services as auth_services
from movie.movies.services import NonExistentArticleException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'bmarshall7688'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'new_user'
    new_password = 'tcvgbjh687Q'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_rank = 3
    review_text = 'Meh, could be better'
    username = 'bmarshall7688'

    # Call the service layer to add the comment.
    movie_services.add_review(movie_rank, review_text, username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews_as_dict = movie_services.get_review_for_movie(movie_rank, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_rank = 1001
    review_text = "Meh, could be better"
    username = 'bmarshall7688'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.NonExistentArticleException):
        movie_services.add_review(movie_rank, review_text, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_rank = 1
    review_text = "I am a non existant user"
    username = 'Nothere'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_review(movie_rank, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_rank = 2

    movie_as_dict = movie_services.get_movie(movie_rank, in_memory_repo)

    assert movie_as_dict['rank'] == movie_rank
    assert movie_as_dict['title'] == 'Prometheus'
    assert movie_as_dict['year'] == 2012
    assert movie_as_dict['description'] == 'Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone.'
    assert movie_as_dict['director'] == 'Ridley Scott'
    assert movie_as_dict['runtime'] == 124
    assert movie_as_dict['rating'] == 7.0
    assert movie_as_dict['metascore'] == '65'
    assert len(movie_as_dict['reviews']) == 0



def test_cannot_get_movie_with_non_existent_rank(in_memory_repo):
    movie_rank = 1001

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(KeyError):
        movie_services.get_movie_by_rank(movie_rank, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['rank'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['rank'] == 1000


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movie_services.get_review_for_movie(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(reviews_as_dict) == 3

    # Check that the comments relate to the article whose id is 1.
    movie_ranks = [rank['movie_rank'] for rank in reviews_as_dict]
    movie_ranks = set(movie_ranks)
    assert 1 in movie_ranks and len(movie_ranks) == 1


def test_get_reviews_for_non_existent_movies(in_memory_repo):
    with pytest.raises(NonExistentArticleException):
        review_as_dict = movie_services.get_review_for_movie(1001, in_memory_repo)


def test_get_reviews_for_movies_without_reviews(in_memory_repo):
    reviews_as_dict = movie_services.get_review_for_movie(2, in_memory_repo)
    assert len(reviews_as_dict) == 0

