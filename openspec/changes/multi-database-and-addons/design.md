## Context

目前模板以單一 git branch 提供 MariaDB + SQLModel/SQLAlchemy async 的組合。`src/shared/database.py` 使用 `DB_URL` 環境變數建立 engine，並在偵測到 `sqlite` 時自動切換為 in-memory fallback（測試用）。docker-compose 包含 MariaDB service 與 DbGate（web DB 管理工具）。

需要在不破壞現有 MariaDB 主線的前提下，提供 PostgreSQL 與 MongoDB 兩條替代路線，並在所有路線上加入 Redis、MinIO、LakeFS 可選服務。

## Goals / Non-Goals

**Goals:**

- 維護三個 git branch，分別對應 MariaDB、PostgreSQL、MongoDB
- 每個 branch 提供完整可運行的 docker-compose + app 程式碼
- 所有 branch 統一支援 Redis、MinIO、LakeFS 可選 add-ons
- Add-on 啟用方式：設定對應環境變數，無需改動程式碼

**Non-Goals:**

- 在同一個 branch 內同時支援多種資料庫的執行期切換
- 提供資料庫遷移工具（Alembic 等）
- 自動化 branch 同步腳本

## Decisions

### Database branch 策略：git branch 而非 cookiecutter/monorepo

**決定**：使用獨立 git branch（`template/mariadb`、`template/postgres`、`template/mongo`）而非 cookiecutter template generator 或 monorepo 子目錄。

**理由**：branch 策略最符合「clone 後立即可用」的使用情境；postgres branch 差異極小（只換 driver），用 cookiecutter 反而過度設計；mongo branch 雖差異大，但使用者預期直接 clone 特定 branch，不需要 generator 介入。

**替代方案**：cookiecutter/copier — 需要額外工具依賴，增加使用門檻，排除。

---

### PostgreSQL driver：asyncpg

**決定**：postgres branch 使用 `asyncpg` 取代 `aiomysql`。

**理由**：`asyncpg` 是 PostgreSQL 最主流的 async driver，SQLAlchemy/SQLModel 官方推薦搭配方式。`database.py` 僅需更新 `DB_URL` 格式（`postgresql+asyncpg://...`），其餘邏輯不變。

---

### MongoDB ORM：Beanie + Motor

**決定**：mongo branch 使用 `beanie`（ODM）+ `motor`（async driver），移除 `sqlmodel`、`sqlalchemy`、`aiomysql`。

**理由**：Beanie 是目前最成熟的 async MongoDB ODM，API 風格與 SQLModel 相似（`Document` 類似 `SQLModel`），學習曲線平緩。Motor 為 Beanie 底層 driver，官方推薦組合。

**替代方案**：直接使用 Motor 不加 ODM — 過於底層，不適合 starter template。

**影響**：`src/shared/database.py` 完全重寫；`pyproject.toml` dependencies 完全替換；`init_db()` 改為 `await init_beanie(database=db, document_models=[...])`。

---

### Add-on 啟用機制：環境變數自動偵測（Option A）

**決定**：add-on client（Redis、MinIO、LakeFS）在 module 載入時讀取對應環境變數，未設定時 client 保持 `None`；`main.py` lifespan 統一呼叫各 `init_*()` 函式，有設定才真正連線。

**理由**：與現有 `database.py` 的 fallback pattern 一致；使用者不需修改任何程式碼，只需設定 env var 並啟動對應 Docker Compose profile。

```python
# src/shared/redis.py 範例
_redis_url = os.getenv("REDIS_URL")
redis_client: Redis | None = None

async def init_redis() -> None:
    if not _redis_url:
        return
    global redis_client
    redis_client = Redis.from_url(_redis_url)
```

---

### Add-on infrastructure：Docker Compose profiles

**決定**：Redis、MinIO、LakeFS 以 Docker Compose `profiles` 管理，主 services（app + DB）不需 profile。

**理由**：原生 Docker Compose 功能，無需額外腳本；使用方式直覺（`docker compose --profile redis up`）；與 app 層解耦，即使不用 Docker 也能獨立啟動 add-on。

---

### MinIO client library：miniopy-async

**決定**：MinIO add-on 使用 `miniopy-async`（MinIO 官方 Python SDK 的 async 封裝）。

**理由**：官方支援、API 與 MinIO 文件對齊；`aiobotocore` 雖然更通用（S3 compatible），但複雜度較高，不適合入門模板。

## Risks / Trade-offs

- **[Risk] mongo branch 維護成本高** → 因為底層 ORM 完全不同，`template/mongo` 與 `main` 差異最大，rebase 時衝突較多。Mitigation：`template/mongo` 只 rebase 非 DB 相關的異動（middleware、config 等），DB 相關部分需手動整合。
- **[Risk] add-on env var 設定錯誤時靜默失敗** → client 保持 `None`，使用端若未做 null check 會出現 `AttributeError`。Mitigation：各 shared module 提供 `get_redis()` 等 helper，未啟用時拋出明確的 `RuntimeError`。
- **[Trade-off] branch 分散 vs 單一 repo** → 使用者需要知道選哪個 branch，README 需清楚說明。

## Migration Plan

此為全新 branch 建立，不涉及現有資料遷移。部署順序：

1. 確認 `main` branch 穩定
2. 建立 `template/mariadb`（rebase from main）
3. 在 `main` 加入 add-on files（docker-compose profiles + shared clients）
4. 建立 `template/postgres`（from main，換 driver）
5. 建立 `template/mongo`（from main，換 ORM）
6. 更新 README 說明 branch 選擇方式

## Open Questions

- LakeFS client：使用官方 `lakefs-sdk` 還是直接 `httpx` 呼叫 REST API？（`lakefs-sdk` 目前僅有 sync 版本，可能需要 `asyncio.to_thread` 包裝）
- DbGate 在 mongo branch 是否保留？（DbGate 支援 MongoDB，可保留並更換 engine 設定）
