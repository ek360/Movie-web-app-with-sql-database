from datetime import datetime

from movie.domain.user import User


class Review:
    def __init__(self, user, movie, review, timestamp):
        self.__user: User = user
        self.__movie = movie
        self.__review: Review = review
        self.__timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self.__user

    @property
    def movie(self):
        return self.__movie

    @property
    def review(self) -> str:
        return self.__review

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return other.__user == self.__user and other.__movie == self.__movie and other.__review == self.__review and other.__timestamp == self.__timestamp


def make_review(review_text, user, movie, timestamp: datetime = datetime.today()):
    review = Review(user, movie, review_text, timestamp)
    user.add_review(review)
    movie.add_review(review)
    return review

