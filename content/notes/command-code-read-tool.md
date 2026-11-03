---
title: 重寫 read tool 如何省下數十億 tokens
type: article
source_url: https://x.com/MrAhmadAwais/status/2086521445694517404
source_site: X
added: '2026-08-10'
topics:
- coding-agents
summary: Command Code 透過將 `read_file` 視為「將檔案系統編譯進模型上下文的編譯器」，實作三重上限、自描述錯誤、關係式不變量檢查、自我失效快取、Unicode 檔名修復、串流邊界延遲判斷、圖片品質階梯、筆記本語意化渲染等 14 項工程細節，使每次讀取的 token 成本大幅下降，並在開放模型無法靠智力彌補濫讀的約束下，實現每月節省數十億 token。
abstract: Command Code 創辦人 Ahmad Awais 深度剖析其重寫 `read_file` 工具的 14 項工程決策，展示如何透過多層上限、錯誤恢復、快取失效、檔名修復、串流邊界處理等細節，將每月 5000 萬次讀取操作的 token 浪費從 250 億降至極低，並對比 10 種主流 coding agent 的能力差距。
---

## 完整摘要

### 背景與動機
- **專案**：Command Code（面向開放模型的編碼代理），v1 版本從零重寫 `read_file` 工具。
- **規模**：每月約 5000 萬次讀取；若每次濫讀 500 junk tokens，乘以多輪殘留即達 250 億 junk tokens/月。
- **基準測試**：對比 10 種常見 harness（Claude Code、OpenCode、Cline、Kilo、Codex、Grok、Hermes、Pi、OpenClaw），Claude Code 為閉源，以黑箱探針測試。
- **核心洞見**：coding agent 體感昂貴，帳單多半來自「為建構上下文而讀檔」；開放模型無法像 Claude 那樣「用更多 token 硬讀、靠智力從雜訊找訊號」，必須在工具層省 token。

### 14 項關鍵工程經驗

| # | 主題 | 核心做法與原理 |
|---|------|----------------|
| 1 | **三重上限** | 行窗口 2000 行、位元組預算 128 KB、單行鉗制 2000 字元。缺一不可：大檔、寬行、單行超長各自對應一種「敵對檔案」。 |
| 2 | **沉默是最貴的失敗** | 每個死胡同自帶恢復提示：`empty → "is empty"`、`past EOF → "retry smaller"`、`byte cap → "offset=1847"`、`line cap → "offset=2001"`、`pdf → "pdftotext"`。預計算 resume offset、不加 `Error:` 前綴、byte-truncated 故意在「被截斷的那一行」恢復。 |
| 3 | **關係式不變量 Bug** | `read_file` 記錄「已看內容 + mtime + partial flag」進 ledger；`write_file` 拒絕覆寫 partial 視圖。配合 per-line clamp 產生死循環：read → clamped → ledger partial → write denied → re-read → dedup 回傳 unchanged → 永循環。單一欄位驗證抓不到，需觀察生產流量才能發現。 |
| 4 | **自我失效快取** | 同窗口、同 mtime、同 size 時回傳 stub 而非內容；但若 compaction 吃掉先前 tool result，模型會永遠找不到參考。解法：**dedup hit 即消耗該記錄**，最壞只浪費一輪，避免無界循環。 |
| 5 | **檔名是對抗性的** | macOS 螢幕截圖含 NARROW NO-BREAK SPACE、NFD 分解、引號轉彎。失敗前重試 7 種拼寫變體（窄/寬空格、NFC/NFD、直/彎引號、組合），再做 substring + Levenshtein(2) 的「did you mean」。修復不得越過 workspace 邊界。 |
| 6 | **Chunk 邊界的延遲判斷** | 串流逐 chunk 讀取；若行數限制**剛好在 chunk 邊界**命中，此時「後面還有沒有內容」尚不可知。若猜測會有 ~50% 機率撒謊、多燒一輪。**延遲到下一個 chunk 再決定**，不可知時不發聲。另：別用 `break` 跳出 `for-await`，會觸發 `iterator.return()` 銷毀串流。 |
| 7 | **圖片真正附掛** | 4K 截圖 → JPEG 品質階梯 95→80→60→40→20，首個符合大小即附掛。靠 magic bytes 偵測格式（非副檔名），也為非視覺模型提供 VISION tool。 |
| 8 | **縮圖揭露縮放因子** | 附掛時附帶 `"multiply displayed coords by 2.77"`，否則模型根據縮圖算出的點擊座標全錯。 |
| 9 | **Notebook 渲染為文件** | `.ipynb` 原始 JSON 是 base64 blob + 逐字元 source array。輸出：標籤化 cell、圖表附為真圖片、>10K 字元輸出改為 `jq` 指標。模型能推理資料卻不付 token 代價。 |
| 10 | **無聊格式給單行答案** | `.svg` 當文字（XML 可編輯）、二進位只回 MIME、`.pdf` 給 `pdftotext` 提示（內嵌在規劃中）、按需載入解析器。 |
| 11 | **行號對齊 `cat -n`** | 1-indexed、每行前綴行號。模型、編輯器、堆疊追蹤三方一致，所有 resume offset 與編輯目標依賴此一致性。 |
| 12 | **修復輸入而非拋回** | `filePath` 10 種別名自動修正；數字字串用 `Number()` 強制轉型（`"2abc"` 拒絕、不靜默讀成 2）；小數 offset 拒絕、不取整。**靜默錯誤的窗口比報錯更糟**。 |
| 13 | **必須封鎖的路徑** | `/dev/zero`、`/dev/urandom`、`/dev/stdin`、`/proc/<pid>/fd/*` 在**任何 I/O 前**以名稱拒絕。workspace boundary 在 cwd=/ 時失效，讀 `/dev/zero` 等於自製 DoS。 |
| 14 | **只有被咬到才注意的衛生** | BOM 剝離、CRLF→LF、位元組截斷用二分搜尋 UTF-8 prefix 避免切碼點、dedup 附殺開關 env var。 |

### 基準測試現狀（10 種 harness 對比）
| 能力 | 擁有者數量 |
|------|------------|
| 行窗口（500–2000）+ 第二上限（25K token–128 KB） | 8/10（頂層基本解決） |
| 延遲 chunk 切割 | 1/10 |
| Unicode 檔名重試 | 1/10 |
| 裝置封鎖清單 | 1/10 |
| EOF 回傳提示而非錯誤 | 1/10 |
| 座標縮放提示 | 3/10 |
| Did-you-mean 建議 | 2/10 |
| Partial-view ledger | 2/10 |

**模式**：這些列在 Demo 完全不出現，只在長期會話第 9 小時才開始計費。多數團隊首週憑感覺選 harness 就不再回頭。

### 結論與啟示
- **Claude Code 之所以有趣**：身為現任霸主，擁有 ledger、notebook、vision、empty-file note，卻**無窗口、無位元組上限、無鉗制、無 resume offset、無串流、無 miss 建議**——因為模型夠聰明、團隊尚未被逼迫。
- **Command Code 被迫工程化**：開放模型「浪費一輪即刻體現在評分」，約束反而成了功能，逼出正確解法。
- **開源計畫**：Command Code 即將開源，可直接閱讀程式碼驗證。


## 重點知識與概念拆解

| 概念名 | 一句白話解釋 |
|--------|--------------|
| **三重上限** | 針對「行數多」、「單行寬」、「單行極長」三種敵對檔案，分別設定 2000 行、128 KB、2000 字元/行三道防線，缺一不可。 |
| **自我描述錯誤** | 工具不拋 `Error:`，改回傳人類可讀的狀態句（如 `"is empty"`, `"offset=1847"`），並預計算分頁 offset，讓模型零推理成本直接復原。 |
| **關係式不變量** | 跨工具、跨狀態的不變量（如 read 記錄 partial → write 拒絕覆寫），單一欄位驗證抓不到，唯有觀察生產流量才能發現。 |
| **自我失效快取** | 命中即銷毀記錄；寧可多花一輪重讀，也不可讓模型永遠追著已被 compaction 吃掉的 stub 跑。 |
| **對抗性檔名** | 檔案系統層面的 Unicode 正規化、零寬空間、彎引號差異，模型肉眼看不出來，工具層必須自動重試 7 種變體再做模糊建議。 |
| **Chunk 邊界延遲判斷** | 串流讀取時若限制剛好卡在 chunk 邊界，「後面還有沒有資料」當下不可知；寧可沉默等下一 chunk，也不猜測撒謊。 |
| **JPEG 品質階梯** | 圖片不直接拒絕或硬塞，而是 95→80→60→40→20 逐級壓縮至符合預算，確保視覺模型總能拿到圖。 |
| **縮放因子揭露** | 附掛縮圖時必須附帶座標乘數，否則模型根據縮圖推算的點擊座標會系統性偏移。 |
| **Notebook 語意化渲染** | 將 `.ipynb` 的 JSON 湯轉為標籤化 cell、圖表即圖片、大輸出改 `jq` 指標，模型能推理資料卻不付 token 代價。 |
| **輸入修復而非拋回** | 別名自動對齊、數字字串用 `Number()` 嚴格轉型、拒絕小數 offset；靜默錯誤的讀取窗口比明確報錯危險得多。 |
| **裝置路徑封鎖** | `/dev/zero` 等特殊檔在任何 I/O 前以名稱攔截，防止 cwd=/ 時 workspace boundary 失效導致自製 DoS。 |
| **編碼衛生殺開關** | BOM 剝離、CRLF 正規化、UTF-8 安全截斷、快取附環境變數殺開關，都是「被咬過才會加」的防禦性細節。 |


## 中英金句與解釋

| 原文 | 中譯 | 脈絡/解釋 |
|------|------|-----------|
| "I think the `read_file` tool is like a compiler that turns your filesystem into the model's context. Every decision inside it is a token budget decision multiplied by fifty million times it's used every month." | 「我認為 `read_file` 工具就像一個編譯器，把你的檔案系統編譯進模型的上下文。裡面的每個決策都是 token 預算決策，乘以每月五千萬次使用量。」 | 核心隱喻：將讀檔工具定位為「檔案系統→上下文」的編譯器，強調微小決策經放大後的經濟影響。 |
| "And that's why coding agents feel expensive: the bill is mostly reads building context." | 「這就是為什麼 coding agent 覺得貴：帳單大多數是為了建構上下文而讀檔。」 | 直指成本結構：不是模型推理貴，是工具層濫讀堆出的上下文貴。 |
| "What 'saves billions of tokens' means here: cost per successful read. Claude Code's read tool succeeds by spending more: more tokens per call, more turns per miss, and a model smart enough to fish the signal out of the noise. Ours had to succeed by spending less, because our models can't peek over a sloppy read and our users care about the token bill." | 「這裡的『省下數十億 token』指的是：每次成功讀取的成本。Claude Code 的讀取工具靠花更多 token 成功：每次呼叫更多 token、每次失誤更多輪次、模型夠聰明能從雜訊撈訊號。我們必須靠花更少成功，因為我們的模型沒法從濫讀中撈訊號，用戶也在乎 token 帳單。」 | 對比兩種成功策略：富裕模型靠容錯率、窮模型靠工程精度。 |
| "A naive read and a harness engineered read are both 'correct'. They both work. The difference is that one of them quietly spends a fifth of your context window on bytes the model never needed, and occasionally deadlocks against your own write tool." | 「天真讀取和經工程化的讀取都『正確』。都能動。差別在於其中一個悄悄花掉你五分之一的上下文窗口在模型根本不需要的位元組上，還偶爾跟你自己的寫入工具死結。」 | 「正確性」不等於「工程品質」；隱性成本與死結才是區分業餘與專業的分水嶺。 |
| "The costliest failure is an ambiguous non-answer. An empty result string is indistinguishable, from inside the model, from a broken tool. So it re-reads. Widens the window. Tries a different path. Burns three turns learning what one sentence notice could have told it." | 「最貴的失敗是模稜兩可的非答案。從模型視角看，空結果字串無法區分於壞掉的工具。於是它重讀、放寬窗口、換路徑。燒掉三輪，只為學到一句提示就能知道的事。」 | 定義「沉默」為最高成本失敗模式，並量化其連鎖浪費。 |
| "Shape invariants are checkable per field, and every schema you write already checks them. Relational invariants across stateful tools are where the real bugs live, and you only find them by watching production traffic." | 「形狀不變量可逐欄位檢查，你寫的每個 schema 都在檢查它們。跨有狀態工具的關係不變量才是真正的 Bug 溫床，只有盯著生產流量才能發現。」 | 區分「結構驗證」與「關係不變量」，點出後者需觀測生產才能捕獲。 |
| "A cache whose stale hit is catastrophic should expire itself on use." | 「命中即災難的快取，應該在使用時自我失效。」 | 快取設計原則：若 stale hit 後果不可控（模型永遠找不到參考），寧可犧牲 hit rate 換安全。 |
| "When a failure is invisible to the model, retrying is the tool's job. The model would retry the same wrong bytes forever. This is what harness engineering is about: finding the invisible failure modes and fixing them in the tool so the model can focus on reasoning." | 「當失敗對模型不可見時，重試是工具的責任。模型會用同樣錯誤的位元組無限重試。這就是 harness 工程的核心：找出不可見的失敗模式，在工具層修好，讓模型專注推理。」 | 定義 harness engineering 的使命：吸收模型看不見的環境雜訊。 |
| "Constraint is a feature - it forces you to engineer the right solution instead of hoping the model will figure it out." | 「約束是功能——它逼你工程出正確解法，而不是指望模型自己想辦法。」 | 反轉約束論：資源限制反而催生更優工程，避免依賴模型智力補洞。 |


## 可參考資料

- **Command Code**（文中提及的編碼代理專案，即將開源）  
- **Claude Code**（Anthropic 官方編碼代理，閉源，作為基準對比欄）  
- **其他基準測試對象**：OpenCode、Cline、Kilo、Codex、Grok、Hermes、Pi、OpenClaw（多為開源）  
- **`pdftotext`**（Poppler 工具，用於 PDF 文字擷取提示）  
- **`jq`**（JSON 處理工具，用於 Notebook 大輸出指標）  
- **Unicode 正規化形式**：NFC、NFD（檔名修復章節涉及）  
- **Levenshtein 距離**（檔名模糊建議演算法，距離 ≤ 2）  
- **Magic bytes / File signatures**（圖片格式偵測依據，非副檔名）  

> 本內容未明確提及其他論文、書籍或外部連結資源。
