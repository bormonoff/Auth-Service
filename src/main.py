import contextlib

import uvicorn
from fastapi import FastAPI

from api.v1 import auth, personal, roles
from core.config import get_settings
from db.prepare_db import create_database, redis_shutdown, redis_startup


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
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
    tags=["Authentication service."]
)
app.include_router(
    personal.router,
    prefix=get_settings().URL_PREFIX + "/profile",
    tags=["Personal account."],
)
app.include_router(roles.router, prefix=get_settings().URL_PREFIX + "/roles")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=get_settings().AUTH_FASTAPI_PORT)
