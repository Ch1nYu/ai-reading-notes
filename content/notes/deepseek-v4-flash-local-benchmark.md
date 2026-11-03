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

| 概念名 | 白話解釋與關鍵數據 |
| :--- | :--- |
| **oMLX** | Apple Silicon 專用的 MLX 推論引擎優化版本 (v0.5.4)，支援大模型高效載入與推論，本次測試核心軟體棧。 |
| **oQ4e-mtp 量化** | 4-bit 量化方案 (oQ4e) 加上 MTP (Multi-Token Prediction) 權重。模型體積 ~154 GB (官方 FP16/BF16 ~167 GB)，**資訊密度近乎無損**，是本地部署達陣關鍵。 |
| **Mac Studio M3 Ultra (256GB)** | 統一記憶體架構 (UMA) 讓 CPU/GPU 共享 256 GB RAM，單機即可載入 150GB+ 大模型無需分卡通訊，本地部署大模型的最佳消費級硬體。 |
| **Prefill / Decode 階段** | **Prefill (Prompt Processing)**：處理輸入上下文，本測平均 **125 tok/s** (合成峰值 330 tok/s)；**Decode (Token Generation)**：逐 token 生成，本測 **45 tok/s** 極其穩定。 |
| **Agentic Benchmarks (代理基準測試)** | 非單純問答，而是測試 **Tool Calling (工具呼叫)、Structured Output (結構化輸出)、Planning/Reasoning (規劃推理)、Memory Management (記憶管理)** 等複合能力的 8 大任務包。 |
| **量化精度保真度** | oQ4e-mtp 在 **BugFind (100分)、DataExtract (93分)、StructOutput (94分)** 甚至超越雲端 FP16 基準，證明高精度量化不損核心推理能力。 |
| **TTFT (Time-To-First-Token) 差距** | 雲端 API (官方 Flash/Pro) 在首 Token 回應速度上顯著優於本地 (單卡記憶體頻寬限制)，適合即時聊天；本地適合批次/後台/長流程自動化。 |
| **零速率限制與資料主權** | 本地部署核心價值：無 API 請求上限 (Rate Limits)，敏感程式碼/文件不出機房，滿足企業合規與高頻代理調用需求。 |
| **長尾延遲** | 本地模型在複雜指令遵循 (InstructFollow) 與數學推理 (ReasonMath) 部分案例耗時極長 (達 5 分鐘 Timeout)，顯示 Decode 階段在高邏輯複雜度下的序列依賴瓶頸。 |
| **Jundot (Hugging Face Repo)** | 提供 `DeepSeek-V4-Flash-0731-oQ4e-mtp` 量化權重的社群貢獻者，模型 ID 為 `Jundot--DeepSeek-V4-Flash-0731-oQ4e-mtp`。 |
| **評測維度 A-E** | 基準測試的細項評分維度 (具體定義未公開)，但可觀察：A 常關聯核心任務成功率，B/C 常為格式/邏輯正確性，D/E 可能為邊界情況/穩健度。本地版在 BugFind 全維度 100% 極為罕見。 |
| **多模態擴展需求** | 純文字模型需外掛 Vision Encoder (如 LLaVA 架構) 才能處理圖像，作者預告將釋出低成本整合方案。 |


## 中英金句與解釋

| 原文 | 中譯 | 脈絡/解釋 |
| :--- | :--- | :--- |
| **"The oQ4e scheme retains the vast majority of the original model's information density, ensuring near-lossless precision in local execution."** | **「oQ4e 方案保留了原始模型絕大多數的資訊密度，確保了本地執行的近乎無損精度。」** | 核心技術斷言：4-bit 量化不再是精度妥協的代名詞，配合 MTP 權重可達生產級品質。 |
| **"Cloud APIs retain an advantage in raw Time-To-First-Token (TTFT) for rapid multi-turn chat, but local quants excel in continuous, privacy-first agentic automation where zero rate-limits are paramount."** | **「雲端 API 在首 Token 延遲 (TTFT) 上保有優勢，適合快速多輪對話；但本地量化模型在連續、隱私優先的代理自動化中脫穎而出，因為零速率限制才是關鍵。」** | 精準定義雲端與本地的適用邊界：延遲敏感 vs. 吞吐/隱私/成本敏感。 |
| **"DeepSeek-V4-Flash-0731 demonstrates a massive leap in tool-calling precision, low-hallucination structured output, and complex multi-step reasoning compared to previous generations."** | **「DeepSeek-V4-Flash-0731 在工具呼叫精度、低幻覺結構化輸出、複雜多步推理上，較前代展現大幅躍進。」** | 定調模型代際進步的質變點：Agentic 能力成熟度。 |
| **"Whether deployed locally via oMLX or accessed through cloud endpoints, it currently stands as the most cost-effective open-weight model on the market for agentic automation and heavy coding workflows."** | **「無論透過 oMLX 本地部署或雲端端點存取，它目前都是市場上針對代理自動化與重度編碼工作流，最具成本效益的開放權重模型。」** | 商業價值判斷：開放權重 + 高性能 + 低部署門檻 = 目前最佳 ROI 選擇。 |
| **"In code debugging and static analysis tests, the local model demonstrated precise bug localization without introducing extra hallucinated dependencies, matching the official Cloud API’s reasoning capabilities."** | **「在程式碼除錯與靜態分析測試中，本地模型展現精準的 Bug 定位，未引入額外幻覺依賴，推理能力匹配官方雲端 API。」** | 實證 BugFind 100 分的具體內涵：不只是過測試，而是推理過程可靠。 |
| **"Synthetic benchmarks via omlx bench hit a peak Prompt Processing speed of 330.0 tok/s (pp 16K). In real-world agentic workloads... the average effective Prefill sustained a solid 125.2 tok/s"** | **「合成基準測試 Prefill 峰值 330 tok/s (16K context)。實際代理工作負載下... 平均有效 Prefill 維持穩固 125.2 tok/s。」** | 區分「跑分數據」與「實戰吞吐」的誠實報告，動態上下文與工具歷史會顯著降低 Prefill 效率。 |


## 可參考資料

1.  **評測套件作者**：[@stevibe](https://x.com/stevibe) — 提供開源 Agentic 評測套件 (BenchLocal / Agent API 介面)。
2.  **推論引擎**：**oMLX** (v0.5.4) — Apple Silicon 優化推論引擎，基於 MLX。
3.  **模型權重來源**：**Hugging Face - Jundot** — `Jundot/DeepSeek-V4-Flash-0731-oQ4e-mtp` (約 154 GB)。
4.  **官方模型權重**：**Hugging Face - DeepSeek** — `deepseek-ai/DeepSeek-V4-Flash-0731` (官方 167 GB 權重)。
5.  **硬體平台**：**Mac Studio M3 Ultra** (256GB Unified Memory, 60-core GPU) — Apple 官網規格。
6.  **官方雲端 API**：**DeepSeek Official API** (`deepseek-v4-flash`, `deepseek-v4-pro`) 及 **OpenCode** (`deepseek-v4-flash-free`) 作為基準比較對象。
7.  **作者後續內容預告**：Jerry Xiong (@Jerry_Galaxy) 將發布 DeepSeek 多模態視覺整合成本效益分析。
