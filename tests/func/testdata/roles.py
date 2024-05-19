from http import HTTPStatus

INSERT_ROLE_DB = [
    """INSERT INTO public.role (id,
                         title,
                         description,
                         created_at,
                         modified_at)
    VALUES ('11111111-1111-1111-1111-111111111111',
            'auth_admin',
            'test auth_admin description',
            '2024-04-26 17:26:11.42932',
            '2024-04-26 17:26:11.429322');
""",
    """INSERT INTO public.role (id,
                         title,
                         description,
                         created_at,
                         modified_at)
    VALUES ('22222222-2222-2222-2222-222222222222',
            'subscriber',
            'test subscriber description',
            '2024-04-26 17:26:11.42932',
            '2024-04-26 17:26:11.429322');
""",
]

GET_ROLE = [
    {
        "role_title": "auth_admin",
        "result": HTTPStatus.OK,
        "body": {
            "title": "auth_admin",
            "description": "test auth_admin description",
        },
    },
    {
        "role_title": "1",
        "result": HTTPStatus.UNPROCESSABLE_ENTITY,
    },
    {
        "role_title": "qwerty",
        "result": HTTPStatus.NOT_FOUND,
    },
]

DELETE_ROLE = [
    {
        "role_title": "auth_admin",
        "result": HTTPStatus.OK,
    },
    {
        "role_title": "1",
        "result": HTTPStatus.UNPROCESSABLE_ENTITY,
    },
    {
        "role_title": "qwerty",
        "result": HTTPStatus.NOT_FOUND,
    },
]

CREATE_ROLE = [
    {
        "title": "somo_role",
        "description": "some description",
    },
    {
        "title": "some_role2",
        "description": "some description",
    },
]


UPDATE_ROLE = [
    {
        "role_title": "auth_admin",
        "update_data": {
            "title": "updated_auth_admin",
        },
        "result": {
            "status": HTTPStatus.OK,
            "body": {
                "title": "updated_auth_admin",
                "description": "test auth_admin description",
            },
        },
    },
    {
        "role_title": "subscriber",
        "update_data": {
            "title": "updated_subscriber",
            "description": "updated test subscriber description",
        },
        "result": {
            "status": HTTPStatus.OK,
            "body": {
                "title": "updated_subscriber",
                "description": "updated test subscriber description",
            },
        },
    },
    {
        "role_title": "some_not_existing_role",
        "update_data": {
            "title": "some_not_existing_role",
        },
        "result": {
            "status": HTTPStatus.NOT_FOUND,
        },
    },
    {
        "role_title": "auth_admin",
        "update_data": {
            "title": "role title with spaces",
        },
        "result": {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    },
    {
        "role_title": "subscriber",
        "update_data": {
            "id": "21111111-1111-1111-1111-111111111111",
        },
        "result": {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    },
    {
        "role_title": "auth_admin",
        "update_data": {
            "title": "",
            "description": "",
        },
        "result": {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    },
    {
        "role_title": "auth_admin",
        "update_data": {
            "title": "auth_admin",
        },
        "result": {
            "status": HTTPStatus.UNPROCESSABLE_ENTITY,
        },
    },
]


INVALID_ROLE = {
    "title": "so",
    "description": "some description",
}
