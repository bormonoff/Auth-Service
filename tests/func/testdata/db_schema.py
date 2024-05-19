TABLES_SCHEMA = [
    {
        "table": "public.user",
        "data": """CREATE TABLE IF NOT EXISTS "user" (
            id UUID NOT NULL,
            login VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            modified_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            is_active BOOLEAN NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (id),
            UNIQUE (login),
            UNIQUE (email)
            )""",
    },
    {
        "table": "fingerprint",
        "data": """CREATE TABLE IF NOT EXISTS fingerprint (
            id UUID NOT NULL,
            user_id UUID NOT NULL,
            fingerprint VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            modified_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (id),
            FOREIGN KEY(user_id) REFERENCES "user" (id)
            )""",
    },
    {
        "table": "role",
        "data": """CREATE TABLE IF NOT EXISTS role (
            id UUID NOT NULL,
            title VARCHAR(50) NOT NULL,
            description VARCHAR(50),
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            modified_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (id),
            UNIQUE (title)
        )""",
    },
    {
        "table": "user_role",
        "data": """CREATE TABLE IF NOT EXISTS user_role (
            id UUID NOT NULL,
            user_id UUID NOT NULL,
            role_id UUID NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            PRIMARY KEY (id),
            CONSTRAINT unique_role_for_user UNIQUE (user_id, role_id),
            UNIQUE (id),
            FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE,
            FOREIGN KEY(role_id) REFERENCES role (id) ON DELETE CASCADE
            )""",
    },
    {
        "table": "token",
        "data": """CREATE TABLE IF NOT EXISTS token (
            id UUID NOT NULL,
            user_id UUID NOT NULL,
            refresh_token VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (id),
            FOREIGN KEY(user_id) REFERENCES "user" (id),
            UNIQUE (refresh_token)
            )""",
    },
]

USER_CREATION = [
    """INSERT INTO "user" (
        id,
        login,
        email,hashed_password,
        first_name,
        last_name,
        created_at,
        modified_at,
        is_active
    )
    VALUES (
        '8afd98c5-a349-4904-b5a8-403e61517999',
        'login',
        'example@email.com',
        '$argon2id$v=19$m=65536,t=3,p=4$uCOdRliaIxLn0RcxehobrA$BaRe4kIfbhHuFBtvGPGIfIHzcivYnMrGElhcSWqdVxY',
        'name',
        'password',
        '2024-04-26 17:26:11.42932',
        '2024-04-26 17:26:11.429322',
        'true'
    );
""",
    """INSERT INTO "user" (id,
                         login,
                         email,hashed_password,
                         first_name,
                         last_name,
                         created_at,
                         modified_at,
                         is_active)
    VALUES ('11111111-1111-1111-1111-111111111111',
            'superuser',
            'super@user.com',
            '$argon2id$v=19$m=65536,t=3,p=4$Ob48V4Gse3I38Og+6/YyCg$QiY5iKBfmowKgSTduOME5e60r75QyojaE+cSQxn8/74',
            'superuser',
            'superuser',
            '2024-04-26 17:26:11.42932',
            '2024-04-26 17:26:11.429322',
            'true');
""",
]
