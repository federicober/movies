from fastapi import status


class MoviesException(Exception):
    """Generic exception raised by the API"""


class NotFoundException(MoviesException):
    pass


class UserNotFound(NotFoundException):
    pass


class IncorrectUserOrPassword(UserNotFound):
    pass


class AlreadyExists(MoviesException):
    pass


class UserAlreadyExists(AlreadyExists):
    pass


class MovieAlreadyExists(AlreadyExists):
    pass
