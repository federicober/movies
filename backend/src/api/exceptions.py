from fastapi import status


class ApiException(Exception):
    """Generic exception raised by the API"""


class NotFoundException(ApiException):
    """Will trigger a 404 exception in the API"""

    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "Resource not found"


class UserNotFound(NotFoundException):
    def __init__(self, user_id_or_username: int | str) -> None:
        super().__init__(user_id_or_username)
        self.message = f"User {user_id_or_username} not found"
