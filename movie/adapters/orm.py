from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie.domain.movie import Movie
from movie.domain.actor import Actor
from movie.domain.genre import Genre
from movie.domain.director import Director
from movie.domain.user import User
from movie.domain.review import Review

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('article_id', ForeignKey('movies.rank')),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('rank', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director', String(255), nullable=False),
    Column('year', Integer, autoincrement=True),
    Column('runtime', Integer, autoincrement=True),
    Column('metascore', String(255), nullable=False),
    Column('rating', Integer, autoincrement=True),
    Column('genre', String(255), nullable=False),
    Column('actors', String(255), nullable=False),
    Column('votes', Integer),
    Column('revenue', Integer)


)


def map_model_to_tables():
    mapper(User, users, properties={
        '__username': users.c.username,
        '__password': users.c.password,
        '__comments': relationship(Review, backref='_user')
    })
    mapper(Review, reviews, properties={
        '_comment': reviews.c.comment,
        '_timestamp': reviews.c.timestamp
    })
    mapper(Movie, movies, properties={
        'rank': movies.c.rank,
        'title': movies.c.title,
        'description': movies.c.description,
        'director': movies.c.director,
        'year': movies.c.year,
        'runtime_minutes': movies.c.runtime,
        'metascore': movies.c.metascore,
        'rating': movies.c.rating,
        'reviews': relationship(Review, backref='_movie')
    })




