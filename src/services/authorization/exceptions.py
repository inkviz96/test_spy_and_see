from fastapi import HTTPException, status


class TokenHTTPException(HTTPException):
    def __init__(self, details: str = ""):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"FORBIDDEN. {details}.",
        )
