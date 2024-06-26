import contextlib

import uvicorn
from fastapi import FastAPI
from fastapi.params import Security

from api.v1 import access, auth, personal, roles
from core.config import get_settings
from db.prepare_db import redis_shutdown, redis_startup
from util.JWT_helper import token_check


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_startup()
    yield
    await redis_shutdown()


app = FastAPI(
    lifespan=lifespan,
    title=get_settings().PROJECT_NAME,
    version=get_settings().VERSION,
    description=get_settings().DESCRIPTION,
    docs_url=get_settings().OPEN_API_DOCS_URL,
    openapi_url=get_settings().OPEN_API_URL,
)

app.include_router(
    auth.router,
    prefix=get_settings().URL_PREFIX + "/auth",
    tags=["Authentication service."],
)
app.include_router(
    personal.router,
    prefix=get_settings().URL_PREFIX + "/profile",
    tags=["Personal account."],
)
app.include_router(
    roles.router,
    prefix=get_settings().URL_PREFIX + "/roles",
    tags=["Roles"],
    dependencies=[Security(token_check, scopes=["auth_admin"])],
)
app.include_router(
    access.router,
    prefix=get_settings().URL_PREFIX + "/access",
    tags=["Access"],
    dependencies=[Security(token_check, scopes=["auth_admin"])],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=get_settings().AUTH_FASTAPI_PORT)
