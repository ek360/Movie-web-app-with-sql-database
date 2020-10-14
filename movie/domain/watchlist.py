from domainmodel.movie import Movie

class WatchList:

    def __init__(self):
        self.__watch_list = []

    def add_movie(self,movie):
        if type(movie) is Movie:
            if movie not in self.__watch_list:
                self.__watch_list += [movie]

    def remove_movie(self,movie):
        if movie in self.__watch_list:
            self.__watch_list.remove(movie)

    def select_movie_to_watch(self,index):
        if index >= len(self.__watch_list) or index <= -1:
            return None
        else:
            return self.__watch_list[index]

    def size(self):
        return len(self.__watch_list)

    def first_movie_in_watchlist(self):
        if len(self.__watch_list) != 0:
            return self.__watch_list[0]
        else:
            return None

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        if self.i >= len(self.__watch_list)-1:
            raise StopIteration
        self.i += 1
        return self.__watch_list[self.i]


