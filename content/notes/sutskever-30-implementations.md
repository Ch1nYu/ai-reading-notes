---
title: Ilya Sutskever 推薦的 30 篇論文實作
type: article
source_url: https://github.com/pageman/sutskever-30-implementations
source_site: GitHub
added: '2026-09-09'
topics:
- llm-internals
summary: pageman 以純 NumPy 完成 Ilya Sutskever「讀完這 30 篇論文就懂 90% 重要深度學習知識」清單的全套教學實作，涵蓋 RNN、Transformer、擴展法則、記憶網路等主題，並提供四條學習路徑供不同程度學習者循序漸進。
abstract: 這是一個 GitHub 倉庫，包含 30 篇 Ilya Sutskever 推薦的深度學習基礎論文的完整 NumPy 實作，每篇都以 Jupyter Notebook 形式提供、附合成資料與視覺化，旨在讓學習者不依賴深度學習框架即可從零理解核心機制。
---

## 完整摘要

### 專案背景與完成度
此倉庫源自 Ilya Sutskever 告訴 John Carmack 的經典閱讀清單，作者 pageman（Paul 'The Pageman' Pajo）在 2025 年 12 月前完成全部 30 篇論文的實作（30/30，100%）。每個 Notebook 皆使用純 NumPy、內建合成資料、可直接在 Jupyter 執行，並附帶詳細視覺化與解釋。README 另列出三個延伸專案：Sutskever-Agent（給 Agent 使用）、sutskever-30-beyond-numpy（多語言/多後端實作）與付費 Google Colab 完整程式碼包。

### 論文分類與重點實作
30 篇論文依主題分為四大類：(1) 基礎概念（第 1-5 篇）：複雜度動力學、字元級 RNN、LSTM、RNN 正則化、神經網路剪枝與 MDL 原則。(2) 架構與機制（第 6-15 篇）：Pointer Networks、AlexNet、Seq2Seq for Sets、GPipe、ResNet、擴張卷積、圖神經網路、Transformer、Bahdanau Attention、Pre-activation ResNet。(3) 進階主題（第 16-22 篇）：關係推理、VAE、Relational RNN（含約 1100 行手寫反向傳播）、Coffee Automaton（不可逆性）、Neural Turing Machine、Deep Speech 2（CTC 語音辨識）與擴展法則（Scaling Laws）。(4) 理論與元學習（第 23-30 篇）：MDL 原則、機器超級智慧（AIXI）、Kolmogorov 複雜度、CS231n 視覺管線、多 token 預測（Multi-token Prediction）、密集段落檢索（DPR）、RAG 與 Lost in the Middle。

### 學習路徑與實作哲學
README 規劃四條學習軌：入門（字元 RNN→LSTM→AlexNet→ResNet→VAE）、進階（RNN 正則化→Bahdanau Attention→Pointer Networks→Seq2Seq for Sets→CS231n→GPipe→Transformer→擴張卷積→擴展法則）、高階（Pre-activation ResNet→GNN→關係網路→Neural Turing Machine→CTC→密集檢索→RAG→Lost in the Middle）、理論與基礎（MDL 原則→Kolmogorov 複雜度→複雜度動力學→Coffee Automaton）。

### 關鍵洞見與延伸方向
作者總結四大架構演進脈絡：RNN→LSTM（閘機制解決梯度消失）、Plain Net→ResNet（跳躍連結實現深層）、RNN→Transformer（注意力實現並行化）、固定詞表→Pointer（輸出可參考輸入）。四大基本機制：注意力（可微分選擇）、殘差連結（梯度高速公路）、閘控（學習資訊流控制）、外部記憶體（儲存與計算分離）。訓練層面強調擴展法則可預測、正則化與最佳化技巧、Compute-Optimal 權衡。理論基石包含資訊論（壓縮、熵、MDL）、複雜度（Kolmogorov 複雜度、冪律）、生成模型（VAE、ELBO、潛在空間）與記憶體（可微分資料結構）。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 純 NumPy 實作教學策略 | 刻意不使用 PyTorch/TensorFlow，強迫學習者手寫前向/反向傳播、卷積、注意力等核心運算，避免框架 API 遮蔽細節，使原理可遷移至任何框架。 | README 'Implementation Philosophy' 章節列出四點理由：Deepen understanding、Educational clarity、Core concepts、Transferable knowledge；所有 30 個 Notebook 均標示 ✅ Uses only NumPy。 |
| 合成資料即時可執行 | 每個 Notebook 內建資料生成程式碼（如字元 RNN 用莎士比亞文本、VAE 用二維高斯混合、CTC 用合成語音序列），免去下載與前處理，適合快速實驗與修改驗證。 | Quick Start 僅需 `pip install numpy matplotlib scipy` 即可執行任一 Notebook；'Synthetic Data Approach' 段落說明：Immediate execution、Controlled experiments、Concept focus、Rapid iteration。 |
| Relational RNN 手寫反向傳播（約 1100 行） | 第 18 篇論文實作不僅示範前向架構（關係記憶體+多頭自注意力），還在 Section 11 完整手寫所有元件的反向傳播並通過數值梯度驗證，展示最完整的從零實作深度。 | Featured Implementations > Advanced Topics > `18_relational_rnn.ipynb` 項目明列：'Section 11: Manual backpropagation implementation (~1100 lines)'、'Complete gradient computation for all components'、'Gradient checking with numerical verification'。 |
| Coffee Automaton 深度探討不可逆性 | 第 19 篇以咖啡混合為切入點，跨越統計物理（李烏維爾定理、龐加萊回歸）、資訊論（Landauer 原則、單向函數）、機器學習（Information Bottleneck）、生物學等 10 個章節，將熱力學時間之箭與計算不可逆性串聯。 | Latest Additions 列出 Paper 19 新增；Featured Implementations > Advanced Topics 列出 10 個子主題：Coffee mixing、Entropy growth、Phase space、Poincaré recurrence、Maxwell's demon、Landauer's principle、Computational irreversibility、Information bottleneck、Biological irreversibility、Arrow of time。 |
| CS231n 完整視覺管線（kNN→CNN）純 NumPy 重現 | 第 26 篇將 Stanford CS231n 整學期課程壓縮為單一 Notebook，含 kNN、線性分類器（SVM/Softmax）、優化器（SGD/Momentum/Adam/LR 排程）、兩層神經網路反向傳播、卷積/池化/ReLU、Mini-AlexNet、濾波器視覺化、遷移學習、調參實務建議，共 10 章節。 | Featured Implementations > Scaling & Theory > `26_cs231n_cnn_fundamentals.ipynb` 列出 10 項內容；Latest Additions 標註 Paper 26 新增；Repository Structure 顯示檔案名稱。 |
| 機器超級智慧（AIXI、Solomonoff 歸納、遞歸自我改進）形式化理論實作 | 第 24 篇將 Legg & Hutter 的通用智慧定義 Υ(π)、Solomonoff 先驗、AIXI 最優強化學習代理人、蒙地卡羅近似（MC-AIXI）、Kolmogorov 複雜度估測、智慧測量、智慧爆炸情境等 6 大章節以 NumPy 實作，串聯第 23、25、8 篇概念。 | Featured Implementations > Scaling & Theory > `24_machine_super_intelligence.ipynb` 列出 10 項內容含 'Formal theory of intelligence (Legg & Hutter)'、'AIXI: Theoretically optimal RL agent'、'Recursive self-improvement dynamics'、'Intelligence explosion scenarios'、'6 sections: from psychometrics to superintelligence'。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| If you really learn all of these, you'll know 90% of what matters today. | 如果你真的把這些全學會，你就會懂今天 90% 重要的事情。 | README 結語引用 Ilya Sutskever 原話，強調此 30 篇清單的核心地位。 |
| These implementations deliberately avoid PyTorch/TensorFlow to: Deepen understanding: See what frameworks abstract away | 這些實作刻意避開 PyTorch/TensorFlow，為了：加深理解：看清框架抽象掉了什麼 | Implementation Philosophy > Why NumPy-only? 章節第一點理由。 |
| Progress: 30/30 papers (100%) - COMPLETE! 🎉 | 進度：30/30 篇論文（100%）——完成！🎉 | Overview 章節開頭標示專案完成狀態。 |

## 可參考資料
- **Ilya Sutskever's Reading List (GitHub)**：原始 30 篇論文清單來源，Sutskever 推薦給 John Carmack 的閱讀清單。 — <https://github.com/dzyim/ilya-sutskever-recommended-reading>
- **Aman's AI Journal - Sutskever 30 Primers**：對應每篇論文的詳細解讀筆記，輔助理解實作背景。 — <https://aman.ai/primers/ai/top-30-papers/>
- **The Annotated Transformer**：Transformer 架構逐行註解教學，與第 13 篇實作互補。 — <http://nlp.seas.harvard.edu/annotated-transformer/>
- **Andrej Karpathy's Blog**：第 2 篇字元級 RNN 實作參考來源（Karpathy 'The Unreasonable Effectiveness of RNNs' 部落格文章）。 — <http://karpathy.github.io/>
- **PaperCode**：啟發本專案的互動式論文實作網站。 — <https://papercode.vercel.app/>
- **Sutskever-Agent**：本專案姊妹專案，供 AI Agent 使用同組實作。 — <https://github.com/pageman/Sutskever-Agent>
- **sutskever-30-beyond-numpy**：多語言/多後端版本實作（不限 NumPy）。 — <https://github.com/pageman/sutskever-30-beyond-numpy>
- **Google Colab Code (Gumroad)**：付費提供可直接在 Colab 執行的完整程式碼包。 — <https://pageman.gumroad.com/l/sutskever30colabcode>
- **Stanford CS231n: Convolutional Neural Networks**：第 26 篇實作參考課程，涵蓋 kNN 到 CNN 完整管線。
- **Stanford CS224n: NLP with Deep Learning**：推薦延伸課程，涵蓋注意力、Transformer 等 NLP 核心主題。
- **MIT 6.S191: Introduction to Deep Learning**：推薦入門課程，適合在學習本專案前建立基礎。
