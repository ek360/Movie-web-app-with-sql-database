import csv


from movie.domain.movie import Movie
from movie.domain.actor import Actor
from movie.domain.genre import Genre
from movie.domain.director import Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = []
        self.__dataset_of_actors = []
        self.__dataset_of_directors = []
        self.__dataset_of_genres = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])

                self.__dataset_of_movies += [Movie(title, release_year)]

                for act in row['Actors'].split(","):  # csv file split by commas
                    if Actor(act) not in self.__dataset_of_actors:
                        self.__dataset_of_actors += [Actor(act)]

                if Director(row["Director"]) not in self.__dataset_of_directors:
                    self.__dataset_of_directors += [Director(row["Director"])]

                for gen in row['Genre'].split(","):  # csv file split by commas
                    if Genre(gen) not in self.__dataset_of_genres:
                        self.__dataset_of_genres += [Genre(gen)]

                index += 1

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres
