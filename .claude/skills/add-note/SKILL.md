---
name: add-note
description: 新增一篇筆記到 AI 閱讀筆記網站。使用時機：使用者給一個整理工具的輸出資料夾（含 notes.md）、一個網址，或貼上一段筆記，要求加進網站。
---

# 新增一篇筆記

格式規則以 `AGENTS.md` 的「筆記檔格式」為準，這裡只寫步驟。每一步都要達到「完成」條件才進下一步。

## 1. 判斷來源

- **整理工具的資料夾**（有 `notes.md`，通常也有 `README.md`）：走步驟 2A。
- **只有網址或貼上的文字**：走步驟 2B。

**完成**：確定走 2A 或 2B，並且已經讀完來源內容（2A 讀 `notes.md`，2B 讀網址內容或貼文）。

## 2A. 用 script 匯入

1. 決定 slug、title、topics（規則見 AGENTS.md），並確認 `content/notes/<slug>.md` 還不存在。
2. 執行：
   ```
   uv run scripts/import_note.py "<資料夾>" --slug <slug> --title "<標題>" --topics <a,b>
   ```
3. 打開產生的檔案，檢查 `summary` 是否只有一句；內文如果有簡體字，改成繁體中文。

**完成**：script 結束碼為 0，而且已經讀過產生的檔案。

## 2B. 手寫筆記

1. 新建 `content/notes/<slug>.md`，照 AGENTS.md 填 frontmatter。
2. 依序寫四個 H2：`完整摘要`（用 H3 分段）、`重點知識與概念拆解`（表格）、`中英金句與解釋`（表格，中文來源可省略）、`可參考資料`。
3. 內容只寫自己的整理，不貼原文全文。

**完成**：四個區塊都有實質內容，或已省略不適用的區塊；frontmatter 必填欄位都填好。

## 3. 驗證

```
uv run scripts/build.py
```

**完成**：結束碼為 0，且沒有 `ERROR` 或 `WARN`。出現錯誤時修正筆記檔，不要改 `build.py` 的驗證規則。

## 4. 預覽

執行 `uv run python -m http.server 8000 -d dist`，確認以下三點：

- 首頁最上方的「最新收錄」或列表裡有這篇；
- 用標題中的一個詞搜尋，能搜到這篇；
- 筆記頁的目錄、表格和「閱讀原文」連結都正常。

**完成**：三項都確認過。

## 5. 回報

告訴使用者新增的檔案路徑、選用的 topics 和理由。如果新增了 topic，也要說明。提交 commit 前先問使用者，commit message 用 `feat(notes): add <slug>`。
