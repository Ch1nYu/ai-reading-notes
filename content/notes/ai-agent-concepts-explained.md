---
title: AI Agent 概念白話解析
type: video
source_url: https://x.com/cyrilXBT/status/2081337484168843626
source_site: X
language: en
duration: 61m 41s
added: '2026-08-07'
topics:
- agents
summary: CyrilXBT的影片介紹了如何使用Hermes Agent Harness建立一個AI代理人，協助處理客戶的詢問和預約，並強調了ClockCode MCP工具在建立AI代理人中的重要性。
---

## 完整摘要

### Hermes Agent Harness 的功能與互動方式
Hermes Agent Harness 是一個開源的 AI 代理系統，允許使用者與其互動並執行各種任務。該系統具有自我改進的能力，能夠從經驗中學習並搭配四層記憶（工作記憶、程序記憶、語義記憶、情節記憶）與 RAG 機制檢索所需脈絡。使用者可以透過 WhatsApp 或桌面應用程式與 Hermes Agent 互動，發送命令和查詢，讓代理執行瀏覽網頁、運行 Python 腳本、管理技能與記憶等工作。

### ClockCode MCP 與 AI 代理人建置
ClockCode MCP 是一個建立 AI 代理人的工具，提供如 Add Knowledge 等 MCP 工具，讓使用者可以輕鬆建立像是 Calendly Assistant 這類業務代理人並整合到自己的工作流程中。透過 ClockCode MCP，使用者能夠快速部署 AI 代理人來處理客戶的詢問、預約和其他日常事務。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| Hermes Agent Harness | 一個開源的 AI 代理控制系統，具備自我改進能力，支援透過 WhatsApp 或桌面應用程式發送指令，執行瀏覽網頁、運行 Python 腳本、管理技能與記憶等任務。 | 影片前半段介紹 Hermes Agent Harness 的開源架構、多通道互動與自我改進特性。 |
| 自我改進機制 | Hermes Agent 能夠從過去執行任務與互動的經驗中學習，持續累積技能與記憶以改善後續表現。 | 影片說明 Hermes Agent 可從經驗中學習並隨使用時間自我改進。 |
| 四類記憶架構（工作、程序、語義、情節） | 工作記憶儲存臨時對話歷史與系統提示；程序記憶儲存代理的行為規則與技能；語義記憶儲存事實與使用者資料；情節記憶儲存過去的對話與事件序列。 | 影片拆解 Agent 記憶系統的四種分類與各自負責儲存的資訊。 |
| RAG（Retrieval Augmented Generation） | 代理從長期記憶與知識庫中提取相關資訊並注入上下文，以輔助生成準確回應的過程。 | 影片講解記憶提取時說明透過 RAG 從記憶庫檢索相關內容。 |
| ClockCode MCP 與 Calendly Assistant | ClockCode MCP 提供 Add Knowledge 等 MCP 工具，讓使用者能快速建立並整合專屬業務代理人（如處理預約與客戶詢問的 Calendly Assistant）。 | 影片示範：「So now it's using this MCP tool called Add Knowledge」並建立名為 Calendly Assistant 的新代理人。 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
| --- | --- | --- |
| "A large language model is like a horse, it's very powerful, but if you don't have a good set of tools to ride it, you could just get hurt." | 一個大型語言模型就像一匹馬，非常強大，但如果你沒有好的工具來控制它，你可能會受到傷害。 | 強調了控制 AI 模型與建立 Harness 工具鏈的重要性。 |
| "We need to have a good control over this technology, so that it works the way we want." | 我們需要對這項技術有良好的控制，讓它按照我們的期望運作。 | 強調透過控制層引導 AI 技術按預期行為運作。 |
| "So now it's using this MCP tool called Add Knowledge." | 現在正在使用 MCP 工具中的新增知識功能。 | 示範如何使用 ClockCode MCP 為 AI 代理人注入知識。 |
| "You can see that we have this new agent called Calendly Assistant" | 你可以看到我們有一個新的代理人叫做 Calendly Assistant。 | 示範建立處理行程預約的專屬 AI 代理人。 |
| "With this product, you'll just be able to handle it without much of a concern." | 使用這個產品，你就可以毫無顧慮地處理客戶的詢問和預約。 | 強調使用 ClockCode MCP 自動化客服與預約流程的效益。 |

## 可參考資料
- **Hermes Agent Harness**：影片介紹的開源自我改進 AI 代理控制系統，支援 WhatsApp 與桌面端互動。
- **ClockCode MCP**：影片示範用於建立業務 AI 代理人（如 Calendly Assistant）與新增知識的 MCP 工具。
- **Calendly**：影片中整合至 AI 代理人以自動處理客戶預約的行程排程服務。
- **CyrilXBT (@cyrilXBT)**：影片發布者，以白話與實作示範解析 AI Agent、記憶系統與 MCP 工具。 — <https://x.com/cyrilXBT/status/2081337484168843626>
