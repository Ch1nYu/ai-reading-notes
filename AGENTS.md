# AI 閱讀筆記 · AGENTS.md

這是一個靜態網站：把讀過、看過的 AI 與技術文章和影片整理成**結構一致的中文筆記**，讓讀者能搜尋、依主題篩選，並舒適地閱讀長文。每篇筆記是 `content/notes/` 裡的一個 Markdown 檔，`scripts/build.py` 會把它們轉成 `dist/` 裡的網站，再由 GitHub Pages 發布。

網站網址：<https://ch1nyu.github.io/ai-reading-notes/>

## 指令

所有 Python script 都用 `uv run` 執行，依賴寫在各 script 開頭的 PEP 723 區塊，不需要另外安裝。

| 目的 | 指令 |
|---|---|
| 驗證所有筆記，不輸出檔案 | `uv run scripts/build.py --check` |
| 建置網站到 `dist/` | `uv run scripts/build.py` |
| 本機預覽 | `uv run python -m http.server 8000 -d dist`，然後開 <http://localhost:8000/> |
| 從整理工具的輸出匯入一篇 | `uv run scripts/import_note.py <來源資料夾> --slug <slug> --title <標題> --topics <a,b>` |

**完成標準**：`uv run scripts/build.py` 結束碼為 0，且沒有任何 `WARN` 輸出。改到版面時，另外在本機預覽中打開首頁和至少一篇筆記頁，確認桌機寬度和 375px 手機寬度都正常。

## 目錄結構

```
content/notes/<slug>.md   一篇筆記一個檔案（唯一的內容來源）
content/topics.yml        主題分類詞彙表（唯一的分類來源）
templates/                Jinja2 模板：base.html 為外框，index.html 為首頁，note.html 為筆記頁
static/css/site.css       全站樣式，設計 token 都在檔案開頭的 :root
static/js/site.js         搜尋、篩選、目錄高亮、閱讀進度條、深色模式
scripts/build.py          驗證並建置；輸出 dist/index.html、dist/notes/<slug>/index.html，並複製 static/
scripts/import_note.py    把整理工具產生的資料夾（notes.md + README.md）轉成 content/notes/<slug>.md
.claude/skills/add-note/  新增筆記的完整流程
dist/                     建置輸出，不進 git，不手動修改
```

## 筆記檔格式

### Frontmatter

```yaml
---
title: Building Effective AI Agents
type: article            # article | video
source_url: https://www.anthropic.com/engineering/building-effective-agents
source_site: anthropic.com
language: en             # 選填：en | zh
duration: 110m 12s       # 選填：影片才有
added: 2026-09-08        # 收錄日期 YYYY-MM-DD
topics: [agents]         # 1–3 個，必須是 content/topics.yml 的 key
summary: 一句話講完這篇在說什麼。
abstract: 選填，兩到四句的導讀，顯示在筆記頁開頭。
---
```

- **slug** 就是檔名（不含 `.md`），只能用小寫英數字和連字號，例如 `kv-cache-handbook`。以內容命名，不用日期或流水號。
- **title** 用讀者看得懂的標題：英文原文標題保留英文；簡體或口語化的社群貼文標題，改寫成繁體中文的描述性標題（例如把「holy sh*t this is an absolute gold mine」改成「用 DeepSeek V4 Flash 在 Codex 建立自我改進編碼循環」）。
- **summary** 只寫一句，上限 200 字，會顯示在首頁卡片和筆記頁標題下方。
- **topics** 先從 `topics.yml` 現有的 key 挑選。只有現有分類都明顯不合適，而且預期之後會有 3 篇以上同類筆記時，才新增分類；新增時要同時寫 `label` 和 `description`。

### 內文

內文由固定的四個 H2 區塊組成，順序也固定。缺少的區塊直接省略，不要自己發明新的 H2：

1. `## 完整摘要`：用 H3 分段，每段一個主題
2. `## 重點知識與概念拆解`：表格，欄位為「概念｜白話解釋｜來源證據」
3. `## 中英金句與解釋`：表格，欄位為「原文｜中譯｜脈絡／解釋」
4. `## 可參考資料`：清單，格式為 `- **名稱**：說明 — <網址>`

文章標題、來源和一句話總結由模板依 frontmatter 顯示，內文不要再寫 H1 或來源區塊。`build.py --check` 會檢查 H2 是否屬於上面四個。

### 寫作規範

- 一律使用繁體中文（台灣用語）；technical terms、產品名稱和程式碼保留原文。唯一的例外是「中英金句」表格的「原文」欄，要照原文保留，簡體也不轉換。
- 原文全文、字幕和逐字稿**不放進 repo**，只放自己整理的筆記，並透過 `source_url` 連到原始來源。

## 設計系統

整體方向是**編輯排版**：像一本安靜的雜誌，版面主角是文字。

- **色彩**：只用 `site.css` 開頭 `:root` 定義的 token（`--paper`、`--ink`、`--muted`、`--rule`、`--accent` 等），深色模式則在 `[data-theme="dark"]` 覆寫同一組 token。強調色只有一個（朱紅 `--accent`），用在連結、目前位置和少量標記。
- **字體**：標題用 `--font-serif`（Noto Serif TC），內文用 `--font-sans`（Noto Sans TC），程式碼用 `--font-mono`。
- **閱讀寬度**：內文欄寬上限為 `--measure`（約 40em），行高 1.85。
- **層次**：用字級、字重、細線和留白分層；卡片是有上框線的條目，不用陰影或圓角大卡片。
- **元件**：新增 UI 前，先在 `site.css` 找現有的 class 重用，例如 `.kicker`、`.topic-chip`、`.note-row`、`.table-wrap`；需要新元件時，寫在對應區段的註解標題下。
- **無障礙**：互動元素都要能用鍵盤操作並有可見的 focus 樣式；圖示按鈕要有 `aria-label`；色彩對比至少 WCAG AA。

## 新增或修改內容

- **新增筆記**：照 `.claude/skills/add-note/SKILL.md` 的步驟進行。不使用 Claude 的 agent 也可以直接讀這份檔案。
- **新增頁面類型**（例如「關於」或主題總覽）：在 `templates/` 新增模板並 `{% extends "base.html" %}`，在 `build.py` 加上輸出邏輯，並從首頁頁首導覽連過去。所有連結使用模板提供的 `root` 相對路徑，網站才能在 `/ai-reading-notes/` 子路徑下正常運作。
- **修改樣式**：先改 token，再改元件；改完依「完成標準」預覽首頁和筆記頁。
- **新增依賴**：只加在 script 的 PEP 723 區塊；前端維持零依賴，只用原生 HTML、CSS、JS。
