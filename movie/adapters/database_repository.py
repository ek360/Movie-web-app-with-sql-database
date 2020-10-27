import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie.domain.movie import Movie
from movie.domain.actor import Actor
from movie.domain.genre import Genre
from movie.domain.director import Director
from movie.domain.user import User
from movie.domain.review import Review, make_review
from movie.adapters.repository import AbstractRepository, RepositoryException


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_actor(self, actor: Actor):
        raise NotImplementedError

    def get_actor(self, actor) -> Actor:
        raise NotImplementedError

    def add_director(self, director: Director):
        raise NotImplementedError

    def get_director(self, director) -> Director:
        raise NotImplementedError

    def add_genre(self, genre: Genre):
        raise NotImplementedError

    def get_genre(self, genre) -> Genre:
        raise NotImplementedError

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(user_name=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, rank) -> Movie:
        article = None
        try:
            article = self._session_cm.session.query(Movie).filter(Movie.rank == rank).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return article

    def get_movie_by_rank(self, target_rank):
        if target_rank is None:
            movies = self._session_cm.session.query(Movie).all()
            return movies
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            movies = self._session_cm.session.query(Movie).filter(Movie.rank == target_rank).all()
            return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_first_movie(self):
        article = self._session_cm.session.query(Movie).first()
        return article

    def get_last_movie(self):
        article = self._session_cm.session.query(Movie).order_by(desc(Movie.rank)).first()
        return article

    def get_rank_of_previous_movie(self, movie):
        result = None
        prev = self._session_cm.session.query(Movie).filter(Movie.rank < movie.rank).order_by(desc(Movie.rank)).first()

        if prev is not None:
            result = prev.rank

        return result

    def get_rank_of_next_movie(self, movie):
        result = None
        next = self._session_cm.session.query(Movie).filter(Movie.rank > movie.rank).order_by(asc(Movie.rank)).first()

        if next is not None:
            result = next.rank

        return result

    def get_reviews(self):
        comments = self._session_cm.session.query(Review).all()
        return comments

    def add_review(self, review):
        super().add_comment(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()


def article_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            movie_data = row

            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]

            yield movie_data


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    insert_movies = """
        INSERT INTO movies (
        rank, title, genre,description, director,actors, year, runtime, rating, votes, revenue, metascore)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, article_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))

    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    #insert_reviews = """
    #   INSERT INTO reviews (
    #   id, user, movie, review, timestamp)
    #    VALUES (?, ?, ?, ?, ?)"""
    #cursor.executemany(insert_reviews, generic_generator(os.path.join(data_path, 'reviews.csv')))

    conn.commit()
    conn.close()
