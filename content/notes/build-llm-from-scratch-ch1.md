---
title: 從零打造 LLM：第 1 章核心概觀
type: article
source_url: https://apps.twinkleai.tw/llm-from-scratch-course/ch01.html
source_site: TwinkleAI
language: zh
added: '2026-08-08'
topics:
- llm-internals
summary: LLM 本質是將「預測下一個 token」這極簡單的自監督任務，透過龐大參數量（如 175B）與海量資料（如 3,000 億 tokens）訓練出的深度神經網路，經由 Transformer decoder 架構的自回歸生成，展現出翻譯、摘要、對話等未被明確教導的湧現能力。
abstract: 這是《Build a Large Language Model (From Scratch)》第 1 章的互動教材版本，零程式碼建立 LLM 核心世界觀：從定義、應用、預訓練/微調流程、Transformer 架構、GPT 自回歸機制、資料規模量化，到全書三階段實作藍圖，一次看清「簡單目標 × 巨大規模」如何長出類人語言能力。
---

## 完整摘要

### 本章定位：全書鳥瞰圖
- 唯一純概念章節，不寫程式碼，建立正確世界觀。
- 後續章節對應管線圖各階段：`資料 → Tokenize → Embedding → 架構 → 預訓練 → 微調 → 應用`。
- 讀者目標：會寫 Python，無需 ML 博士學位，親手打造 GPT。

### 三個天文數字（以 GPT-3 為例）
| 指標 | 數值 | 意義 |
|------|------|------|
| 參數量 | 175B (175,000,000,000) | 模型規模「Large」的第一層意思 |
| 預訓練 Tokens | ~3,000 億 (300B) | 資料規模「Large」的第二層意思 |
| 預訓練成本 | ~$4.6M (雲端算力) | 為何第 5 章採用載入開源權重策略 |

### 1.1 What is an LLM?
- **定義**：在極大量文字上訓練、被設計來理解/生成/回應類人文字的深度神經網路。
- **核心任務**：Next-word prediction（給前文，輸出下一個 token 的機率分佈）。
- **Large 雙關**：參數規模（數百億可調權重）× 資料規模（公開網路大部分）。
- **免責聲明**：「理解」指生成連貫切題文字，非人類意識；屬 Generative AI (GenAI)。
- **AI 版圖定位**：AI ⊃ ML ⊃ DL ⊃ LLM（最內圈）。
- **特徵學習差異**：傳統 ML 需專家手工設計特徵（如垃圾郵件關鍵字）；DL/LLM 特徵自動從資料學習，架構為 Transformer，具選擇性注意機制。

### 1.2 Applications of LLMs
- **舊範式**：一任務一模型（分類器不會翻譯）。
- **新範式**：一模型多任務。只要能描述為「文字進、文字出」，LLM 幾乎皆適用。
- **例子**：翻譯、分類、摘要、程式碼、對話。
- **關鍵**：GPT 翻譯能力非特別教出，屬 Emergent Behavior（湧現行為），1.6 節詳細說明。

### 1.3 Stages of Building and Using LLMs
- **為何自造**：理解機制與極限、客製模型勝過通用模型（如 BloombergGPT）、隱私與自主（可跑於邊緣裝置）。
- **工具**：PyTorch（附錄 A 有速成）。
- **兩階段配方**：Pretraining → Fine-tuning。
  - **Pretraining**：海量無標註文字做 Next-word prediction，自監督學習，標籤「右移一格」自動生成，吃掉絕大多數算力，產出 Foundation Model。
  - **Fine-tuning**：小量標註資料精修。兩大類：Instruction Fine-tuning（→ 助理）與 Classification Fine-tuning（→ 分類器）。

### 1.4 Introducing the Transformer Architecture
- **來源**：2017 論文《Attention Is All You Need》，原為機器翻譯設計。
- **結構**：Encoder（讀懂輸入，捕捉上下文向量）+ Decoder（逐字生成輸出）。
- **靈魂零件**：Self-Attention，讓 tokens 彼此衡量重要性，抓住長距離依賴。
- **後代路線**：
  - BERT：取 Encoder，做 Masked Word Prediction（克漏字），擅長理解/分類。
  - GPT：取 Decoder，做 Next-word Prediction（接龍），擅長生成。
- **Zero-shot / Few-shot**：不改權重、不改架構，透過 Prompt 完成新任務。

### 1.5 Utilizing Large Datasets
- **GPT-3 資料配方**（Table 1.1，總計 499B tokens，實際訓練 ~300B tokens）：
  - CommonCrawl (filtered) 60% / WebText2 22% / Books1 8% / Books2 8% / Wikipedia 3%。
  - 比例為訓練抽樣權重，非資料大小比例。
- **公開替代語料**：Dolma (3T tokens)、LLaMA 額外加入 ArXiv (92GB)、StackExchange (78GB)。
- **規模換算器**：
  - 300B tokens ≈ 300 萬本 300 頁小說。
  - 人以 250 tokens/分不眠不休讀完需 ~2,283 年。
  - 每參數平均僅見 1.7 tokens（300B/175B），極度稀疏。
- **策略**：第 5 章用小資料集實作機制，再載入開源 GPT-2 權重，繞過 $4.6M 成本。

### 1.6 A Closer Look at the GPT Architecture
- **出身**：Radford 等人《Improving Language Understanding by Generative Pre-Training》；GPT-3 為放大版；ChatGPT 初版 = GPT-3 + InstructGPT 方法微調。
- **架構簡化**：只留 Decoder，但疊 96 層（原始 Transformer 各 6 層），175B 參數。
- **Autoregressive (自回歸)**：一次生成一 token，輸出接回輸入再算下一個，故 ChatGPT 逐字吐出。
- **Emergent Behavior**：訓練目標僅 Next-word prediction，卻湧現翻譯、拼字修正、分類、摘要等能力。源於大量多語資料接觸。

### 1.7 Building a Large Language Model (三階段藍圖)
| 階段 | 章節 | 核心步驟 | 對應管線圖 |
|------|------|----------|------------|
| **Stage 1: 打地基** | Ch 2–4 | 1. 資料準備/取樣 → Ch2 (Tokenize, Embedding, Data Loader) <br> 2. Attention 機制 → Ch3 (Self-Attention 手刻) <br> 3. LLM 架構 → Ch4 (組裝 GPTModel) | 📚 ✂️ ▦ 🧱 |
| **Stage 2: 預訓練** | Ch 5 | 4. 預訓練（小資料驗證機制） → 載入開源 GPT-2 權重 | 🏋️ |
| **Stage 3: 微調** | Ch 6–7 | 5. Classification Fine-tuning → 分類器 <br> 6. Instruction Fine-tuning → 對話助理 | 🎯 💬 |

### 本章小結（七大重點）
1. LLM 定義與雙關 Large；座標 AI⊃ML⊃DL⊃LLM，屬 GenAI。
2. 預訓練 = 自監督，標籤右移一格，無需人工標註。
3. 兩步訓練：預訓練得 Foundation Model → 微調（Instruction / Classification）。
4. Transformer (2017) = Encoder + Decoder，核心 Attention。
5. BERT (Encoder/理解) vs GPT (Decoder/生成)；GPT-3: 96層/175B/300B tokens/$4.6M。
6. 自回歸生成 + 湧現行為 = Zero/Few-shot 多任務能力。
7. 三階段九步驟藍圖，Ch2 起跑。

### 知識檢核（七題精華）
- Q1: 預訓練唯一目標 = 輸出下一個 token 機率分佈。
- Q2: Large = 參數量 (175B) × 資料量 (300B tokens)。
- Q3: Self-supervised，右移一格自動得標籤。
- Q4: 原始 Transformer 為 Encoder-Decoder 翻譯模型。
- Q5: BERT 雙向遮罩預測 (理解) vs GPT 單向自回歸生成。
- Q6: Zero-shot = 未見任務泛化；Few-shot = Prompt 給範例；皆不改權重。
- Q7: 翻譯等能力為 Emergent Behavior (湧現行為)。


## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| **LLM (Large Language Model)** | 把「猜下一個字」練到極致的深度神經網路，參數與資料雙重「大」。 | 1.1 節定義：在極大量文字上訓練、理解與生成類人文字的深度神經網路，座標位於 AI ⊃ ML ⊃ DL ⊃ LLM 最內圈。 |
| **Next-word Prediction / 自回歸** | 核心訓練任務：給前文輸出下一 token 機率；生成時輸出接回輸入循環產出序列。 | 1.1 與 1.6 節：Autoregressive 機制一次生成一 token 並將輸出接回輸入，解釋 ChatGPT 逐字吐出的原因。 |
| **Self-Supervised Learning (自監督學習)** | 不需人工標註，句子「右移一格」即得 (input, target) 配對，讓全網文字成教材。 | 1.3 節與知識檢核 Q3：標籤藏在資料裡，右移一格自動生成，吃掉絕大多數預訓練算力並產出 Foundation Model。 |
| **Pretraining (預訓練) vs Fine-tuning (微調)** | 先在大雜資料練通用語言能力 (Foundation Model)，再用小精資料調整特定行為 (助理/分類器)。 | 1.3 節兩階段配方：Pretraining 學習通用語言表徵，Fine-tuning 分為 Instruction Fine-tuning 與 Classification Fine-tuning。 |
| **Transformer 架構** | 2017 年為翻譯設計的 Encoder-Decoder 架構，核心 Self-Attention 實現選擇性注意。 | 1.4 節：源自 Vaswani et al. (2017)《Attention Is All You Need》，藉由 Self-Attention 捕捉長距離語意依賴。 |
| **BERT vs GPT** | BERT 取 Encoder 做雙向遮罩預測 (理解/分類)；GPT 取 Decoder 做單向接龍 (生成)。 | 1.4 與 1.6 節：BERT 採 Masked Word Prediction，GPT 簡化為僅 Decoder 並堆疊至 96 層（175B 參數）。 |
| **Scaling Laws / 三大天文數字** | GPT-3 為例：175B 參數、300B tokens、$4.6M 成本；「大」可量化、非形容詞。 | 1.5 節 Table 1.1 與規模換算器：300B tokens 約等於 300 萬本小說，人以 250 tokens/分不眠不休讀完需約 2,283 年。 |
| **Emergent Behavior (湧現行為)** | 未被明確訓練的能力 (翻譯、推理等) 隨規模自然出現，是「一模型多任務」價值來源。 | 1.2 與 1.6 節：訓練目標僅 Next-word prediction，卻因接觸海量多語資料而自然湧現翻譯、摘要、分類能力。 |
| **Zero-shot / Few-shot** | 不改權重、不重訓，純靠 Prompt (零/少範例) 完成新任務，展現極強泛化。 | 1.4 節與知識檢核 Q6：Zero-shot 對未見任務泛化、Few-shot 在 Prompt 提供範例，皆無需修改模型權重。 |
| **開源權重策略與三階段九步驟藍圖** | 自行預訓練成本極高，實務上先在小資料集實作機制，再載入開源權重（如 GPT-2）於消費級硬體微調。 | 1.5 與 1.7 節藍圖：Stage 1 打地基（Ch2–4）→ Stage 2 預訓練與載入 GPT-2 權重（Ch5，繞過 $4.6M 成本）→ Stage 3 微調（Ch6–7）。 |


## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| **Simple training objective × massive scale = seemingly magical capabilities.** | **簡單的訓練目標 × 巨大的規模 ＝ 看似神奇的能力。** | 本章核心心法：Next-word prediction 極簡單，配上 175B 參數與 300B tokens 即產生類人智慧。 |
| **LLM = a deep neural network trained on vast amounts of text to understand, generate, and respond with human-like text.** | **LLM = 在海量文字上訓練、能理解/生成/回應類人文字的深度神經網路。** | 1.1 節一句話定義，點出架構(深度網路)、資料(海量文字)、功能(理解/生成/回應)三要素。 |
| **“Large” is a double entendre: parameter count and dataset size are both unprecedented.** | **「Large」是雙關：參數量與資料量雙雙空前地大。** | 釐清「大」非形容詞，而是兩個可量化規模 (1.5 節有互動換算器)。 |
| **Self-supervised learning: the labels are inside the data — just shift right by one.** | **自監督學習：標籤藏在資料裡——右移一格即得。** | 1.3 節解釋為何無需人工標註：`The model predicts` → input `The model` target `predicts`。 |
| **GPT simplifies the transformer to decoder-only but stacks 96 layers (175B params).** | **GPT 將 Transformer 簡化為僅 Decoder，卻疊 96 層達 175B 參數。** | 1.6 節對比原始 Transformer (Enc 6層 + Dec 6層) 與 GPT 架構選擇差異。 |
| **Autoregressive: the model feeds its own output back as the next input.** | **自回歸：模型把自己的輸出餵回去當下一輪輸入。** | 解釋 ChatGPT 逐字吐出的機制原因，而非單純打字特效。 |
| **Emergent behavior: abilities not explicitly trained (e.g., translation) appear naturally at scale.** | **湧現行為：未被明確訓練的能力 (如翻譯) 隨規模自然出現。** | 1.6 節核心觀察：單一目標訓練卻獲得多任務能力，打破「一任務一模型」舊範式。 |
| **Zero-shot / Few-shot: generalize to new tasks without changing weights or architecture.** | **Zero-shot / Few-shot：不改權重、不改架構，泛化到新任務。** | 1.4 節強調 Transformer/GPT 靈活性來源，Prompt Engineering 的理論基石。 |


## 可參考資料

- **Sebastian Raschka, Build a Large Language Model (From Scratch)**：Manning Publications 出版的原著書籍，本互動教材內容、數值與圖表皆對應第 1 章。
- **Vaswani et al. (2017) "Attention Is All You Need"**：提出 Transformer（Encoder-Decoder 與 Self-Attention）架構的奠基論文。
- **GPT 系列核心論文**：含 Radford et al. (2018) GPT-1、Brown et al. (2020) GPT-3（175B 參數、300B tokens、$4.6M 估算來源）、Ouyang et al. (2022) InstructGPT 微調方法。
- **開放預訓練語料庫**：含 CommonCrawl（佔 GPT-3 訓練權重 60%）、Allen AI Dolma（約 3T tokens）、The Pile、RedPajama 與 FineWeb。
- **開源模型權重與領域模型**：含 OpenAI GPT-2（124M–1.5B，第 5 章載入實作用）、Meta LLaMA 系列與金融領域客製化的 BloombergGPT。
- **PyTorch**：全書實作採用的深度學習框架（附錄 A 提供速成教學）。
- **TwinkleAI 互動教材網站**：提供規模換算器、注意力視覺化與知識檢核等互動元件。 — <https://apps.twinkleai.tw/llm-from-scratch-course/ch01.html>
