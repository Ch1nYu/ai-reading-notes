---
title: The Shorthand Guide to Everything Claude Code
type: article
source_url: https://x.com/affaan/status/2012378465664745795
source_site: X
added: '2026-09-07'
topics:
- coding-agents
summary: 作者系統化整理 Claude Code 的進階配置體系，強調透過技能、鉤子、子代理與 MCP 的模組化組合、嚴格控制上下文視窗、善用並行工作流，才能在大型專案中穩定高效地發揮 AI 程式設計助手的效能。
abstract: 這篇文章是 cogsec (@affaan) 在使用 Claude Code 10 個月後的完整配置指南，涵蓋技能、鉤子、子代理、MCP、外掛、編輯器搭配等核心功能，並分享上下文視窗管理、並行工作流等實戰心得，適合想深度客製化 Claude Code 的開發者參考。
---

## 完整摘要

### 核心架構：技能、命令、鉤子與子代理的分工
文章將 Claude Code 的擴充機制劃分為四層：技能儲存於 ~/.claude/skills，定義較廣泛的工作流程；命令儲存於 ~/.claude/commands，為可透過斜線指令快速呼叫的提示詞；鉤子則是基於工具呼叫與生命週期事件的觸發式自動化，分為 PreToolUse、PostToolUse、UserPromptSubmit、Stop、PreCompact、Notification 六種型別；子代理是主代理可委派任務的獨立流程，可限制工具、MCP 與權限範圍，並在背景或前景執行，釋放主代理上下文。作者示範將技能與子代理結合，讓子代理自主執行特定技能集，並建議用 hookify 外掛以對話方式建立鉤子，避免手寫 JSON。

### 規則、記憶與 MCP 的管理策略
規則系統提供兩種模式：單一 CLAUDE.md 或模組化的 .rules 資料夾，作者列舉的範例包括禁止表情符號、避免紫色系前端配色、部署前必測試、優先模組化、不提交 console.log 等專案級最佳實踐。MCP（Model Context Protocol）被定義為提示詞驅動的外部服務封裝，而非 API 替代品；作者強調上下文視窗管理至關重要：雖然使用者層級配置了 14 個 MCP，但每專案僅啟用 5-6 個，維持活躍工具數在 80 個以下，否則 200k 上下文可能剩 70k 且效能嚴重下降。Chrome in Claude 為內建 MCP，可讓 Claude 自主操作瀏覽器。

### 外掛、編輯器整合與實用技巧
外掛將技能、MCP、鉤子、工具打包安裝，LSP 外掛對非 IDE 環境特別有用，提供即時型別檢查、跳轉定義、智能補全，同樣需注意上下文佔用。編輯器方面作者主推 Zed（Rust 編寫、輕量、Agent Panel 整合、即時檔案追蹤、Vim 模式），並給出螢幕分欄、Ctrl+G 快速開啟檔案、自動儲存、Git 整合、檔案監聽等具體搭配建議；VSCode/Cursor 也是可行選擇，可透過 \ide 啟用 LSP 或使用擴充功能。鍵盤快捷鍵、/fork 分叉對話、Git worktree、tmux 監控長指令、mgrep 取代 grep、/rewind、/statusline、/checkpoints、/compact、GitHub Actions 程式碼審查、沙箱模式等技巧皆有實際操作說明。

### 作者的實戰配置與關鍵心法
作者展示個人配置：外掛安裝多但同時啟用 4-5 個；MCP 使用者層配置 14 個但專案層僅啟用 5-6 個；關鍵鉤子與自訂狀態列（顯示使用者、目錄、Git 分支髒污標記、上下文剩餘百分比、模型、時間、待辦計數）；規則採模組化結構；子代理按職責劃分。五大心法：1) 配置視為微調而非架構，別過度設計；2) 上下文視窗珍貴，停用未用 MCP/外掛；3) 善用並行：/fork 與 Git worktree；4) 自動化重複任務：鉤子處理格式化、檢查、提醒；5) 子代理限定工具權限以聚焦執行。作者並說明此為部分細節，若有興趣後續會發更多專題。

## 重點知識與概念拆解

| 概念 | 白話解釋 | 來源證據 |
|------|----------|----------|
| 技能與命令的區別與串聯 | 技能定義較廣泛的工作流程並存放在 ~/.claude/skills，命令是可透過斜線指令直接執行的提示詞並存放在 ~/.claude/commands，兩者可在同一提示詞中串聯呼叫（如 /refactor-clean 後接 /tdd），形成模組化的自動化管線。 | 原文：「Skills operate like rules, constricted to certain scopes and workflows... Commands are skills executed via slash commands. They overlap but are stored differently... Skills and commands can be chained together in a single prompt」 |
| 六種鉤子型別與 hookify 外掛 | 鉤子針對工具呼叫與生命週期事件觸發自動化，分為 PreToolUse（驗證/提醒）、PostToolUse（格式化/回饋）、UserPromptSubmit（使用者送訊息）、Stop（回應結束）、PreCompact（壓縮前）、Notification（權限請求）。作者建議使用 hookify 外掛以自然語言描述需求自動生成鉤子配置，避免手寫 JSON。 | 原文列出六種 Hook Types 並說明：「Pro tip: Use the hookify plugin to create hooks conversationally instead of writing JSON manually. Run /hookify and describe what you want.」 |
| 子代理的沙箱化與技能授權 | 子代理可被委派任務並在背景/前景執行，釋放主代理上下文；可為每個子代理單獨配置允許的工具、MCP 與權限，實現沙箱化；子代理亦可被授權執行特定技能子集，自主完成委派工作。 | 原文：「Subagents work nicely with skills - a subagent capable of executing a subset of your skills can be delegated tasks and use those skills autonomously. They can also be sandboxed with specific tool permissions. Configure allowed tools, MCPs, and permissions per subagent for proper scoping.」 |
| MCP 數量直接影響上下文視窗可用大小 | 作者實測：啟用過多 MCP 會嚴重壓縮可用上下文（200k 可能剩 70k）並導致效能下降。因此採取「配置多、啟用少」策略：使用者層配置 14 個 MCP，但每專案僅啟用 5-6 個，活躍工具數控制在 80 個以下。這是具體可驗證的效能管理經驗。 | 原文：「Your 200k context window before compacting might only be 70k with too many tools enabled. Performance degrades significantly. Rule of thumb: Have 20-30 MCPs in config, but keep under 10 enabled / under 80 tools active.」 |
| Zed 編輯器與 Claude Code 的深度整合優勢 | 作者選用 Zed 的原因包括：Agent Panel 即時追蹤檔案變更、Rust 撰寫效能極佳不搶資源、命令面板整合自訂斜線指令、Vim 模式、Git 整合與檔案監聽。並給出具體操作建議：螢幕分欄、Ctrl+G 快速開啟 Claude 正在編輯的檔案、啟用自動儲存確保讀取最新版本。 | 原文：「Why Zed works well with Claude Code: - Agent Panel Integration... - Performance - Written in Rust... - CMD+Shift+R Command Palette... - Minimal Resource Usage... - Vim Mode」以及後續 5 項具體搭配建議。 |
| 並行工作流：/fork 與 Git worktree 的互補 | /fork 可將對話分叉處理不重疊任務，避免排隊訊息；Git worktree 則提供獨立檔案系統檢出，適合需同時修改重疊檔案的平行 Claude 實例，兩者解決不同層面的並行需求。 | 原文：「Parallel Workflows: /fork - Fork conversations to do non-overlapping tasks in parallel instead of spamming queued messages. Git Worktrees - For overlapping parallel Claudes without conflicts. Each worktree is an independent checkout」 |
| 沙箱模式與 --dangerously-skip-permissions 的風險對比 | 沙箱模式讓 Claude 在受限環境執行風險操作不影響實際系統；反之 --dangerously-skip-permissions 移除所有限制讓 Claude 自由行動，作者明確警告若不小心可能造成破壞。這是作者主動揭露的使用條件與風險界定。 | 原文：「Use sandbox mode for risky operations - Claude runs in restricted environment without affecting your actual system. (Use --dangerously-skip-permissions - to do the opposite of this and let claude roam free, this can be destructive if not careful.)」 |

## 中英金句與解釋

| 原文 | 中譯 | 脈絡／解釋 |
|------|------|------------|
| Don't overcomplicate - treat configuration like fine-tuning, not architecture | 別過度複雜化——把配置當成微調，別當成架構設計 | Key Takeaways 第一點，作者對配置心法的總結 |
| Context window is precious - disable unused MCPs and plugins | 上下文視窗很寶貴——停用未使用的 MCP 和外掛 | Key Takeaways 第二點，強調上下文管理的核心策略 |
| Your 200k context window before compacting might only be 70k with too many tools enabled. Performance degrades significantly. | 啟用太多工具時，壓縮前的 200k 上下文視窗可能只剩 70k，效能會嚴重下降。 | MCPs 章節中關於上下文視窗管理的關鍵警告與經驗數據 |

## 可參考資料
- **Claude Code**：本文討論的核心 AI 程式設計助手工具
- **Opus 4.5**：作者提到長時間編碼會話所使用的模型版本
- **Anthropic x Forum Ventures hackathon**：作者與 @DRodriguezFX 使用 Claude Code 獲勝的黑客松活動
- **Zenith**：作者在黑客松中獲勝的專案名稱
- **hookify plugin**：用於以對話方式建立鉤子的外掛，作者強力推薦
- **Supabase MCP**：範例 MCP，讓 Claude 直接拉取資料、執行 SQL
- **Chrome in Claude**：內建 MCP，讓 Claude 自主操作瀏覽器
- **LSP (Language Server Protocol)**：外掛提供的即時型別檢查、跳轉定義、智能補全功能基礎
- **Zed**：作者主力使用的 Rust 編寫編輯器，深度整合 Claude Code
- **VSCode / Cursor**：替代編輯器選擇，支援終端機模式與擴充功能整合
- **mgrep**：優於 ripgrep/grep 的搜尋工具，可透過外掛市集安裝
- **tmux**：用於串流監控 Claude 執行的長時間指令與日誌
- **GitHub Actions**：設定 PR 自動程式碼審查的 CI/CD 平台
- **Plugins Reference**：文末參考連結之一
- **Hooks Documentation**：文末參考連結之一
- **Checkpointing**：文末參考連結之一
- **Interactive Mode**：文末參考連結之一
- **Memory System**：文末參考連結之一
- **Subagents**：文末參考連結之一
- **MCP Overview**：文末參考連結之一
- **DRodriguezFX**：作者在黑客松中的合作夥伴
- **cogsec (@affaan)**：本文作者 — <https://x.com/affaan>
