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
本課程由 Automatus.io 創辦人、前 Google Business Messaging 工程師 Sean Chan 主講，橫跨 AI Agent 系統設計全棧知識體系。

**第一階段：RAG 與知識檢索實作**（分段 1-3）  
以電商 D2C 客服為例，建立 70% 自動化、CSAT > 4.5 的目標系統。架構採多 Agent 協作：Gateway（認證/限流）→ Router Agent（意圖識別）→ Q&A Agent（前端對話中樞）→ Planner Agent（工具調用執行），並設 Human-in-the-loop 機制處理複雜個案。核心技術為 RAG：文件切塊 → Embedding（1536/3072 維） → 向量資料庫（Supabase pgvector） → 語義檢索 → LLM 生成。實作開源專案 `yt-rag`（FastAPI + Supabase），示範本地開發、種子資料建庫、API 端點設計，並部署至 Google Cloud Run 實現即時知識熱更新。

**第二階段：Agent 系統設計八大原則與 Agentic RAG**（分段 3-4）  
歸納八大核心原則：(1) 智慧預設優於無限客製，(2) 順應既有工作流，(3) 垂直領域優先（20-30 筆高品質範例鎖定行為），(4) 範例數量與品質平衡，(5) 自然語言撰寫明確工作流規格，(6) 引入人工審核迴路並以好壞案例持續訓練，(7) 建立單一記憶層共享上下文，(8) 持續評估防止模型退化。示範 `yt-agentic-rag` 專案結合向量檢索與工具呼叫（Google Calendar/Gmail），支援多輪對話、排程、發信。並介紹 AutoManus：針對高客單價客製化商品的 B2B AI 接待員，自動資格審核、線索結構化、共用 WhatsApp 號碼多業務路由。

**第三階段：Agent Harness、記憶體系與 Loop Engineering**（分段 5-7）  
提出「Harness（馬具）」隱喻：LLM 是強大但不認識你的馬，需透過 Harness 注入四類記憶——程序記憶（技能/如何行動）、語義/耐久事實（私有知識）、事件記憶（跨對話時間序列）、工作記憶（當下上下文）。深度解析 Hermes Agent Harness（New Research 開源，GitHub 200k+ stars）：本地優先、系統提示詞 `soul.md`、Loop Engineering（自主工具迴路）、三層記憶檔案（`Skills/*.md`、`memory.md`、`state.db` SQLite）、自我演進閉環（錯誤/重複任務自動蒸餾更新技能與記憶）、缺乏內建 Eval 需自行整合 LangSmith/Langfuse。

**第四階段：工程演進階梯與 Graph 架構**（分段 8）  
回顧三年演進：Prompt Engineering → Context Engineering → Skills/Procedural Memory → Loop（目標導向、逐步決定工具） → Graph（預定義節點邊、支援並行、確定/非確定混合）。強調 Loop 與 Graph 共存互補：Loop 適合探索性任務（Deep Research），Graph 適合 SOP 固定的企業級流程。示範開源專案 `waku-agent`：儀表板與 CLI、Graph 定義（`triage` 並行查行曆、`gather` 多源綜合）、Retrieval Gate 三類記憶檢索、LLM Ops 追蹤回饋。現代 Agent Graph 新點在於非確定性節點（LLM 呼叫）、LLM Routing（模型選擇邊）、需加入 Guards 防護。

**第五階段：產品化部署與生態**（分段 5, 9）  
AutoManus 提供兩條部署路徑：MCP Server（Claude Code 整合，<1 分鐘爬站建立代理）與 REST API（單一 curl 指令、Web Chat Widget 嵌入、WhatsApp 入口）。課程結尾邀請加入社群（shangchen.io 私有 Discord、雙月直播、原始設計圖）、GitHub 專案給星支持。


## 重點知識與概念拆解

### 3.1 多 Agent 系統架構
| 組件 | 職責 | 關鍵技術 |
|------|------|----------|
| **Gateway** | 認證、限流、請求分發 | API Gateway 模式 |
| **Router Agent** | 意圖識別、任務分派 | 分類模型 / LLM Routing |
| **Q&A Agent** | 唯一對外接口、對話協調 | 系統提示詞工程、上下文管理 |
| **Planner Agent** | 複雜任務拆解、工具編排 | Function Calling、ReAct 模式 |
| **Human-in-the-loop** | 低信心/負面情緒轉人工 | 情緒偵測、信心閾值、工單系統 |

### 3.2 RAG 完整流程與實作
1. **Chunking**：長文件切分（避免超過 Context Window、降低雜訊）
2. **Embedding**：OpenAI `text-embedding-3-large` (3072 維) 或同級模型
3. **Vector DB**：Supabase + pgvector（PostgreSQL 擴充），RPC 封裝 `match_chunks`、`get_chunk_stats`
4. **Retrieval**：查詢向量化 → 餘弦相似度 Top-K 檢索
5. **Generation**：檢索結果注入 Prompt → LLM 生成（含引用來源）
6. **Seeding**：`/seed` 端點一次性/定期執行「切塊→向量化→寫入」
7. **熱更新**：修改原始文件 → 重跑 Seeding → 即時生效，無需重新部署

### 3.3 記憶體系四層架構
| 記憶類型 | 存儲形式 | 更新機制 | 檢索方式 | 用途 |
|----------|----------|----------|----------|------|
| **工作記憶** | Context Window | 每次 Run 組裝 | 直接讀取 | 當下對話、系統提示、相關長期記憶片段 |
| **程序記憶** | `Skills/*.md` (Markdown) | Agent 自動生成/更新 | 關鍵字/標籤匹配 | 「如何做事」：技能腳本、工具調用 SOP |
| **語義/耐久事實** | `memory.md` / `rag_chunks` 表 | 摘要 Agent 定期蒸餾 (如每 2000 筆) | RAG 向量檢索 / 關鍵字 Top-K | 「知道什麼」：用戶偏好、領域政策、蒸餾事實 |
| **事件記憶** | `state.db` (SQLite) / 時序資料庫 | 每輪對話自動追加 | SQL 時間範圍 + 語意搜尋混合 | 「發生過什麼」：完整對話歷史、工具調用軌跡 |

### 3.4 Loop Engineering vs Graph Engineering
| 維度 | **Loop (Agent Loop)** | **Graph (Agent Graph)** |
|------|------------------------|--------------------------|
| **核心隱喻** | 模型逐步決定「下一步工具」 | 預定義節點與有向邊，「已知流程形狀」 |
| **適用場景** | 探索性、非結構化任務（Deep Research、修 Bug、開放式規劃） | SOP 固定、需並行、企業級確定性流程（退貨處理、入職流程） |
| **控制機制** | End-loop Guardrails（任務完成判斷、用戶確認、權限等待） | Guards（防護）、LLM Routing（非確定性邊選擇） |
| **並行能力** | 順序執行（可委派子 Agent 平行） | 原生支援並行節點執行 |
| **演進關係** | **共存互補**，非取代關係 | **共存互補**，非取代關係 |

### 3.5 AI Agent 系統設計八大核心原則
1. **智慧預設優於無限客製** — 使用者不擅長 Prompt，領域專家內建最佳預設，保持黑盒穩定。
2. **順應使用者既有工作流** — 整合試算表、Notion、CRM 等既有工具，不強迫換介面。
3. **垂直領域優先** — 20-30 筆高品質、高細節領域範例鎖定單一垂直，驗證 PMF 再水平擴展。
4. **範例數量與品質平衡** — 太少限制模型、太多錯誤範例導致過擬合，需精心策展。
5. **以自然語言撰寫明確工作流規格** — 多行、逐步指令降低幻覺、提升可預測性，視同指導實習生。
6. **引入人工審核迴路** — 客戶憤怒/要求真人時觸發，並以好壞案例持續微調訓練。
7. **建立單一記憶層** — 多 Agent 共享聊天歷史、行為、行程、資料表，解決「產品不同部分不記得用戶先前行為」。
8. **持續評估防止退化** — 自動化評測覆蓋關鍵步驟（郵件主旨、簽名、問候語），模型更新時即時偵測退化。

### 3.6 LLM Ops / Eval 閉環
- **Tracing**：事件樹記錄（提問、檢索、工具呼叫、延遲、Token 用量），工具：Langfuse、LangSmith。
- **評估雙軌**：
  - *健康度*：延遲、Token 成本、工具觸發率、錯誤率。
  - *品質*：LLM-as-a-judge 打分、人工標註。
- **診斷與修復**：
  - *熱修復*：調整 Prompt/參數/檢索設定 → 直接回推 Agent Run。
  - *冷修復*：修 Bug、重跑 Pipeline、重新 Trace/Eval。
- **自演進系統**：觀測 → 評估 → 診斷 → 修復 → 部署 → 觀測。

### 3.7 關鍵開源專案對照表
| 專案 | 定位 | 技術棧 | 核心特色 | 連結 |
|------|------|--------|----------|------|
| **yt-rag** | RAG 教學基礎版 | FastAPI, Supabase/pgvector, OpenAI Embeddings | 文件切塊、向量化、API 端點、Cloud Run 部署 | `github.com/shanshengchen/yt-rag` |
| **yt-agentic-rag** | Agentic RAG 進階版 | FastAPI, Supabase, Google Calendar/Gmail API, Function Calling | 多輪對話、工具呼叫、排程會議、發送確認信 | `github.com/shenshongchen/yt-agentic-rag` |
| **Hermes Agent** | 本地優先自演進 Harness | Python, SQLite, Markdown Skills, MCP, Gemini/Claude | `soul.md`、Loop Engineering、三層記憶檔案、自我迭代、WhatsApp/Desktop Gateway | `github.com/newresearch/hermes` (200k+ stars) |
| **Waku-Agent** | Graph 架構生產級框架 | Python, LangGraph 隱含, MCP, Dashboard + CLI | Graph 定義（並行/非確定節點）、Retrieval Gate、LLM Ops 回饋、社群工作流分享 | `github.com/shanshongchen/waku-agent` |
| **AutoManus** | B2B 銷售 AI 接待員產品 | MCP Server, REST API, WhatsApp Business API, Web Chat Widget | 共用 WhatsApp 路由、線索管線、MCP 一鍵部署、沙箱驗證、批次處理 | `automatus.io` / `automannus.io` |


## 中英金句與解釋

| 原文 | 中文翻譯 | 脈絡與解釋 |
|------|----------|------------|
| "If we can reduce the amount of automation of using agents for cases where it doesn't really need an agent, then your system will be more reliable." | 如果我們能減少在不需要 Agent 的場景中使用自動化 Agent，系統會更加可靠。 | **分段 1**：步驟固定、確定性高的流程應優先用傳統工作流（Deterministic Workflow），避免濫用 LLM 引入隨機性。 |
| "The Q&A agent is just like the central brain or the CEO of the company who needs to do all the communication with their customers." | Q&A Agent 就像是公司的中央大腦或 CEO，負責所有與客戶的溝通。 | **分段 1**：多 Agent 架構中，Q&A Agent 為唯一對外接口，協調內部 Planner、Tools，對外統一口徑。 |
| "Smart defaults are more important than infinite customization." | 智慧預設比無限客製化更重要。 | **分段 3**：使用者不會寫 Prompt，產品應內建領域最佳實務作為預設，減少決策疲勞與失誤。 |
| "Meet users where they are, don't change how users work today." | 在使用者所在位置滿足他們，別改變他們今天的工作方式。 | **分段 3**：B2B 產品須嵌入既有工具鏈（Excel、Notion、CRM），零遷移成本才能落地。 |
| "Vertical first strategy… high volume, detailed, domain-specific examples will make the model stop doing stupid stuff." | 垂直優先策略……大量、詳細、領域特定的範例能讓模型不再做蠢事。 | **分段 3**：投資人建議：用 20-30 筆高密度範例「鎖定」模型行驶，驗證 PMF 再做 Mixture-of-Experts 水平擴展。 |
| "Multi-line, step-by-step natural language instructions will minimize hallucination and give an agent stable, predictable behavior." | 多行、逐步的自然語言指令能將幻覺降到最低，讓 Agent 行為穩定可預測。 | **分段 3**：工作流規格用自然語言寫成詳細 SOP（何時呼叫什麼工具、參數怎麼傳、例外怎麼處理），優於 JSON/表格直餵。 |
| "If an agent messes things up, it's almost always, almost always, your prompt's fault instead of the model's fault." | 若 Agent 搞砸了，幾乎永遠是提示詞的錯，而非模型的錯。 | **分段 4**：創辦人朋友語錄，強調 Prompt Engineering 是杠桿點，模型選擇是次要。 |
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

### 官方專案與文檔
- **課程原始推文**：https://x.com/LunarResearcher/status/2084984207495827776
- **講者個人網站 / 社群入口**：https://shangchen.io（私有 Discord、雙月直播、原始系統設計圖 Excalidraw 檔）
- **Automatus / AutoManus 產品官網**：https://automatus.io / https://automannus.io
- **Hermes Agent Harness 官網**：https://hermes-agent.newresearch.com

### GitHub 開源專案（按學習階段排序）
1. **RAG 基礎教學專案**：`github.com/shanshengchen/yt-rag`
   - FastAPI + Supabase pgvector，含 `main.py`、`services/rag.py`、`sql/init_supabase.sql`、`test_setup.py`、`Dockerfile`
2. **Agentic RAG 進階專案**：`github.com/shenshongchen/yt-agentic-rag`
   - 整合 Google Calendar/Gmail API、Function Calling、多輪對話
3. **Hermes Agent Harness**：`github.com/newresearch/hermes` (200k+ stars)
   - 本地優先、`soul.md`、Loop Engineering、三層記憶檔案、MCP、WhatsApp/Desktop Gateway
4. **Waku-Agent**：`github.com/shanshongchen/waku-agent` (700+ stars)
   - Graph 架構、Dashboard/CLI、Retrieval Gate、LLM Ops 回饋、社群工作流 PR 機制
5. **MCP Server (AutoManus)**：`github.com/automatus/mcp-server`（需自行搜尋確認）

### 核心工具與服務
| 類別 | 工具/服務 | 用途 |
|------|-----------|------|
| **向量資料庫** | Supabase (pgvector), Pinecone, Weaviate | 儲存 Embedding、語義檢索 |
| **LLM 提供商** | OpenAI (GPT-4o, text-embedding-3-large), Anthropic (Claude 3.5 Sonnet), Google (Gemini 3.1) | 生成、Embedding、評估 |
| **後端框架** | FastAPI, Uvicorn | 高效能非同步 API 服務 |
| **雲端部署** | Google Cloud Run, Cloud Build, Docker | 容器化部署、環境變數/Secrets 管理 |
| **觀測與評估** | Langfuse, LangSmith | Tracing、Eval、LLM-as-a-judge |
| **通訊閘道** | WhatsApp Business API, Web Chat Widget | 客戶端接入 |
| **開發工具** | Cursor IDE, Claude Code, OpenClaw | 程式碼生成、MCP 整合、本地 Agent 開發 |
| **資料庫** | PostgreSQL (pgvector), SQLite (`state.db`) | 結構化資料、向量、事件記憶 |

### 參考公司與案例
- **客服/客體驗 AI 服務商**：Fin, Ada, Sierra AI
- **人工介入案例**：DoorDash
- **多 Agent 系統範例**：Notion
- **確定性工作流代表 (2023)**：Airflow, AWS Step Functions
