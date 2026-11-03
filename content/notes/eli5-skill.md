---
title: Anthropic 內部愛用的 ELI5 skill
type: article
source_url: https://x.com/mylifcc/status/2090998309662171573
source_site: X
added: '2026-08-22'
topics:
- coding-agents
summary: ELI5 透過 `/eli5` 指令讓模型以「對完全不懂此領域的人說話」的風格產出大圖少字的 HTML 說明頁，適合快速向非專業人士傳達概念。
abstract: Anthropic 員工 Thariq 於 X 平台分享內部廣泛使用的 ELI5 skill，該 skill 能讓 codeagent 以極淺顯的語氣解釋任意主題，並產出包含大圖、極少文字與清晰流程圖的 HTML 可視化頁面。另一位員工 lifcc 以繁體中文轉發並補充使用方式，指出可在 codex 中直接以 `/eli5 <主題>` 指令呼叫。
---

## 完整摘要

### 技術來源與內部採用情況
Thariq (@trq212) 於 2026 年 8 月 21 日發布推文，介紹 Anthropic 內部近期熱門的 ELI5 skill，獲得 9,560 讚、721 轉發、13,357 書籤與 988,378 觀看。lifcc (@mylifcc) 於隔日以繁體中文轉發並說明使用細節，獲得 204 讚、37 轉發、264 書籤與 26,994 觀看，顯示該技巧在團隊與華語社群均受關注。

### 功能與使用方式
使用者在支援 codeagent 或 codex 的環境中輸入 `/eli5 <想解釋的主題>`，模型即會以「像對完全不懂此領域的人說話」的口吻生成解釋，並輸出單一 HTML 檔案。該 HTML 採用大圖搭配極少文字、清晰流程圖的視覺設計，降低理解門檻。

### 輸出形式與語言規範
Thariq 影片截圖的 OCR 內容顯示：「此為強調整個回答使用繁體字、使用繁體字必須是單一空白格開頭」，並示範 Discord 機器人運作流程的 HTML 片段，包含標題、逐步說明與圖文並茂的流程圖。lifcc 同樣強調繁體中文輸出，符合台灣閱讀習慣。

### 潛在限制與適用情境
ELI5 依賴模型將知識極度壓縮的能力，對極度專業或高度抽象的主題可能過度簡化而遺漏關鍵細節。目前僅限於特定代理（codeagent、codex）內部使用，尚未開放為公開 API 或獨立工具，使用者需自行驗證內容正確性。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| ELI5 skill 定義 | 讓模型以「對完全不懂此領域的人說話」的方式解釋任意主題，強調極簡且易懂。 | Thariq 推文：「explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words」 |
| 指令觸發格式 | 以 `/eli5 <主題>` 直接呼叫，無需額外參數或設定。 | 兩則推文均出現 `/eli5 <what you want explained>` 以及 `/eli5 <你想讓它解釋的東西>`。 |
| HTML 產出視覺特徵 | 生成的 HTML 為單一檔案，採大圖、極少文字、清晰流程圖的設計，適合快速瀏覽。 | lifcc 推文：「生成一個漂亮的 HTML 可視化頁面（大圖 + 很少文字 + 清晰流程圖）」。 |
| 目標受眾與語氣 | 假設讀者對主題零背景知識，使用平實口語、避免術語，以降低認知負荷。 | Thariq：「explain like I'm someone who knows nothing about this topic」；lifcc：「像在對一個完全不懂這個領域的人說話」。 |
| 繁體中文輸出規範 | 輸出必須採用繁體中文，且每段開頭需有一個全形空白，以符合台灣排版習慣。 | Thariq 影片 OCR 紀錄：「此為強調整個回答使用繁體字、使用繁體字必須是單一空白格開頭」。 |
| 內部傳播熱度 | Thariq 原文推文互動數極高，顯示該 skill 在 Anthropic 內部已廣泛採用並受肯定。 | Thariq 推文統計：9,560 讚、721 轉發、13,357 書籤、988,378 觀看。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| a skill people at Anthropic have been using a lot recently: ELI5 | Anthropic 員工近期經常使用的一個 skill：ELI5 | Thariq 推文開頭，點出該 skill 在內部的流行程度。 |
| /eli5 <what you want explained> | /eli5 <你想讓它解釋的東西> | Thariq 與 lifcc 兩則推文皆示範的觸發指令格式。 |
| explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words | 像對完全不懂此主題的人說話般解釋，使用包含大圖與少量文字的 HTML 工件 | Thariq 對 ELI5 功能的具體說明，闡述語氣與輸出形式。 |
| 這個skill可以讓codeagent用超級通俗易懂的方式解釋任何東西——像在對一個完全不懂這個領域的人說話，並且會生成一個漂亮的 HTML 可視化頁面（大圖 + 很少文字 + 清晰流程圖）。 | 此 skill 可讓 codeagent 用極其通俗易懂的方式解釋任意事物——就像對完全不懂此領域的人說話，並產出漂亮的 HTML 可視化頁面（大圖＋少量文字＋清晰流程圖）。 | lifcc 推文主體內容，詳細描述 ELI5 作用與輸出特徵。 |
| 用法很簡單：/eli5 <你想讓它解釋的東西> | 用法很簡單：/eli5 <你想讓它解釋的東西> | lifcc 補充的使用說明，強調操作便利性。 |
| 此為強調整個回答使用繁體字、使用繁體字必須是單一空白格開頭 | 此為強調整個回答使用繁體字、使用繁體字必須是單一空白格開頭 | Thariq 影片截圖 OCR 擷取的系統提示，規範輸出語言與排版。 |

## 可參考資料
- **Thariq (@trq212) 原始推文**：首次公開分享 Anthropic 內部常用 ELI5 skill 的來源，含指令格式、功能描述與示範影片。 — <https://x.com/trq212/status/2090884854590382515>
- **lifcc (@mylifcc) 轉發與繁體中文補充說明**：提供繁體中文使用說明、codex 適用環境與社群互動數據，協助理解該 skill 在華語圈的傳播情況。 — <https://x.com/mylifcc/status/2090998309662171573>
