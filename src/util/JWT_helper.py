import base64
import json
from datetime import datetime, timezone
from functools import lru_cache

from Cryptodome.Hash import HMAC, SHA256
from pydantic import BaseModel

from core.config import get_settings
from core.exceptions import ExpireToken
from schemas.token import TokenPayload


class JWTHelper:
    """JWTHelper provides methods to encode, decode and verify the token."""
    def __init__(self):
        self.encoding = get_settings().JWT_CODE
        self.key = get_settings().JWT_SECRET.encode(self.encoding)

    async def encode(self, header: BaseModel, payload: BaseModel) -> str:
        """Basic encode function.

        Gets the header and payload pydantic objects and returns a JWT token."""
        hasher = HMAC.new(self.key, digestmod=SHA256)

        encode_header = await self.encode_basemodel(header)
        encode_payload = await self.encode_basemodel(payload)

        combined_str = f"{encode_header.decode(self.encoding)}.{encode_payload.decode("utf-8")}"

        hasher.update(combined_str.encode(self.encoding))
        digest = hasher.hexdigest()

        return f"{combined_str}.{digest}"

    async def decode_payload(self, token: str) -> TokenPayload:
        """Gets a token and return string with it's payload data."""
        token_parts = token.split(".")
        decoded_str = base64.b64decode(token_parts[1]).decode(self.encoding)
        payload = TokenPayload(**(json.loads(decoded_str.replace("'", "\""))))
        self.verify_exp_time(payload=payload)
        return payload

    async def verify_token(self, token: str) -> None:
        """Gets a token string and verifies it."""
        hasher = HMAC.new(self.key, digestmod=SHA256)

        token_parts = token.split(".")
        payload = f"{token_parts[0]}.{token_parts[1]}"
        hasher.update(payload.encode(self.encoding))
        hasher.hexverify(token_parts[2])

    async def verify_exp_time(self, payload: BaseModel) -> None:
        """Helper verifies payload exp time."""
        now = datetime.now(timezone.utc).timestamp()
        if float(payload.exp) < now:
            raise ExpireToken

    async def encode_basemodel(self, model: BaseModel) -> str:
        """Helper incapsulates pydantic serialization logic."""
        serialized_str = str(model.model_dump())
        return base64.b64encode(serialized_str.encode(self.encoding))


@lru_cache()
def get_jwt_helper() -> JWTHelper:
    return JWTHelper()


