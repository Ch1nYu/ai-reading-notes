---
title: OpenAI Codex 的 skills 目錄
type: article
source_url: https://github.com/openai/skills
source_site: GitHub
added: '2026-09-09'
topics:
- coding-agents
summary: openai/skills 收錄可重複使用的技能資料夾，透過 $skill-installer 安裝並說明未來應改用 Plugins 框架。
abstract: 此 repo 為 OpenAI Codex 的技能目錄，說明何謂 Agent Skills、如何安裝與使用，並標示該專案已棄用、改向 OpenAI Plugins 發展。
---

## 完整摘要

### Agent Skills 概念與結構
Agent Skills 是由指令、腳本與資源組成的資料夾，AI 代理可發現並重複使用以完成特定任務，達到一次撰寫、處處可用的目標。這些技能分別放在 skills/.system（自動安裝）、skills/.curated 與 skills/.experimental 三個子目錄中。

### 技能安裝與使用流程
位於 .system 的技能會在 Codex 最新版時自動安裝；若要安裝 curated 或 experimental 技能，可在 Codex 內使用 $skill-installer 指令，例如 `$skill-installer gh-address-comments` 或提供完整的 GitHub 路徑。安裝後（根據舊說法）需要重新啟動 Codex 才能載入新技能。

### 存儲庫狀態與後續方向
repo 的重要說明標示此專案已棄用，建議使用者改向 OpenAI Plugins repository 取得最新的 Codex skill 範例，並參考 Build plugins guide 建立專屬技能。同時也提供 Agent Skills open standard（agentskills.io）作為跨框架技能互通的參考。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| Agent Skills 的定義 | 指令、腳本與資源的集合，使 AI 代理能在不同專案中重複使用同一套邏輯來完成特定任務。 | Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform at specific tasks. Write once, use everywhere. |
| .system 資料夾的自動安裝機制 | 放在此資料夾中的技能在 Codex 啟動時會被自動偵測並安裝，無需額外指令。 | Skills in [`.system`](https://github.com/openai/skills/blob/main/skills/.system) are automatically installed in the latest version of Codex. |
| 透過 $skill-installer 安裝 curated 與 experimental 技能 | 使用者可在 Codex 內呼叫 $skill-installer，給定技能名稱（預設查詢 .curated）或完整資料夾 URL，來手動加入非自動安裝的技能。 | Curated skills can be installed by name (defaults to `skills/.curated`):```$skill-installer gh-address-comments```For experimental skills, specify the skill folder... |
| 專案已棄用，改向 OpenAI Plugins 發展 | 維護者明確告訴使用者此 repo 不再更新，未來的 Codex skill 範例與開發指引應該移至 OpenAI Plugins repository 並遵循 Build plugins guide。 | **This repository is deprecated.** For current Codex skill and plugin examples, use the [OpenAI Plugins repository](https://github.com/openai/plugins). If you want to add your own skills to Codex, follow the [Build plugins](https://developers.openai.com/codex/plugins/build) guide... |
| Agent Skills open standard 提供跨框架互通性 | 透過 agentskills.io 所定義的開放規格，不同 AI agent 框架皆可共用同一套技能描述，提高可重用性與生態系相容性。 | Learn more: * [Agent Skills open standard](https://agentskills.io/) |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform at specific tasks. Write once, use everywhere. | Agent Skills 是指令、腳本與資源的資料夾，AI 代理可發現並使用來執行特定任務。一次撰寫，處處可用。 | 出現在 「Agent Skills」 小節，用以定義什麼是 Agent Skills。 |
| Skills in [`.system`](https://github.com/openai/skills/blob/main/skills/.system) are automatically installed in the latest version of Codex. | 位於 `.system` 資料夾中的技能會在最新版的 Codex 中自動安裝。 | 在 「Installing a skill」 小節說明哪些技能會自動載入。 |
| After installing a skill, restart Codex to pick up new skills. | 安裝技能後，請重新啟動 Codex 以載入新技能。 | 同一小節提到安裝完畢後需重新啟動以使新技能生效（後續說明此步驟已過時）。 |

## 可參考資料
- **GitHub Copilot**：AI 程式碼輔助工具，在導覽選單中被列為 AI CODE CREATION 下的功能。 — <https://github.com/features/copilot>
- **MCP Registry**：用於將外部工具整合到 Codex 的註冊表，出現在導覽選單。 — <https://github.com/mcp>
- **GitHub Actions**：工作流程自動化平台，在導覽選單的 DEVELOPER WORKFLOWS 下列出。 — <https://github.com/features/actions>
- **GitHub Codespaces**：即時開發環境服務，同樣在 DEVELOPER WORKFLOWS 下。 — <https://github.com/features/codespaces>
- **GitHub Advanced Security**：提供弱點偵測與修復的安全功能，出現在導覽選單的 APPLICATION SECURITY 下。 — <https://github.com/security/advanced-security>
- **OpenAI Plugins repository**：專案已棄用後建議使用者前往此 repo 取得最新的 Codex skill 範例。 — <https://github.com/openai/plugins>
- **Build plugins guide**：說明如何為 Codex 建立 skill‑only 插件，是棄用公告中提供的後續學習資源。 — <https://developers.openai.com/codex/plugins/build>
- **Agent Skills open standard**：提供跨框架技能規格的開放網站，讓不同 agent 皆可共用同一套技能。 — <https://agentskills.io/>
- **GitHub Marketplace**：探索與取得 GitHub 整合工具與動作的平台，出現在導覽選單的 EXPLORE 下。 — <https://github.com/marketplace>
