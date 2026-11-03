---
title: Andrew Ng 與 LangChain 的 LangGraph Agent 課程
type: video
source_url: https://x.com/AnatoliKopadze/status/2088684163167670725
source_site: X
language: en
duration: 110m 12s
added: '2026-08-20'
topics:
- agents
summary: 課程完整示範如何使用 LangGraph 從零建構具備規劃、工具調用、反思、持久化、人機介入與時間旅行能力的生產級 Agent 系統，並延伸至多代理協作與流程工程架構。
abstract: 本影片為 DeepLearning.AI 與 LangChain 合作課程，由 Andrew Ng 主持，Harrison Chase (LangChain CEO) 與 Anatoli Kopadze 等講師共同講解，完整示範從零構建具備工具調用、持久化、人機回路與時間旅行能力的 Agent 系統。核心框架為 LangGraph，以有向循環圖建模 Agent 行為，核心抽象為 Nodes、Edges、Conditional Edges 及 State 持久化。課程涵蓋 Agentic Workflow 設計模式、ReAct 模式實作、平行/序列工具調用、Checkpointer 與 Thread 機制、Human-in-the-loop 中斷點、狀態快照與時間旅行、結構化輸出、Plan-and-Execute + Reflection 循環架構（Essay Writer 專案），並延伸介紹 Multi-agent、Supervisor、Flow Engineering (LATS) 等進階架構。全程以程式碼實作為主，強調可控性、可除錯性與生產級部署考量。
---

## 完整摘要

### Agentic Workflow 基礎與 LangGraph 核心架構
Andrew Ng 開場對比傳統 Zero-shot LLM 生成與 Agentic Workflow：後者引入 Planning、Tool Use、Reflection、Multi-agent Collaboration、Memory 五大設計模式，讓模型能迭代產出、自我修正。Harrison Chase 指出過去一年關鍵進展為 Function Calling 穩定工具調用，以及 Agentic Search (如 Tavily) 回傳結構化答案而非連結。LangGraph 以有向循環圖建模流程，三大核心概念為 Nodes (代理/函式)、Edges (固定流向)、Conditional Edges (決策分流)，內建 State 持久化支援 Human-in-the-loop 與斷點續傳。State 定義使用 TypedDict 搭配 Annotated[..., operator.add] 實現訊息與中間步驟的累加語義，未標註欄位則為覆寫。編譯後的 Graph 即為 LangChain Runnable，支援 invoke/stream/batch 標準介面。

### ReAct Agent 實作、工具調用與狀態管理
課程先以純 Python + OpenAI API 手刻 ReAct 迴圈：系統提示詞定義 Thought→Action→Pause→Observation 格式，正則解析 Action 呼叫工具 (calculate、average_dog_weight)，while 迴圈自動執行至 Answer 或達 max_turns。隨後遷移至 LangGraph：定義 call_model (LLM 節點)、action (工具節點)、should_continue (條件邊) 三節點，利用 operator.add 合併訊息。展示現代 LLM 的平行工具調用 (一次產生多個 tool_calls 並行 invoke) 與序列調用 (需前一工具結果才能決定下一步，如查超級盃冠軍→再查該州 GDP)。引入 SqliteSaver (記憶體模式) 作為 Checkpointer，配合 thread_id 實現多會話隔離與持久化，graph.stream 可串流訊息層級事件供前端即時顯示。

### 人機回路、時間旅行與進階狀態操作
透過 compile(interrupt_before=["action"]) 在呼叫工具前暫停，配合 get_state 取得當前狀態與 next 節點、update_state 修改工具參數 (如將查詢地點從洛杉磯改為路易斯安那)。get_state_history 列出所有歷史快照 (含唯一 thread_ts)，以歷史 config 呼叫 stream 實現時間旅行：回溯至過去分支重新執行。示範手動插入 ToolMessage 並指定 as_node="action"，欺騙圖認為工具已執行完成，直接進入 LLM 節點生成最終回答。引入自訂 reduce_messages 函數處理同 ID 訊息取代邏輯，支援人機回路中修正工具呼叫。非同步串流使用 astream_events 搭配 AsyncSqliteSaver 逐 token 推送。最終專案 Essay Writer 採用 Plan-and-Execute + Reflection 循環：planner→research_plan→generate→(reflect→research_critique→generate...) 迴環，狀態包含 task、plan、draft、critique、content、revision_number、max_revisions。

### Essay Writer 完整專案與進階架構展望
完整構建寫作代理人：使用 Pydantic 模型 Queries 強制 LLM 結構化輸出查詢列表，確保可直接迭代呼叫 Tavily。五大節點分工明確：planner 產大綱、research_plan 依計畫搜尋累加 content、generate 撰寫草稿並遞增 revision_number、reflect 產出 critique、research_critique 依評論補充搜尋。條件邊 should_continue 依 revision_number >= max_revisions 決定 END 或進入 reflect。編譯時傳入 MemorySaver 並設定 interrupt_after 針對各節點中斷，配合教學用 GUI 實現逐步執行、檢視快照、修改狀態、時光旅行、多執行緒隔離。課程總結三種擴展架構：Multi-agent (共享單一 State)、Supervisor (監督者路由子代理，各擁獨立 State)、Flow Engineering/AlphaCodium (線性管線夾雜關鍵迴圈)。尾聲強調 LangGraph 核心價值為高度可控性，支援任意循環/非循環流程建構，並說明 Language Agent Tree Search (LATS) 需仰賴持久化實現回溯與父節點更新。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| Agentic Workflow (代理式工作流) | 將 LLM 從單次生成轉為迭代流程：規劃→執行→檢視→修正，模擬人類寫作過程，顯著提升產出品質。包含 Planning、Tool Use、Reflection、Multi-agent Collaboration、Memory 五大設計模式。 | "an agentic workflow asks AI to use a much more iterative workflow... write a draft outline... do web research... write first draft... critique it... improve it" (00:00:23-00:00:48) |
| LangGraph 圖抽象 (Nodes, Edges, Conditional Edges, State) | 以有向循環圖建模 Agent 控制流。Nodes 為處理單元 (LLM 或函式)，Edges 為固定流向，Conditional Edges 為決策分流。State 為全域可見資料結構，使用 operator.add 註解欄位實現累加 (如訊息、中間步驟)，未註解者為覆寫。編譯後為標準 LangChain Runnable。 | "Three of the core concepts of Langraph are nodes, edges, and conditional edges... annotated with operator.add... it doesn't override the existing messages, but rather it adds them to that state" (00:12:47-00:14:29) |
| Checkpointer 與 Thread 機制 | Checkpointer (如 MemorySaver, SqliteSaver, AsyncSqliteSaver) 在每個節點前後保存狀態快照，配合 thread_id 識別會話執行緒，實現跨請求記憶、中斷續跑、多會話隔離。生產環境需外接 PostgreSQL/Redis。 | "A checkpointer basically checkpoints the state after and between every node... thread config is simply a dictionary with a configurable key... thread ID" (00:02:48-00:05:10) |
| Human-in-the-loop 與 Interrupt 機制 | 編譯時指定 interrupt_before 或 interrupt_after 讓圖在特定節點暫停，前端可取得狀態供人工審核/修改工具參數，再透過 update_state 寫回並恢復執行。支援針對高風險工具 (刪除、發送郵件) 進行把關。 | "pass this interrupts-before equals action parameter... add an interrupt before we call the action node... requires manual approval" (00:29:52-00:30:19) |
| 時間旅行 | 利用 get_state_history 取得歷史快照的 thread_ts，以該 config 呼叫 stream/invoke 從過去分支重新執行，實現實驗不同決策路徑、修正錯誤、A/B 測試。會產生新分支，原分支保留。 | "This is effectively time travel... call graph.stream again, pass in none, and now notice that we're passing in toreplay.config" (00:34:24-00:39:01) |
| Plan-and-Execute + Reflection 循環 (Essay Writer) | 複雜任務架構：Planner 產大綱 → Researcher 依計畫搜尋累加素材 → Writer 生成草稿 → Critic 反思產出評論 → Researcher 依評論補充搜尋 → Writer 再生成... 以 revision_number 與 max_revisions 控制迴圈終止。狀態欄位豐富 (task, plan, draft, critique, content, revision_number, max_revisions)。 | "generate a plan... do some research... generate... reflect... another research step... append those... go all the way back to the generate step" (01:25:44-01:26:37) |
| 結構化輸出與 Function Calling | 使用 Pydantic 模型 (如 Queries: List[str]) 限制 LLM 輸出格式，配合 bind_tools 或 with_structured_output 確保回傳可直接迭代的 JSON，避免正則解析失敗，提升工具調用穩定性。 | "For generating these list of queries to pass to Tavily, we're going to use function calling to ensure that we get back a list of strings from the language model." (01:29:04-01:29:11) |
| Agentic Search 與標準搜尋差異 | Agentic Search 針對機器消費：理解問題→拆解子查詢→選擇最佳資料源 (API/搜尋引擎)→Chunking+向量檢索→評分過濾→回傳結構化 JSON。標準搜尋回傳連結給人類點擊，需人工清洗。Agentic Search 適合下游 Agent 直接引用。 | "This is the exact answer an agent would want, as structure data... That's exactly the difference between what a human need and what an agent need" (01:00:53-01:01:19) |
| Flow Engineering 與 Language Agent Tree Search (LATS) | Flow Engineering 為設計代理資訊流向的工程化思維。LATS 將決策建模為樹狀搜尋：生成動作→反思→擴展子節點→反思，並能根據反思回溯至較早節點並更新父節點資訊 (back-propagate)，引導後續搜尋。持久化為回溯必要條件。 | "it can basically reflect on where in the tree of action states it wants to jump back to. So it can back propagate and update parent nodes to have more information... you need to be able to go back in time to previous states" (第六段金句 3,4) |
| LangGraph 可控性定位 | LangGraph 核心差異化價值為高度可控性：開發者精確定義圖結構、邊緣條件、錯誤處理，支援任意循環/非循環流程，而非被框架預設流程綁死。適合需精細控制的生產級 Agent 系統，但學習曲線較高。 | "LingGraph is really aimed at being highly controllable and allowing you to create these cyclical or non-cyclical flows. This degree of controllability is really what differentiates it from other frameworks" (第六段金句 5) |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| That's a bit like asking someone, could you please type out an essay for me by writing from the first word to the last word in one go without ever using backspace. | 這有點像請某人幫我打一篇文章，要求從第一個字打到最後一個字，中間絕不使用退格鍵。 | Andrew Ng 形容傳統 Zero-shot LLM 生成的不自然。 |
| With agentic workflows, we ended up taking a much more iterative approach to deriving results... does much better than forcing the AI to write from start to finish. | 採用代理式工作流時，我們採取了更迭代的方式產出結果……效果遠優於強迫 AI 從頭寫到尾。 | Andrew Ng 肯定迭代流程優於單次生成。 |
| To my surprise, I actually completely forgotten that I also gave the agent a Wikipedia search option. This agent pivoted from saying, web search isn't working. Let me do a Wikipedia search instead. | 令我驚訝的是，我完全忘記還給了 Agent 維基百科搜尋選項。Agent 從『網頁搜尋失效』自主轉向『改用維基百科搜尋』。 | Andrew Ng 親身見證 Agent 自主容錯與決策能力。 |
| Langraph helps you describe and orchestrate that control flow... allows you to create cyclic graphs... built in persistence. | LangGraph 幫助你描述並編排控制流……允許建立循環圖……內建持久化。 | Harrison Chase 定義 LangGraph 定位。 |
| This persistence also enables really cool human in the loop features. | 這種持久化也啟用了非常酷的人機回路功能。 | 說明持久化帶來 HITL 能力。 |
| The state that is tracked over time... is local to the graph, and it can be stored in persistence layer, meaning that you can resume with that state at any point in time later on. | 隨時間追蹤的狀態……屬於圖的局部，可存於持久化層，意味著你未來可隨時帶著該狀態恢復執行。 | 解釋 State 可序列化、可恢復。 |
| This is effectively time travel. | 這實際上就是時光旅行。 | 示範使用歷史 thread_ts 回溯分支重跑。 |
| The crucial thing here, and the differentiator between the next thing that we'll see, is that they all work on the same shared state... Let's contrast that with a supervisor agent... those agents themselves could have different states inside them... One term that's popped up a bunch recently is flow engineering... looking at it, you can see that it's basically a pipeline, but there are a few key nodes where there's actually a loop. | 關鍵在於它們都在同一個共享狀態上運作……對比監督者代理……那些代理內部可能擁有不同狀態……近期常聽到的術語是流程工程……觀察可見它基本上是管線，但在幾個關鍵節點存在迴圈。 | 對比 Multi-agent、Supervisor、Flow Engineering 三種架構。 |

## 可參考資料
- **LangGraph 官方文件**：核心框架文件，含 Nodes/Edges/State/Checkpointer/HITL/Time Travel/Streaming 完整 API 說明。 — <https://langchain-ai.github.io/langgraph/>
- **LangChain 官方文件**：基礎框架文件，含 ChatModel、Tools、Runnable、Prompt Hub、Community Tools 等。 — <https://python.langchain.com/>
- **Tavily Search API**：課程示範使用的 Agentic Search 服務，回傳結構化答案，適合 Agent 消費。 — <https://tavily.com/>
- **ReAct 論文 (Reasoning + Acting)**：早期 Agent 範式來源，LangGraph 示範從零實作該模式。 — <https://arxiv.org/abs/2210.03629>
- **Language Agent Tree Search (LATS) 論文**：樹狀搜尋+反思+回溯架構，影片尾聲作為 Flow Engineering 代表範例介紹。 — <https://arxiv.org/abs/2310.04406>
- **AlphaCodium / Flow Engineering 論文**：程式碼生成 SOTA 架構，線性管線夾雜關鍵迴圈，啟發 Flow Engineering 概念。 — <https://arxiv.org/abs/2401.08500>
- **DeepLearning.AI 課程：Functions, Tools, and Agents with LangChain**：講師建議的前置課程，奠基 LangChain 工具與 Agent 基礎。 — <https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/>
- **LangSmith 平台**：生產級 Debug/Monitor/Playground/Evaluation 工具鏈，配合 LangGraph 部署觀測。 — <https://www.langchain.com/langsmith>
- **LangServe**：將 LangGraph 應用打包為 API 服務的部署工具。 — <https://github.com/langchain-ai/langserve>
