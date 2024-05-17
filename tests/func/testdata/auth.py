TOKENS = [
    {
        "type": "access_token",
        "payload_fields": [
            "sub",
            "fingerprint",
            "roles",
            "exp"
        ]
    },
    {
        "type": "refresh_token",
        "payload_fields": [
            "sub",
            "fingerprint",
            "exp"
        ]
    }
]

GET_REFRESH_TOKEN_REQUEST = """
    SELECT * FROM public.user
        JOIN public.refresh_token AS token
        ON token.user_id=public.user.id
        WHERE public.user.login='superuser'
"""

INSERT_SUPERUSER_FINGERPRINT_REQUEST = """
    INSERT INTO "fingerprint" (
        id,
        user_id,
        fingerprint,
        created_at,
        modified_at
        )
    VALUES (
        '8afd98c5-a349-4904-b5a8-403e61517999',
        '11111111-1111-1111-1111-111111111111',
        '1969592216488832520',
        '2024-04-26 17:26:11.42932',
        '2024-04-26 17:26:11.42932'
    );
"""

INSERT_SUPERUSER_REFRESH_TOKEN_REQUEST = """
    INSERT INTO "refresh_token" (
        id,
        user_id,
        fingerprint_id,
        refresh_token,
        created_at
        )
    VALUES (
        '8afd98c5-a349-4904-b5a8-403e61517999',
        '11111111-1111-1111-1111-111111111111',
        '8afd98c5-a349-4904-b5a8-403e61517999',
        'eyd0eXAnOiAnSldUJywgJ2FsZyc6ICdIUzI1Nid9.eydzdWInOiAnc3VwZXJ1c2VyJywgJ2ZpbmdlcnByaW50JzogJzkxMjA2MzA4OTg3NjYwNzMzNScsICdleHAnOiAnMTgxNTUwODAwNS42NTU4Myd9.7b6f957ab28921c15e543f79718cc08b1fe936abf8350c222e391327fba4731f',
        '2024-04-26 17:26:11.42932'
    );
"""