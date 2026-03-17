from contextlib import asynccontextmanager
from fastapi import FastAPI
from shared import init_db
from shared.sessions import SessionMiddleware
from shared.redis import init_redis, close_redis
from shared.storage import init_storage
from shared.lakefs import init_lakefs
import os
import secrets

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    await init_storage()
    await init_lakefs()
    yield
    await close_redis()

app = FastAPI(lifespan=lifespan)

# Set session middleware
## Detect session secret key is set.
SESSION_SECRET=os.getenv("SESSION_SECRET")
if not SESSION_SECRET:
    SESSION_SECRET = secrets.token_hex(32)

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

@app.get("/")
async def root():
    return { "message": "root page" }