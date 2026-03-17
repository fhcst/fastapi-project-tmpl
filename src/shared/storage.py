import os
from miniopy_async import Minio

import logging

logger = logging.getLogger("uvicorn.error")

_minio_endpoint = os.getenv("MINIO_ENDPOINT")
_minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
_minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
_minio_secure = os.getenv("MINIO_SECURE", "false").lower() == "true"

storage_client: Minio | None = None


async def init_storage() -> None:
    """
    初始化 MinIO 連線。

    透過 MINIO_ENDPOINT 環境變數自動偵測是否啟用。
    未設定時靜默跳過，storage_client 保持 None。

    範例:
        >>> @asynccontextmanager
        >>> async def lifespan(app: FastAPI):
        >>>     await init_storage()
        >>>     yield
    """
    if not _minio_endpoint:
        return
    global storage_client
    storage_client = Minio(
        _minio_endpoint,
        access_key=_minio_access_key,
        secret_key=_minio_secret_key,
        secure=_minio_secure,
    )
    logger.info(f"[MINIO] connected: {_minio_endpoint}")


def get_storage() -> Minio:
    """
    取得 MinIO client。

    Returns:
        Minio: 已設定的 MinIO client。

    Raises:
        RuntimeError: 若 MINIO_ENDPOINT 未設定（MinIO 未啟用）。
    """
    if storage_client is None:
        raise RuntimeError(
            "MinIO is not enabled. Set MINIO_ENDPOINT environment variable "
            "and run with `docker compose --profile minio up`."
        )
    return storage_client
