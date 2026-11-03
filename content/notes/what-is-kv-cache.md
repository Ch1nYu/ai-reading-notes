---
title: What is KV Cache in LLMs?
type: article
source_url: https://x.com/amitiitbhu/status/2037413998279491927
source_site: X
added: '2026-09-07'
topics:
- llm-internals
summary: KV Cache 只在每一步為新 token 計算 Key、Value，並從快取取出過去 token 的 Key/Value，避免重複運算，使文字生成的時間複雜度從平方級降為線性級，代價是記憶體隨序列長度線性成長。
abstract: 本文解釋大型語言模型（LLM）在逐 token 生成文字時，因注意力機制需要重複計算先前 token 的 Key 與 Value 而導致 O(n²) 的運算量。KV Cache 透過將每個 token 的 Key、Value 快取並重複使用，使運算量降至 O(n)，但隨序列長度線性增加記憶體佔用，且作者預告下一篇將介紹 Paged Attention 以解決此記憶體問題。
---

## 完整摘要

### LLM 逐 token 生成與注意力機制的角色
LLM 每次只產出一個 token，預測時必須「看過」所有先前 token，這由注意力層完成。注意力層將每個 token 轉換為 Query（Q）、Key（K）、Value（V）：當前 token 用 Query 與過去所有 token 的 Key 比較取得注意力分數，再加權取得對應的 Value。文章以課堂比喻說明：Query 是新生的提問、Key 是舊生胸前的名牌（標示專長）、Value 是舊生手中的筆記內容。此機制使得每一步都需要重新計算過去 token 的 K、V，因而產生重複運算的問題。

### 重複計算步驟的具體示範
以 "I love → I love teaching → I love teaching AI" 三步為例，第 1 步需為 I、love 計算 K、V、Q；第 2 步必須重新為 I、love、teaching 計算一次；第 3 步則再次重新為 I、love、teaching、AI 計算。隨序列增長，第 n 步必須重新計算前 n‑1 個 token 的 K、V，導致總運算量呈 O(n²) 級增長（文中試算 100 tokens 無快取需 5,049 次 K/V 計算），嚴重拖慢生成速度。

### KV Cache 的運作流程與核心概念
核心想法是每個 token 的 K、V 僅計算一次、存入快取，之後只為新 token 計算 K、V、Q，並從快取取出過去的 K、V。文章以開會筆記作類比：不必讓過去發言者重複說話，只需閱讀筆記並聽取新發言者。如此，100 tokens 的 K/V 計算次數從 5,049 次降至 101 次（2 + 1×99），約快 50 倍。Query 不會被快取，因為它只服務於當前 token，預測完成即失效。此方法將時間複雜度降為 O(n)。

### 為何只快取 Key 與 Value 而非 Query
Query 代表當前 token 的「需求」，僅在該 token 的預測階段使用，預測完成後即不再需要；相反，每個過去 token 的 Key 與 Value 在每一個未來步驟都可能被注意力機制檢索，因此必須持久化。文中明確指出：「The Query is only needed for the current token … But the Key and Value of every past token are needed at every future step…」，這解釋了 KV Cache 僅保存 K、V 的原因。

### 計算量減少的量化與速度提升
文章提供具體試算：生成 100 tokens，無快取時 K/V 計算總數為 2+3+…+100 = 5,049；使用 KV Cache 後為 2 + 1×99 = 101，減少約 98% 的運算，相當於約 50 倍的速度提升。此數據說明 KV Cache 將時間複雜度從 O(n²) 降至 O(n)。然而，隨序列增長，快取會佔用額外記憶體，極長序列（數千 tokens）可能造成記憶體壓力。

### 記憶體權衡與後續發展：Paged Attention 預告
KV Cache 以記憶體換取速度：序列越長、快取佔用的記憶體越大，對於上下文達數千 tokens 的情況，記憶體佔用可能變得顯著。文章結尾預告下一篇將介紹 Paged Attention，以解決 KV Cache 的記憶體問題，並署名為 Outcome School 創辦人 Amit Shekhar。此後續技術旨在透過分頁管理降低記憶體碎片與峰值佔用。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| LLM 自迴歸生成需查看全部過去 tokens | 模型每次預測新 token 時，都必須參考之前產出的所有 tokens，這是注意力機制運作的基礎，也是重複計算的根源。 | "The important thing to notice here is: every time the model predicts a new token, it needs to look at all the previous tokens to decide what comes next." |
| 注意力層的 Q、K、V 職責分工 | Query 代表當前 token 想要找的資訊，Key 描述過去 token 所含的資訊，Value 則是實際內容。當前 token 透過 Query 與過去的 Key 比較取得注意力分數，再用該分數加權取得過去的 Value。 | 課堂比喻：「Query: The new student's question… Key: The name tag… Value: The actual notes…」 |
| 重複計算的量化試算 | 以 100 tokens 為例，未使用 KV Cache 時需進行 5,049 次 K/V 運算；使用 KV Cache 後僅需 101 次，運算量減少約 98%，速度提升約 50 倍。 | "if the model is generating a sequence of 100 tokens, without KV Cache… 5,049 computations. With KV Cache… 101 computations. That is roughly 50 times fewer computations." |
| 僅快取 Key 與 Value 的原因 | Query 隨著當前 token 的產生而產生並消失，不會被後續 token 重用；反之，每個過去 token 的 Key 與 Value 在每一個未來步驟都可能被注意力機制需要，因此必須持久化。 | "The Query is only needed for the current token… But the Key and Value of every past token are needed at every future step…" |
| 記憶體隨序列長度線性增長的代價 | 每個 token 的 K、V 向量大小取決於模型隱藏層與注意力頭數，固定不變；因此序列越長、快取佔用的記憶體越長，極長上下文可能耗盡 GPU 顯存。 | "As the sequence gets longer, the cache grows larger. For very long sequences with thousands of tokens, the cache can consume a significant amount of memory." |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| The important thing to notice here is: every time the model predicts a new token, it needs to look at all the previous tokens to decide what comes next. | 這裡要注意的重點是：模型每次預測新 token 時，都需要查看所有先前的 token 才能決定下一個是什麼。 | 說明 LLM 自迴歸生成的基本特性，為後續引出重複計算問題鋪路。 |
| Think of it like taking notes. Imagine you are in a meeting. Every time someone new speaks, instead of asking all the previous speakers to repeat what they said, you simply read from your notes and only listen to the new speaker. The notes are your cache. | 把它想成做筆記。想像你在開會。每當有新發言者，你不需要請所有前面的人重複一遍，只需閱讀筆記並聽新發言者即可。筆記就是你的快取。 | 以會議筆記比喻 KV Cache 的核心直覺：避免重複聽取（計算）已知內容。 |
| The Query is only needed for the current token - the one being generated right now. The current token uses its Query to compare against the Keys of all previous tokens to find which ones are relevant. Once the prediction is done, that Query is no longer needed. | Query 僅用於當前正在生成的 token。當前 token 用它的 Query 比對所有先前 token 的 Key 以找出相關者。預測完成後，該 Query 就不再需要了。 | 解釋為何 KV Cache 不快取 Query，強調 Query 的一次性與 K/V 的持久性差異。 |

## 可參考資料
- **Amit Shekhar (@amitiitbhu)**：文章作者，Outcome School 創辦人，發布於 X (Twitter) 平台。 — <https://x.com/amitiitbhu/status/2037413998279491927>
- **Paged Attention**：作者預告下一篇將介紹的技術，旨在解決 KV Cache 的記憶體問題。
