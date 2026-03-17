## 1. Main Branch：Add-on Infrastructure（Docker Compose profiles）

- [x] 1.1 在 `main` branch 的 `docker-compose.yml` 加入 Redis add-on infrastructure（`redis:7-alpine`，port 6379，profile `redis`）— 實作 add-on infrastructure：docker compose profiles 決策
- [x] 1.2 在 `main` branch 的 `docker-compose.yml` 加入 MinIO add-on infrastructure（port 9000/9001，profile `minio`）— 使用 minio client library：miniopy-async
- [x] 1.3 在 `main` branch 的 `docker-compose.yml` 加入 LakeFS add-on infrastructure（port 8001，profile `lakefs`）
- [x] 1.4 更新 `main` branch 的 `.env.example`：加入 add-on environment variables in .env.example（全部 commented-out），包含 `REDIS_URL`、`MINIO_ENDPOINT`、`MINIO_ACCESS_KEY`、`MINIO_SECRET_KEY`、`LAKEFS_ENDPOINT`、`LAKEFS_ACCESS_KEY`、`LAKEFS_SECRET_KEY`

## 2. Main Branch：Add-on App-level Clients

- [x] 2.1 新增 `src/shared/redis.py`：實作 Redis app-level client，依 add-on 啟用機制：環境變數自動偵測（option a），`REDIS_URL` 未設定時 `redis_client` 保持 `None`，提供 `get_redis()` helper（未啟用時拋出 `RuntimeError`）
- [x] 2.2 新增 `src/shared/storage.py`：實作 MinIO app-level client（miniopy-async），透過 `MINIO_ENDPOINT` 環境變數自動偵測啟用，未設定時 `storage_client` 保持 `None`，並提供 `get_storage()` helper（未啟用時拋出 `RuntimeError`）
- [x] 2.3 新增 `src/shared/lakefs.py`：實作 LakeFS app-level client，透過 `LAKEFS_ENDPOINT` 環境變數自動偵測啟用，sync SDK 呼叫以 `asyncio.to_thread` 包裝，未設定時 `lakefs_client` 保持 `None`，並提供 `get_lakefs()` helper（未啟用時拋出 `RuntimeError`）
- [x] 2.4 更新 `pyproject.toml` 加入 add-on dependencies：`redis[asyncio]`、`miniopy-async`、`lakefs-sdk`
- [x] 2.5 更新 `src/main.py` lifespan：加入 add-on initialization in app lifespan，呼叫 `init_redis()`、`init_storage()`、`init_lakefs()`

## 3. Template/mariadb Branch：MariaDB branch availability

- [ ] 3.1 請通知使用者切換至 `template/mariadb` branch（或建立 branch）— 實作 database branch 策略：git branch 而非 cookiecutter/monorepo 決策
- [ ] 3.2 確認 `template/mariadb` branch-specific environment variables 已從 `main` rebase，包含所有 add-on 相關變更

## 4. Template/postgres Branch：PostgreSQL branch availability

- [ ] 4.1 請通知使用者切換至 `template/postgres` branch（或建立 branch）
- [ ] 4.2 更新 `docker-compose.yml`：將 MariaDB service 替換為 PostgreSQL service，更新 DbGate engine 設定
- [ ] 4.3 更新 `pyproject.toml`：將 `aiomysql` 替換為 `asyncpg`（postgresql driver：asyncpg 決策）
- [ ] 4.4 更新 `.env.example`：填入 branch-specific environment variables（`POSTGRES_USER`、`POSTGRES_PASSWORD`、`POSTGRES_DB`，`DB_URL` 使用 `postgresql+asyncpg://` scheme）
- [ ] 4.5 確認 `src/shared/database.py` 的 SQLite fallback preserved on SQL branches（`DB_URL` 未設定時退回 `sqlite+aiosqlite:///:memory:`）

## 5. Template/mongo Branch：MongoDB branch availability

- [ ] 5.1 請通知使用者切換至 `template/mongo` branch（或建立 branch）
- [ ] 5.2 更新 `docker-compose.yml`：將 MariaDB service 替換為 MongoDB service，更新 DbGate engine 設定（DbGate 支援 MongoDB）
- [ ] 5.3 更新 `pyproject.toml`：移除 `aiomysql`、`sqlmodel`、`sqlalchemy`，加入 `motor`、`beanie`（mongodb orm：beanie + motor 決策，MongoDB branch has no SQLModel dependency）
- [ ] 5.4 完全重寫 `src/shared/database.py`：改用 Motor + Beanie，`init_db()` 呼叫 `beanie.init_beanie()`（MongoDB branch initializes with Beanie）
- [ ] 5.5 更新 `.env.example`：填入 mongo branch-specific environment variables（`MONGO_URL`、`MONGO_DB`，移除 `DB_URL`）
- [ ] 5.6 更新 `src/main.py`：調整 import 以使用新的 `init_db()` 介面

## 6. 驗證

- [ ] 6.1 在 `main`/`template/mariadb` 執行 `docker compose up` 確認 MariaDB branch availability 正常
- [ ] 6.2 在 `main`/`template/mariadb` 執行 `docker compose --profile redis --profile minio --profile lakefs up` 確認所有 add-on services 啟動
- [ ] 6.3 在 `template/postgres` 執行 `docker compose up` 確認 PostgreSQL branch availability 正常連線
- [ ] 6.4 在 `template/mongo` 執行 `docker compose up` 確認 MongoDB branch availability 正常連線
- [ ] 6.5 執行 `pytest` 確認現有測試在各 branch 均通過（SQL branches 使用 SQLite fallback preserved on SQL branches）
