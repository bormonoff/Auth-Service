import base64
import json

from Cryptodome.Hash import HMAC, SHA256
from settings import get_settings


async def decode_payload_helper(payload: str) -> str:
    decoded_str = base64.b64decode(payload).decode(get_settings().JWT_CODE)
    payload = json.loads(decoded_str.replace("'", '"'))
    return payload

async def generate_sign_helper(token_parts: list[str]) -> str:
    hasher = HMAC.new(get_settings().JWT_SECRET.encode(get_settings().JWT_CODE),
                      digestmod=SHA256)
    token_data = f"{token_parts[0]}.{token_parts[1]}"
    hasher.update(token_data.encode(get_settings().JWT_CODE))
    digest = hasher.hexdigest()
    return digest

