---
title: dots3-note Preview 模型介紹
type: article
source_url: https://studio.dots.ai/dots/dots3-en.html
source_site: studio.dots.ai
added: '2026-08-16'
topics:
- models
summary: dots3-note Preview 是一個 280B/16B 的多模態開源模型，透過 TEMPO 強化學習實現自我評估與長時程任務學習，在推理、代理、多模態等多項基準測試中表現優異，並開源 VibeSearchBench 與 VibeLifeBench 兩個真實場景評測環境。
abstract: dots3-note Preview 是 dots3 系列中最輕量的模型，總參數 280B、啟用參數 16B，支援 512K 上下文視窗，具備文本、視覺、語音多模態理解能力，並針對複雜推理與長期任務代理進行優化。該模型採用 TEMPO 強化學習方法，實現自我評估與長時程任務學習，在多項基準測試中達到或超越更大規模模型的表現。模型已在 Hugging Face 和 GitHub 以 Apache 2.0 開源授權發布，並提交至 Transformers 庫。
---

## 完整摘要

### 模型架構與發布資訊
dots3-note Preview 為 dots3 系列最輕量模型，總參數 280B、啟用參數 16B（推測採用 MoE 架構），支援 512K 上下文視窗，具備文本、視覺、語音三模態理解能力。模型在 Hugging Face (dots-studio/dots3-note-prev) 和 GitHub (studio-dots-ai/dots3-note-prev) 以 Apache 2.0 授權開源，架構已提交 Transformers (PR #47844)，並可透過 OpenRouter 申請免費 API 存取。完整技術報告將於一週內發布。

### TEMPO 強化學習與自我評估能力
TEMPO (Test-time-scaled Value Estimation with Macro-step Policy Optimization) 將長時程任務分解為多個巨步，每個巨步包含多輪模型與環境互動。巨步結束時，同一代理從行動者切換為評論者，利用測試時擴展推理估算當前狀態的預期剩餘回報，從而在任務完成前更新策略。此方法解決了單次軌跡超過十小時導致的訓練低效與稀疏獎勵信用分配難題。在 ARC-AGI-3 上，TEMPO 平均分數比基準檢查點高 31.5%、比 GRPO 高 20.6%，且在相同水平下所需步數更少。評論者能區分表面相似但實質不同的軌跑分支，識別真正突破環境規則理解的分支並給予更高價值估計。

### 遞迴自我批評與持續學習
模型展現出強大的自我評估能力：即使尚未解決問題，也能作為評論者區分相似狀態、識別真正突破並給出不同價值估計。蒙地卡羅採樣分析顯示測試時擴展使代理成為特別優秀的評論者，支持「評估比生成容易」的假設。在 IMO 2026 中，基於 dots3-note Preview 分支構建的內部哈勃讓代理能遞迴生成證明並使用工具評估改進，最終獲得官方認證的 42/42 滿分與金牌。此能力推廣至陌生環境：在 ARC-AGI-3 (40-50 小時、數千次互動) 和 Slay the Spire 2 中，模型能主動觀察、形成並驗證假設、更新記憶並在未來決策中使用。強化學習教會模型在任務遠超上下文視窗時創建支援未來決策的記憶。

### 真實場景長時程任務與評測基準
為從封閉環境邁向真實生活，團隊構建涵蓋旅行、醫療、採購、履約、社交等服務的複雜模擬環境，擁有獨立後端狀態機與模擬時間線。用戶意圖在多輪互動中逐漸浮現並隨中間結果演變；任務跨越數天甚至數週，需保持並更新狀態；外部環境（天氣、價格、庫存、航班）異步變化。開源兩大評測基準：VibeSearchBench 評估逐步揭示意圖的多輪深度搜索 (200 任務、20 領域、Triplet F1 為主指標)；VibeLifeBench 評估動態環境中跨階段任務執行 (20 任務、10 領域、20-30 階段、1,247 原子檢查)。dots3-note Preview 在 VibeLifeBench 28.1%、VibeSearchBench 25.7% 表現領先或接近最強模型。

### 基準測試綜合表現
推理與代理能力：ARC-AGI-2 81.4%、ARC-AGI-3 general harness 32.1%、ClawEval Pass^3 73.4%、WildClawBench 61.7%、SWE-bench Verified 78.4%、SWE-bench-pro 61.0%、Codeforces 3056 分、LiveCodeBench v6 91.5%。多模態能力：WorldVQA 42.7、SimpleVQA 72.5、MMMU Pro 79.1、MathVision 87.7、CharxivReasoning 83.1、GDP.pdf 60.7、PerceptionBench 53.4、MME Video-V2 39.3、VoiceBench 92.4、MMAU-PRO 69.8。資訊檢索：BrowseComp w/ CM 83.3%、DeepSearchQA 92.1%、WideSearch 78.9%。工具使用：Terminal-Bench 2.1 75.1%、Toolathlon-Verified 55.6%、APEX-Agent 30.8%。整體在同參數級別模型中具備強競爭力。

### 局限性與未來方向
作為預覽版，強化學習尚未完成，存在幻覺緩解、文本與多模態能力平衡、整體穩定性等限制。真實生活任務目前在模擬環境運行，轉化為可靠的真實體驗仍需健壯的哈勃、連接器、數據源、安全權限機制與產品設計。團隊承諾不僅開源模型權重，也分享方法、教訓、失敗與反思，邀請社區共同建設真正服務於大眾的 AI。未來重點：從可驗證長時程任務邁向模糊的日常任務，解決缺乏可驗證獎勵信號的挑戰，深化遞迴自我批評能力。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| TEMPO 強化學習框架 | TEMPO 將長時程任務分解為多個巨步，每個巨步結束時讓同一模型從行動者切換為評論者，利用測試時擴展推理進行自我價值估計，從而在任務完成前更新策略。此方法解決單次軌跡過長導致的訓練低效與稀疏獎勵信用分配問題，在 ARC-AGI-3 上比基準高 31.5%、比 GRPO 高 20.6%。 | 文中詳細描述 TEMPO 架構：'TEMPO decomposes a long-horizon task into multiple macro-steps... At the end of each macro-step, the same agent switches from actor to critic and uses test-time-scaled reasoning to estimate the expected remaining return from the current state.' 並展示『place knights』遊戲中評論者區分 Branch A/B 的案例，Branch A 價值 3.80、Branch B 價值 2.29。 |
| 遞迴自我批評與 IMO 2026 金牌 | 模型具備強大的自我評估能力，甚至在無法解決問題時也能作為評論者識別突破。此能力在 IMO 2026 獲得驗證：基於 dots3-note Preview 分支構建的哈勃讓代理遞迴生成證明、使用工具評估改進，最終獲得官方認證 42/42 滿分與金牌。 | 文中明確指出：'At IMO 2026... we built an internal harness around a branch of dots3-note Preview. The harness enabled the agent to generate proofs recursively and use tools to evaluate and improve them... earned an officially certified perfect score of 42/42 and an IMO gold medal.' |
| 陌生環境中的持續學習與記憶更新 | 模型在遠超上下文視窗的超長時程任務中，學會透過探索環境、形成驗證假設、更新記憶並應用於未來決策。此能力在 ARC-AGI-3 (40-50 小時、數千次互動) 和 Slay the Spire 2 中得到驗證，並泛化至未訓練過的陌生環境。 | 文中記載：'We found that dots3-note Preview not only demonstrates excellent problem-solving ability, but also exhibits a strong research-oriented mode of thinking: it can observe through interaction with the environment, proactively form and test hypotheses, update its memory, and use that memory in future decisions.' 並附 ARC-AGI-3 平均分數與推理成本關係圖。 |
| 真實生活模擬環境與雙基準開源 | 為解決真實任務三大特徵（意圖逐漸浮現、跨階段執行、環境動態變化），團隊構建涵蓋旅行、醫療、採購等服務的複雜模擬環境，並開源 VibeSearchBench (多輪深度搜索、200 任務) 與 VibeLifeBench (跨階段動態執行、20 任務、1,247 原子檢查) 供社區復現測量。 | 文中完整描述兩基準：'VibeSearchBench: Evaluates multi-turn search with progressively disclosed intent... 200 tasks across 20 domains... Triplet F1 as the primary metric.' 'VibeLifeBench: Evaluates cross-stage task execution in dynamic environments... 20 tasks across 10 domains, each spanning 20–30 stages... 1,247 atomic checks.' |
| 多模態統一架構與綜合基準領先表現 | dots3-note Preview 為系列首個在單一模型內整合文本、視覺、音頻理解的版本，同時在推理、代理、編碼、工具使用、多模態等廣泛基準上達到或超越同量級甚至更大模型，展現統一多模態架構的效能優勢。 | 附錄兩大表格完整記錄：推理代理表中 ARC-AGI-2 81.4%、ARC-AGI-3 general 32.1%、SWE-bench Verified 78.4%、Codeforces 3056；多模態表中 VoiceBench 92.4、MMAU-PRO 69.8、MathVision 87.7、MMMU Pro 79.1 等。 |
| 開源策略與社區共建願景 | 模型權重、架構、評測環境全面開源 (Apache 2.0)，並承諾分享方法、教訓、失敗與反思，邀請社區共同建設真正服務大眾的 AI。技術報告將於一週內發布，Transformers 整合 PR 已提交。 | 文中結語：'We believe that open-sourcing model weights is only one part of being open. We also want to share the methods, lessons, failures, and reflections from our exploration so that more people can understand, use, and build on these technologies.' |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| We have always hoped to build AI that benefits everyone and helps people solve the many problems they encounter in life. | 我們一直希望構建造福大眾、幫助人們解決生活中遇到的諸多問題的 AI。 | 文章開頭闡述 dots 團隊的核心使命與願景。 |
| A model's ability to evaluate itself is critically important. | 模型自我評估的能力至關重要。 | 在遞迴自我批評章節，強調自我評估能力對從可驗證任務邁向模糊日常任務的關鍵角色。 |
| TEMPO therefore enables effective reinforcement learning on tasks in which a single run takes tens of hours. | 因此 TEMPO 使得在單次運行需耗費數十小時的任務上進行有效強化學習成為可能。 | TEMPO 方法介紹結尾，總結其解決超長時程任務訓練的核心價值。 |

## 可參考資料
- **dots3-note Preview 官方發布頁面**：本文主要內容來源，包含模型規格、方法介紹、基準結果、開源連結等完整資訊。 — <https://studio.dots.ai/dots/dots3-en.html>
- **TEMPO 方法詳細部落格**：TEMPO 強化學習框架的深度技術說明。 — <https://studio.dots.ai/dots/tempo-blog.html>
- **VibeSearchBench 官方網站**：多輪深度搜索評測基準的詳細規格、任務與評分標準。 — <https://vibebench.github.io/VibeSearchBench.github.io/>
- **VibeLifeBench 官方網站**：動態環境跨階段任務執行評測基準的詳細規格與原子檢查說明。 — <https://vibebench.github.io/VibeLifeBench_homepage/>
- **Hugging Face 模型倉庫**：模型權重下載、模型卡片與推理示例。 — <https://huggingface.co/dots-studio/dots3-note-prev>
- **GitHub 代碼倉庫**：模型實現代碼、使用指南與相關工具腳本。 — <https://github.com/studio-dots-ai/dots3-note-prev>
- **Transformers 整合 PR**：模型架構官方整合進度與技術細節討論。 — <https://github.com/huggingface/transformers/pull/47844>
- **IMO 2026 成果說明**：基於 dots3-note Preview 獲得 IMO 金牌的技術細節與哈勃設計。 — <https://studio.dots.ai/dots/imo-en.html>
