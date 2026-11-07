---
title: Building Effective AI Agents
type: article
source_url: https://www.anthropic.com/engineering/building-effective-agents
source_site: anthropic.com
added: '2026-09-08'
topics:
- agents
summary: 成功的 AI agent 系統不在於使用複雜框架，而在於採用簡單可組合的模式、優先考慮透明度與工具介面設計，並只在單輪 LLM 無法解決問題時才引入多步驟 agentic 系統。
abstract: Anthropic 分享過去一年與數十個團隊合作建構 LLM agents 的實務經驗，區分 workflows（預定義代碼路徑）與 agents（LLM 動態自主決策）兩種架構，並提供六種常見工作流模式與 agent 設計原則，強調從簡單提示詞開始、只有在必要時才增加複雜度。
---

## 完整摘要

### 核心定義：Agentic Systems、Workflows 與 Agents 的架構區分
Anthropic 將所有具備 LLM 自主性的系統統稱為「agentic systems（代理式系統）」，但在架構上劃分為兩類：Workflows 指 LLM 與工具由預先寫好的代碼路徑編排，適合定義明確、需一致性的任務；Agents 則指 LLM 根據環境回饋動態規劃自身流程與工具使用，保有對完成方式的控制權，適合開放式、步驟難以預測的問題。文章建議開發者先尋找最簡單方案——許多場景僅需優化單輪 LLM 呼叫（加上 retrieval 與 in-context examples）即可，只有當靈活性與模型驅動的決策能顯著提升效果時，才值得付出額外延遲與成本引入多步驟 agentic 系統。

### 六種生產級 Workflow 模式與適用場景
文章依複雜度遞增介紹五種 workflow 模式：1) Prompt chaining：將任務拆解為固定子任務序列，每輪 LLM 處理上一輪輸出，可在中間加入程式化閘門檢查，適用於可乾淨分解的任務（如生成文案再翻譯、寫大綱再正文）。2) Routing：先分類輸入再導向專門的下游流程，避免單一提示詞兼顧多類別導致效能下降，適用於客服分流、簡易問題導向小模型、困難問題導向大模型。3) Parallelization：包含 Sectioning（獨立子任務並行）與 Voting（同任務多輪取多樣輸出），前者如護欄檢查與核心回應分開執行，後者如多視角審查程式碼漏洞。4) Orchestrator-workers：中央 LLM 動態拆解任務、分派給多個 worker LLM 並彙整結果，適用於無法預先確定哪些檔案需要修改的程式變更。5) Evaluator-optimizer：一個 LLM 生成初稿、另一個 LLM 依評估標準回饋並迭代修正。

### Agents：自主規劃與環境互動的循環架構
Agents 在關鍵能力成熟（理解複雜輸入、推理規劃、可靠使用工具、錯誤恢復）後浮現於生產環境。其運作循環為：接收人類指令或對話澄清任務 → 獨立規劃執行 → 每步從環境獲取「ground truth」（工具結果、代碼執行輸出）評估進度 → 於檢查點或受阻時暫停請求人類介入 → 完成或觸發停止條件（如最大迭代次數）結束。實作上常只是「LLM 在迴圈中根據環境回饋使用工具」，因此工具集與文檔設計（ACI，agent-computer interface）至關重要。Anthropic 自身範例包括解決 SWE-bench Verified 跨多檔案 GitHub issue 的 coding agent，以及操作電腦完成任務的 Computer Use 參考實作。

### 三大設計原則與框架使用建議
文章總結三項核心原則：1) 保持簡潔——agent 設計應盡量簡單；2) 優先透明化——明確展示 agent 的規劃步驟；3) 精心打造 ACI——投入與人機介面同等精力設計工具文檔與測試。關於框架，雖有 Claude Agent SDK、Strands Agents SDK、Rivet、Vellum 等工具降低門檻，但抽象層易遮蔽底層 prompt/response 導致難除錯，且誘使過度設計。建議先直接用 LLM API 實作（幾行代碼即可），若用框架必須理解底層代碼，錯誤假設是常見錯誤來源。附錄 2 進一步建議給模型足夠 token 先思考、讓工具格式貼近自然文本、避免行號計數與 JSON 轉義開銷，並以防呆設計（Poka-yoke）如強制絕對路徑來降低工具呼叫失誤。

### 實務應用領域：客服與程式開發
附錄 1 指出兩大高價值場域：A) 客服：天然符合對話流程且需外部資訊與動作（查詢訂單、退款）、成功標準明確（用戶定義解決）、可量化衡量，已有公司採用按成功付費模式。B) 程式開發：代碼解法可經自動化測試驗證、agent 可用測試結果迭代、問題空間結構化、品質可客觀衡量。Anthropic 自身 agent 已能在 SWE-bench Verified 基準上單憑 PR 描述解決真實 GitHub issue，但人工審查仍關鍵以確保符合整體系統需求。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| Workflow vs Agent 架構區分 | Workflow 的控制流在代碼中預先寫死（如 prompt chaining、routing 的分支邏輯由開發者決定），Agent 的控制流由 LLM 在運行時根據觀察動態決定（何時呼叫何工具、何時轉向、何時結束）。這不是能力強弱之分，而是「誰決定下一步」的區別。Anthropic 強調：若任務步驟可預測，workflow 更可靠、成本更低；只有當步驟無法硬編碼時才需 agent。 | 文章「What are agents?」一節定義：Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks. |
| Augmented LLM 為基礎建構塊 | 所有模式的共同基石是擁有 retrieval、tools、memory 三項增強能力的 LLM。模型主動生成搜尋查詢、選擇工具、決定記憶讀寫。Anthropic 推出 Model Context Protocol (MCP) 作為整合第三方工具的標準化介面。實作重點在於：針對具體用例裁剪能力、提供清晰易用的介面給 LLM。 | 「Building block: The augmented LLM」一節與圖 1 所示：LLM 中心，下方三模組 Retrieval（Query/Results）、Tools（Call/Response）、Memory（Read/Write）。 |
| Evaluator-Optimizer 迴圈模仿人類寫作迭代 | 此模式讓一個 LLM 生成初稿，另一個 LLM 依明確評估標準給予反饋並決定是否接受，若拒絕則帶著具體反饋回給生成器重寫。關鍵在於：人類能清楚說明如何改進時、LLM 也能給出同等品質反饋時最有效。適用於文學翻譯（細微語感需多輪潤飾）、需多輪搜尋的複雜研究任務。 | 「Workflow: Evaluator-optimizer」一節：two signs of good fit: LLM responses can be demonstrably improved when a human articulates their feedback; and the LLM can provide such feedback. 圖 6 顯示 Generator → Solution → Evaluator → Accepted/Rejected+Feedback 迴圈。 |
| 工具設計即 ACI（Agent-Computer Interface），需投入同等 HCI 努力 | 工具定義格式對 LLM 成功率影響極大。Anthropic 在 SWE-bench 專案中發現：相對路徑導致 agent 切換目錄後出錯，改為強制絕對路徑後模型完美使用。原則：給模型足夠 tokens 思考、格式貼近自然文本分布、避免格式開銷（如行數計數、JSON 轉義）、參數命名像寫給初級工程師的 docstring、在 workbench 大量測試觀察失敗模式、Poka-yoke（防呆設計）讓錯誤更難發生。 | Appendix 2 完整內容：We actually spent more time optimizing our tools than the overall prompt... changed the tool to always require absolute filepaths—and we found that the model used this method flawlessly. |
| 框架抽象層帶來除錯困難與過度設計風險 | 框架（Claude Agent SDK、Strands、Rivet、Vellum）簡化了呼叫 LLM、定義工具、串聯調用等底層任務，但引入額外抽象層遮蔽 prompt 與 response 細節，導致除錯困難；且易誘使開發者在簡單方案足夠時仍加入不必要複雜度。Anthropic 建議：先直接用 API 實作模式（幾行代碼），若用框架必須讀懂底層代碼，錯誤假設是常見客戶錯誤來源。 | 「When and how to use frameworks」一節：they often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug... Incorrect assumptions about what's under the hood are a common source of customer error. |
| Agent 部署需沙箱測試與防護機制 | Agent 的自主性帶來更高成本與錯誤複合風險。Anthropic 建議在沙箱環境大量測試、設置適當防護（guardrails）、包含最大迭代次數等停止條件。這不是理論建議，而是自身構建 coding agent 與 computer use demo 的實務經驗總結。 | 「Agents」一節：The autonomous nature of agents means higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails. |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs. | 在 LLM 領域，成功不在於建構最複雜的系統，而在於建構適合你需求的正確系統。 | Summary 區段開頭，強調務實原則：從簡單提示詞開始，只有在簡單方案不足時才引入複雜 agentic 系統。 |
| When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. | 建構 LLM 應用時，我們建議尋找最簡單的解決方案，僅在必要時增加複雜度。這可能意味著完全不建構 agentic 系統。 | When (and when not) to use agents 區段，直接說明何時不應使用 agent。 |
| One rule of thumb is to think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces (ACI). | 一個經驗法則：思考人機介面 (HCI) 投入多少精力，就規劃投入同等精力建構良好的 agent-電腦介面 (ACI)。 | Appendix 2 關於工具設計的核心建議，強調工具文檔與介面設計的重要性。 |
| Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production. | 框架能幫你快速上手，但在進入生產環境時，不要猶豫減少抽象層、改用基礎組件構建。 | Summary 區段三大原則總結後的框架建議。 |

## 可參考資料
- **Claude Agent SDK**：Anthropic 官方提供的 agent 開發 SDK，文中列為框架範例之一。 — <https://platform.claude.com/docs/en/agent-sdk/overview>
- **Strands Agents SDK by AWS**：AWS 提供的 agent 框架，文中列為框架範例之一。 — <https://strandsagents.com/latest/>
- **Rivet**：拖拉式 GUI LLM workflow 建構工具，文中列為框架範例之一。 — <https://rivet.ironcladapp.com/>
- **Vellum**：另一個建構與測試複雜 workflow 的 GUI 工具，文中列為框架範例之一。 — <https://www.vellum.ai/>
- **Model Context Protocol (MCP)**：Anthropic 發布的標準化協議，讓開發者以簡單 client 實作整合第三方工具生態系。 — <https://www.anthropic.com/news/model-context-protocol>
- **MCP Client 建構教學**：MCP 官方教學，示範如何建構 client 連接工具生態系。 — <https://modelcontextprotocol.io/tutorials/building-a-client#building-mcp-clients>
- **Anthropic Cookbook: Patterns - Agents & Basic Workflows**：提供本文提到各種模式的範例實作代碼。 — <https://platform.claude.com/cookbook/patterns-agents-basic-workflows>
- **SWE-bench / SWE-bench Verified**：Anthropic 用於評估 coding agent 能力的基準測試，文中多次引用為 agent 實際表現證據。 — <https://www.anthropic.com/research/swe-bench-sonnet>
- **Computer Use Demo (anthropic-quickstarts)**：Claude 使用電腦完成任務的參考實作，作為 agent 應用範例。 — <https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo>
- **Tool Use GA 發布公告**：Claude 正式支援工具調用功能的發布說明，Appendix 2 參考此文件定義 tool use block 格式。 — <https://www.anthropic.com/news/tool-use-ga>
- **Tool Use 文檔 - tool use block 範例**：API 回應中 tool use block 的具體格式範例。 — <https://docs.anthropic.com/en/docs/build-with-claude/tool-use#example-api-response-with-a-tool-use-content-block>
- **Anthropic Console Workbench**：Appendix 2 建議用於大量測試工具使用、觀察模型錯誤模式的互動式環境。 — <https://console.anthropic.com/workbench>
- **Poka-yoke (防呆設計) - Wikipedia**：Appendix 2 引用的製造業防錯設計概念，應用於工具參數設計使錯誤更難發生。 — <https://en.wikipedia.org/wiki/Poka-yoke>
- **How we built Claude Managed Agents**：文章開頭註記：工具生態已變化，最新做法請參考此文與 Managed Agents 文檔。 — <https://www.anthropic.com/engineering/managed-agents>
- **Managed Agents Documentation**：Claude Managed Agents 的官方文檔入口。 — <https://platform.claude.com/docs/en/managed-agents/overview>
- **Erik S. 與 Barry Zhang**：文章作者（Acknowledgements 註明），內容基於他們在 Anthropic 建構 agent 的經驗與客戶洞見。
