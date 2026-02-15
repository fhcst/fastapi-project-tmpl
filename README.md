![FastAPI Project Banner](./docs/assets/banner.png)

# FastAPI Project Template (建立專案後要修改)

> [!IMPORTANT]
> **給使用本範本的同學：**
> 請將本 `README.md` 檔案內容修改為適合你或是你們小組專案的說明。
> 凡是看到 `[ ]` 包起來的文字，都需要替換成實際的內容。
> 本區塊說明 (Note) 可以刪除。

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-ECL%202.0-blue)

這是一個特別為臺北市立復興高級中學學生設計的 **FastAPI** 專案範本。本專案旨在提供一個標準化的開發環境，讓學生能夠練習建構現代化的 Web App Service 或 Web API，並模擬真實的 **Open Source Software (OSS)** 開發模式。

本專案採用 **Python 3.13+**，並使用現代化的套件管理器 **uv** 進行依賴管理，搭配 **Docker** 進行資料庫環境的部署。

## 🎯 專案目標

- 學習 **FastAPI** 框架的基礎與進階應用。
- 熟悉 **Asynchronous Programming (非同步程式設計)**。
- 實踐 **OSS 協作模式** (Fork, Branch, PR)。
- 掌握 **Docker** 與 **Database** 的整合應用。

## 🛠️ 技術堆疊 (Tech Stack)

- **Language**: Python 3.13+
- **Web Framework**: FastAPI
- **Package Manager**: uv
- **Database**: MariaDB (via Docker)
- **ORM**: SQLModel / SQLAlchemy (Async)
- **Database GUI**: DbGate (via Docker)


## 📋 前置需求 (Prerequisites)

在開始之前，請確保你的開發環境已經安裝以下工具：

1.  **Python 3.13+**: [下載 Python](https://www.python.org/downloads/)
2.  **Git**: [下載 Git](https://git-scm.com/downloads)
3.  **Docker Desktop** (或是 OrbStack / Podman): 用於運行資料庫。
4.  **VS Code** (推薦): 建議安裝 Python 及 Pylance 擴充套件。

## 🚀 快速開始 (Quick Start)

請依照以下步驟設定你的開發環境。

### 1. 安裝 uv

本專案使用 `uv` 作為套件管理器，它比 `pip` 或 `poetry` 更快且更易於使用。

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安裝完成後，請重啟 Terminal 或執行 `source` 命令以更新路徑。

### 2. 下載專案 (Clone)

```bash
# 如果你是直接開發，使用 clone
git clone https://github.com/[你的 GitHub 帳號]/[專案].git
cd fastapi-project-tmpl

# 如果你是要進行協作開發，請先 Fork 本專案，然後 Clone 你自己的 Fork
# git clone https://github.com/[你的 GitHub 帳號]/[專案].git
```

### 3. 安裝依賴 (Install Dependencies)

使用 `uv` 同步專案所需的套件。這會自動建立虛擬環境 (Virtual Environment)。

```bash
uv sync
```

### 4. 設定環境變數 (Environment Variables)

複製範本檔案 `.env.example` 並重新命名為 `.env`。

```bash
cp .env.example .env
```

請打開 `.env` 檔案，檢查設定值。預設設定通常適用於 Docker 環境：

```ini
# FastAPI Application Settings
FASTAPI_APP_ENVIRONMENT=dev
SESSION_SECRET=your_super_secret_key_here # 請修改為隨機字串

# Database Connection Settings
DB_HOST=mariadb
DB_PORT=3306

# MariaDB Settings (Docker)
MARIADB_ROOT_PASSWORD=rootpassword
MARIADB_DATABASE=online_mall
MARIADB_USER=mall_user
MARIADB_PASSWORD=mall_user_password
```

### 5. 啟動應用程式與資料庫 (Start Application & Database)

使用 Docker Compose 啟動所有服務，包含 **FastAPI App**、**MariaDB** 和 **DbGate**。

```bash
docker-compose up -d
```

或是如果你想要看到 App 的 Log 輸出：

```bash
docker-compose up
```

服務啟動後，你可以訪問：

- **API Root**: [http://localhost:8000](http://localhost:8000)
- **Interactive API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **DbGate (Database GUI)**: [http://localhost:3000](http://localhost:3000)

> [!NOTE]
> 如果你修改了程式碼，Docker 會自動掛載 `src/` 目錄，因此大多數的程式碼變更會自動重新載入 (Hot Reload)，不需要重啟 Docker。
> 但如果有新增新的 Python 套件依賴 (修改 `pyproject.toml`)，則需要重新 Build Docker Image：
> ```bash
> docker-compose build
> docker-compose up -d
> ```

## 📂 專案結構 (Project Structure)

> [!NOTE]
> 以下描述的是普遍習慣性的專案結構，若是你自己或小組有特別約定，可以忽視以下結構的規範。
> 但若是沒有，建議按照專案結構開發。


```plaintext
fastapi-project-tmpl/
├── .venv/                  # uv 建立的虛擬環境 (Virtual Environment)
├── src/                    # 原始碼目錄 (Source Code)
│   ├── main.py             # 程式進入點 (Application Entrypoint)
│   ├── configs/            # APP 設定 (Environment -- pydantic-settings/Specific Setting)
│   ├── routers/            # API 路由定義 (Routes)
│   ├── models/             # 資料庫模型 (Database Models)
│   ├── schemas/            # Pydantic Schemas (Request/Response Models)
│   └── shared/             # 共用模組 (Utils, Database Config)
├── tests/                  # 測試程式碼 (Tests)
├── docs/                   # 文件 (Documentation)
├── docker-compose.yml      # Docker 服務定義
├── pyproject.toml          # 專案設定與依賴清單
├── uv.lock                 # 依賴版本鎖定檔
├── README.md               # 專案說明文件
└── CONTRIBUTING.md         # 貢獻指南
```

## 🤝 參與貢獻 (Contributing)

我們非常歡迎同學參與專案的開發與維護。本專案採用標準的 GitHub Flow / OSS 開發模式。

詳細的開發流程、Branch 命名規則及 PR 規範，請務必閱讀 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 📝 授權 (License)

[Educational Community License, Version 2.0 (ECL-2.0)](LICENSE)
