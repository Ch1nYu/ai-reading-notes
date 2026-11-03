---
title: OMPChamber：Oh My Pi 的桌面工作台
type: article
source_url: https://github.com/realchendahuang/OMPChamber
source_site: GitHub
added: '2026-08-12'
topics:
- coding-agents
- tools
summary: OMPChamber 是整合 OMP 代理核心與 OpenChamber 介面的跨平台桌面工作空間，讓開發者能在桌面、Web、VS Code、行動裝置與 CLI 間無縫運行、監督、審查與協作 AI 代理任務。
abstract: OMPChamber 是一個基於 OpenChamber UI/UX 基礎建構的桌面客戶端，專為 OMP (Oh My Pi) 代理運行時設計，提供統一工作空間來運行、監督、審查代理工作，支援跨裝置同步、多模型並行、變更導覽、即時預覽與 GitHub 整合，解決開發者在多平台間管理 AI 代理工作流的碎片化問題。
---

## 完整摘要

### 專案背景與定位
OMPChamber 衍生自 OpenChamber 專案，核心差異在於將原本的 OpenCode 代理核心替換為 OMP (Oh My Pi) 提供的代理內核（Models、Tools、Sessions、Skills、MCP、Subagents）。OpenChamber 負責產品體驗層（UI/UX），OMP 負責代理能力層，兩者分工明確。專案強調「Run agent work. Keep control. Ship from anywhere.」——在保持控制權的前提下，從任何裝置啟動代理工作並推向發布。

### 核心功能架構
功能分為三大面向：(1) 執行與控制：Session Goals 讓代理朝目標自主推進直到完成/受阻/達上限；Multi-run 可對同一任務啟動最多五個模型會話（可選獨立 worktree），再以 Fusion 合併優秀片段；(2) 審查與理解：Changes Walkthrough 將大型 diff 轉為 AI 導覽式逐步講解；Preview 內建瀏覽器讓代理可即時檢視網頁元素、截圖、樣式、錯誤；(3) 流程整合：GitHub issue/PR 上下文直連、跨裝置會話同步（Desktop/Web/VS Code/iOS/Android/CLI）、Private Relay 零開放端口端到端加密遠端存取、排程任務支援 cron 與 Session Goals。

### 部署形態與快速上手
提供五大介面：Desktop (macOS/Windows/Linux AppImage，內建 OpenCode CLI 無需額外安裝)、VS Code Extension (Marketplace 直接安裝)、Web/PWA (Node.js 22+，一鍵安裝腳本)、iOS/Android 原生 App、CLI/Server (無頭模式排程與遠端管理)。Linux 需 FUSE (libfuse.so.2) 或加環境變數 APPIMAGE_EXTRACT_AND_RUN=1 執行。CLI 指令涵蓋 status、connect-url --qr、tunnel start (Cloudflare/Ngrok)、startup enable、logs、stop、update，預設綁定 localhost，--lan 僅限受信網路並建議搭配 --ui-password。

### 技術棧與依賴致謝
核心依賴 OpenCode 提供代理式編碼能力；Pierre 提供高效能 diff 檢視與語法高亮；Ghostty-web 提供 Ghostty 終端機網頁渲染；Yulia Ivashko 貢獻推送成功的煙火慶祝動畫。專案採 MIT 授權，獨立於 OpenCode 團隊，文件齊全（Quick start、Installation、Connect devices、Private Relay、Multi-run、Session Goals、Changes Walkthrough、Preview、GitHub workflows、Mobile、Security、Troubleshooting、Reverse proxy、Custom themes）。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 雙核心架構分工 | OpenChamber 負責 UI/UX 產品體驗，OMP 負責代理內核能力（Models、Tools、Sessions、Skills、MCP、Subagents），兩者職責分離，降低耦合。 | README 開頭說明：'OpenChamber owns the product experience; OMP owns the agent capability.' 以及 'This repository is derived from OpenChamber, with the agent kernel ... provided by OMP instead of OpenCode.' |
| Session Goals 自主推進機制 | 為會話設定完成條件，代理每輪執行後自動檢查是否達成，未達成則持續工作，即使關閉 App 也不中斷，適合長時間任務。 | 「Goals that continue on their own」段落：'OMPChamber checks the result after every turn and keeps the agent working until the goal is complete, blocked, or reaches the limit you set — even after you close the app.' |
| Multi-run 與 Fusion 多模型並行評估 | 同一任務最多啟動五個模型會話（可各自獨立 worktree），開發者可比較產出並用 Fusion 合併優點，降低單一模型失誤風險。 | 「Compare and combine runs」段落：'Use Multi-run to give the same task to up to five models, each in its own session and optionally its own worktree... use Fusion to combine the strongest parts into a new session.' |
| Changes Walkthrough AI 導覽式變更審查 | 將大型 diff 拆解為邏輯步驟，按變更合理性排序並解釋關聯，幫助快速理解複雜修改全貌。 | 「Guided changes walkthroughs」段落：'Changes Walkthrough turns a large diff into an AI-guided tour of the change. It groups related edits into steps, puts them in the order the change makes sense, and explains how the pieces fit together.' |
| Private Relay 零配置端到端加密遠端存取 | 掃描一次性 QR Code 即可配對裝置，無需開放埠口、無公網伺服器，連線可隨時撤銷，另支援 LAN/VPN、Cloudflare/Ngrok、SSH 多種通道。 | 「Private remote access」段落：'Pair a device with a one-time QR code and connect through Private Relay without opening ports or exposing a public server. The connection is end-to-end encrypted and can be revoked at any time.' |
| 跨平台會話無縫續接 | Desktop、Web/PWA、VS Code、iOS、Android、CLI/Server 共享專案與會話狀態，可隨時切換裝置查看進度、回覆問題、審查變更、重接終端機。 | 「Continue on another device」段落：'Open the same projects and sessions from Desktop, Web/PWA, VS Code, iOS, or Android. Check progress, answer questions, review changes, and reattach to a running terminal.' 以及「Use it where you work」表格列出五大介面。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| OMPChamber is a desktop workspace for running, supervising, and reviewing OMP agent work, powered by the OpenChamber UI. | OMPChamber 是一個桌面工作空間，用於運行、監督和審查 OMP 代理工作，由 OpenChamber UI 提供動力。 | README 核心定位段落，說明專案定位與 UI 來源。 |
| Run agent work. Keep control. Ship from anywhere. | 運行代理工作。保持控制權。從任何地方發布。 | 專案標語，凝縮核心價值主張。 |
| This repository is derived from OpenChamber, with the agent kernel (Models, Tools, Sessions, Skills, MCP, Subagents) provided by OMP instead of OpenCode. | 本倉庫衍生自 OpenChamber，代理內核（模型、工具、會話、技能、MCP、子代理）由 OMP 提供，而非 OpenCode。 | 開頭架構說明，闡述與上游專案的關係與核心差異。 |
| OMPChamber uses OpenCode to power its coding agents. We chose it because we believe it provides the best open-source agentic coding experience today: capable, extensible, and open by design. | OMPChamber 使用 OpenCode 為其編碼代理提供動力。我們選擇它是因為相信它提供了當今最好的開源代理式編碼體驗：能力強、可擴展、且設計上開放。 | 「Why OpenCode?」段落，說明選擇 OpenCode 的理由。 |

## 可參考資料
- **OMP (Oh My Pi) Agent Runtime**：提供代理內核能力的上游專案 — <https://omp.sh/>
- **OpenChamber**：UI/UX 基礎專案，本專案衍生來源 — <https://github.com/openchamber/openchamber>
- **OpenCode**：代理式編碼引擎提供者 — <https://opencode.ai/>
- **Pierre (diff viewer & syntax highlighting)**：高效能 diff 檢視與語法高亮庫 — <https://pierrejs-docs.vercel.app/>
- **Ghostty-web**：Ghostty 終端機網頁渲染器 — <https://github.com/coder/ghostty-web>
- **THIRD_PARTY_NOTICES.md**：第三方授權聲明文件 — <https://github.com/realchendahuang/OMPChamber/blob/main/THIRD_PARTY_NOTICES.md>
- **CONTRIBUTING.md**：開發環境設置與貢獻指南 — <https://github.com/realchendahuang/OMPChamber/blob/main/CONTRIBUTING.md>
- **Documentation Guides**：涵蓋 Quick start、Installation、Connect devices、Private Relay、Multi-run、Session Goals、Changes Walkthrough、Preview、GitHub workflows、Mobile、Security、Troubleshooting 等完整指南 — <https://github.com/realchendahuang/OMPChamber/tree/main/packages/docs/content/docs>
- **Reverse Proxy Guide**：自架部署反向代理設定指南 — <https://github.com/realchendahuang/OMPChamber/blob/main/docs/REVERSE_PROXY.md>
- **Custom Themes Guide**：自定義主題撰寫指南 — <https://github.com/realchendahuang/OMPChamber/blob/main/docs/CUSTOM_THEMES.md>
- **GitHub Releases (Desktop 下載)**：Desktop 版本發布頁面 — <https://github.com/realchendahuang/OMPChamber/releases/latest>
- **VS Code Marketplace**：VS Code 擴充套件安裝頁面 — <https://marketplace.visualstudio.com/items?itemName=fedaykindev.ompchamber>
- **Install Script**：CLI/Web/PWA 一鍵安裝腳本 — <https://raw.githubusercontent.com/realchendahuang/OMPChamber/main/scripts/install.sh>
