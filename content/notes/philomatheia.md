---
title: Philomatheia：以證據為本的學習 skill
type: article
source_url: https://github.com/Ch1nYu/philomatheia
source_site: GitHub
added: '2026-09-06'
topics:
- coding-agents
- practice
summary: Philomatheia 以目標導向的知識地圖、五層級掌握度追蹤與跨會話精確檢查點，將學習過程結構化、證據化並可中斷續接。
abstract: Philomatheia 是一個持久化、基於證據的學習技能，能將學習目標轉為可視的知識地圖，透過小型適應性迴路教學，記錄學習者實際能展示的能力，並在跨會話中從精確檢查點恢復。它適用於任何可載入技能目錄的代理框架（如 Codex、Claude Code），旨在培養持久能力而非一次性答案。
---

## 完整摘要

### 專案定位與解決的問題
Philomatheia 針對傳統學習流程的四大痛點：固定目錄不符個人目標、接觸或測驗即視為完成、依賴聊天記錄恢復進度、單一路徑無法適應個別差異。它改為：依學習者目標建構必要的先備知識主幹；分別追蹤回憶、解釋、引導使用、獨立使用、遷移五個層級的掌握度；將完整狀態持久化到專案目錄的 .philomatheia/learning-state.json，不需重讀對話歷史；根據觀察到的證據動態調整前沿節點大小、呈現方式、提示與複習。專案明確聲明 v0.2.0 為 alpha 狀態，狀態模型、驗證器、安裝程式已測試，但長期學習成效尚無對照或縱向研究證實。

### 核心運作流程與資料結構
流程為：目標與限制 → 經核准的目標子圖與完成契約 → 2-3 個活躍前沿節點（負荷高時降為 1 個） → 擷取→解釋→預測→練習→驗證→整合 → 產生證據、掌握度、複習與精確檢查點 → 進入下一螺旋迴圈。每個學習專案擁有獨立的 .philomatheia/ 目錄，包含 learning-state.json（機器可讀的真實來源）、LEARNING.md（面向學習者的簡潔投射）、artifacts/（作為證據的可選工作產出）。路徑由學習者控制：目標變更、必要節點變更、目標掌握度變更、完成契約變更皆需重新核准；僅有教學微調可在證據支持下自動發生。

### 可觀測的操作效果與驗證機制
設計目標為產生可觀測的操作效果：新會話能直接接續待解決問題而非重建聊天歷史；大量提示下的正確答案不建立獨立掌握度；先備知識閘門不可因目標權重高而跳過；後續失敗可降低當前掌握度但保留歷史證據；完成需同時滿足必要目標子圖與獨立整合任務；來源衝突與未知項保持可見。倉庫提供確定性的狀態不變量檢查腳本與可重現的行為評估指引，不保證分數提升、學習加速、專業勝任力或長期保留率提高。EVALUATION.md 列出目前證據狀態、行為情境與縱向驗證協定。

### 安裝、啟動與技術需求
支援 Node.js 18+ 透過 npx philomatheia 直接執行，或 clone 後執行平台專屬安裝腳本（Windows 用 PowerShell 7，macOS/Linux 用 POSIX shell）。安裝程式僅複製執行期檔案，列出已知框架與狀態供選擇，預設不勾選任何項目，按 Enter 即不更動系統。支援 --list、--all、--update、--dry-run、--dest-root 等旗標。啟動方式：在專屬空資料夾開啟代理，輸入學習目標與限制（如每週四小時），要求診斷現況並提出首條知識地圖路徑供核准。也支援「從精確檢查點恢復、從一題回憶開始、不重複已完成內容」等指令。核心腳本需 Python 3.10+，無第三方套件相依。

### 設計靈感、授權與擴充點
靈感來源為 ai-engineering-from-scratch 專案與 ChongWen 的技能設計筆記，將其泛化為使用者自定義學習流程，不捆綁原課程內容。採 MIT 授權，貢獻同授權。倉庫結構包含 SKILL.md（觸發邊界與核心工作流）、references/（知識地圖、教學、證據、狀態、來源、領域規則）、scripts/（專案初始化、狀態驗證、套件檢查）、assets/（初始 JSON 與 Markdown 模板）、agents/openai.yaml（可選顯示元資料）、EVALUATION.md。外部研究工具在需要當前或專業來源時仍可能被呼叫。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 目標導向知識地圖 | 不使用預設目錄，而是根據學習者具體目標（如「能批判性閱讀 ML 論文的統計學」）反向建構必要的先備知識主幹，形成有向無環圖；每個節點記錄來源、關係與重要宣稱的出處，學習者可見並可要求修改。 | README「Why use it」表格對比：傳統「Follows a fixed table of contents」→ Philomatheia「Builds the useful prerequisite trunk around the learner's goal」；「How it works」流程圖起點為「goal and constraints」經過「approved goal subgraph and completion contract」。 |
| 五層級掌握度追蹤 | 將掌握度拆解為回憶、解釋、引導使用、獨立使用、遷移五個可觀測層級，分別記錄證據。大量提示下的正確答案只能計入較低層級，不可直接建立獨立使用或遷移層級的掌握度。 | README 表格：傳統「Marks a lesson complete after exposure or a quiz」→ Philomatheia「Tracks recall, explanation, guided use, independent use, and transfer separately」；「What effect means here」列出「a correct answer with heavy hints cannot establish independent mastery」。 |
| 跨會話精確檢查點 | 完整學習狀態序列化為 .philomatheia/learning-state.json，包含當前前沿節點、各節點掌握度證據、複習排程、完成契約等。新會話啟動時直接載入此檔案，無需重讀聊天歷史即可從上一題待解決問題繼續。 | README 表格：傳統「Restarts from chat history」→ Philomatheia「Persists an exact, self-contained checkpoint in the project」；「How it works」列出 .philomatheia/ 目錄結構與 learning-state.json 為「machine-readable source of truth」。 |
| 基於證據的自適應前沿 | 每輪僅聚焦 2-3 個活躍前沿節點（認知負荷高時降為 1 個），根據觀察到的證據動態調整前沿大小、呈現表徵、提示策略與複習間隔。教學微調可自動發生，但結構性變更需學習者核准。 | 「How it works」流程圖：「2-3 node active frontier, or 1 when load requires it」→「retrieve -> explain -> predict -> practise -> verify -> integrate」→「evidence, mastery, review, and exact checkpoint」；「The route remains learner-controlled... Small teaching adjustments can happen automatically when evidence supports them。」 |
| 可驗證的狀態不變量與評估協定 | 提供 deterministic checks（scripts/validate_state.py）驗證狀態不變量，以及 EVALUATION.md 定義的行為情境與縱向驗證協定。專案明確不承諾學習成效提升，僅保證操作層面的可觀測效果。 | 「What effect means here」列出六項可觀測效果；「Requirements」與「Validate locally」給出驗證指令；「Project status」註記「Long-term learning-outcome improvements have not yet been established by a controlled or longitudinal study.」。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Philomatheia turns a learning goal into a visible knowledge map, teaches through small adaptive loops, records what the learner can actually demonstrate, and resumes from an exact checkpoint across sessions. | Philomatheia 將學習目標轉為可視的知識地圖，透過小型適應性迴路教學，記錄學習者實際能展示的能力，並在跨會話中從精確檢查點恢復。 | 專案 README 開頭的核心定位敘述，概括四大核心能力。 |
| Project status: `v0.2.0` alpha. The state model, validators, and installers are tested. Long-term learning-outcome improvements have not yet been established by a controlled or longitudinal study. | 專案狀態：`v0.2.0` alpha。狀態模型、驗證器與安裝程式已測試。長期學習成效改善尚未經對照或縱向研究證實。 | 專案狀態聲明，誠實揭露現階段驗證範圍與局限。 |
| Philomatheia is useful when the desired result is durable ability rather than a one-off answer. It deliberately stays out of generic research, ordinary code review, and work completed on the user's behalf without a learning goal. | 當期望結果是持久能力而非一次性答案時，Philomatheia 很有用。它刻意不介入一般研究、普通程式碼審查、以及無學習目標下替用戶完成的工作。 | 說明適用場景與刻意排除的使用情境。 |

## 可參考資料
- **ai-engineering-from-scratch**：Philomatheia 的設計靈感來源之一，將其課程結構泛化為使用者自定義學習流程。 — <https://github.com/rohitg00/ai-engineering-from-scratch>
- **ChongWen's notes on Skill design**：Philomatheia 的設計靈感來源之二，關於 Agent Skill 設計的筆記。 — <https://www.chongwenz.cn/tech/AI/ai-skill-01/>
- **SKILL.md**：定義技能觸發邊界與核心學習工作流，代理框架據此判斷是否啟用 philomatheia。 — <https://github.com/Ch1nYu/philomatheia/blob/main/SKILL.md>
- **EVALUATION.md**：記錄目前證據狀態、行為情境與縱向驗證協定，說明專案不承諾學習成效提升。 — <https://github.com/Ch1nYu/philomatheia/blob/main/EVALUATION.md>
- **INSTALL.md**：手動安裝、釋出套件與其他框架的安裝說明。 — <https://github.com/Ch1nYu/philomatheia/blob/main/INSTALL.md>
- **README.zh-TW.md**：繁體中文版說明文件。 — <https://github.com/Ch1nYu/philomatheia/blob/main/README.zh-TW.md>
- **Agent Skills 標準**：Philomatheia 遵循的 Agent Skill 開放標準，可在支援該標準的框架（Codex、Claude Code 等）中載入。 — <https://agentskills.io/>
