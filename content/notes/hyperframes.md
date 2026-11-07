---
title: HyperFrames：用 HTML 與 CSS 製作影片
type: article
source_url: https://github.com/heygen-com/hyperframes
source_site: GitHub
added: '2026-09-09'
topics:
- tools
summary: HyperFrames 透過 HTML 框架與插件技能，使開發者能以程式化方式撰寫影片內容並獲得完全可重現的 MP4 輸出。
abstract: HyperFrames 是一個開源框架，讓開發者使用 HTML、CSS、媒體與可尋找的動畫生成確定性的 MP4 影片，特別適合 AI 編碼代理人與本地 CLI 工作流。它解決了將網頁樣式直接轉成影片的重複建構問題，提供可重現、免建置的製作過程，適用於 CI、測試與自動化內容管道。
---

## 完整摘要

### 核心概念與架構
HyperFrames 將影片定義為普通 HTML 檔案，使用 data-* 屬性標記時間、軌道與剪輯（clip）。透過插件化的運作時序適配器（GSAP、CSS、Lottie、Three.js、Anime.js、WAAPI 或自訂執行環境），在無頭 Chrome 中逐幀擷取畫面，最後由 FFmpeg 編碼為 MP4。因為整個流程只依賴輸入的 HTML 與資產，相同的輸入永遠產出相同的影片，適合做為 CI 回歸測試或自動化內容產生的基礎。

### 技能系統與工作流程
專為 AI 編碼代理人設計的「skills」機制提供 20 個預設工作流（如 product‑launch‑video、faceless‑explainer、pr‑to‑video 等）以及更細部的 domain skill（核心合約、動畫、關鍵框架、創意、媒體使用、CLI、音訊等）。代理人透過 npx skills add heygen‑com/hyperframes 安裝技能組，之後僅需描述需求（例如「產出 10 秒產品介紹，含淡入標題、背景影片與輕柔背景音樂」），技能會引導代理人完成規劃、撰寫有效的 HTML、串接可尋找的動畫、加入媒體資產、執行 lint 檢查、預覽到最終渲染的完整製作流程。

### 使用方式與生態系統
開發者亦可直接使用 CLI：先執行 npx hyperframes init my-video 建立專案，進入目錄後使用 npx hyperframes preview 即時預覽（帶熱重載），最後以 npx hyperframes render 產出 MP4。框架附帶 Catalog（如 flash‑through‑white、instagram‑follow、data‑chart）可直接加入為區塊或元件，同時提供 Studio 瀏覽器編輯器、AWS Lambda 渲染以及 Playground 線上試玩。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 確定性渲染（Deterministic） | 因為影片完全由靜態 HTML、CSS、媒體檔案與可尋找的動畫產生，沒有隨機或外部狀態，同一組輸入在任何機器上都會產出逐幀相同的 MP4。這使得 HyperFrames 能在 CI 環境中作為回歸測試的基準，也適合需要重現性的自動化影片產生。 | 文件中明確提到「same input, same frames, same output」並說明渲染器在無頭 Chrome 中逐幀擷取並由 FFmpeg 編碼。 |
| 技能（Skill）驅動的 AI 代理人協作 | HyperFrames 提供一套可隨需求安裝的技能（skills），代理人只需透過自然語言描述所需影片，技能會自動引導代理人完成從規劃、撰寫 HTML、加入媒體、預覽到最終渲染的全流程，無需代理人具備前端或影片製作專業知識。 | 在「With an AI coding agent」段落說明「The skills teach agents the HyperFrames production loop: plan the video, write valid HTML, wire seekable animations, add media, lint, preview, and render.」並列出支援的代理人如 Claude Code、Cursor、Gemini CLI、Codex 等。 |
| 免建置、直接預覽 | 組成影片的僅是標準 HTML 檔案，透過瀏覽器即可即時預覽，無需 Webpack、Babel 或其他建置步驟。這降低了門檻，使得設計師與開發者能在熟悉的網頁開發工作流中直接看到影片效果。 | 在「HyperFrames vs Remotion」比較表格中，「Build step」欄位標明 HyperFrames 為「None; index.html plays as-is」，以及「No build step: an index.html composition plays as-is and can be previewed directly in the browser。」 |
| 豐富的動畫適配器 | HyperFrames 不綁定單一動畫庫，開發者可選擇 GSAP、CSS 動畫、Lottie、Three.js、Anime.js、WAAPI，甚至自訂的 frame 適配器，所有適配器皆需實作可尋找（seekable）介面以確保每一幀的狀態可被重現。 | 在「How It Works」段落列出「Use GSAP, CSS, Lottie, Three.js, Anime.js, WAAPI, or your own frame adapter for seekable animation.」以及「Domain skills」中的 `/hyperframes-animation` 說明涵蓋「All animation knowledge — atomic motion rules, scene blueprints, transitions, runtime adapters (GSAP / Lottie / Three.js / Anime.js / CSS / WAAPI / TypeGPU）。 |
| 媒體統一管理（Media OS） | 透過 `/media-use` domain skill，HyperFrames 能解析各類媒體需求（背景音樂、聲效、圖像、圖示、Logo、聲音、色階、LUT 等），在需要時透過 TTS/音樂/圖像模型產生資產，並建立本地檔案與帳本記錄，確保同一個專案內的媒體使用可追蹤與重複使用。 | 在「Domain skills (loaded on demand)」表格中，`/media-use` 的描述為「The media OS — resolve any media need … generate via TTS/music/image models when the catalog misses, transcribe, caption, remove backgrounds, and reuse assets across projects. One shared audio engine + manifest tracking.」 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| HyperFrames is an open-source framework for turning HTML, CSS, media, and seekable animations into deterministic MP4 videos. | HyperFrames 是一個開源框架，用於將 HTML、CSS、媒體與可尋找的動畫轉為確定性的 MP4 影片。 | 出現在專案 README 的開頭敘述，說明 HyperFrames 的核心功能與定位。 |
| Use it locally with the CLI, from AI coding agents with skills, or as the rendering core behind hosted authoring workflows. | 可以在本地透過 CLI 使用，也可由具備技能的 AI 編碼代理人呼叫，或作為託管作者工具流程背後的渲染核心。 | 同樣出現在 README 引言部分，說明 HyperFrames 的使用方式與目標對象。 |
| The skills teach agents the HyperFrames production loop: plan the video, write valid HTML, wire seekable animations, add media, lint, preview, and render. | 這些技能會教導代理人完成 HyperFrames 的製作流程：規劃影片、撰寫有效的 HTML、連線可尋找的動畫、加入媒體、進行 lint、預覽以及最終渲染。 | 在「With an AI coding agent」章節中，說明技能對代理人的引導內容。 |

## 可參考資料
- **HyperFrames**：專案原始碼與文件的主要來源。 — <https://github.com/heygen-com/hyperframes>
- **Quickstart guide**：提供快速上手步驟的官方文件。 — <https://hyperframes.heygen.com/quickstart>
- **Showcase**：展示使用 HyperFrames 製作的影片範例。 — <https://hyperframes.heygen.com/showcase>
- **Playground**：線上編輯與預覽工具，可直接在瀏覽器體驗 HyperFrames。 — <https://www.hyperframes.dev/>
- **Catalog**：提供可復用的區塊與元件（如圖表、特效）的庫。 — <https://hyperframes.heygen.com/catalog/blocks/data-chart>
- **Discord community**：用於提問、討論與取得即時支援的社群平台。 — <https://discord.gg/EbK98HBPdk>
- **Node.js requirement**：說明 HyperFrames 需要 Node.js 22+ 才能運行。 — <https://nodejs.org/>
- **Apache 2.0 License**：專案授權條款。 — <https://github.com/heygen-com/hyperframes/blob/main/LICENSE>
