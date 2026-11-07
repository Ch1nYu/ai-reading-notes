---
title: Reducing cost and improving performance with Claude Platform
type: article
source_url: https://x.com/ClaudeDevs/status/2097369738968195513
source_site: X
added: '2026-09-09'
topics:
- practice
summary: 透過優化提示詞快取、清理過時提示詞指令、精準調整 effort 等級，並善用 claude-api 技能的自動化審計與搜尋功能，開發者可在維持或提升效能的同時大幅降低 Claude API 成本。
abstract: 這篇文章由 ClaudeDevs 團隊發布，詳細說明如何在不犧牲效能的前提下降低 Claude Platform 的使用成本，提出三大核心策略：最大化提示詞快取命中率、移除升級前沿模型時的提示詞反模式、以及根據任務校準 effort 參數，並提供三個內建指令（prompt-audit、cost-optimize、hillclimb）幫助開發者自動化成本優化流程。
---

## 完整摘要

### 提示詞快取（Prompt Cache）機制與優化策略
文章首先解釋提示詞快取的運作原理：Claude 在生成回應前會將提示詞轉換為內部工作狀態（prefill），這是處理輸入最昂貴的步驟。快取儲存這個鍵值（KV）狀態，當後續請求具有相同前綴時直接讀取而非重新計算，快取讀取價格僅為完整輸入價格的一小部分。快取有三大限制：綁定特定模型、前綴必須位元級完全相同、有限的存活時間（TTL，預設 5 分鐘）。基於此，文章列出八項具體優化建議：監控快取命中率與失敗原因；將低頻工具標記為 defer_loading 避免污染快取前綴；將系統提示詞更新改為以訊息形式插入；請求結構將靜態上下文（工具定義與系統提示詞）置於前端、動態增長的對話置於後端；在壓縮等快取本就會失效的時機才切換模型或 effort；啟用自動快取讓斷點隨對話推進；以 `max_tokens: 0` 預熱快取；當工具或子代理執行超過 5 分鐘時改設 1 小時 TTL。

### 移除前沿模型的提示詞反模式
升級到前沿 Claude 模型時，舊提示詞中針對舊模型弱點設計的指令可能成為反模式，反而增加成本並降低效能。文章列舉六類常見反模式：驗證儀式（如「雙重檢查」）、徹底度與強調助推器（如「極度徹底」、「關鍵：必須」）、強制程序與草稿腳手架（如固定步驟思考）、過時範例、矛盾規則、過時配置（如手動思考預算）。作者在 Opus 4.8 遷移至 Opus 5 的客服基準測試中，逐一植入這六個反模式，發現運行 /claude-api prompt-audit 移除反模式後，平均成本下降 14.6%、準確率提升 5.3%。

### Effort 參數校準與成本效能權衡
Effort 控制 Claude「努力程度」：低 effort 結論較快，高 effort 會審議、驗證、探索替代方案。同一模型不同 effort 等級的成本效能差異顯著：Fable 5 在 FrontierCode Diamond 基準上，低 effort 得分 11.5%、每任務 $5.35；高 effort 得分 30.9%、每任務 $19.00，分數提升約 2.7 倍、成本約 3.5 倍。Fable 5.1 在 Humanity's Last Exam 上，低 effort 約 53%、$0.30/任務，高 effort 約 61%、$2.23/任務，最後一階僅增加 0.5 分卻多花 46% 成本；而在 CursorBench 3.2 上，Fable 5.1 低 effort 能以約 1/3 的成本達到與 Fable 5 高 effort 相當的表現。

### 自動化成本優化工具鏈：prompt-audit、cost-optimize、hillclimb
文章介紹三個內建於 claude-api 技能的指令：`/claude-api prompt-audit` 掃描工作目錄中的提示詞、技能、工具描述，移除常見反模式；`/claude-api cost-optimize` 從組織用量報告、API 回應 usage 物件或請求建構代碼分析 token 支出，依序應用快取優化、修剪請求載荷、限制輸出、批次處理無人值守工作，若提供評測還會跨模型與 effort 等級搜尋最佳配置。實測四個公開基準：LegalBench 成本降 ~58%、tau2-bench retail 降 72%、OfficeQA Pro 從 $136.20 降至 $64.87、SWE-bench Verified 成本降 ~55%。

### 實戰遷移案例：從 Opus 4.8 到 Sonnet 5 的成本與效能雙贏
作者展示完整遷移流程：起始於 Opus 4.8 高 effort 基線（訓練集準確率 98.9%），hillclimb 先嘗試 Opus 5 低 effort 並配合 prompt-audit 移除強制工具調用儀式、草稿步驟、矛盾規則，成本降至 2.6 分/張單；再降級至 Sonnet 5 低 effort 成本僅 1 分/張單但準確率跌至 88.9%，根據失敗案例補充路由規則與退款上限交叉參考，Sonnet 5 恢復至 98.9% 且成本不變。在 14 張未見測試單上，最終配置達 90.5% 對基線 78.6%，成本僅約原始配置的五分之一。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 提示詞快取（Prompt Cache） | Claude 將提示詞前綴轉換為內部 KV 快取狀態，相同前綴的後續請求可直接讀取快取而非重新計算 prefill，快取讀取價格遠低於完整輸入。快取綁定模型、要求位元級完全一致、預設 TTL 5 分鐘。任何動態數值（時間戳、ID）、工具定義順序變更、effort 設定變更（Opus 5 和 Fable 5.1 除外）、對話分支前綴不一致都會導致快取失效。 | 文章〈Prompt cache〉段落：「Prompt caching saves that state (the key–value, or KV, cache): when a request starts with the same prefix, Claude reads it back instead of recomputing it. Cache reads are billed at a fraction of the full input price.」並列出四項破壞快取的常見情況與七項修正建議。 |
| 提示詞反模式（Prompt Anti-patterns） | 針對舊模型弱點設計的提示詞指令在前沿模型上可能適得其反。六大類包括：驗證儀式導致字面執行重複工具調用；強調助推器觸發過度搜尋；強制程序與草稿腳手架與模型原生推理疊加浪費 token；過時範例教導冗長推理鏈；矛盾規則被更字面地執行導致效能下降；過時配置被新 API 拒絕。移除這些反模式可同時降低成本與提升準確率。 | 文章〈Instructions〉段落實驗：在客服基準上植入六個反模式，遷移至 Opus 5 後運行 prompt-audit，平均成本下降 14.6%、準確率提升 5.3%。具體案例：驗證儀式導致每次退款重複查詢訂單；強調助推器觸發數十次不必要知識庫搜尋；手動草稿與 Opus 5 內建思考衝突導致工具調用寫在推理中未執行。 |
| Effort 參數校準 | Effort 決定模型思考深度，並非越高越好。高 effort 可能過度思考增加成本延遲並降低品質；低 effort 可能過早停止基於部分資訊答題。關鍵在於任務形狀：在非飽和評測上，若成本效能曲線平坦則任務不受思考算力限制，提高 effort 無益。較強模型在低 effort 下可能比較弱模型高 effort 更便宜且效能相當（如 Fable 5.1 低 effort 在 CursorBench 3.2 匹配 Fable 5 高 effort、成本僅 1/3）。 | 文章〈Effort〉段落數據：Fable 5 在 FrontierCode Diamond 上低 effort 11.5%/$5.35、高 effort 30.9%/$19.00；Fable 5.1 在 Humanity's Last Exam 上低 effort ~53%/$0.30、高 effort ~61%/$2.23，最後一步僅增 0.5 分卻多花 46% 成本，落在雜訊範圍內。CursorBench 3.2 上 Fable 5.1 低 effort 匹配 Fable 5 高 effort、成本 1/3。 |
| hillclimb 自動化搜尋 | hillclimb 指令給定評測集，自動拆分訓練/測試集，提出配置變更，閱讀失敗訓練案例修正提示詞，最終在未見測試集驗證。作者在客服基準上從 Opus 4.8 高 effort 起步，hillclimb 依序嘗試 Opus 5 低 effort + prompt-audit、Sonnet 5 低 effort + 補充路由規則與退款交叉參考，最終配置在 14 張舉出測試單達 90.5% 準確率、成本約為原始 1/5。 | 文章〈Effort〉→〈How to fix it〉段落完整記錄 hillclimb 運行過程與數據：起始 Opus 4.8 高 effort 98.9% 訓練準確率；Opus 5 低 effort + prompt-audit 後 2.6 分/單；Sonnet 5 低 effort 1 分/單但 88.9%，補充規則後恢復 98.9%；測試集 90.5% 對基線 78.6%。 |
| cost-optimize 綜合成本審計 | cost-optimize 從組織用量報告、API 回應 usage 物件或請求代碼估算 token 支出，依優先序應用：提示詞快取、修剪請求載荷（含 prompt-audit）、限制輸出、批次處理無人值守工作。若提供評測，進一步跨模型與 effort 等級搜尋。四個公開基準實測：LegalBench 透過共享前綴快取、低 effort、Batch API 成本降 ~58%；tau2-bench retail 透過顯式快取斷點降 72%；OfficeQA Pro 透過批次處理與文件快取從 $136.20 降至 $64.87；SWE-bench Verified 透過中 effort 限制輸出，中位步數 29→17、prompt tokens 75.2M→33.7M、成本降 ~55%。 | 文章〈Automating cost reduction〉段落 Figure 7 總結四基準實測數據與優化手段。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Performance and cost are often viewed as a trade-off: to spend less, you accept worse results. | 效能與成本常被視為取捨：要花較少錢，就得接受較差的結果。 | 文章開頭核心論點，指出實務上透過三大修正可打破這個迷思。 |
| Cache reads are billed at a fraction of the full input price. | 快取讀取的計費價格僅為完整輸入價格的一小部分。 | 解釋提示詞快取機制的經濟效益。 |
| Running /claude-api prompt-audit removed the anti-patterns, decreasing costs by 14.6% and increasing accuracy by 5.3% on average. | 運行 /claude-api prompt-audit 移除反模式後，平均成本下降 14.6%、準確率提升 5.3%。 | Opus 4.8 遷移 Opus 5 客服基準實驗的量化結果。 |
| A stronger model at low effort can be cheaper than a weaker model working hard (high effort). | 較強模型在低 effort 下可能比較弱模型在高 effort 下更便宜。 | Effort 校準章節的核心洞見，以 Fable 5.1 低 effort 對比 Fable 5 高 effort 為例。 |
| On the 14 held-out tickets the search never saw, the final configuration scored 90.5% against the original setup's 78.6%, at about one-fifth the cost. | 在 14 張搜尋過程未見過的舉出測試單上，最終配置達 90.5% 準確率，而原始配置為 78.6%，成本約為原始的五分之一。 | hillclimb 自動化搜尋在客服基準上的最終驗證結果。 |

## 可參考資料
- **claude-api skill**：內建於 Claude Code 的技能，提供 prompt-audit、cost-optimize、hillclimb 三個指令，為文章核心工具鏈。
- **Claude Console**：提供提示詞快取診斷介面，可查看快取命中率與失敗原因。
- **Cache Diagnostics API**：程式化獲取提示詞快取診斷資訊，包含失敗原因與請求差異位置。
- **Claude Admin API**：cost-optimize 可從組織用量與成本報告獲取 token 支出分析。
- **Batch API**：cost-optimize 在 LegalBench 基準上建議使用批次處理無人值守工作以進一步降低成本。
- **FrontierCode Diamond**：最難 50 個任務的程式設計基準，用於展示 Fable 5 不同 effort 等級的成本效能曲線。
- **Humanity's Last Exam**：不使用工具的綜合基準，用於展示 Fable 5.1 不同 effort 等級的遞減邊際效益。
- **CursorBench 3.2**：用於對比 Fable 5.1 低 effort 與 Fable 5 高 effort 成本效能的基準。
- **tau2-bench retail**：cost-optimize 實測基準之一，透過顯式快取斷點放置成本降 72%。
- **OfficeQA Pro**：cost-optimize 實測基準之一，透過批次處理與文件快取成本從 $136.20 降至 $64.87。
- **SWE-bench Verified**：cost-optimize 實測基準之一，透過中 effort 限制輸出成本降 ~55%。
- **LegalBench**：cost-optimize 實測基準之一，透過共享前綴快取、低 effort、Batch API 成本降 ~58%。
- **Lance Martin (@RLanceMartin)**：文章合著者之一。
- **Brad Abrams (@brada)**：文章合著者之一。
- **Isabella He (@IsabellaKHe)**：文章合著者之一。
- **Ben Lehrburger (@benlehrburger)**：文章合著者之一。
- **Claude Blog 文章連結**：原文發布推文連結，文末「See this article on the Claude Blog here」指向此處。 — <https://x.com/ClaudeDevs/status/2097369738968195513>
