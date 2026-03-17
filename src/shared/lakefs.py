import asyncio
import os
from typing import Any

import logging

logger = logging.getLogger("uvicorn.error")

_lakefs_endpoint = os.getenv("LAKEFS_ENDPOINT")
_lakefs_access_key = os.getenv("LAKEFS_ACCESS_KEY", "")
_lakefs_secret_key = os.getenv("LAKEFS_SECRET_KEY", "")

lakefs_client: Any | None = None


async def init_lakefs() -> None:
    """
    初始化 LakeFS 連線。

    透過 LAKEFS_ENDPOINT 環境變數自動偵測是否啟用。
    未設定時靜默跳過，lakefs_client 保持 None。
    由於官方 SDK 僅有 sync 版本，透過 asyncio.to_thread 包裝呼叫。

    範例:
        >>> @asynccontextmanager
        >>> async def lifespan(app: FastAPI):
        >>>     await init_lakefs()
        >>>     yield
    """
    if not _lakefs_endpoint:
        return
    global lakefs_client

    def _create_client() -> Any:
        import lakefs_sdk
        configuration = lakefs_sdk.Configuration(
            host=_lakefs_endpoint,
            username=_lakefs_access_key,
            password=_lakefs_secret_key,
        )
        return lakefs_sdk.ApiClient(configuration)

    lakefs_client = await asyncio.to_thread(_create_client)
    logger.info(f"[LAKEFS] connected: {_lakefs_endpoint}")


def get_lakefs() -> Any:
    """
    取得 LakeFS ApiClient。

    Returns:
        lakefs_sdk.ApiClient: 已設定的 LakeFS client。

    Raises:
        RuntimeError: 若 LAKEFS_ENDPOINT 未設定（LakeFS 未啟用）。
    """
    if lakefs_client is None:
        raise RuntimeError(
            "LakeFS is not enabled. Set LAKEFS_ENDPOINT environment variable "
            "and run with `docker compose --profile lakefs up`."
        )
    return lakefs_client
