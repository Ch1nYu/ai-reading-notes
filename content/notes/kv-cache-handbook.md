---
title: Understanding KV Cache Handbook
type: article
source_url: https://drive.google.com/file/d/12KlRm0YLYrfpLF2q3_tBDNMMkJ7_bYNF/view
source_site: drive.google.com
added: '2026-09-13'
topics:
- llm-internals
summary: KV 快取利用因果遮罩使過去層狀態對未來 token 不變，避免重複計算 Key/Value 投影，但隨序列增長帶來記憶體容量與頻寬壓力，需透過注意力架構變體與系統級管理（分頁、前綴共享、卸載、量化）在計算、容量、頻寬三維資源間取得平衡。
abstract: 本手冊《Understanding KV Cache》（Handbook 03 - Understanding AI Series，作者 @techNaak）從第一性原理出發，系統闡述大型語言模型推論中 KV 快取的運作機制、記憶體模型與優化權衡。內容涵蓋自回歸解碼的預填充與解碼兩階段、KV 快取的數學有效性、記憶體估算公式、注意力架構變體（MHA、MQA、GQA、MLA）對 KV 成本的不同影響，以及 PagedAttention、前綴快取、卸載與量化等系統級優化如何實際改變計算、容量與頻寬三種資源的權衡。
---

## 完整摘要

### 自回歸解碼與 KV 快取的基本機制
解碼器語言模型依條件機率 p(x_{t+1}|x_{1:t}) 生成 token，形成 x_1 → x_2 → … → x_T 的依賴鏈，因此推論自然分為「預填充（Prefill）」與「解碼（Decode）」兩階段。Prefill 階段在因果遮罩下一次並行處理所有提示詞 token，建立初始 KV 快取；Decode 階段則逐 token 產出新的 k_t、v_t 並附加至快取，查詢向量對完整歷史做注意力。KV 快取的核心價值在於避免重複計算歷史 token 的投影（q/k/v），大幅降低計算量；但並不消除注意力機制對歷史 Key/Value 的讀取，隨著序列長度 T 增長，記憶體容量與頻寬壓力隨之上升。手冊並指出 KV 快取不儲存「符號事實」，僅為各層、各 token 位置的中間 Key/Value 狀態，物理佈局取決於推論引擎實作。

### 記憶體資源三維度與注意力變體對 KV 成本的影響
手冊明確區分三種資源：計算（投影與注意力的算術運算）、容量（儲存龐大 K/V 狀態所需記憶體空間，隨上下文線性增長）與記憶體流量/頻寬（解碼時反覆讀取 K/V 張量的位元組傳輸量）。KV 快取大幅減少計算，但容量與頻寬仍是主要瓶頸。標準多頭注意力（MHA）的快取規模隨頭數線性增長；多查詢注意力（MQA）將所有查詢頭共享單一 Key/Value 頭（H_KV=1），大幅縮減快取體積但品質無數學保證；群組查詢注意力（GQA）在 MHA 與 MQA 間取折衷，查詢頭分組共享 K/V 頭（1< r_kv < r_hq），實驗顯示品質接近 MHA、速度可比 MQA；多頭潛在注意力（MLA）則透過壓縮潛在表示而非僅共享頭部來降低 KV 成本。記憶體估算公式 Key = 2 × L × D_h × D_t（2 代表 K 與 V 兩張矩陣及每元素位元組數）說明快取隨層數、頭數、頭維度與 token 數線性增長。

### 系統層面優化：分頁快取、前綴共享、卸載與量化
PagedAttention 受作業系統虛擬記憶體啟發，將邏輯序列切分為固定大小區塊，映射至非連續物理 KV 快取區塊，區塊表記錄地址映射，支援動態分配/釋放與前綴共享（vLLM block caching），核心觀念為 logical token history ≠ contiguous physical allocation。前綴快取跨請求重用已計算的 KV 區塊，僅減少預填充階段計算（例：10k tokens 可節省 20‑30% 查詢處理時間），不加速解碼階段；正確性需比對模型身分、配置、適配等狀態，而非僅 token 文本。當 GPU 快取滿載時，需採用驅逐策略（LRU 風格、優先級租戶、保護活躍序列區塊等）將可重用區塊移出，儘管不影響模型正確性但會增加未來請求的端到端延遲；卸載至 CPU/磁碟可擴大容量，但資料搬移延遲可能超過重新計算成本。KV 快取量化以較低精度（16‑bit → 8‑bit/FP8/INT8）儲存激活值，理論儲存需求減半，實際部署需處理對齊、量化參數與後端專用佈局，量化引入噪聲影響未來注意力計算；現行 LLM 框架允許選擇性保留特定層或注意力類型不量化，反映量化不需均一化。多租戶環境下快取命中會改變延遲，未驗證讀取可能洩漏他人快取狀態，xULP 機制將風險納入最後區塊的可快取性，並主張 coarse‑domain、shard‑cache、trust‑domain 原則以降低側信道攻擊。

### 常見認知捷徑與量化工程權衡
手冊列舉六大錯誤心智模型：將 KV Cache 視為模型記憶體、認為 KV Cache 能使解碼時間恆定等，並逐一糾正。量化並非免費：將 16-bit 降至 8-bit/FP8/INT8 雖理論減半儲存，但對齊、量化參數、後端佈局會引入額外開銷與精度損失，實際節省不等於理論位元寬度比例；且量化噪聲會傳遞至未來注意力計算，需在記憶體/硬體成本與模型品質間取捨。選擇性量化（保留特定層或注意力類型不量化）雖降低理論 KV Cache，但引入異質精度管理複雜度，工程實作需評估收益與複雜度權衡。手冊僅 33 頁，目標為建立理解而非詳盡實作細節，深度實作仍需參考其他資料。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| KV 快取（KV Cache） | 在每個自注意力層、每個 token 位置儲存該層的 Key 投影與 Value 投影，使後續解碼步驟可重用這些中間狀態，避免重複計算歷史 token 的 q/k/v 投影。快取不儲存符號事實，物理佈局屬實作細節。 | 第5頁「What exactly is cached?」給出完整數學定義與附加邏輯；第7頁表格對比 Prefill/Decode 的快取動作與查詢長度；第5頁「What is not cached by this idea」說明非符號性質。 |
| Prefill 與 Decode 兩個執行階段 | Prefill 階段利用因果遮罩一次並行處理所有提示詞 token，建立初始 KV 快取；Decode 階段則逐 token 產出新的 k_t、v_t 並附加至快取，查詢向量對完整歷史做注意力。兩階段的快取建立方式不同，Prefill 是並行初始化，Decode 是循序附加。 | 第3頁「Why decoding is sequential」與流程圖；第7頁章節標題「The cache is created differently in the two phases」。 |
| 三種資源維度：計算、容量、記憶體流量/頻寬 | 三者在解碼階段扮演不同角色：計算（FLOPs）在 Prefill 為主導瓶頸，Decode 階段隨序列增長轉為記憶體頻寬受限；容量決定可支援的最大上下文長度與並發請求數；頻寬決定 Decode 步進的延遲下限。MQA/GQA 主要降低頻寬需求（讀取較少 K/V 頭），而非大幅減少計算（投影仍需對所有查詢頭計算）。將三者混為一談會導致優化方向錯誤，例如只優化 FLOPs 卻忽略頻寬牆。 | 第12頁「Three different resources / Do not collapse these into one」與 MQA 採用動機說明；第12頁「KV caching avoids recomputing... But for ordinary decoder attention, the new query still needs access to past K/V state. As T grows, the attention operation for the new position will interact with a longer history.」 |
| 注意力變體 MQA、GQA、MLA 對 KV 成本的影響 | MQA 讓所有查詢頭共享單一 Key/Value 頭（H_KV=1），將快取體積壓縮至 MHA 的 1/H 倍，但品質下降無數學保證（Shazeer 警告「Beware of the cliff!」）；GQA 將查詢頭分組共享 K/V 頭（1< r_kv < r_hq），以分組數作為超參數在品質與速度間取得經驗平衡；MLA（DeepSeek-V2）透過低秩壓縮潛在表示（而非僅共享頭部）降低 KV 維度，改變了快取的數學結構。三者機制不同：MQA/GQA 是結構性共享，MLA 是表示壓縮。 | 第2頁學習目標第4項；第10頁數值範例表格（MHA/GQA/MQA 在 8192 tokens 下的比較）；第13頁「The expensive baseline for KV state」說明 MHA 32 頭基準；第12頁 MQA 採用動機；第13頁 GQA 定義與 Anders et al. 實驗結果；第2 項提及 MLA 壓縮潛在表示。 |
| 記憶體估算公式 | KV 快取大小 = 2 × L × H_KV × D_h × T × bytes_per_element（2 為 K 與 V 兩矩陣）。L 為層數、H_KV 為 KV 頭數、D_h 為頭維度、T 為快取 token 數。模型權重記憶體通常為 KV 快取的數百至數千倍。此公式可量化不同架構（MHA/GQA/MQA）在相同上下文長度下的顯存差異。 | 第9頁「THE MEMORY FORMULA」與參考文獻 Narayanan et al., 2024; Dao et al., 2023；第10頁表格參數 λ=22, d_k=128, h=2 layers, H_λ=22, tokens=8192 的數值驗證。 |
| PagedAttention 與分頁快取管理 | 受作業系統虛擬記憶體啟發，將邏輯序列切分為固定大小區塊，映射至非連續物理 KV 快取區塊，區塊表記錄地址映射，支援動態分配/釋放與前綴共享（vLLM block caching）。核心觀念為 logical token history ≠ contiguous physical allocation，解決連續分配造成的外部碎片與預留浪費。區塊大小無通用最優解，取決於模型、硬體、工作負載、資料集。 | 第2頁學習目標第6項；第12頁系統層面優化技術；第13頁「Page allocation appears as operating system inspired data to KV stores」與「The durable idea: logical token history ≠ contiguous physical allocation」; 第2段「There is no universal optimal block size independent of model, hardware, workload, and dataset.」 |
| 前綴快取（Prefix Caching）的效益與限制 | 跨請求重用已計算的 KV 區塊，僅減少預填充階段計算（例如 10k tokens 可節省 20‑30% 查詢處理時間），不加速解碼階段。正確性需比對模型身分、配置、適配、方法論輸入等完整狀態，而非僅 token 文本；自動前綴快取甚至可能延長 query-processing 時間。效益在短序列或無共享前綴場景有限。 | 第13頁「Reuse profile state across requests」；「It reduces prefill work, not future decode work」；當前 LLM 文件指出自動前綴快取會延長 query‑processing 時間但不減少 decode 階段產生新 token 所需時間；第2段「That would be a wonderful demonstration by a very long generated sequence, say 10k tokens, of 20-30% query-processing savings.」 |
| KV 快取量化與選擇性量化 | 以較低精度（16‑bit → 8‑bit/FP8/INT8）儲存 K/V 激活值，理論儲存需求減半；實際部署需處理對齊、量化參數、後端專用佈局，量化引入噪聲影響未來注意力計算。精度損失取決於模型架構/層密度、Key/Value 啟動分佈、上下文長度、量化粒度/層級、硬體支援/頻寬。現行 LLM 框架允許選擇性保留特定層或注意力類型不量化，反映量化不需均一化，但引入異質精度管理複雜度。 | 第28頁 OCR「KV Cache 量化（儲存更少位元）」；第29頁 OCR「量化非免費」與「Current LLMs allow selective layer or attention types to remain unquantized」；第3段「KVQuant 等研究的準確率/預算權衡強依賴具體方法、模型、硬體、基準」。 |
| 快取安全與 xULP 機制 | 多租戶環境下快取命中會改變延遲，未驗證讀取可能洩漏他人快取狀態；攻擊者可透過時序差異推測他人快取內容。xULP 機制將風險納入最後區塊的可快取性，並主張 coarse‑domain、shard‑cache、trust‑domain 原則以降低側信道攻擊。雜湊碰撞在共享環境下產生額外隱私顧慮。 | 第13頁「In a multi-user server, cache hits can change latency...」以及「cache coarse-domain shard-cache trust-domain」描述；第2段「If unvalidated reads are allowed to share per-cache state, an attacker may be able to select whether user contact was already cached by choosing timing differently.」 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| A KV cache is easy to describe badly. It is often called 'LLM memory,' a 'speed trick,' or simply 'cached attention.' Those shortcuts hide the mechanism that matters. | KV 快取很容易被描述得不準確。它常被稱為「LLM 記憶體」、「加速技巧」或單純的「快取注意力」。這些捷徑隱藏了關鍵機制。 | 手冊開頭指出常見認知捷徑掩蓋核心機制，強調從第一原理建立正確心智模型。 |
| KV caching is valid because past layer states are invariant to future tokens under the model's causal computation. It is not a heuristic guess. | KV 快取之所以有效，是因為在模型的因果計算下，過去層狀態不隨未來 token 而改變。這不是啟發式猜測。 | 闡述 KV 快取數學有效性的核心論點：因果遮罩阻斷資訊反向流動，使歷史 Key/Value 可安全重用。 |
| Three different resources / Do not collapse these into one: • Compute: arithmetic required by projections and attention. • Capacity: limits needed by large K/V state context. • Memory traffic/bandwidth: bytes needed to feed the attention layer during decoding. | 三種不同資源／不可將其合併為一：• 計算：投影與注意力所需的算術運算。• 容量：大型 K/V 狀態上下文所需的空間限制。• 記憶體流量/頻寬：解碼時餵養注意力層所需的位元組數。 | 手冊核心觀點：優化 KV 快取必須區分計算、容量、頻寬三個維度，MQA/GQA 主要針對頻寬而非計算。 |
| Beware of the cliff! | 小心斷崖！ | Noam Shazeer 於 2019 年 MQA 論文中對模型品質可能非線性劣化、無數學保證的警告。 |
| The durable idea: logical token history ≠ contiguous physical allocation | 核心觀念：邏輯 token 歷史 ≠ 連續物理分配 | PagedAttention 設計哲學，受作業系統虛擬記憶體啟發，以區塊表管理非連續物理快取塊。 |

## 可參考資料
- **@techNaak (作者/社群)**：手冊作者與發布社群，提供 Understanding AI Series 系列技術手冊。
- **Handbook 03 - Understanding AI Series (叢書系列)**：本手冊所屬系列編號，封面標示為 Handbook 03，PDF 檔名為 Handbook_02。
- **Narayanan et al., 2024**：手冊 Page 9 記憶體估算公式引用的參考文獻之一。
- **Dao et al., 2023**：手冊 Page 9 記憶體估算公式引用的參考文獻之一。
- **Noam Shazeer (2019) - Multi-Query Attention 論文**：提出 MQA 架構，針對增量解碼優化，警告品質風險「Beware of the cliff!」。
- **Anders et al. - Group-Query Attention (GQA) 論文**：提出 GQA 作為 MQA 推廣，實驗顯示品質接近 MHA、速度可比 MQA。
- **DeepSeek-V2 團隊 - MLA (Multi-head Latent Attention) 架構**：提出多頭潛在注意力，透過壓縮潛在表示降低 KV 快取成本，屬架構演進方向之一。
- **vLLM (PagedAttention, block caching)**：實作 PagedAttention 與區塊快取管理的開源推論引擎，手冊多處引用其設計。
- **TensorRT-LLM (驅逐策略、FP8 支援)**：NVIDIA 推論框架，文件描述快取驅逐優先策略與 FP8 量化支援。
- **KVQuant (量化研究系統)**：探索低位元 KV 快取表示的研究系統，手冊量化章節引用。
- **Understanding Attention (Handbook 01)**：前置手冊，涵蓋注意力數學核心，為本手冊先修基礎。
- **Rotary Position Embedding (RoPE)**：位置嵌入方法，影響快取中 Key 的儲存格式與一致性處理，不同框架實作可能不一。
- **xULP 機制**：多租戶快取安全相關機制，將風險納入最後區塊的可快取性，具體全名未在摘錄中給出。
- **University of California, Berkeley**：手冊頁腳標示來源機構之一。
