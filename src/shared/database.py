import os
from typing import Type

import motor.motor_asyncio
from beanie import Document, init_beanie

import logging

logger = logging.getLogger("uvicorn.error")

# 1. 建立 MongoDB client
_mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
_mongo_db = os.getenv("MONGO_DB", "db")

client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(_mongo_url)
database = client[_mongo_db]


# 2. 定義初始化 DB 的函式 (通常在 app startup 時呼叫)
async def init_db(document_models: list[Type[Document]] | None = None) -> None:
    """
    初始化 MongoDB 連線與 Beanie ODM。

    這通常在應用程式啟動時呼叫。需傳入所有 Document model 清單。

    Args:
        document_models: 要初始化的 Beanie Document model 清單。

    範例:
        >>> from contextlib import asynccontextmanager
        >>> from fastapi import FastAPI
        >>> from myapp.models import User, Item
        >>>
        >>> @asynccontextmanager
        >>> async def lifespan(app: FastAPI):
        >>>     await init_db(document_models=[User, Item])
        >>>     yield
        >>>
        >>> app = FastAPI(lifespan=lifespan)
    """
    logger.info(f"[DATABASE INFO] MongoDB url: {_mongo_url}, db: {_mongo_db}")
    await init_beanie(
        database=database,
        document_models=document_models or [],
    )


# 3. Beanie Document 使用方式
# 定義 model 時繼承 beanie.Document 取代 sqlmodel.SQLModel：
#
# from beanie import Document
#
# class User(Document):
#     name: str
#     email: str
#
#     class Settings:
#         name = "users"  # MongoDB collection name
#
# 在 router 中直接使用 Document 的 async 方法，不需要 session：
#
# @app.get("/users/")
# async def read_users():
#     return await User.find_all().to_list()
