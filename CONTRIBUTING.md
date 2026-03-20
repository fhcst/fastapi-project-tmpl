# 貢獻指南 (Contributing Guide)

> [!IMPORTANT]
> **TODO：這份文件是給你改的！**
> 在開始使用前，請搜尋所有標有 `TODO:` 的區塊，並依照說明替換成你的專案實際內容。
> 沒有 `TODO:` 標示的段落（例如 Git 流程、Commit 規範）可以直接沿用，不需要修改。

感謝你有興趣參與本專案的開發！本專案旨在模擬真實的 **OSS (Open Source Software)** 開發流程，讓同學熟悉團隊協作的模式。

為了確保開發流程順暢，請務必遵守以下的開發規範。我們採用 **Feature Branch Workflow** 與 **Pull Request (PR)** 的模式進行協作。

## 🤝 行為準則 (Code of Conduct)

- 請保持尊重與友善。
- 所有的討論與程式碼審查 (Code Review) 都應以建設性為原則。
- 若發現 Bug 或有新功能建議，請先開設 **Issue** 進行討論。

## 🛠️ 開發流程 (Development Workflow)

請依照以下步驟進行開發：

### 1. Fork 專案

點選 GitHub 頁面右上角的 **Fork** 按鈕，將本專案複製到你自己的 GitHub 帳號下。

### 2. Clone 到本地端

將你 Fork 下來的專案 Clone 到你的電腦中。

> [!IMPORTANT]
> **TODO：** 將以下指令中的 `YOUR_USERNAME` 替換為你的 GitHub 帳號，`YOUR_PROJECT` 替換為你的 Repository 名稱。

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_PROJECT.git
cd YOUR_PROJECT
```

### 3. 設定 Upstream Remote

為了保持與原專案同步，請設定 `upstream`。

> [!IMPORTANT]
> **TODO：** 將以下指令中的 URL 替換為**原始 Repository**（你 Fork 來源）的網址。

```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/YOUR_PROJECT.git
```

### 4. 建立功能分支 (Feature Branch)

**嚴格禁止直接在 `main` 分支上進行開發！**
每次開發新功能或修復 Bug 時，請建立一個新的 Branch。Branch 名稱應具備描述性。

- **功能開發**: `feature/功能名稱` (例如: `feature/login-page`, `feature/user-api`)
- **錯誤修復**: `fix/錯誤描述` (例如: `fix/db-connection-error`)
- **文件更新**: `docs/文件名稱` (例如: `docs/update-readme`)

```bash
# 建立並切換到新分支
git checkout -b feature/my-new-feature
```

### 5. 進行開發與測試

在你的分支上進行程式碼撰寫。完成後，請務必執行測試以確保程式碼正常運作。

```bash
# 執行所有測試
uv run pytest
```

### 6. 提交變更 (Commit)

請遵守 **Commit Message Convention**（詳見下方說明）。

```bash
git add .
git commit -m "feat: 完成使用者登入 API"
```

### 7. 推送至 GitHub (Push)

將你的分支 Push 到你自己的 GitHub Repo (Origin)。

```bash
git push origin feature/my-new-feature
```

### 8. 發起 Pull Request (PR)

1. 回到 GitHub 上你的 Repo 頁面。
2. 你會看到一個 "Compare & pull request" 的提示，點擊它。
3. **Base repository** 選擇原始專案的 `main` 分支。
4. **Head repository** 選擇你的 Repo 與剛才 Push 的分支。
5. 填寫 PR 的標題與描述，清楚說明你做了什麼改變。
6. 等待專案維護者 (Maintainers) 進行 Code Review。

### 9. 同步原專案 (Sync Upstream)

如果在你開發的過程中，原專案 (Upstream) 有更新，你需要同步這些變更到你的本地端，以免發生衝突。

```bash
git checkout main
git pull upstream main
git checkout feature/my-new-feature
git rebase main
# 若有衝突 (Conflict)，請解決衝突後繼續
# git add .
# git rebase --continue
```

## 📝 Commit Message 規範

我們採用 **Angular Commit Convention**，格式如下：

```plaintext
<type>: <subject>

<body> (非必要)
<footer> (非必要)
```

### Type 類別
- **feat**: 新增功能 (Feature)
- **fix**: 修復 Bug
- **docs**: 文件變更 (Documentation)
- **style**: 程式碼格式調整 (不影響程式邏輯，如空白、排版)
- **refactor**: 重構 (既不是新增功能也不是修復 Bug)
- **perf**: 效能優化 (Performance)
- **test**: 新增或修改測試
- **chore**: 建置過程或輔助工具的變動 (例如更新依賴)

### 範例
- `feat: 新增使用者註冊 API`
- `fix: 修正資料庫連線逾時問題`
- `docs: 更新 README 安裝步驟`

## 🎨 程式碼風格 (Code Style)

- 請使用 **PEP 8** 風格撰寫 Python 程式碼。
- 變數命名請使用具備描述性的英文單字（例如 `user_list` 而非 `ul`）。
- 建議使用 `uv run ruff check` 來檢查程式碼品質（若有設定）。
- 確保所有新的 API 都有對應的測試案例。

## ✅ Pull Request 檢查清單

在送出 PR 之前，請確認：
- [ ] 程式碼可以正常執行且通過所有測試。
- [ ] 沒有包含不必要的檔案（如 `.DS_Store`、`__pycache__` 等）。
- [ ] Commit Message 符合規範。
- [ ] 相關文件（如 API 文件）已更新。

感謝你的貢獻！讓我們一起讓這個專案變得更好！
