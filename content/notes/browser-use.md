---
title: Browser Use：讓 AI agent 操作瀏覽器
type: article
source_url: https://github.com/browser-use/browser-use
source_site: GitHub
added: '2026-09-09'
topics:
- tools
- agents
summary: Browser Use 透過可插入的 LLM 與靈活的程式庫或雲端代理，讓開發者以最少程式碼實現網頁自動化，同時提供基準測試與排行榜以驗證效能。
abstract: Browser Use 是一個讓 AI 代理能像人類般操作網頁瀏覽器的開源專案，提供 Python 函式庫與託管雲端服務，可自動完成表單填寫、資料擷取等網頁任務。
---

## 完整摘要

### 核心功能與使用範例
Browser Use 讓 AI 代理模擬人類瀏覽器行為，能開啟頁面、點擊按鍵、輸入文字、填寫表單以及結構化資料擷取（例如追蹤追隨者並匯出 CSV）。它支援多種 LLM（OpenAI、Anthropic、Google 等）透過統一的 ChatBrowserUse 介面，且提供 CLI 與 Python library 兩種使用方式，可依任務頻率選擇。此外，內建的自訂工具機制允許開發者擴展代理能力，例如加入專屬動作來處理特定網站邏輯。

### 安裝與快速開始
首先使用 uv（或 pip）安裝 browser-use（需 Python 3.11+）：`uv add browser-use` 或 `pip install browser-use`。接著在專案根目錄建立 `.env` 檔案，填入取得自 Browser Use Cloud 或自行提供的 LLM API 金鑰（如 BROWSER_USE_API_KEY=your-key）。安裝完成後，可參考範例程式碼建立 Agent 並執行任務，例如查詢 browser-use 儲存庫的星星數。若已有其他代理（Claude Code、Codex、Cursor、Hermes、OpenClaw 等），也可直接執行 `browser-use skill install` 註冊技能並連線瀏覽器。

### 開源版與雲端版比較
開源版免費且提供完整程式碼，適合想要自訂模型與深度整合的開發者；雲端版則提供託管代理與瀏覽器、內建隱身功能、Proxy 輪換、驗證碼處理、持久化檔案系統以及可擴展的平行執行。根據 BU Bench V1 基準測試，不同模型的成功率分布顯示 Cloud v4 Opus 4.8 達 85.0%、Cloud v4 (default) 78.0%，而開源版的 claude opus-4-7 為 74.0%，隨後逐步下降。Browser Use 在 Odysseys 排行榜（200 項長時程網頁任務）上以 87.4% 平均分領先來自 OpenAI、Anthropic、Google 與 Microsoft 的電腦使用代理。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| AI 瀏覽器代理自動化 | Browser Use 能讓代理模擬人類操作瀏覽器，包括開啟網頁、點擊元件、輸入文字與提交表單，使得 AI 能完成原本需要人工的網頁流程。 | Browser Use lets an AI agent use a web browser the same way humans do — it opens pages, clicks buttons, types, and fills in forms. |
| Python 程式庫安裝與使用 | 透過 uv 或 pip 安裝 browser-use，設定 .env 中的 API 金鑰後，即可使用 Agent 類別與指定的 LLM 模型執行自訂任務。 | Install Browser Use (Python >= 3.11): uv add browser-use # or: pip install browser-use |
| LLM 整合與模型選擇 | ChatBrowserUse 接受供應商前綴的模型識別符號，使得單一 BROWSER_USE_API_KEY 可達到 OpenAI、Anthropic、Google 等多家供應商，並推薦使用專屬的 bu-* 模型以獲得最佳速度與準確度。 | ChatBrowserUse accepts provider-prefixed model ids, so a single BROWSER_USE_API_KEY reaches all of them — no separate OpenAI/Anthropic/Google keys required: |
| 雲端服務與免費額度 | 符合條件的新 Google、GitHub 或 Microsoft 使用者可獲一次性 $15 雲端點數，無需信用卡，獲得託管代理、持久化檔案系統與 Proxy 輪換等功能。 | Eligible new Google, GitHub or Microsoft signups get a one‑time $15 Cloud credit. |
| 基準測試與排行榜表現 | 在 100 項真實瀏覽器任務上的基準測試顯示不同模型的成功率分布，且 Browser Use 在 Odysseys 排行榜上以 87.4% 平均分領先其他電腦使用代理。 | We benchmark Browser Use across 100 real‑world browser tasks. |
| 客製化工具與擴展能力 | 透過 Tools 類別可加入自訂動作（例如回傳特定結果），擴展代理功能；同時提供 CLI 與 Python library 兩種使用方式，依任務頻率選擇最適合的介面。 | You can add custom tools to extend the agent's capabilities: |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Browser Use lets an AI agent use a web browser the same way humans do — it opens pages, clicks buttons, types, and fills in forms. | Browser Use 讓 AI 代理能像人類一樣使用網頁瀏覽器 —— 它會開啟頁面、點擊按鍵、輸入文字、填寫表單。 | 出現在「What can Browser Use do?」段落開頭，說明該專案的核心功能。 |
| Eligible new Google, GitHub or Microsoft signups get a one‑time $15 Cloud credit. | 符合條件的新 Google、GitHub 或 Microsoft 使用者可取得一次性 $15 雲端點數。 | 位於「Start with Browser Use Cloud」段落，說明雲端服務的免費試用額度。 |
| We benchmark Browser Use across 100 real‑world browser tasks. | 我們在 100 項真實瀏覽器任務上對 Browser Use 進行基準測試。 | 出現在「Open Source vs Cloud」段落前的基準測試說明，用以評估不同模型的表現。 |

## 可參考資料
- **Browser Use GitHub repository**：專案原始碼與文件首頁，含安裝、使用說明與範例程式碼。 — <https://github.com/browser-use/browser-use>
- **Browser Use Cloud**：提供託管代理與瀏覽器、免費點數、持久化檔案系統及 Proxy 輪換服務。 — <https://cloud.browser-use.com/>
- **Browser Use Docs**：開源與雲端版的詳細使用文件，包括安裝、設定、進階功能與 API 說明。 — <https://docs.browser-use.com/>
- **Browser Use Benchmark**：開源基準測試腳本與結果，用於評估不同 LLM 在網頁自動化任務上的成功率。 — <https://github.com/browser-use/benchmark>
- **Odysseys Leaderboard**：展示 Browser Use 在網頁代理排行榜上的表現，以 87.4% 平均分領先其他電腦使用代理。 — <https://odysseysbench.com/leaderboard>
- **Browser Use Pricing**：說明雲端服務的費用結構與免費額度資格條件。 — <https://browser-use.com/pricing.md>
- **Browser Use Terms of Service**：開源庫與雲端服務的法律條款與使用規範。 — <https://browser-use.com/legal/terms-of-service>
- **Browser Use Privacy Policy**：說明個人資料收集、使用與保護的隱私政策。 — <https://browser-use.com/privacy/>
