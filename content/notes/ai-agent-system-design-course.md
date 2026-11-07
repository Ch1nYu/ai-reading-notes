---
title: 前 Google 工程師的 AI Agent 系統設計課
type: video
source_url: https://x.com/LunarResearcher/status/2084984207495827776?s=20
source_site: X
language: en
duration: 163m 44s
added: '2026-08-07'
topics:
- agents
summary: 前 Google 工程師 Sean Chan 釋出免費 3 小時完整課程，從 RAG 基礎、多 Agent 系統架構、記憶體系設計、Loop/Graph 工程化，到 LLM Ops 評估閉環與開源專案（Hermes、Waku-Agent、AutoManus）實戰部署，完整示範如何打造可靠、可演進、可量產的 AI Agent 系統。
---

## 完整摘要

### 第一階段：RAG 與知識檢索實作（分段 1-3）
本課程由 Automatus.io 創辦人、前 Google Business Messaging 工程師 Sean Chan 主講，橫跨 AI Agent 系統設計全棧知識體系。第一階段以電商 D2C 客服為例，建立 70% 自動化、CSAT > 4.5 的目標系統。架構採多 Agent 協作：Gateway（認證/限流）→ Router Agent（意圖識別）→ Q&A Agent（前端對話中樞）→ Planner Agent（工具調用執行），並設 Human-in-the-loop 機制處理複雜個案。核心技術為 RAG：文件切塊 → Embedding（1536/3072 維） → 向量資料庫（Supabase pgvector） → 語義檢索 → LLM 生成。實作開源專案 `yt-rag`（FastAPI + Supabase），示範本地開發、種子資料建庫、API 端點設計，並部署至 Google Cloud Run 實現即時知識熱更新。

### 第二階段：Agent 系統設計八大原則與 Agentic RAG（分段 3-4）
歸納八大核心原則：(1) 智慧預設優於無限客製，(2) 順應既有工作流，(3) 垂直領域優先（20-30 筆高品質範例鎖定行為），(4) 範例數量與品質平衡，(5) 自然語言撰寫明確工作流規格，(6) 引入人工審核迴路並以好壞案例持續訓練，(7) 建立單一記憶層共享上下文，(8) 持續評估防止模型退化。示範 `yt-agentic-rag` 專案結合向量檢索與工具呼叫（Google Calendar/Gmail），支援多輪對話、排程、發信。並介紹 AutoManus：針對高客單價客製化商品的 B2B AI 接待員，自動資格審核、線索結構化、共用 WhatsApp 號碼多業務路由。

### 第三階段：Agent Harness、記憶體系與 Loop Engineering（分段 5-7）
提出「Harness（馬具）」隱喻：LLM 是強大但不認識你的馬，需透過 Harness 注入四類記憶——程序記憶（技能/如何行動）、語義/耐久事實（私有知識）、事件記憶（跨對話時間序列）、工作記憶（當下上下文）。深度解析 Hermes Agent Harness（New Research 開源，GitHub 200k+ stars）：本地優先、系統提示詞 `soul.md`、Loop Engineering（自主工具迴路）、三層記憶檔案（`Skills/*.md`、`memory.md`、`state.db` SQLite）、自我演進閉環（錯誤/重複任務自動蒸餾更新技能與記憶）、缺乏內建 Eval 需自行整合 LangSmith/Langfuse。

### 第四階段：工程演進階梯與 Graph 架構（分段 8）
回顧三年演進：Prompt Engineering → Context Engineering → Skills/Procedural Memory → Loop（目標導向、逐步決定工具） → Graph（預定義節點邊、支援並行、確定/非確定混合）。強調 Loop 與 Graph 共存互補：Loop 適合探索性任務（Deep Research），Graph 適合 SOP 固定的企業級流程。示範開源專案 `waku-agent`：儀表板與 CLI、Graph 定義（`triage` 並行查日曆、`gather` 多源綜合）、Retrieval Gate 三類記憶檢索、LLM Ops 追蹤回饋。現代 Agent Graph 新點在於非確定性節點（LLM 呼叫）、LLM Routing（模型選擇邊）、需加入 Guards 防護。

### 第五階段：產品化部署與生態（分段 5, 9）
AutoManus 提供兩條部署路徑：MCP Server（Claude Code 整合，<1 分鐘爬站建立代理）與 REST API（單一 curl 指令、Web Chat Widget 嵌入、WhatsApp 入口）。課程結尾邀請加入社群（shangchen.io 私有 Discord、雙月直播、原始設計圖）、GitHub 專案給星支持。


## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| **多 Agent 客服系統架構** | 由 Gateway（認證限流）、Router Agent（意圖識別）、Q&A Agent（唯一對外對話中樞）、Planner Agent（拆解任務並編排工具）與 Human-in-the-loop（低信心或負面情緒時轉人工）協同運作。 | 分段 1–2：以 D2C 電商客服達成 70% 自動化、CSAT > 4.5 為目標的設計架構圖。 |
| **RAG 完整流程與熱更新** | 長文件切塊（Chunking）→ OpenAI `text-embedding-3-large` 向量化 → 存入 Supabase pgvector → 透過 `match_chunks` 餘弦相似度 Top-K 檢索 → 注入 Prompt 附來源生成；透過 `/seed` 端點重跑即可即時熱更新知識。 | 分段 2–3：開源教學專案 `yt-rag`（FastAPI + Supabase + Google Cloud Run）實作示範。 |
| **記憶體系四層架構** | 工作記憶（Context Window 組裝當下對話）、程序記憶（`Skills/*.md` 記錄工具調用 SOP）、語義/耐久事實（`memory.md` 或 `rag_chunks` 定期蒸餾領域政策與偏好）、事件記憶（`state.db` SQLite 記錄完整時序軌跡）。 | 分段 5–7：解析 Hermes Agent Harness 本地優先的三層持久化記憶檔案與自我演進蒸餾機制。 |
| **Loop Engineering vs Graph Engineering** | Loop 由模型逐步決定下一步工具，靠 End-loop Guardrails 控制停止，適合探索性任務（如 Deep Research、修 Bug）；Graph 預定義節點與有向邊並支援原生並行、非確定性節點與 Guards，適合 SOP 固定的企業流程，兩者共存互補。 | 分段 6–8：對比 Hermes Agent（Loop 代表）與 `waku-agent`（Graph 代表，`triage` 並行查日曆與 `gather` 多源綜合）。 |
| **AI Agent 系統設計八大原則** | (1) 智慧預設優於無限客製；(2) 順應既有工作流；(3) 垂直領域優先（20–30 筆高密度範例鎖定行為）；(4) 範例數量與品質平衡；(5) 多行逐步自然語言寫工作流規格；(6) 人工審核迴路；(7) 單一共享記憶層；(8) 持續評估防退化。 | 分段 3–4：講者從 Google 與 Automatus 實戰歸納的八大工程原則與 `yt-agentic-rag` 示範。 |
| **LLM Ops 與 Eval 閉環** | 以 Langfuse / LangSmith 記錄事件樹（Tracing），雙軌評估系統健康度（延遲、Token 成本、錯誤率）與品質（LLM-as-a-judge、人工標註），再分熱修復（調 Prompt/檢索）與冷修復（改程式重跑）形成自演進閉環。 | 分段 6 與 8：定義 LLM Ops 為「觀測 → 評估 → 診斷 → 修復 → 部署 → 觀測」的持續回饋系統。 |
| **五大實戰專案矩陣** | 課程串聯 `yt-rag`（RAG 基礎）、`yt-agentic-rag`（結合 Calendar/Gmail 工具呼叫）、`Hermes Agent`（本地自演進 Harness）、`Waku-Agent`（Graph 生產級框架）與 `AutoManus`（MCP Server / REST API 一鍵部署 B2B 接待員）。 | 分段 2–9：逐步展示從基礎 RAG 到企業級多通道部署的五個開源與商業專案。 |


## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| "If we can reduce the amount of automation of using agents for cases where it doesn't really need an agent, then your system will be more reliable." | 如果我們能減少在不需要 Agent 的場景中使用自動化 Agent，系統會更加可靠。 | **分段 1**：步驟固定、確定性高的流程應優先用傳統工作流（Deterministic Workflow），避免濫用 LLM 引入隨機性。 |
| "The Q&A agent is just like the central brain or the CEO of the company who needs to do all the communication with their customers." | Q&A Agent 就像是公司的中央大腦或 CEO，負責所有與客戶的溝通。 | **分段 1**：多 Agent 架構中，Q&A Agent 為唯一對外接口，協調內部 Planner、Tools，對外統一口徑。 |
| "Smart defaults are more important than infinite customization." | 智慧預設比無限客製化更重要。 | **分段 3**：使用者不會寫 Prompt，產品應內建領域最佳實務作為預設，減少決策疲勞與失誤。 |
| "Meet users where they are, don't change how users work today." | 在使用者所在位置滿足他們，別改變他們今天的工作方式。 | **分段 3**：B2B 產品須嵌入既有工具鏈（Excel、Notion、CRM），零遷移成本才能落地。 |
| "Vertical first strategy… high volume, detailed, domain-specific examples will make the model stop doing stupid stuff." | 垂直優先策略……大量、詳細、領域特定的範例能讓模型不再做蠢事。 | **分段 3**：投資人建議：用 20-30 筆高密度範例「鎖定」模型行為，驗證 PMF 再做 Mixture-of-Experts 水平擴展。 |
| "Multi-line, step-by-step natural language instructions will minimize hallucination and give an agent stable, predictable behavior." | 多行、逐步的自然語言指令能將幻覺降到最低，讓 Agent 行為穩定可預測。 | **分段 3**：工作流規格用自然語言寫成詳細 SOP（何時呼叫什麼工具、參數怎麼傳、例外怎麼處理），優於 JSON/表格直餵。 |
| "If an agent messes things up, it's almost always, almost always, your prompt's fault instead of the model's fault." | 若 Agent 搞砸了，幾乎永遠是提示詞的錯，而非模型的錯。 | **分段 4**：創辦人朋友語錄，強調 Prompt Engineering 是槓桿點，模型選擇是次要。 |
| "If Claude can learn code bases, can learn how to write code, your agent has no excuse. You should give them as much of an example as possible." | Claude 都能學會程式碼庫與寫代碼，你的 Agent 沒藉口。你應盡量給它大量範例。 | **分段 4**：Claude 系統提示詞洩露事件證實：範例密度決定表現上限，少給範例就是偷懶。 |
| "A large language model has no clue with how you want it to perform. This is why the concept called harness becomes really important." | 大型語言模型完全不知道你希望它如何表現，這就是為什麼「馬具」概念至關重要。 | **分段 5-6**：LLM 是通用大腦，Harness（記憶+工具+迴路+評估）才是讓它「認識你、聽你話」的關鍵。 |
| "The very very essential part of this loop is that it needs to know when it should stop. That's why we need this end loop guardrails." | 迴路最核心的部分是必須知道何時停止，這就是為什麼我們需要結束迴路的護欄。 | **分段 6**：Loop Engineering 核心非「如何開始」而是「何時結束」，避免無限呼叫工具或卡住等待。 |
| "We need a feedback loop to help us understand is this agent actually performing properly… and can I continuously get feedback on how do we fix it and actually fix it ourselves… that is called large language model operations system, LLM ops." | 我們需要回饋迴路來了解 Agent 是否正確執行……並持續獲得如何修復的回饋並自行修復，這就是大型語言模型運營系統（LLM Ops）。 | **分段 6**：定義 LLM Ops 為「觀測→評估→診斷→修復→部署」閉環，使系統具備自演進能力。 |
| "It creates its own skills from experience instead of you telling the AI, like Claude Code, to make skills. And then it also improves over time when you keep using it because it persistently stores knowledge in your local machine." | 它從經驗中自動創建技能，而不是像 Claude Code 那樣要你指示 AI 建立技能；持續使用時它會持久化知識於本地端而自我改進。 | **分段 6**：Hermes 差異化賣點——自動技能生成 + 本地持久化學習，形成用戶鎖定。 |
| "Harness is a very vague concept. Just don't fantasize it. It's nothing complicated. It's just a buzzword." | Harness 是個很模糊的概念，別想太複雜，它其實沒什麼複雜的，只是個流行詞罷了。 | **分段 7**：去魅 Harness，本質只是「包裹 LLM 的工具鏈」（記憶、工具、迴路、評估），別被術語嚇倒。 |
| "Every time when it realizes that something is a mistake that you should learn from or it's a repeated task, it will start to summarize, okay, here's some new memories I should know for the future in order to serve this user well." | 每當它發現錯誤或重複任務時，就會開始總結：好，這些是我未來為了更好服務用戶該記住的新記憶。 | **分段 7**：Hermes 自我演進核心邏輯——錯誤/重複觸發蒸餾，自動更新 `Skills/*.md` 與 `memory.md`。 |
| "You cannot say graph engineering is replacing loop engineering because they're co-existing... a loop is something you need when the model decides what to call one step at a time, a graph is something like when you know the shape and you just want them to move together." | 不能說 Graph Engineering 取代 Loop Engineering，因為它們共存……Loop 是模型逐步決定下一步調用時需要的；Graph 是你已知流程形狀、只想讓它們一起跑時用的。 | **分段 8**：徹底釐清兩者適用邊界，Loop=探索/開放，Graph=確定/並行/SOP，企業級系統通常混合使用。 |
| "What is new now is that some of the nodes that we're using right now are non-deterministic. It could be a LLM call. And at the same time, sometimes the model can pick the edge... you need some guards, which a previous directional graph scheduler never did." | 現在的新點在於，我們使用的某些節點是非確定性的，可能是 LLM 呼叫；同時模型也可選擇邊（路由）……你需要一些防護機制，這是過去的有向圖排程器從未做過的。 | **分段 8**：現代 Agent Graph vs 2023 確定性工作流 的本質區別：非確定性節點 + LLM Routing + Guards。 |


## 可參考資料

- **課程原始推文**：Sean Chan 釋出 3 小時 AI Agent 系統設計課程的 X 貼文。 — <https://x.com/LunarResearcher/status/2084984207495827776>
- **講者個人網站與社群入口**：提供私有 Discord、雙月直播與原始系統設計圖 Excalidraw 檔。 — <https://shangchen.io>
- **Automatus / AutoManus 產品官網**：B2B 銷售 AI 接待員產品，支援共用 WhatsApp 路由、MCP Server 與 REST API 部署。 — <https://automatus.io>
- **Hermes Agent Harness 官網**：New Research 開源的本地優先自演進 Harness（`soul.md`、三層記憶檔案、MCP 整合）。 — <https://hermes-agent.newresearch.com>
- **yt-rag（RAG 基礎教學專案）**：FastAPI + Supabase pgvector 實作文件切塊、向量化、API 端點與 Cloud Run 部署（`github.com/shanshengchen/yt-rag`）。
- **yt-agentic-rag（Agentic RAG 進階專案）**：整合 Google Calendar/Gmail API、Function Calling 與多輪對話排程（`github.com/shenshongchen/yt-agentic-rag`）。
- **Waku-Agent（Graph 架構生產級框架）**：支援並行與非確定性節點、Retrieval Gate、Dashboard/CLI 與 LLM Ops 回饋（`github.com/shanshongchen/waku-agent`）。
- **核心工具與技術棧**：Supabase (pgvector)、FastAPI、Google Cloud Run、Langfuse、LangSmith、WhatsApp Business API、Cursor 與 Claude Code。
