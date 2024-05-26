import pytest
from Cryptodome.Hash import HMAC, SHA256

from settings import get_settings
from testdata.common import HEADERS


@pytest.fixture(scope="function")
async def get_acess_token():
    """Creates an acess token for the superuser. This acess token expires in 2027."""
    hasher = HMAC.new(
        get_settings().JWT_SECRET.encode(get_settings().JWT_CODE),
        digestmod=SHA256,
    )

    token_without_sign = "eyd0eXAnOiAnSldUJywgJ2FsZyc6ICdIUzI1Nid9.eydzdWInOiAnc3VwZXJ1c2VyJywgJ2ZpbmdlcnByaW50JzogJzE5Njk1OTIyMTY0ODg4MzI1MjAnLCAncm9sZXMnOiBbJ2F1dGhfYWRtaW4nXSwgJ2V4cCc6ICcxODE0MjIxODQxLjk1NTIzJ30="
    hasher.update(token_without_sign.encode(get_settings().JWT_CODE))
    digest = hasher.hexdigest()

    return f"{token_without_sign}.{digest}"


@pytest.fixture(scope="function")
async def prepare_headers_with_superuser_token(get_acess_token):
    """Prepares superuser headers."""
    headers = HEADERS
    headers["Authorization"] = f"Bearer {get_acess_token}"

    return headers
