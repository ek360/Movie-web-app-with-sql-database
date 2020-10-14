import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from movie.adapters.repository import AbstractRepository, RepositoryException
from movie.domain.movie import Movie
from movie.domain.actor import Actor
from movie.domain.genre import Genre
from movie.domain.director import Director
from movie.domain.user import User
from movie.domain.review import Review, make_review


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__dataset_of_movies = []
        self.__dataset_of_actors = []
        self.__dataset_of_directors = []
        self.__dataset_of_genres = []
        self.__dataset_of_movies_rank = dict()
        self.__users = []
        self.__reviews = []

    def add_actor(self, actor: Actor):
        self.__dataset_of_actors.append(actor)

    def get_actor(self, actor) -> Actor:
        return next((actor_holder for actor_holder in self.__dataset_of_actors if actor_holder.actor == actor), None)

    def add_director(self, director: Director):
        self.__dataset_of_directors.append(director)

    def get_director(self, director) -> Director:
        return next((director_holder for director_holder in self.__dataset_of_directors if
                     director_holder.director == director), None)

    def add_genre(self, genre: Genre):
        self.__dataset_of_genres.append(genre)

    def get_genre(self, genre) -> Genre:
        return next((genre_holder for genre_holder in self.__dataset_of_genres if genre_holder.genre == genre), None)

    def add_movie(self, movie: Movie):
        self.__dataset_of_movies += [movie]
        self.__dataset_of_movies_rank[movie.rank] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self.__dataset_of_movies_rank[id]
        except KeyError:
            pass

        return movie

    def get_first_movie(self):
        movie = None

        if len(self.__dataset_of_movies) > 0:
            movie = self.__dataset_of_movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self.__dataset_of_movies) > 0:
            movie = self.__dataset_of_movies[-1]
        return movie

    def get_movie_by_rank(self, target_rank):
        if target_rank > len(self.__dataset_of_movies):
            raise KeyError
        return [self.__dataset_of_movies_rank[target_rank]]

    def get_rank_of_previous_movie(self, movie):
        previous_rank = None

        try:
            if movie.rank - 1 > 0:
                previous_rank = movie.rank - 1
        except ValueError:
            pass

        return previous_rank

    def get_rank_of_next_movie(self, movie):
        next_rank = None

        try:
            if movie.rank + 1 <= len(self.__dataset_of_movies):
                next_rank = movie.rank + 1
        except ValueError:
            pass

        return next_rank

    def add_user(self, user):
        self.__users.append(user)

    def get_user(self, username):
        return next((user for user in self.__users if user.user_name == username), None)

    def movies_rank(self, movie):
        ranking = bisect_left(self.__dataset_of_movies, movie)
        if ranking != len(self.__dataset_of_movies) and self.__dataset_of_movies[ranking].rank == movie.rank:
            return ranking
        raise ValueError

    def add_review(self, review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def get_number_of_movies(self):
        return len(self.__dataset_of_movies)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        headers = next(reader)

        for row in reader:
            row = [item.strip() for item in row]
            yield row


def load_movies(data_path: str, repo: MemoryRepository):
    for data_row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        movie_rank = int(data_row[0])

        movie = Movie(
            rank=movie_rank,
            title=data_row[1],
            year=int(data_row[6]),
            description=data_row[3],
            director=data_row[4],
            runtime_minutes=int(data_row[7]),
            rating=float(data_row[8]),
            metascore=data_row[11]
        )
        # add genre and actors later maybe.
        repo.add_movie(movie)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()
    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user

    return users

def load_reviews(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat((data_row[4]))
        )
    repo.add_review(review)


def populate(data_path, repo):
    load_movies(data_path, repo)
    users = load_users(data_path, repo)
    load_reviews(data_path, repo, users)
