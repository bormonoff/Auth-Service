from fastapi import HTTPException, status


class UserInactiveException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has been deleted and now is inactive.",
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User hasn't been found.",
        )


class TokenNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token hasn't been found.",
        )


class UserHasBeenDeletedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has been deleted.",
        )


class DBException(HTTPException):
    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class RoleNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not exists"
        )


class AccessNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't have specified role",
        )


class InvalidUserOrPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong user or password.",
        )


class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is incorrect.",
        )


class ExpireToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid due to it's exp time.",
        )


class FingerprintExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This fingerprint already exists.",
        )


class FingerprintNotExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error. Fingerprint doesn't assosiate with the token.",
        )


class CommonExistsException(HTTPException):
    def __init__(self, info=""):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"DB Error - already exists. {info}",
        )


class UnAuthorizedException(HTTPException):
    def __init__(self, detail="", authenticate_value=""):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{detail}",
            headers={"WWW-Authenticate": authenticate_value},
        )
