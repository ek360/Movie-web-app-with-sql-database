class Genre:

    def __init__(self, genre_n: str):
        if genre_n == "" or type(genre_n) is not str:
            self.__genre_n= None
        else:
            self.__genre_n = genre_n.strip()

    def __repr__(self):
        return f"<Genre {self.__genre_n}>"

    def __eq__(self, other):
        return self.__genre_n == other.__genre_n

    def __lt__(self, other):
        if self.__genre_n < other.__genre_n:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__genre_n)
  
