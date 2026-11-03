---
title: Diagram Design：讓 coding agent 畫架構圖的 skill
type: article
source_url: https://github.com/cathrynlavery/diagram-design
source_site: GitHub
added: '2026-09-13'
topics:
- coding-agents
- tools
summary: 透過讀取使用者網站的配色與字型，Diagram Design 能在 60 秒內產出符合品牌風格且免除 Figma 手工調整的專業圖表。
abstract: Diagram Design 是一個適用於 Claude Code、Codex 與 Pi 的 Agent Skill，能自動從網站抓取品牌色彩與字型，產出 27 種編輯品質的圖表，解決設計師在繪圖時需要手動調色與排版的問題。
---

## 完整摘要

### 產品動機與設計哲學
作者 Cathryn Lavery 在寫部落格與經營 BestSelf.co 時，每次需要圖表時只能得到 Claude 產出的通用圓角方塊樣式，要麼花 30 分鐘在 Figma 調整，要麼直接省略圖表。因此她開發了此 Skill，目標是讓圖表自動匹配網站的品牌語言，並強調「最高品質的動作通常是刪除」，每個節點必須有其存在價值，目標密度為 4/10。

### 核心功能與圖表種類
該 Skill 包含 27 種圖表類型（架構圖、流程圖、時序圖、狀態機、ER 模型、時間線、泳道圖、象限圖、嵌套圖、樹狀圖、組織圖、維恩圖、圖層堆疊、金字塔/漏斗、顧問 2×2、雷達圖、迴路圖、IT 現狀圖、高階圖、長條圖、折線圖、甘特圖、散布圖、流程圖、醇泥圖、資料流圖、DP 整合、DP 安全矩陣等），每種圖表提供 minimal light、minimal dark 與 full-editorial 三種變體，可直接在瀏覽器開啟無需建置步驟。

### 使用方式與品牌對接流程
使用者只需透過對應的 Agent（Pi、Claude Code、Codec）安裝該 Skill，然後執行 onboarding 指令（例如 `onboard diagram-design to https://yoursite.com`），Skill 會抓取網站的主頁、提取主要色板與字型堆疊，將其映射至語意角色（paper、ink、muted、accent、title、node-name、sublabel），並自行進行 WCAG AA 對比檢查。完成後，所有新產出的圖表會自動使用該網站的品牌樣式，亦可手動編

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 品牌對照自動化 | Skill 會從目標網站的 <body> 背景抓取 paper 色彩，從主要文字顏色抓取 ink，從次要文字抓取 muted，從最常用的品牌色（CTA、連結、標題）抓取 accent，並分別將 <h1>、<body>、<code>/<pre> 的字型對應為 title、node-name、sublabel。這使得產出的圖表在視覺上與網站保持一致，無需設計師手動調色。 | 文件中說明：`<body>` background → `paper` token，Primary text color → `ink` token，Secondary / caption text → `muted` token，Most-used brand color → `accent` token，`<h1>` font family → `title` font，`<body>` font family → `node-name` font，`<code>` / `<pre>` font → `sublabel` font。 |
| 編輯品質設計準則 | 設計系統限定每張圖只使用一種強調色（accent），且每圖僅保留 1–2 個焦點元素，所有寬高、間距必須是 4 的倍數，邊框為 1px 髮線，圓角上限 10px，且不使用陰影。這些規則避免圖表看起來像是 AI 生成的通用圖形，同時確保視覺層次分明。 | 在「The design system (in one paragraph)」段落中提到：One accent color, 1–2 focal elements per diagram. 1px hairline borders, no shadows, max border-radius 10px. Every coord, width, and gap divisible by 4. |
| 多種輸出與匯入能力 | 使用者可以將現有的 draw.io 或 Mermaid 圖檔案透過 Skill 匯入，系統會依照指定的格式（HTML/SVG/PNG）、大小（如 slide-16x9）、細節等級（faithful/balanced/simplified）以及對象（engineer/mixed/executive）重新繪製，並提供 fidelity ledger 說明哪些節點被合併、刪除或保留。 | 章節「Import from draw.io or Mermaid」列出指令範例與說明，並提到「The four dials」：Format、Size、Detail、Audience，以及「Every import ends with a fidelity ledger」。 |
| 即時預覽與零建置 | 所有 27 種圖表都內嵌為自含 HTML，直接在瀏覽器開啟即可查看，無需任何建置步驟、外部圖像或 JavaScript 依賴。這使得設計師可以即時截圖或匯出為 SVG/PNG，適合快速迭代與文件嵌入。 | 在「What it makes」段落：All 27 diagrams ship in three variants: minimal light, minimal dark, and full-editorial. Open any of them directly in a browser — no build step, no JS, no external images. |
| 可變的樣式與手動覆寫 | 若使用者偏好手動調整，可以直接編輯 `skills/diagram-design/references/style-guide.md` 檔案，裡面的 token 表會被所有圖表、匯入流程與圖庫共用，使得樣式調整即時生效且不會被套件更新覆寫（除非重新 clone）。 | Manual override 小節說明：Open `skills/diagram-design/references/style-guide.md` and edit the table. Everything downstream reads from there — all 27 diagrams, the annotation primitive, and the gallery all inherit semantic role names. |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| The highest-quality move is usually deletion. | 最高品質的動作通常是刪除。 | 作者在解釋設計哲學時所言，強調每個節點必須證明其存在價值。 |
| Every node earns its place. | 每個節點都必須赢得其位置。 | 同上，用以闡述圖表設計中「節點必有其存在意義」的原則。 |

## 可參考資料
- **littlemight.com**：作者的個人部落格與新聞信箱，文中多次提及作為靈感來源與範例網站。 — <https://littlemight.com?utm_source=diagram-design&utm_medium=readme&utm_campaign=github&utm_content=intro>
- **BestSelf.co**：作者兼任的副業公司，文中提到其在開發 Diagram Design 時同樣運營。 — <https://bestself.co?utm_source=diagram-design&utm_medium=readme&utm_campaign=github&utm_content=intro>
- **GitHub repository**：項目原始碼所在，包含所有說明文件、範例與腳本。 — <https://github.com/cathrynlavery/diagram-design>
- **X (formerly Twitter) - Cathryn Lavery**：作者的社群平台，文末邀請讀者前往互動。 — <https://x.com/cathrynlavery>
- **Tabler Icons**：提供 55 個單色 IT/cloud 圖示，用於 Diagram Design 的圖示集。 — <https://tabler.io/icons>
- **Simple Icons**：提供品牌 silhouettes 圖示，同样用於圖示集，採 CC0 授權。 — <https://simpleicons.org>
