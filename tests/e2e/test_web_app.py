import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,             a lower case letter and a digit'),
        ('kilic20', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'bmarshall7688'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Movie Web App' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/movies?rank=1')

    response = client.post(
        '/review',
        data={'review': 'Bad movie not even good', 'movie_rank': 1}
    )
    assert response.headers['Location'] == 'http://localhost/movies?rank=1&view_reviews_for=1'


@pytest.mark.parametrize(('review', 'messages'), (
        ("What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, "
         "and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and "
         "I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision "
         "the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over "
         "the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so "
         "you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, "
         "anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have "
         "access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the "
         "continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, "
        "maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury "
        "all over you and you will drown in it. You're fucking dead, kiddo.", (b'Your review must not contain profanity')),
        ('Hey', (b'Your review is too short')),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to review on an movie.
    response = client.post(
        '/review',
        data={'review': review, 'movie_rank': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movies_without_rank(client):
    # Check that we can retrieve the movie page.
    response = client.get('/movies')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first movie.
    assert b'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.' in response.data
    assert b'Guardians of the Galaxy' in response.data


def test_movies_with_rank(client):
    # Check that we can retrieve the movie page.
    response = client.get('/movies?rank=3')
    assert response.status_code == 200

    # Check that movie on the requested rank are included on the page.
    assert b'Three girls are kidnapped by a man with a diagnosed 23 distinct personalities. They must try to escape before the apparent emergence of a frightful new 24th.' in response.data
    assert b'Split' in response.data


def test_movies_with_review(client):
    # Check that we can retrieve the movie page.
    response = client.get('/movies?rank=1&view_reviews_for=1')
    assert response.status_code == 200

    # Check that all reviews for specified movie are included on the page.
    assert b'Eh, it was ok' in response.data
    assert b'The movie was recommended to me by a friend who saw the reviews and somehow believed those' in response.data




