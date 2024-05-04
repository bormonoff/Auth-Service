import base64
import binascii
from functools import lru_cache

from Cryptodome.Hash import HMAC, SHA256
from pydantic import BaseModel

from core.config import get_settings


class JWTHelper:
    def __init__(self):
        self.key = get_settings().JWT_SECRET.encode("utf-8")
        self.hasher = HMAC.new(self.key, digestmod=SHA256)

    async def encode(self, header: BaseModel, payload: BaseModel):
        header_str = str(header.model_dump())
        encode_header = base64.b64encode(header_str.encode("utf-8"))

        payload_str = str(payload.model_dump())
        encode_payload = base64.b64encode(payload_str.encode("utf-8"))

        combined_str = f"{encode_header.decode("utf-8")}.{encode_payload.decode("utf-8")}"
        self.hasher.update(combined_str.encode("utf-8"))
        digest = self.hasher.digest()
        hex_digest = binascii.hexlify(digest).decode("utf-8")

        return f"{combined_str}.{hex_digest}"

@lru_cache()
async def get_jwt_helper() -> JWTHelper:
    return JWTHelper()



