from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from movie.adapters.memory_repository import MemoryRepository
from movie.domain.movie import Movie
from movie.domain.actor import Actor
from movie.domain.genre import Genre
from movie.domain.director import Director
import movie.adapters.repository as repo
import movie.movies.services as services

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from movie.authentication.authentication import login_required

# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies', methods=['GET'])
def movies():
    target_rank = request.args.get('rank')
    movie_to_show_comments = request.args.get('view_reviews_for')

    rank_one = services.get_first_movie(repo.repo_instance)
    rank_hundread = services.get_last_movie(repo.repo_instance)

    if target_rank is None:
        target_rank = rank_one['rank']
    else:
        target_rank = int(target_rank)

    if movie_to_show_comments is None:
        movie_to_show_comments = -1
    else:
        movie_to_show_comments = int(movie_to_show_comments)

    movies, previous_rank, next_rank = services.get_movie_by_rank(target_rank, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if previous_rank is not None:
        prev_movie_url = url_for('movies_bp.movies', rank=previous_rank)
        first_movie_url = url_for('movies_bp.movies', rank=1)

    if next_rank is not None:
        next_movie_url = url_for('movies_bp.movies', rank=next_rank)
        last_movie_url = url_for('movies_bp.movies', rank=1000)

    movies[0]['view_review_url'] = url_for('movies_bp.movies', rank=target_rank, view_reviews_for=movies[0]['rank'])
    movies[0]["add_review_url"] = url_for('movies_bp.review_on_movie',movie=movies[0]['rank'])

    return render_template(
        'news/articles.html',
        title='Movie Rankings',
        movies=movies[0],
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movies=movie_to_show_comments
    )

@movies_blueprint.route('/review',methods=['GET', 'POST'])
@login_required
def review_on_movie():
    username = session['username']

    form = ReviewForm()

    if form.validate_on_submit():
        movie_rank = int(form.movie_rank.data)
        services.add_review(movie_rank, form.review.data, username, repo.repo_instance)
        movie = services.get_movie(movie_rank,repo.repo_instance)
        return redirect(url_for('movies_bp.movies', rank=movie['rank'], view_reviews_for=movie['rank']))

    if request.method == 'GET':
        movie_rank = int(request.args.get('movie'))
        form.movie_rank.data = movie_rank
    else:
        movie_rank = int(form.movie_rank.data)

    movie = services.get_movie(movie_rank,repo.repo_instance)
    return render_template(
        'news/comment_on_article.html',
        title='Edit article',
        movies=movie,
        form=form,
        handler_url=url_for('movies_bp.review_on_movie'),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_rank = HiddenField("Movie Rank")
    submit = SubmitField('Submit')