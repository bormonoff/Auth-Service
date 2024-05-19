USER_DATA = [
    (
        {
            "login": "login",
            "email": "user@example.com",
            "first_name": "name",
            "last_name": "surname",
            "password": "password",
        }
    ),
    (
        {
            "login": "login2",
            "email": "user@example2.com",
            "first_name": "name",
            "last_name": "surname",
            "password": "password",
        }
    ),
]

INVALID_USER_LOGIN_DATA = [
    (
        {
            "login": "lo",
            "email": "user@example.com",
            "first_name": "name",
            "last_name": "surname",
            "password": "password",
        }
    ),
    (
        {
            "login": "login51length______________________________________",
            "email": "user@example2.com",
            "first_name": "name",
            "last_name": "surname",
            "password": "password",
        }
    ),
]

INVALID_USER_NAME = [
    (
        {
            "login": "login",
            "email": "user@example.com",
            "first_name": "na",
            "last_name": "surname",
            "password": "password",
        }
    )
]

INVALID_USER_SURNAME = [
    (
        {
            "login": "login",
            "email": "user@example.com",
            "first_name": "name",
            "last_name": "su",
            "password": "password",
        }
    )
]

SUPERUSER_DATA = {
    "login": "superuser",
    "email": "super@user.com",
    "first_name": "superuser",
    "last_name": "superuser",
    "password": "superuser",
}

NEW_USER_DATA = {
    "login": "new_user_login",
    "email": "new_user@email.com",
    "first_name": "new_user_name",
    "last_name": "new_user_surname",
    "password": "new_password",
}
