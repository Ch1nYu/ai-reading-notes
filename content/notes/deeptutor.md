---
title: DeepTutor：Agent-native 的個人化學習助理
type: article
source_url: https://docs.deeptutor.info/zh-cn/
source_site: docs.deeptutor.info
added: '2026-08-27'
topics:
- tools
- agents
summary: DeepTutor 是開源的 Agent 原生學習伴侶，整合聊天、RAG、多層記憶與書籍生成，並能將持久學習夥伴部署到即時通訊軟體中。
abstract: DeepTutor 是由香港大學數據智能實驗室開發的開源、Agent-native 個人化學習伴侶，提供共享運行時驅動聊天、深度能力、夥伴系統、書籍生成、協作寫作、RAG 與三層記憶，並可透過 Partners 將同一 Agent 循環接入微信、QQ 等 IM 渠道。
---

## 完整摘要

### 專案定位與核心架構
DeepTutor 定位為「開源、agent-native 的個性化學習伴侶」。其核心是一個共享運行時，負責驅動 Chat、深度 Capabilities、Partners、Book Generation、Co-Writer Editing、RAG（檢索增強生成）以及三層 Memory 系統。這意味著所有功能模組共用同一組 Agent 循環與狀態，而非獨立的微服務拼湊。

### Partners：將 Agent 引入 IM 渠道
Partners 機制把同一個 Chat Agent Loop 帶入個人微信、企業微信、QQ/NapCat 等即時通訊渠道。每個 Partner 擁有獨立的 Soul（人設/提示詞）、Library（知識庫）、Tools（工具集）與 Workspace（工作空間），使同一核心邏輯能以不同人格、不同知識邊界服務不同使用場景。

### 文件導覽與擴充生態
官方文件提供五大入口：快速上手、探索 DeepTutor、Partners 夥伴與渠道、DeepTutor CLI、模型與搜尋提供商。涵蓋 PyPI、原始碼、Docker、純 CLI 四種安裝路徑，以及 LLM、Embedding、搜尋引擎的提供商配置。社群支援包含 Discord、GitHub Discussions、Issue Tracker，並提供 SKILL.md 供 AI 代理間標準化交接。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| Agent-native 設計 | 整個系統以 Agent 循環為核心，所有功能（聊天、RAG、寫作、記憶）均在同一運行時協作，避免模組間斷層。 | 原文：「共享 runtime 驅動 Chat、深層 capabilities、Partners、Book generation、Co-Writer editing、RAG 和三層 Memory。」 |
| 三層 Memory 系統 | 雖未展開細節，但明確提到擁有三層記憶架構，推測包含短期會話記憶、長期用戶偏好記憶與知識庫級語義記憶。 | 原文：「共享 runtime 驅動……三層 Memory。」 |
| Partners 多渠道部署 | 同一 Agent 邏輯可無縫接入微信、企業微信、QQ/NapCat 等 IM，每個渠道實例擁有獨立人設、知識庫、工具與工作空間。 | 原文：「Partners 把同一個 chat agent loop 帶到 IM 渠道裡，同時擁有自己的 soul、library、tools 和 workspace。」 |
| 四種安裝路徑 | 支援 PyPI 套件安裝、原始碼安裝、Docker 容器部署、純 CLI 模式，滿足從快速體驗到生產部署的不同需求。 | 原文：「PyPI、原始碼、Docker、純 CLI 四種安裝路徑。」 |
| 可配置的模型與搜尋提供商 | 提供統一介面配置 LLM、Embedding 模型與搜尋引擎，避免綁定單一供應商。 | 原文：「配置 LLM、Embedding、搜尋引擎。」 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| DeepTutor 是开源、agent-native 的个性化学习伴侣。 | DeepTutor 是開源、Agent 原生的個人化學習伴侶。 | 專案簡介首句，定義專案性質與定位。 |
| 共享 runtime 驱动 Chat、深层 capabilities、Partners、Book generation、Co-Writer editing、RAG 和三层 Memory。 | 共享運行時驅動聊天、深度能力、夥伴、書籍生成、協作寫作、RAG 與三層記憶。 | 說明核心架構：單一運行時支撐所有主要功能模組。 |
| Partners 把同一个 chat agent loop 带到 IM 渠道里，同时拥有自己的 soul、library、tools 和 workspace。 | Partners 將同一個聊天 Agent 循環帶入即時通訊渠道，同時擁有自己的靈魂、知識庫、工具與工作空間。 | 闡述 Partners 機制如何實現多渠道、多人設部署。 |

## 可參考資料
- **DeepTutor 官方文件首頁**：本筆記的主要資料來源，包含導覽結構與專案核心描述。 — <https://docs.deeptutor.info/zh-cn/>
- **快速上手指南**：提供 PyPI、原始碼、Docker、CLI 四種安裝方式的詳細步驟。 — <https://docs.deeptutor.info/zh-cn/get-started/>
- **探索 DeepTutor 功能**：涵蓋 Chat、沉浸式閱讀、Partners、子智能體、Co-Writer、Book、學習空間、擴充、Memory、Knowledge、Settings 等功能細節。 — <https://docs.deeptutor.info/zh-cn/explore/>
- **Partners 夥伴與渠道文件**：說明如何將持久學習夥伴接入個人微信、企業微信、QQ/NapCat 等 IM 渠道。 — <https://docs.deeptutor.info/zh-cn/partners/>
- **DeepTutor CLI 文件**：從終端驅動 capabilities、KB、sessions、notebooks、memory、books 與 partners。 — <https://docs.deeptutor.info/zh-cn/cli/>
- **模型與搜尋提供商配置**：配置 LLM、Embedding、搜尋引擎的提供商設定指南。 — <https://docs.deeptutor.info/zh-cn/get-started/providers/>
- **Discord 社群**：官方標註「提問最快的地方」，即時互助與討論管道。 — <https://discord.gg/eRsjPgMU4t>
- **GitHub Discussions**：長篇問答與設計討論的公開論壇。 — <https://github.com/HKUDS/DeepTutor/discussions>
- **Issue Tracker**：Bug 回報與功能建議的正式追蹤系統。 — <https://github.com/HKUDS/DeepTutor/issues>
- **SKILL.md 規範**：給驅動 DeepTutor 的 AI 代理使用的標準化交接文件規範。 — <https://github.com/HKUDS/DeepTutor/blob/main/SKILL.md>
