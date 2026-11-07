---
title: Requests：Python HTTP 函式庫
type: article
source_url: https://github.com/psf/requests
source_site: GitHub
added: '2026-10-15'
topics:
- tools
summary: Requests 以人性化的 API 成為 Python 生態系事實標準的 HTTP 客戶端，解決了 urllib 複雜難用的問題，並持續維護現代化相容性與安全性。
abstract: Requests 是一個廣泛使用的 Python HTTP 客戶端函式庫，以簡潔優雅的 API 封裝 HTTP/1.1 請求，支援連線池、Cookie 持久、TLS 驗證、串流下載等企業級功能，週下載量達 300M 次，被 400 萬以上儲存庫依賴。
---

## 完整摘要

### 專案定位與採用規模
Requests 定位為「簡單優雅的 HTTP 函式庫」，主打 for humans 的設計哲學。根據 README，該專案擁有 54.5k GitHub Stars、12.9k Forks、1.3k Watchers，PyPI 統計約 300M downloads/week，且 GitHub 顯示有 4,000,000+ 個儲存庫依賴它（Used by 4.2M）。最新版本 v2.34.2 釋出於 2026-05-14，官方支援 Python 3.10+，授權為 Apache-2.0。專案由 Python Software Foundation（PSF）託管與維護。

### 核心功能與最佳實踐清單
README 列出 13 項支援特性：Keep-Alive & Connection Pooling、International Domains and URLs、Sessions with Cookie Persistence、Browser-style TLS/SSL Verification、Basic & Digest Authentication、Familiar dict-like Cookies、Automatic Content Decompression and Decoding、Multi-part File Uploads、SOCKS Proxy Support、Connection Timeouts、Streaming Downloads、Automatic honoring of `.netrc` 與 Chunked HTTP Requests。

### 安裝、複製與開發環境細節
安裝指令為 `python -m pip install requests`。複製倉庫時需加參數避免時間戳錯誤：`git clone -c fetch.fsck.badTimezone=ignore https://github.com/psf/requests.git`，或全域設定 `git config --global fetch.fsck.badTimezone ignore`。專案採用 src layout（原始碼在 `src/requests`），測試在 `tests/`，文件在 `docs/`。

### 授權變更與相依性治理歷程
2020-08-27 依 Apache 基金會指引正確套用 Apache-2.0 授權並新增 NOTICE 檔。2021-07-06 將 LGPL 授權的 `chardet` 替換為 MIT 授權的 `charset_normalizer`（PR #5797），保留 `requests[lgpl]` extra 讓使用者可選擇回退 chardet。2022-04-29 導入自動程式碼格式化（PR #6095）。2026-02-06 移除 Python 3.9 支援（PR #7196）。近期 dependabot 持續更新 GitHub Actions（如 CodeQL action v4.38.0）與 pre-commit 設定。

### 社群與貢獻者生態
專案有 659 位貢獻者，前排顯示 kennethreitz（原作者）、Lukasa、sigmavirus24、nateprewitt、slingamn、BraulioVM、dpursehouse、jgorset、gazpachoking、idan、schlamar 等核心維護者。文件網站託管於 Read the Docs（https://requests.readthedocs.io/），程式碼品質由 GitHub Actions（CodeQL）與 pre-commit（ruff）把關。贊助連結指向 PSF 官方贊助頁面。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 人性化 API 設計 | Requests 將 urllib 繁瑣的流程（手動拼 query string、form-encode、處理編碼）封裝成直觀的方法呼叫，例如 `requests.get(url, auth=('user','pass'))` 即可完成 Basic Auth，回應物件直接提供 `.status_code`、`.headers`、`.json()`、`.text` 等常用屬性，大幅降低認知負荷。 | README 程式碼範例展示 `r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))` 後直接讀取 `r.status_code`、`r.headers['content-type']`、`r.json()`。 |
| 連線池與 Keep-Alive 自動管理 | 底層使用 urllib3 的 HTTPConnectionPool，同一 Session 內重複請求同一 host 會自動複用 TCP 連線，減少握手延遲；開發者無需手動管理連線生命週期。 | README『Supported Features』明確列出『Keep-Alive & Connection Pooling』與『Sessions with Cookie Persistence』；原始碼 `src/requests/sessions.py` 實作 `Session` 類別內建 `HTTPAdapter` 與連線池。 |
| 編碼偵測去 LGPL 化 | 為避免下游專案打包時觸發 LGPL 傳染，專案在 2021 年將預設編碼偵測依賴從 chardet（LGPL）換成 charset_normalizer（MIT），並提供 `requests[lgpl]` extra 讓既有使用者平滑遷移，維護者表示實測兩者偵測結果一致。 | .gitignore 的提交訊息（2021-07-06）詳細說明更換動機與相容策略，並標註 PR #5797。 |
| 最低 Python 版本隨生態演進 | 專案定期移除 EOL Python 版本，2026-02-06 移除 3.9 支援（PR #7196），現行官方支援 Python 3.10+，確保可使用現代語法（如 union type `X \| Y`、pattern matching）並減少相容性維護負擔。 | setup.py、tox.ini 同步更新的提交訊息『Drop support for Python 3.9 (#7196)』；README『Supported Versions』區塊標註『Python 3.10+』。 |
| 企業級安全與供應鏈防護 | 專案啟用 GitHub Advanced Security（CodeQL 靜態分析）、dependabot 自動更新依賴、pre-commit 鉤子（ruff 格式化/檢查）、簽署提交（dependabot 提交帶 Signed-off-by），並在 SECURITY.md 規範漏洞回報流程。 | 最新提交為 dependabot 更新 CodeQL action 至 4.38.0（2026-09-21）；.pre-commit-config.yaml 追蹤 ruff-pre-commit v0.16.4；README 頁面顯示『Security and quality 4』頁籤。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Requests is a simple, yet elegant, HTTP library. | Requests 是一個簡單、優雅的 HTTP 函式庫。 | README 開頭與 GitHub 專案描述（About 區塊）重複出現的專案標語。 |
| Requests is one of the most downloaded Python packages today, pulling in around `300M downloads / week` — according to GitHub, Requests is currently depended upon by `4,000,000+` repositories. | Requests 是目前下載量最大的 Python 套件之一，每週約 300M 次下載——根據 GitHub，目前有 4,000,000+ 個儲存庫依賴它。 | README『Supported Features & Best–Practices』上方的專案採用規模說明。 |
| Requests officially supports Python 3.10+. | Requests 官方支援 Python 3.10+。 | README『Installing Requests and Supported Versions』區塊。 |
| By changing out this dependency for one under MIT we remove all license ambiguity. | 透過將此依賴換成 MIT 授權的套件，我們移除了所有授權模糊地帶。 | .gitignore 2021-07-06 提交訊息，說明將 chardet 換為 charset_normalizer 的動機。 |

## 可參考資料
- **Requests 官方文件**：完整 API 參考、進階用法、最佳實踐指南。 — <https://requests.readthedocs.io/en/latest/>
- **GitHub 儲存庫**：原始碼、Issue 追蹤、Pull Request、Release 歷程、安全性政策。 — <https://github.com/psf/requests>
- **Python Software Foundation 贊助頁面**：專案接受贊助的官方管道。 — <https://www.python.org/psf/sponsorship/>
- **charset_normalizer 專案**：取代 chardet 的 MIT 授權編碼偵測庫，Requests 目前預設依賴。
- **urllib3 專案**：Requests 底層 HTTP 協定實作與連線池管理的核心依賴。
- **Kenneth Reitz 個人網站**：Requests 原始作者。 — <https://kennethreitz.org/>
