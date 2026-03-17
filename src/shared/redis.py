import os
from redis.asyncio import Redis

import logging

logger = logging.getLogger("uvicorn.error")

_redis_url = os.getenv("REDIS_URL")

redis_client: Redis | None = None


async def init_redis() -> None:
    """
    初始化 Redis 連線。

    透過 REDIS_URL 環境變數自動偵測是否啟用。
    未設定時靜默跳過，redis_client 保持 None。

    範例:
        >>> @asynccontextmanager
        >>> async def lifespan(app: FastAPI):
        >>>     await init_redis()
        >>>     yield
    """
    if not _redis_url:
        return
    global redis_client
    redis_client = Redis.from_url(_redis_url, decode_responses=True)
    logger.info(f"[REDIS] connected: {_redis_url}")


async def close_redis() -> None:
    """關閉 Redis 連線（在 app shutdown 時呼叫）。"""
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None


def get_redis() -> Redis:
    """
    取得 Redis client。

    Returns:
        Redis: 已連線的 Redis client。

    Raises:
        RuntimeError: 若 REDIS_URL 未設定（Redis 未啟用）。
    """
    if redis_client is None:
        raise RuntimeError(
            "Redis is not enabled. Set REDIS_URL environment variable "
            "and run with `docker compose --profile redis up`."
        )
    return redis_client
