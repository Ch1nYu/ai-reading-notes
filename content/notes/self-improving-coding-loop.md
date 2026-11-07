---
title: 用 DeepSeek V4 Flash 在 Codex 建立自我改進編碼循環
type: article
source_url: https://x.com/cyrilXBT/status/2088542962854629672
source_site: X
added: '2026-09-13'
topics:
- coding-agents
summary: CyrilXBT 公開自動化自我優化編碼循環與 10 週 Graph Architect 實戰課程，提供從工具設定到求職級作品集的完整路徑。
abstract: CyrilXBT 分享兩項 AI 開發實戰資源：一是利用 DeepSeek v4-flash 於 Codex 內建立自我改進編碼循環（3 模型、2 文件、3 分鐘設定）；二是從零開始的 10 週「Graph Architect」完整課程，涵蓋知識圖譜建構、實體抽取管線、代理圖設計與作品集專案，並附上 Anthropic、Neo4j、arXiv 等公開教材。
---

## 完整摘要

### 自我改進編碼循環（Self-Improving Coder Loop）
首則推文展示一個可在 2 分鐘內於 Codex 部署的自我改進循環：克隆 repo「codex-self-imrpoving-loop」，將「3 loop workflow」圖片交給代理即可運行。系統採用三模型協作——DEEPSEEK 執行任務、LUNA 評估並寫入 log.md、SOL 依評估重寫 prompt.md——並以 watcher.md 與 rewriter.md 兩份規則文件限制行數不超過 12 行、Prompt 增長不超過 20%。作者表示已將 Opus 5 換為 DeepSeek v4-flash，在不犧牲品質的前提下大幅降低自動迭代迴圈的執行成本。

### Graph Architect 10 週課程架構與核心技能
課程分四階段：第 1-2 週建立「為何圖譜優於純檢索」的概念並完成手動實體關係繪製練習；第 3-4 週依 Anthropic 官方 Cookbook 實作四階段管線——抽取、解析、組裝、查詢——並強調實體解析的關鍵性；第 5-6 週轉向代理圖設計，採用不可變計畫、分離層級、嚴格升級三大承諾，將代理決策顯性化為狀態圖；第 7-10 週構建兼具知識圖譜與代理圖的作品集專案，要求誠實記錄失敗模式與修正過程。

### 學習資源、就業路徑與持續精進習慣
作者列出三大公開資源：Anthropic Claude Cookbook（知識圖譜建構）、DeepLearning.AI Andreas Kollegger 課程（代理知識圖譜端到端）、2026 年 4 月 arXiv 論文（代理圖設計理論）。就業面強調「Graph Architect」尚非標準職稱，建議以 AI Engineer、Agent Systems Engineer 等職缺投遞並亮出作品集；自由案源較易切入。長期習慣方面，要求從第 1 週起建立錯誤日誌，記錄每次抽取、解析、查詢失敗的輸入、問題、修正方式與驗證結果，並定期回顧整理為可複用原則，在啟動新任務前調取相關經驗形成複利。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 自我改進編碼循環 | 在 Codex 內以三模型（DEEPSEEK、LUNA、SOL）與兩文件（watcher.md、rewriter.md）形成自動迭代：DEEPSEEK 執行、LUNA 評估寫 log、SOL 依評估改 prompt，並限制程式碼 ≤12 行、Prompt 增長 ≤20%，達到低成本自優化。 | 推文第 1 條列出 3 步驟設定，圖片 OCR 顯示三節點循環與 watcher/rewriter 規則細節。 |
| 知識圖譜四階段管線 | 依 Anthropic 官方流程：Extract（單一文件抽實體與三元組）、Resolve（語意聚類同一實體不同寫法）、Assemble（建立帶溯源的標準節點與邊）、Query（子圖序列化交模型推理並引用具體邊）。 | Phase Two 完整列出四階段定義與 Extract/Resolve 範例 Prompt。 |
| 實體解析為新手最大盲點 | 同一實體不同表述（如 Edwin Aldrin vs Buzz Aldrin）若僅靠字串比對會誤判；需用模型結合上下文語意聚類，並同時防範誤合併與漏合併兩種錯誤。 | Phase Two 強調 Resolve 步驟最被低估，並要求手動檢查錯誤類型。 |
| 代理圖三大承諾 | 不可變計畫（鎖定執行計畫不隨模型即興改變）、分離層級（規劃、執行、恢復互為獨立角色）、嚴格升級（失敗恢復遵循預設協議且有重試上限），以可審計性換取靈活度。 | Phase Three 明列三大承諾與設計意圖。 |
| 作品集專案以誠實紀錄失敗為核心價值 | 招聘方關注的是真實除錯紀錄：解析錯誤、查詢缺口、重試上限設定理由等，而非視覺化成品；作者建議公開完整 Prompt、Schema、圖結構。 | Phase Four「What Makes A Project Actually Demonstrate Competence」段落詳細說明。 |
| 錯誤日誌習慣決定長期成長 | 從第 1 週起以具體、有日期條目記錄每次失敗的輸入、錯誤、修正、驗證結果；定期回顧並整理為可複用原則，再於啟動新任務前調取相關經驗，形成複利。 | 「Building The Habit That Actually Compounds」一節完整闡述。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| holy sh*t this is an absolute gold mine | 天哪，這簡直是絕對的金礦 | 推文開頭表達對自我改進循環價值的極高評價。 |
| Zero prior experience isn't a disadvantage here the way it would be in a mature field. It's the actual starting condition almost everyone in this space shares. | 零經驗在這裡不像成熟領域那樣是劣勢，它幾乎是這個領域所有人共同的實際起點。 | 課程開頭說明為何現在切入 Graph Architect 沒有經驗劣勢。 |
| The difference between a portfolio project that gets you hired and one that doesn't isn't complexity, it's honesty about what actually works and what doesn't. | 能讓你被錄取的作品集專案與不能的區別不在複雜度，而在於對什麼真正有效、什麼無效的誠實度。 | Phase Four 強調作品集需記錄失敗模式而非僅展示成功。 |
| Keep a running log of every extraction error, resolution mistake, and query failure you encounter, from week one through week ten and beyond. | 從第 1 週到第 10 週乃至之後，持續記錄遇到的每一個抽取錯誤、解析失誤與查詢失敗。 | 「Building The Habit That Actually Compounds」節點提出的核心習慣建議。 |

## 可參考資料
- **codex-self-imrpoving-loop**：自我改進編碼循環的程式碼倉庫，推文指示克隆此 repo 即可啟動。
- **Anthropic Claude Cookbook - Knowledge Graph Construction**：官方公開的知識圖譜建構指南，涵蓋 Extract/Resolve/Assemble/Query 四階段管線。
- **DeepLearning.AI - Agentic Knowledge Graph Construction by Andreas Kollegger**：Neo4j Innovation Lead 主講的完整課程，涵蓋端到端代理知識圖譜建構與多代理系統。
- **arXiv paper (April 2026) - Agentic Graph Design Framework**：提出不可變計畫、分離層級、嚴格升級三大承諾與五步驟結構的理論基礎論文。
- **Excalidraw**：推文附圖所使用的線上白板工具，展示自我改進循環流程圖與規則文件。 — <https://excalidraw.com>
