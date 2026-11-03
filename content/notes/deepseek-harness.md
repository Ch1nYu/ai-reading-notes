---
title: DeepSeek Harness：一切皆 agent 的開源框架
type: article
source_url: https://github.com/deepseek-ai/deepseek-harness
source_site: GitHub
added: '2026-08-16'
topics:
- agents
- tools
summary: DeepSeek Harness 是一個基於 Cordis 的插件化 AI Agent 框架，透過「一切皆插件」的架構實現高度可組合與擴展的智能體開發體驗。
abstract: DeepSeek Harness (dsh) 是 DeepSeek AI 開發的開源智能體框架，採用「一切皆插件」的架構設計，基於 Cordis 框架構建，提供高度可組合與擴展的 AI Agent 開發平台。目前處於開發者預覽階段，迭代快速且存在破壞性變更。
---

## 完整摘要

### 專案背景與定位
DeepSeek Harness 由 DeepSeek AI 開發，定位為開源的智能體開發框架。其核心設計理念是「一切皆插件」，意味著框架的所有功能（包括核心功能）都以插件形式存在，透過 Cordis 框架實現時空可組合性。專案目前擁有 120.9k GitHub stars、11.9k forks，顯示社群高度關注。專案處於開發者預覽階段，官方明確警告將有破壞相容性的變更。

### 架構設計與技術棧
框架建構於 Cordis 之上，Cordis 是一個專為時空可組合性設計的編程範式框架。專案採用 Monorepo 架構（pnpm workspace），包含多個關鍵目錄：packages（核心套件）、apps（應用入口）、native（原生模組）、python（Python 綁定）、examples（範例）、docs（文件）、website（官網）。技術棧包含 TypeScript、Node.js、Vitest 測試框架，並支援 Web UI 介面（預設端口 3080）。

### 使用方式與開發流程
提供兩種執行方式：1) 直接使用 npx @deepseek-ai/dsh web 快速啟動 Web UI；2) 從源碼構建（git clone → pnpm install → pnpm run build → pnpm dsh web）。開發者可參考 AGENTS.md 進行 Agent 開發，遵循 CONTRIBUTING.md 貢獻代碼。專案提供完整的開發指南、架構文檔與使用者指南，並設有 Discord 社群與 GitHub Discussions 管道。

### 生態系統與擴展性
透過 dsh-plugin 主題標籤鼓勵社群開發插件，形成插件生態。專案結構顯示支援多語言（Python、原生模組）、多平台應用。第三方依賴授權聲明於 THIRD_PARTY_NOTICES.md。MIT 授權允許商業使用與修改。專案包含基準測試文檔（BENCHMARK.md），顯示重視效能評估。

### 現階段限制與風險
處於開發者預覽階段，API 不穩定且會有破壞性變更，不適合生產環境直接使用。文檔雖完整但可能隨版本快速過時。Monorepo 結構龐大（12,293 commits），新貢獻者學習曲線陡峭。缺乏詳細的遷移指南與版本相容性說明。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 一切皆插件架構 | 框架核心功能皆以插件形式實現，無硬編碼的核心邏輯，透過 Cordis 的服務註冊與依賴注入機制實現極致的模組化與可組合性。 | README 中標題 'Everything is a Plugin' 及說明 'It uses an architecture where everything is a plugin, and is powered by Cordis' |
| Cordis 框架基礎 | Cordis 提供時空可組合性編程範式，支援插件的動態載入、卸載、熱更新與跨進程通訊，是 Harness 架構的核心支撐。 | README 連結至 Cordis 專案與論文 'A Programming Paradigm for Spatiotemporal Composability' |
| Monorepo 多套件管理 | 使用 pnpm workspace 管理 packages、apps、native、python 等多個子專案，統一建置、測試與版本控管。 | 目錄結構顯示 packages、apps、native、python 等目錄，根目錄有 pnpm-workspace.yaml、pnpm-lock.yaml |
| Web UI 開箱即用 | 提供開箱即用的 Web 介面，預設於 http://127.0.0.1:3080 運行，降低開發者體驗門檻。 | README 'Run from npm' 章節：'npx @deepseek-ai/dsh web' 啟動 Web UI，預設端口 3080 |
| 開發者預覽與破壞性變更 | 專案明確標示為開發者預覽，API 不穩定，將持續有破壞相容性的變更，需謹慎評估採用時機。 | README 'Developer preview' 章節：'THERE WILL BE COMPATIBILITY-BREAKING CHANGES.' |
| 社群驅動的插件生態 | 鼓勵開發者建立 dsh-plugin 標籤的插件倉庫，透過 GitHub Discussions 與 Discord 建立社群回饋循環。 | README 'Community and support' 章節：'Add the dsh-plugin topic to your plugin repository' 與 Discord 連結 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Everything is a Plugin. | 一切皆插件。 | 專案標語，出現在 README 標題與 About 區塊，代表核心設計哲學 |
| DeepSeek Harness is currently in developer preview and is iterating rapidly. THERE WILL BE COMPATIBILITY-BREAKING CHANGES. | DeepSeek Harness 目前處於開發者預覽階段並快速迭代。將會有破壞相容性的變更。 | README 'Developer preview' 章節，重要警告訊息 |
| It uses an architecture where everything is a plugin, and is powered by Cordis, whose design is described in 'A Programming Paradigm for Spatiotemporal Composability'. | 它採用一切皆插件的架構，並由 Cordis 提供支援，其設計理念詳見《時空可組合性的編程範式》論文。 | README 開頭架構說明，連結核心技術依賴與理論基礎 |

## 可參考資料
- **DeepSeek Harness GitHub Repository**：專案原始碼、Issue、Discussions、Release 主要來源 — <https://github.com/deepseek-ai/deepseek-harness>
- **Cordis Framework**：Harness 核心依賴框架，提供插件系統與時空可組合性實現 — <https://github.com/cordiverse/cordis>
- **Cordis Design Paper**：Cordis 架構理論基礎論文《A Programming Paradigm for Spatiotemporal Composability》 — <https://github.com/cordiverse/paper>
- **DeepSeek Harness Discord**：官方社群即時討論與支援管道 — <https://discord.gg/Ycq5dCaS4>
- **Web UI Guide**：Web 介面使用指南文檔 — <https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/index.md>
- **Development Guide**：開發者貢獻與二次開發指南 — <https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/development.md>
- **Architecture Documentation**：系統架構詳細設計文檔 — <https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md>
- **AGENTS.md**：Agent 開發規範與指引 — <https://github.com/deepseek-ai/deepseek-harness/blob/master/AGENTS.md>
