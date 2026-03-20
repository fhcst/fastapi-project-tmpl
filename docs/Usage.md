# 使用說明 — 如何從這個 Template 開始你的 FastAPI 專案

本文件將帶你從「取得 template」到「新增你的第一個 API」，完成整個開發環境的建置。

---

## 目錄

1. [取得 Template](#1-取得-template)
2. [建置開發環境](#2-建置開發環境)
3. [驗證服務是否正常運作](#3-驗證服務是否正常運作)
4. [新增你的第一個 API Endpoint](#4-新增你的第一個-api-endpoint)

---

## 1. 取得 Template

### 1.1 Fork 此 Repository

> [!IMPORTANT]
> **Fork** 是把別人的 GitHub Repository 複製一份到你自己的帳號。這樣你就有一個屬於自己的版本，可以自由修改。

1. 前往本專案的 GitHub 頁面
2. 點擊右上角的 **Fork** 按鈕
3. 選擇你自己的 GitHub 帳號作為目的地
4. 等待 Fork 完成

### 1.2 Clone 到你的電腦

Fork 完成後，把你帳號下的 Repository 下載到本地端：

```bash
# 將 YOUR_USERNAME 替換成你的 GitHub 帳號名稱
# 將 YOUR_PROJECT 替換成你的 Repository 名稱
git clone https://github.com/YOUR_USERNAME/YOUR_PROJECT.git

# 進入專案目錄
cd YOUR_PROJECT
```

> [!TIP]
> 你也可以在 GitHub 頁面點擊綠色的 **Code** 按鈕，複製 URL 後再貼到 `git clone` 後面。

---

## 2. 建置開發環境

### 2.1 安裝 uv（套件管理器）

本專案使用 `uv` 來管理 Python 套件。如果你還沒安裝，請先執行：

**macOS / Linux：**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows（PowerShell）：**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安裝完成後，**重新開啟 Terminal**，再繼續下一步。

### 2.2 安裝 Python 套件

```bash
uv sync
```

這個指令會自動建立虛擬環境（Virtual Environment）並安裝所有必要的套件。

### 2.3 設定環境變數

環境變數用來設定資料庫帳號密碼等敏感資訊，不會上傳到 GitHub。

```bash
# 複製範本檔案（只需要做一次）
cp .env.example .env
```

用文字編輯器打開 `.env`，你會看到類似以下的內容：

```ini
# FastAPI Application Settings
FASTAPI_APP_ENVIRONMENT=dev
SESSION_SECRET=your_super_secret_key_here  # ← 請改成任意隨機字串

# Database Connection Settings
DB_HOST=mariadb
DB_PORT=3306

# MariaDB Settings (Docker)
MARIADB_ROOT_PASSWORD=rootpassword
MARIADB_DATABASE=online_mall
MARIADB_USER=mall_user
MARIADB_PASSWORD=mall_user_password
```

> [!IMPORTANT]
> 請將 `SESSION_SECRET` 的值改成你自己的隨機字串，例如 `my_secret_abc123`。其他設定預設值可以直接使用。

### 2.4 啟動所有服務（Docker）

確保你的電腦已安裝 **Docker Desktop**（或 OrbStack），然後執行：

```bash
docker-compose up -d
```

第一次執行需要下載 Docker Image，可能需要幾分鐘。

`-d` 表示在背景執行。如果你想看到即時的 Log 輸出，可以省略 `-d`：

```bash
docker-compose up
```

---

## 3. 驗證服務是否正常運作

服務啟動後，打開瀏覽器：

| 服務 | 網址 |
|------|------|
| API 根目錄 | http://localhost:8000 |
| **Swagger UI（互動式 API 文件）** | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| DbGate（資料庫管理介面）| http://localhost:3000 |

打開 **http://localhost:8000/docs**，如果看到類似下圖的頁面，表示服務已成功啟動：

```
┌─────────────────────────────────────────┐
│  FastAPI                                │
│                                         │
│  GET /   root                           │
│                                         │
└─────────────────────────────────────────┘
```

你可以點擊 `GET /` → **Try it out** → **Execute**，應該會看到回應：

```json
{
  "message": "root page"
}
```

---

## 4. 新增你的第一個 API Endpoint

現在來示範如何新增一個新的 API。我們會新增一個 `GET /items` endpoint，回傳一份簡單的清單。

### 4.1 建立 Router 檔案

在 `src/` 目錄下新建 `routers/` 資料夾，然後建立 `items.py`：

```
src/
├── main.py
├── routers/          ← 新建此資料夾
│   └── items.py      ← 新建此檔案
└── shared/
```

`src/routers/items.py` 的內容：

```python
from fastapi import APIRouter

router = APIRouter()

# 這是一個簡單的 in-memory 資料（暫時不需要資料庫）
items = [
    {"id": 1, "name": "蘋果", "price": 30},
    {"id": 2, "name": "香蕉", "price": 15},
    {"id": 3, "name": "橘子", "price": 25},
]


@router.get("/items")
async def get_items():
    """回傳所有商品清單"""
    return items


@router.get("/items/{item_id}")
async def get_item(item_id: int):
    """根據 ID 回傳單一商品"""
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "找不到此商品"}
```

### 4.2 在 main.py 中註冊 Router

打開 `src/main.py`，加入以下內容：

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from shared import init_db
from shared.sessions import SessionMiddleware
from shared.redis import init_redis, close_redis
from shared.storage import init_storage
from shared.lakefs import init_lakefs
from routers import items  # ← 新增這行：匯入 items router
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

SESSION_SECRET = os.getenv("SESSION_SECRET")
if not SESSION_SECRET:
    SESSION_SECRET = secrets.token_hex(32)

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

app.include_router(items.router)  # ← 新增這行：註冊 items router


@app.get("/")
async def root():
    return {"message": "root page"}
```

### 4.3 驗證結果

因為 Docker 掛載了 `src/` 目錄，程式碼儲存後會**自動重新載入**，不需要重啟 Docker。

重新整理 **http://localhost:8000/docs**，你應該會看到新增了兩個 endpoint：

```
GET /items       回傳所有商品清單
GET /items/{item_id}  根據 ID 回傳單一商品
```

點擊 `GET /items` → **Try it out** → **Execute**，應該會看到：

```json
[
  {"id": 1, "name": "蘋果", "price": 30},
  {"id": 2, "name": "香蕉", "price": 15},
  {"id": 3, "name": "橘子", "price": 25}
]
```

恭喜！你已經成功新增了第一個 API Endpoint 🎉

---

## 接下來？

- 參考 `src/main.py` 和 `src/routers/items.py` 的結構，新增你自己的 API
- 想連接資料庫？查看 `src/shared/database.py` 了解 ORM 的使用方式
- 想了解如何跟團隊協作開發？閱讀 [CONTRIBUTING.md](../CONTRIBUTING.md)
- FastAPI 官方文件：https://fastapi.tiangolo.com
