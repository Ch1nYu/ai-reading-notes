---
title: DeepSeek V4 Flash 在 Mac Studio 的本地推論基準
type: article
source_url: https://x.com/Jerry_Galaxy/status/2084246725251019162#vision_test
source_site: X
language: en
added: '2026-08-08'
topics:
- models
summary: DeepSeek-V4-Flash-0731 在 Mac Studio M3 Ultra 上透過 oMLX (oQ4e-mtp) 本地部署，以 125 tok/s Prefill 與 45 tok/s Decode 效能，在結構化輸出、工具呼叫與程式碼除錯等 Agentic 任務上達到甚至超越官方雲端 API 的表現，確立了高隱私、無速率限制的本地大模型部署可行性。
abstract: Jerry Xiong 於 Mac Studio M3 Ultra (256GB) 上透過 oMLX 部署完整規格的 DeepSeek-V4-Flash-0731 (oQ4e-mtp 量化)，實測本地推論效能與 8 大類 Agentic 基準測試，證明本地部署可達雲端級推理品質，且具零速率限制與絕對資料隱私優勢。
---

## 完整摘要

### Overview 總覽
- **目的**：評估本地推論在敏感資料環境下的效能與可行性，並與官方雲端 API 直接比較。
- **硬體環境**：Mac Studio M3 Ultra (256GB 統一記憶體, 60-core GPU)。
- **軟體棧**：oMLX 0.5.4，模型為 `Jundot--DeepSeek-V4-Flash-0731-oQ4e-mtp`。
- **評測套件**：感謝 [@stevibe](https://x.com/stevibe) 提供開源評測套件，涵蓋 8 大真實任務包：BugFind, CLI, DataExtract, HermesAgent, InstructFollow, ReasonMath, StructOutput, ToolCall。

### Local Inference Performance & Precision 本地推論效能與精度
- **模型大小**：下載後約 **154 GB**，接近 Hugging Face 官方釋出的 167 GB 權重。oQ4e 量化方案保留絕大多數資訊密度，近乎無損精度。
- **記憶體佔用**：實測 RAM 配置約 **164 GB** (觀測值 164.1 GB，軟限制 197.2 GB，硬限制 208.1 GB)。
- **吞吐效能**：
  - 平均 Prompt Processing (Prefill) 速度：**125.2 tok/s**。
  - 平均 Token Generation (Decode) 速度：**45.4 tok/s**。
  - 合成基準測試 (omlx bench) 峰值 Prefill 可達 **330.0 tok/s** (16K context)，但實際 Agentic 工作負載含動態上下文與多輪工具歷史，平均有效 Prefill 維持在 125.2 tok/s，Decode 極其穩定約 45 tok/s。

### Benchmark Insights & Scenario Analysis 基準測試洞察與場景分析

#### DataExtract & StructOutput (資料萃取與結構化輸出)
- **DataExtract-15**：本地 oQ4e-mtp 量化版獲得 **93 分**，略優於雲端端點 (官方 Flash/Pro 均 88 分，OpenCode Flash-free 88 分)。在嚴格 JSON 格式保留與確定性欄位萃取上表現最佳 (維度 E 達 99%)。
- **StructOutput-15**：本地版獲得 **94 分**，全場最高。官方 Flash 92 分，Pro 87 分，OpenCode Flash-free 90 分。本地版在 A, B, C, E 四維度均達 100%，僅 D 維度 (71%) 稍遜。

#### ToolCall & Agentic Workflows (Hermes / CLI) (工具呼叫與代理工作流)
- **ToolCall-15**：雲端 API 在首 Token 延遲 (TTFT) 上佔優，適合低延遲聊天；本地量化版在連續、隱私優先的代理自動化中勝出 (零速率限制)。本地版總分 **93 分** (A: 67, B-E: 100)，官方 Flash/Flash-free 均 100 分，Pro 97 分。本地版在 TC-03 出現單一失敗 (✗ 16s)，其餘通過。
- **HermesAgent-20**：測試記憶體工具使用與衝突解決。詳細分數圖片截斷，但文中歸類於本地優勢項目。
- **CLI-40 (實際為 CLI-18 顯示)**：本地版總分 **67 分**，超越官方 Flash (63)、Pro (64)、OpenCode Flash-free (51)。在 CLI-01 至 CLI-07 等短任務上速度極快 (14-23s)；長任務 (CLI-08 至 CLI-14) 多達 5 分鐘超時上限，與雲端模型表現一致 (均觸及 5m 00s 上限)。CLI-15, 16 為全模型共同失敗項。

#### BugFind & Coding Tasks (程式碼除錯)
- **BugFind-15**：本地版 **完美拿下 100 分** (A-E 全 100%)，超越官方 Pro (93)、Flash-free (93)、Flash (85)。展現精準定位 Bug (如 Off-by-one) 能力，無幻覺依賴，推理能力與雲端持平。缺點是單案耗時較長 (BF-01 58s, BF-11 60s)，雲端通常在 10s 內。

#### InstructFollow & ReasonMath (指令遵循與數學推理)
- **InstructFollow-15**：本地版 **83 分** (A: 63, D: 52)，落後於雲端模型 (Pro 97, Flash/Flash-free 93)。在複雜格式約束 (IF-02, 03, 10 失敗) 表現較弱，耗時極長 (IF-01 2m 25s, IF-10 5m 00s timeout)。
- **ReasonMath-15**：本地版 **74 分** (A: 95, B: 33)，接近官方 Flash-free (78) 與 Flash (73)，優於 Pro (68)。逐步推理穩固，量化無退化，但在 RM-01, 04, 05, 06, 13 等複雜多步驟題目耗時明顯較長 (21s-48s)。

### Takeaway for AI Engineers 給 AI 工程師的啟示
1. **Agentic 能力大躍進**：DeepSeek-V4-Flash-0731 在工具呼叫精度、低幻覺結構化輸出、複雜多步推理上較前代有巨大飛躍。
2. **無可匹敵的成本效益**：無論本地部署 (oMLX) 或雲端端點，目前市場上最具成本效益的開放權重模型，適用於代理自動化與重度編碼工作流。
3. **雲端 vs 本地策略**：雲端 API 勝在原始 TTFT (低延遲聊天)；本地執行勝在零速率限制與絕對資料隱私 (持續背景代理)。

### What's Next 後續規劃
DeepSeek-V4 原生為純文字模型，多模態工作流對開發者工具與代理至關重要。作者將於次日發布賦予 DeepSeek 無縫視覺能力的成本效益拆解方案。


## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| **oMLX** | Apple Silicon 專用的 MLX 推論引擎優化版本（v0.5.4），支援大模型高效載入與本地推論。 | Overview 段落標明測試軟體棧為 oMLX 0.5.4，並以 `omlx bench` 測得 16K context 下峰值 Prefill 330.0 tok/s。 |
| **oQ4e-mtp 量化** | 4-bit 量化方案（oQ4e）加上 MTP（Multi-Token Prediction）權重，保留絕大多數資訊密度，達到近乎無損的本地執行精度。 | 模型下載後約 154 GB（接近官方 167 GB 權重），模型 ID 為 `Jundot--DeepSeek-V4-Flash-0731-oQ4e-mtp`。 |
| **Mac Studio M3 Ultra (256GB)** | 統一記憶體架構（UMA）讓 CPU/GPU 共享 256 GB RAM（60-core GPU），單機即可載入 150GB+ 大模型無需跨卡通訊。 | 實測 RAM 配置約 164.1 GB（軟限制 197.2 GB、硬限制 208.1 GB），在單台消費級桌機完成全部基準測試。 |
| **Prefill / Decode 階段效能** | Prefill（提示詞處理）負責建立上下文快取，Decode（Token 生成）負責逐字產出回應；動態上下文與工具歷史會降低有效 Prefill 吞吐。 | 合成基準峰值 Prefill 為 330.0 tok/s，真實 Agentic 工作負載下平均有效 Prefill 為 125.2 tok/s，Decode 穩定維持 45.4 tok/s。 |
| **Agentic Benchmarks（八大任務包）** | 測試工具呼叫、結構化輸出、程式碼除錯、指令遵循、數學推理與記憶管理等複合代理能力的開源評測套件。 | 由 @stevibe 提供，涵蓋 BugFind、CLI、DataExtract、HermesAgent、InstructFollow、ReasonMath、StructOutput、ToolCall 八大任務包。 |
| **量化精度保真度** | 高精度量化在程式碼除錯、資料萃取與結構化輸出上不損核心推理能力，甚至在確定性格式保留上優於雲端端點。 | 本地版在 BugFind 拿 100 分（雲端 Pro 93、Flash 85）、DataExtract 拿 93 分（雲端 88）、StructOutput 拿 94 分（全場最高）。 |
| **TTFT 差距與零速率限制** | 雲端 API 在首 Token 延遲（TTFT）佔優，適合即時多輪聊天；本地執行則具備零速率限制與資料不出機房的隱私優勢，適合背景代理自動化。 | ToolCall-15（本地 93 分 vs 官方 Flash 100 分）與 Takeaway #3 對比雲端低延遲聊天與本地連續代理自動化的適用邊界。 |
| **複雜推理的長尾延遲** | 本地模型在複雜格式約束與多步數學推理中，受限於單機解碼頻寬與長思考鏈，部分案例會出現較長耗時或觸及超時上限。 | InstructFollow-15 本地 83 分（IF-01 耗時 2m 25s、IF-10 觸及 5m 00s timeout）；ReasonMath-15 本地 74 分，複雜題耗時 21s–48s。 |


## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
| :--- | :--- | :--- |
| **"The oQ4e scheme retains the vast majority of the original model's information density, ensuring near-lossless precision in local execution."** | **「oQ4e 方案保留了原始模型絕大多數的資訊密度，確保了本地執行的近乎無損精度。」** | 核心技術斷言：4-bit 量化不再是精度妥協的代名詞，配合 MTP 權重可達生產級品質。 |
| **"Cloud APIs retain an advantage in raw Time-To-First-Token (TTFT) for rapid multi-turn chat, but local quants excel in continuous, privacy-first agentic automation where zero rate-limits are paramount."** | **「雲端 API 在首 Token 延遲 (TTFT) 上保有優勢，適合快速多輪對話；但本地量化模型在連續、隱私優先的代理自動化中脫穎而出，因為零速率限制才是關鍵。」** | 精準定義雲端與本地的適用邊界：延遲敏感 vs. 吞吐/隱私/成本敏感。 |
| **"DeepSeek-V4-Flash-0731 demonstrates a massive leap in tool-calling precision, low-hallucination structured output, and complex multi-step reasoning compared to previous generations."** | **「DeepSeek-V4-Flash-0731 在工具呼叫精度、低幻覺結構化輸出、複雜多步推理上，較前代展現大幅躍進。」** | 定調模型代際進步的質變點：Agentic 能力成熟度。 |
| **"Whether deployed locally via oMLX or accessed through cloud endpoints, it currently stands as the most cost-effective open-weight model on the market for agentic automation and heavy coding workflows."** | **「無論透過 oMLX 本地部署或雲端端點存取，它目前都是市場上針對代理自動化與重度編碼工作流，最具成本效益的開放權重模型。」** | 商業價值判斷：開放權重 + 高性能 + 低部署門檻 = 目前最佳 ROI 選擇。 |
| **"In code debugging and static analysis tests, the local model demonstrated precise bug localization without introducing extra hallucinated dependencies, matching the official Cloud API’s reasoning capabilities."** | **「在程式碼除錯與靜態分析測試中，本地模型展現精準的 Bug 定位，未引入額外幻覺依賴，推理能力匹配官方雲端 API。」** | 實證 BugFind 100 分的具體內涵：不只是過測試，而是推理過程可靠。 |
| **"Synthetic benchmarks via omlx bench hit a peak Prompt Processing speed of 330.0 tok/s (pp 16K). In real-world agentic workloads... the average effective Prefill sustained a solid 125.2 tok/s"** | **「合成基準測試 Prefill 峰值 330 tok/s (16K context)。實際代理工作負載下... 平均有效 Prefill 維持穩固 125.2 tok/s。」** | 區分「跑分數據」與「實戰吞吐」的誠實報告，動態上下文與工具歷史會顯著降低 Prefill 效率。 |


## 可參考資料

- **@stevibe（評測套件作者）**：提供涵蓋 8 大真實任務包的開源 Agentic 評測套件（BenchLocal / Agent API 介面）。 — <https://x.com/stevibe>
- **oMLX (v0.5.4)**：基於 MLX 的 Apple Silicon 優化推論引擎，支援大模型高效本地部署。
- **Hugging Face - Jundot**：提供 `Jundot/DeepSeek-V4-Flash-0731-oQ4e-mtp` 量化權重（約 154 GB）。
- **Hugging Face - DeepSeek**：提供 `deepseek-ai/DeepSeek-V4-Flash-0731` 官方原始權重（約 167 GB）。
- **Mac Studio M3 Ultra**：本次測試硬體平台（256GB 統一記憶體、60-core GPU）。
- **DeepSeek Official API & OpenCode**：提供 `deepseek-v4-flash`、`deepseek-v4-pro` 與 `deepseek-v4-flash-free` 雲端基準對照。
- **Jerry Xiong (@Jerry_Galaxy)**：本文作者，實測並發布 DeepSeek V4 Flash 本地推論基準與多模態整合預告。 — <https://x.com/Jerry_Galaxy/status/2084246725251019162>
