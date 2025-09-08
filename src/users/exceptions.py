from fastapi import HTTPException, status


class UserAlreadyExistsHTTPException(HTTPException):
    def __init__(self, details: str = ""):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bad request. {details}.",
        )


class WrongCredentialsOrUserNotFoundHTTPException(HTTPException):
    def __init__(self, details: str = ""):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"FORBIDDEN. {details}.",
        )
