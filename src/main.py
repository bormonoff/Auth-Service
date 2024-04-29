import contextlib

import uvicorn
from fastapi import FastAPI

from api.v1 import auth, roles, users
from db import postgres


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    postgres.startup
    yield

app = FastAPI()

app.include_router(users.router, prefix="/api/v1/auth")
app.include_router(auth.router, prefix="/api/v1/users")
app.include_router(roles.router, prefix="/api/v1/roles")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
