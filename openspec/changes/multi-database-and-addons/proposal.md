## Why

目前 FastAPI 專案模板僅支援 MariaDB，限制了使用者在不同專案情境下的選擇彈性。透過提供 MariaDB、PostgreSQL、MongoDB 三種資料庫分支，以及 Redis、MinIO、LakeFS 可選附加服務，讓模板適用更廣泛的後端開發情境。

## What Changes

- 新增 `template/postgres` git branch：以 PostgreSQL 取代 MariaDB（更換 driver、docker-compose service、環境變數）
- 新增 `template/mongo` git branch：以 MongoDB + Beanie/Motor 取代 SQLModel/SQLAlchemy 整套 ORM
- `template/mariadb` branch：從 main rebase，作為 MariaDB 的明確分支
- 在所有 branch 的 `docker-compose.yml` 加入 Redis、MinIO、LakeFS 可選服務（使用 Docker Compose `profiles`）
- 新增 `src/shared/redis.py`、`src/shared/storage.py`、`src/shared/lakefs.py`：透過環境變數自動偵測是否啟用（未設定時 client 為 `None`，靜默跳過）
- 更新 `src/main.py` lifespan：統一呼叫各 add-on 的初始化函式

## Capabilities

### New Capabilities

- `database-variants`: 支援三種資料庫選擇，透過 git branch 管理（mariadb/postgres/mongo），每個 branch 提供對應的 driver、ORM、docker-compose service 及環境變數設定
- `optional-addons`: 可選附加服務（Redis、MinIO、LakeFS）透過 Docker Compose profiles 管理 infrastructure，並在 `src/shared/` 提供對應的 async client，以環境變數自動偵測啟用

### Modified Capabilities

（無）

## Impact

- Affected code:
  - `docker-compose.yml`（新增 profiles services）
  - `.env.example`（新增 add-on 環境變數）
  - `pyproject.toml`（不同 branch 使用不同 driver 依賴）
  - `src/shared/database.py`（postgres branch 微調；mongo branch 完全重寫）
  - `src/shared/redis.py`（新增）
  - `src/shared/storage.py`（新增）
  - `src/shared/lakefs.py`（新增）
  - `src/main.py`（新增 add-on init 呼叫）
- Affected dependencies:
  - postgres branch：`aiomysql` → `asyncpg`
  - mongo branch：`aiomysql` + `sqlmodel` → `motor` + `beanie`
  - add-ons：`redis`、`miniopy-async`（或 `aiobotocore`）、`lakefs-sdk`
- Git branches affected: `main`, `template/mariadb`, `template/postgres`, `template/mongo`
