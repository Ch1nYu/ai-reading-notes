---
title: Agentic workflow 讓 GPT-3.5 在 HumanEval 達到 95.1%
type: article
source_url: https://x.com/N01ennn/status/2097264706088014123
source_site: X
added: '2026-09-09'
topics:
- agents
summary: 透過結合反思、工具使用、規劃與多智能體協作的 agentic 模式，並以 Harness‑Loop‑Graph 三層結構搭配 GPT-6 Astra 的異步工具呼叫與即時指令調整，可將 296 個智能體縮減為一個具備驗證與復原能力的統一系統。
abstract: 這份筆記整理了 NO1ennn 在 X 上的兩篇貼文，首篇展示了透過 agentic 工作流讓 GPT-3.5 在 HumanEval 基準測試上達到 95.1% 的表現；第二篇則深入探討了如何透過 Harness、Loop 與 Graph 三層工程，將大量智能體組織為單一可控結構，並說明 GPT-6 Astra 在此架構中的角色與零信任設計原則。
---

## 完整摘要

### Agentic 工作流提升 GPT-3.5 在 HumanEval 的表現
作者指出，在 GPT-3.5 上加入四種設計模式——反思（draft, check, revise）、工具使用（retrieve information and test）、規劃（split the task into steps）與多智能體協作（assign distinct responsibilities），使其在 HumanEval 基準測試上的得分從零樣本的 48.1% 提升至 95.1%，遠超 GPT-4 在單次直接回答時的 67.0%。這些模式分別對應於草擬與自我檢查、外部知識檢索與驗證、任務

### Harness、Loop 與 Graph 三層工程的概念與區別
Harness engineering 指的是周邊機制：上下文、工具、權限、持續性、控制、安全與可觀測性，決定模型能存取什麼以及如何執行。Loop engineering 是具體的觀察‑行動‑驗證循環，包含明確觸發與以證據為基礎的停止規則，而非無盡重試。Graph engineering 則以節點與邊模型工作流拓撲，控制允許的下一步、分支、併發、狀態轉移與復原路徑。作者強調，混淆這三層會導致昂貴失誤：未理解行為就繪製圖表、讓同一模型自行評分、製造無上限重試迴圈、在 harness 中塞入過多工具或過於寬鬆權

### GPT-6 Astra 的特性與零信任設計原則
GPT-6 Astra 作為節點內的模型，提供四項關鍵功能：異步工具呼叫（允許在長運行任務時繼續推理、呼叫其他工具或回答獨立請求）、即時指令調整（mid‑turn steering，在不重啟節點的情況下接受更正或需求變更）、每階段推理力度調整（透過 configuration_update 改變節點難易度而不破壞前緩存）以及錯誤監測（misalignment monitoring，由 harness 層負責）。基於零信任論文，作者列出五條規則：僅基於證據前進、限制重試次數、終止狀態必須為驗證輸出或記錄拒絕、

### 實證發現：迴圈失敗與倉庫掃描結果
IAL-Scan 對 6,549 個 LLM agent 倉庫進行分析，發現 68 個確定的無限 agentic 迴失敗（IAL），精準度 91.9%，其中 95.6% 伴隨 API 成本耗盡與模型拒絕服務。LangGraph 與 AutoGen 各自貢獻了 23 與 22 起失敗，因其透過 API 而非可見語法編碼回饋，使失敗在程式碼審閱中不易被發現。另外，對 36,710 個工程軟體倉庫的掃描顯示只有 0.59% 的倉庫運行自主 agent 迴圈，且大多數僅在 pull-request 事件或排程上執行

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 四種設計模式（Reflection、Tool Use、Planning、Multi‑Agent Collaboration） | 這四種模式分別對應於草擬並自我檢查、透過工具檢索外部知識與驗證、將任務分解為可執行步驟，以及分配明確的智能體職責，共同形成反思‑工具‑規劃‑協作的閉環。 | 在 GPT-3.5 上加入這四種模式後，HumanEval 得分從零樣本的 48.1% 提升至 95.1%，遠高於 GPT-4 單次回答的 67.0%。 |
| Harness engineering 決定模型可存取的上下文、工具、權限與持續性 | Harness 為智能體提供執行環境，包括可以呼叫的工具、所允許的權限範圍、狀態的持續機制以及安全與可觀測性設施，直接影響模型能否正確且安全地完成任務。 | 文中描述：Harness engineering is the surrounding machinery: context, tools, permissions, persistence, control, safety, observability. |
| Loop engineering 提供觀察‑行動‑驗證循環與明確停止規則 | Loop 不是無盡重試，而是基於證據（例如程式碼編譯通過、測試綠燈）來決定是否繼續或停止，以防止資源浪費與失控。 | Loop engineering is the repeated observe / act / verify cycle with explicit triggers and evidence-based stopping rules, rather than 'keep trying.' |
| Graph engineering 以節點與邊模型工作流拓撲，使控制流程可視 | 透過將任務分解為子目標的依賴圖、定義智能體拓撲（鏈、路由、扇出/扇入）以及記錄具來源與版本的狀態，圖工程能追蹤錯誤源頭、允許併發並提供從檢查點恢復的機制。 | Graph Engineering makes the relations explicit across three views: Task Organization, Agent Coordination, Runtime State Management. |
| GPT-6 Astra 支援異步工具呼叫、即時指令調整、每階段推理力度調整與錯誤監測 | 異步工具讓長時間任務不阻斷推理；mid‑turn steering 允許在不重啟節點的情況下接受新指令；每階段推理力度可依節點難易度動態調整；錯誤監測則由 harness 層負責，及時發出不對齊警告。 | Async tool calling. Set async: true on a function or custom tool, and Astra continues reasoning, calls other tools, or answers independent parts of a request while your application runs the long one... Mid-turn steering... Reasoning effort per stage... Misalignment monitoring. |
| 零信任五條規則：僅基於證據前進、限制重試次數、終止狀態必須為驗證輸出或記錄拒絕、權限按步驟分配、使用者自行掌控圖結構 | 這五條規則直接來自零信任論文，旨在確保每個智能體的行動都有可驗證的結果，避免無意義的重試、越權操作以及模型自行決策下一步。 | Progress only on evidence: code, deploy, test green. Not on agent prose, and not on a workflow run that exited zero without doing anything. / Cap retries, or the swarm never stops. / The end state is a verified output or a logged refusal. / Permissions are per step, not per session. / You own the graph. |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| 95.1% on HumanEval with an agentic workflow. | 在具備 agentic 工作流的情況下，於 HumanEval 基準測試上達到 95.1%。 | 作者在第一篇貼文中強調 GPT-3.5 與 agentic 工作流的表現。 |
| 67.0% for GPT-4 answering in one pass. | GPT-4 在單次直接回答時的 HumanEval 分數為 67.0%。 | 同上，用來對比 agentic 工作流的提升。 |
| without three layers, 296 agents is noise. With them, 296 agents collapse into one structure. | 若缺少這三層（Harness、Loop、Graph），296 個智能體只是雜訊；具備這三層時，它們會縮減為單一結構。 | 第二篇文章闡述三層架構的必要性。 |
| Progress only on evidence: code, deploy, test green. Not on agent prose, and not on a workflow run that exited zero without doing anything. | 僅在有證據時才前進：程式碼、部署、測試通過。不要僅依賴智能體的文字描述，也不將未實際執行任何工作且退出碼為零的工作流視為進展。 | 零信任論文中的第一條規則。 |
| The reason the distinction matters is that mixing them up produces expensive failures: drawing graphs before understanding behavior, letting the same model grade its own work without safeguards, creating unbounded retry loops, stuffing the harness with too many tools or overly broad permissions, and blaming the model for orchestration problems that belong to a different layer. | 區分這三層的重要在於，混淆它們會導致昂貴失誤：在尚未理解行為前就繪製圖表、讓同一模型在沒有防護措施的情況下自行評分、製造無上限的重試迴圈、在 harness 中塞入過多工具或過於寬鬆的權限，以及將屬於其他層的協調問題歸咎於模型本身。 | 作者解釋為什麼必須區分 Harness、Loop、Graph。 |

## 可參考資料
- **Andrew Ng**：報告 GPT-3.5 與 GPT-4 在 HumanEval 的基準數據
- **DeepLearning.AI**：作者 Andrew Ng 所屬的機構，提供背景資訊
- **Anthropic**：提出五種工作流模式的參考
- **LangGraph**：用於圖工程的 Pregel-style 超步模型，提供節點與邊的程式實現
- **OpenAI Agents SDK**：區分 agents-as-tools 與 handoffs 的機制，影響多智能體協調設計
- **CrewAI**：提供 max_iter 等迴圈控制參數的範例
- **AutoGen**：產生無限迴圈失敗的研究對象，顯示隱蔽回饋路徑的風險
- **Towards Agentic Cloud Engineering: Graph and Loop Engineering with a Zero-Trust Agent Harness (arXiv 2609.00050)**：零信任論文的原始出處，提出三層架構與五條規則
- **影片截圖與技術報告頁面**：展示 From Loop Engineering to Graph Engineering 的圖表與關鍵數據 — <https://video.twimg.com/amplify_video/2097066348039794688/vid/avc1/1300x1742/ikaQuFNyIxKc4shI.mp4?tag=29>
- **來源推文（第一篇）**：本筆記的主要來源，包含 agentic 工作流與 GPT-3.5 表現 — <https://x.com/N01ennn/status/2097264706088014123>
- **來源推文（第二篇）**：第二篇文章的來源，詳細說明 Harness、Loop、Graph 與 GPT-6 Astra — <https://x.com/N01ennn/status/2096962591125905888>
