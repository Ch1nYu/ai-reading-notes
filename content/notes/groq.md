---
title: Groq 與 LPU 推論晶片
type: article
source_url: https://en.wikipedia.org/wiki/Groq
source_site: Wikipedia
added: '2026-09-09'
topics:
- models
summary: Groq 由前 Google TPU 設計者創立，獨特的 LPU 架構與商業佈局（含沙烏地阿拉伯投資、Nvidia 授權協議）使其成為 AI 推理晶片領域的關鍵挑戰者。
abstract: Groq 是一家美國 AI 晶片初創公司，專注於開發語言處理單元（Language Processing Unit，LPU）加速 AI 推理，其確定性單核心架構與編譯器主導設計提供高效能、低延遲的大型語言模型執行環境。
---

## 完整摘要

### 公司概況與產品定位
Groq, Inc. 成立於 2016 年，總部位於加州山景城，是一家開發 AI 加速器專用積體電路（ASIC）的私人公司。其核心產品為語言處理單元（LPU），最初稱為張量流式處理器（Tensor Streaming Processor，TSP），在 ChatGPT 突破後因大型語言模型廣泛採用而更名為 LPU。LPU 可執行大型語言模型、影像分類與預測分析等工作負載，並透過 GroqCloud™ 提供開發者存取。公司 2023 年員工約 250 人，2023 年淨虧損 8800 萬美元，2025 年預估營收 5 億美元。

### 創立沿革與核心團隊
Groq 由前 Google 工程師創立，核心創辦人 Jonathan Ross 為 Tensor Processing Unit（TPU）設計者之一，另一創辦人 Douglas Wightman 來自 Google X（X Development），曾任首任 CEO。現任關鍵人物為 CEO Jonathan Ross 與 COO Sunny Madra。種子輪於 2017 年由 Social Capital 的 Chamath Palihapitiya 投資 1000 萬美元，隨後陸續獲得追加投資。

### 融資歷程與估值躍升
2021 年 4 月完成 C 輪 3 億美元融資，由 Tiger Global Management 與 D1 Capital Partners 領投，投後估值超過 10 億美元成為獨角獸。現有投資人包括 Infinitum、The Spruce House Partnership、Addition、GCM Grosvenor、Xⁿ、Firebolt Ventures、General Global Capital、Tru Arrow Partners 以及 TDK Ventures、XTX Ventures 等追加投資。2024 年 8 月完成 D 輪 6.4 億美元融資，由 BlackRock Private Equity Partners 領投，估值達 28 億美元。2025 年 2 月獲得沙烏地阿拉伯 15 億美元承諾，用於在 Dammam 建設 GroqCloud 資料中心。2026 年 5 月傳出將以按比例認購方式再募 6.5 億美元，由 Disruptive 與 Infinitum 兜底。

### 併購與製造合作
2022 年 3 月收購 Maxeler Technologies，保留其品牌與 Dr. Oskar Mencer 團隊的資料流專長。2024 年 3 月收購 Definitive Intelligence 以強化雲端平台。2023 年 8 月選定三星電子德州 Taylor 廠 4 奈米製程製造新一代晶片，為該廠首單。截至 2025 年，Groq 在美國、加拿大、中東、歐洲已建置十餘座資料中心。

### LPU 架構技術細節
LPU 採功能切片微架構，記憶體單元與向量/矩陣運算單元交錯排列，利用 AI 計算圖的資料流局部性提升效能。設計基於兩大觀察：AI 工作負載具高度資料平行性，可映射至專用硬體；確定性處理器設計搭配生產者-消費者程式模型，能精確控制硬體元件。LPU 為單核心確定性架構，移除分支預測器、仲裁器、重排緩衝區、快取等傳統反應式元件，所有執行由編譯器顯式控制，保證執行確定性。第一代 LPU（TSP）在 14 奈米、25×29 mm、900 MHz 下達到每平方毫米超過 1 TeraOp/s 計算密度；第二代將採三星 4 奈米製程。

### Nvidia 授權協議與後續發展
2025 年 12 月 Nvidia 與 Groq 達成約 200 億美元協議，授權 Groq 的 AI 推理技術並轉移數位高階主管（含 Ross 與 Madra）至 Nvidia。Groq 稱此為非獨家授權協議，將持續獨立運營。2026 年 5 月報導 Groq 正募集 6.5 億美元以轉型為 AI 推理雲端業務，標誌著公司策略進入新階段。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 語言處理單元（LPU）確定性單核心架構 | LPU 移除分支預測、仲裁、重排緩衝、快取等動態硬體機制，改由編譯器在編譯期靜態排程所有指令與資料移動，確保執行時間與功耗可預測，適合大型語言模型推理的低延遲需求。 | 文中說明："The LPU can achieve deterministic execution by avoiding the use of traditional reactive hardware components (branch predictors, arbiters, reordering buffers, caches) and by having all execution explicitly controlled by the compiler thereby guaranteeing determinism in execution of an LPU program." |
| 功能切片微架構與資料流局部性 | 將記憶體單元與向量/矩陣運算單元交錯排列，形成功能切片，使 AI 計算圖的資料流局部性在硬體層面被直接利用，減少資料搬移開銷，提升能效比。 | 文中說明："The LPU features a functionally sliced microarchitecture, where memory units are interleaved with vector and matrix computation units. This design facilitates the exploitation of dataflow locality in AI compute graphs, improving execution performance and efficiency." |
| 分階段融資與估值成長軌跡 | 從 2017 年 1000 萬美元種子輪，到 2021 年 3 億美元 C 輪（估值 >10 億美元）、2024 年 6.4 億美元 D 輪（估值 28 億美元）、2025 年沙烏地 15 億美元策略投資、2026 年擬募 6.5 億美元，顯示資本市場對 AI 推理專用晶片的高度關注。 | 文中列出各輪融資金額、領投機構與估值變化，並註明 2025 年沙烏地承諾與 2026 年最新募資計畫。 |
| 關鍵併購補足軟硬體棧 | 收購 Maxeler 帶來資料流系統與 HPC 專長，收購 Definitive Intelligence 強化雲端平台與企業級 AI 解決方案能力，兩者協同支撐 GroqCloud 開發者生態系。 | 文中記載 2022 年收購 Maxeler、2024 年收購 Definitive Intelligence 及其目的。 |
| 三星 4 奈米代工與產能佈局 | 選定三星電子德州 Taylor 廠 4 奈米製程製造第二代 LPU，為該廠首單訂單，標誌供應鏈從單一代工廠向多元化、在地化生產邁進。 | 文中說明："On August 16, 2023, Groq selected Samsung Electronics' foundry in Taylor, Texas to manufacture its next-generation chips, on Samsung's 4-nanometer (nm) process node. This was the first order at this new Samsung chip factory." |
| Nvidia 非獨家授權協議與人才轉移 | Nvidia 支付約 200 億美元取得 Groq 推理技術授權並吸納核心高管，Groq 保留獨立運營與技術所有權，雙方形成合作而非全資併購關係。 | 文中引用 Reuters、TechCrunch、Groq 官方聲明："Nvidia agreed to purchase assets from Groq for approximately US$20 billion... Groq has described this as a non-exclusive licensing deal." |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| The architecture was originally introduced as a Tensor Streaming Processor (TSP) but was later rebranded as a Language Processing Unit (LPU) following the widespread adoption of large language models after the breakthrough of ChatGPT. | 該架構最初作為張量流式處理器（TSP）推出，但在 ChatGPT 突破後大型語言模型廣泛採用的情況下，後來更名為語言處理單元（LPU）。 | 說明 LPU 命名變更緣起，反映產品定位隨生成式 AI 浪潮調整。 |
| A deterministic processor design, coupled with a producer–consumer programming model, allows for precise control and reasoning over hardware components, allowing for optimized performance and energy efficiency. | 確定性處理器設計搭配生產者-消費者程式模型，能對硬體元件進行精確控制與推理，從而實現效能與能效的優化。 | 描述 LPU 設計哲學的核心論點，出自 ACM 發表的技術論文摘要。 |
| Groq and NVIDIA enter non-exclusive inference technology licensing agreement | Groq 與 NVIDIA 簽訂非獨家推理技術授權協議。 | Groq 官方新聞稿標題，確認 2025 年 12 月雙方協議性質為授權而非收購。 |

## 可參考資料
- **Forbes - The AI Chip Boom Saved This Tiny Startup. Now Worth $2.8 Billion, It's Taking On Nvidia**：報導 Groq D 輪融資與估值 28 億美元細節。 — <https://www.forbes.com/sites/richardnieva/2024/08/05/groq-funding-series-d-nvidia/>
- **TechRadar Pro - 'Feels like magic!': Groq's ultrafast LPU could well be the first LLM-native processor**：LPU 效能展示與業界反應報導。 — <https://www.techradar.com/pro/feels-like-magic-groqs-ultrafast-lpu-could-well-be-the-first-llm-native-processor-and-its-latest-demo-may-well-convince-nvidia-and-amd-to-get-out-their-checkbooks>
- **EETimes - Groq Demonstrates Fast LLMs on 4-Year-Old Silicon**：驗證第一代 LPU 在舊製程上仍具競爭力。 — <https://www.eetimes.com/groq-demos-fast-llms-on-4-year-old-silicon/>
- **Reuters - Nvidia, joining Big Tech deal spree, to license Groq technology, hire executives**：Nvidia 授權協議金額與條款主要來源。 — <https://www.reuters.com/business/nvidia-buy-ai-chip-startup-groq-about-20-billion-cnbc-reports-2025-12-24/>
- **TechCrunch - Nvidia to license AI chip challenger Groq's tech and hire its CEO**：補充 Nvidia 協議細節與高管轉移資訊。 — <https://techcrunch.com/2025/12/24/nvidia-acquires-ai-chip-challenger-groq-for-20b-report-says/>
- **CNBC - Exclusive: Nvidia buying AI chip startup Groq's assets for about $20 billion**：Nvidia 交易為史上最大單筆交易的背景報導。 — <https://www.cnbc.com/amp/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html>
- **Bloomberg - Tiger Global, D1 Lead $300 Million Round in AI Chip Startup Groq**：C 輪融資領投機構與金額確認。 — <https://www.bloomberg.com/news/articles/2021-04-14/tiger-global-d1-lead-300-million-round-in-ai-chip-startup-groq>
- **Groq 官方新聞稿 - Saudi Arabia Announces $1.5 Billion Expansion**：沙烏地阿拉伯 15 億美元承諾官方公告。 — <https://groq.com/saudi-arabia-announces-1-5-billion-expansion-to-fuel-ai-powered-economy-with-groq>
- **The Wall Street Journal - AI Unicorn Groq Charts Data-Center Expansion Plan**：2025 年資料中心佈局十餘座的第三方驗證。 — <https://www.wsj.com/business/ai-unicorn-groq-charts-data-center-expansion-plan-5d6a130e>
- **ACM/IEEE ISCA 2020 - Think Fast: A Tensor Streaming Processor (TSP) for Accelerating Deep Learning Workloads**：LPU/TSP 架構原始技術論文。 — <https://groq.com/wp-content/uploads/2020/06/ISCA-TSP.pdf>
- **ACM ISCA 2022 - A software-defined tensor streaming multiprocessor for large-scale machine learning**：第二代架構與確定性設計詳細論述。 — <https://dl.acm.org/doi/10.1145/3470496.3527405>
