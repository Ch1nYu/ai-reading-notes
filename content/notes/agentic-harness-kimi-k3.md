---
title: How to Build An Agentic Harness using Kimi K3
type: article
source_url: https://x.com/Av1dlive/status/2085405823782842835
source_site: X
language: en
added: '2026-08-11'
topics:
- agents
summary: 建立一個與模型解耦的 Agentic Harness（控制層），透過 11 個可組合的構建元素與 7 個核心原語，讓你的工具鏈能在模型快速更迭、能力參差不齊的環境中持續演進、安全可控。
abstract: 作者 Avid 完整拆解如何建立一個「模型無關」的 AI Agent 控制層，提出 11 個核心構建元素與 7 個基礎原語，讓你的工具鏈能在模型快速更迭中存活，核心主張是「模型是商品，Harness 才是資產」。
---

## 完整摘要

### 背景與動機
- **現狀**：2026 年 8 月，開發者一年換三次主力模型，每次都得重寫整合層，因為每家廠商 CLI 都有自己的方言（session 格式、resume 旗標、核准提示、對「完成」的定義）。
- **不變的需求**：把工作隔離在不碰主分支的地方、可重播的記錄、東西離開機器前的閘門。
- **核心押注**：智力變得廉價且多元（價格年降 10 倍、開閉源差距僅 3 分），但**領域能力不均**（K3 在 Terminal-Bench 第一、FrontierMath Tier 4 僅 39%）、**可靠度低**（最佳開源模型幻覺率 51%、閉源 54.9%）。因此唯一值得建設的地方是在模型之間——**客製化介面即產品介面**。

### 三大法則
1. **智力豐富，Harness 稀缺**：為當下模型建工具 = 買重寫；為「槽位」建工具 = 買選擇權。
2. **介面薄、系統厚**：Harness 可達 6 萬行，薄的是觸碰模型的縫隙（兩個手寫 adapter + JSON 檔）。
3. **一切可調，除了不可調清單，那清單就是代碼**：自我擴展分三層（資料、提案、證據），能力邊界嚴格限制可調參數（5 個可動、15 個禁用關鍵字）。

### 五大核心概念
| 概念 | 關鍵定義 |
|------|----------|
| **Harness** | 針對「工作」而非「工作者」裁剪：你的 repo、檢查、核准習慣、紀錄。智力穿過它，20 個 CLI 通過參考實作，註冊表裡沒有一個被命名。 |
| **Abundance** | 推理成本三年降 1000 倍（MMLU-42：$60/M → $0.06/M）。K3：2.8T 參數、16/896 experts、1M context、$3 in/$15 out、AA 指數 57（Claude Fable 5 為 60）。模型可互換，選模型是排程決策而非架構決策。 |
| **Unevenness** | 同一模型四大基準首尾相差極大：Terminal-Bench 88.3 vs FrontierMath Tier 4 ~39%。 |
| **The Seam** | Harness 與模型接觸的唯一薄層。方言放資料 = 檔案格式；放代碼 = 兩季路線圖。註冊表 2 引擎、磁碟 20 個 manifest，這比率就是押注。 |
| **Self-extension** | 三層：Tier 1 資料（JSON manifest，免審免編譯）、Tier 2 提案（系統起草調參，人工升級）、Tier 3 證據（學習專案事實，需證據鏈驗證）。**自我擴展 ≠ 自我修改**，系統不可授予自己新能力。 |
| **Capability Boundary** | 允許清單 5 欄位（router 閾值、圖模板、detector 閾值、恢復預算、協調器 prompt 片段），拒絕清單 15 子字串。上限只能降不能升。 |

### 七大 Harness 2.0 原語
| 原語 | 定義 | 不變量 | 所在 BUILD |
|------|------|--------|------------|
| **Slot** | 命名的智力插槽，資料宣告 | 代碼無廠商名，註冊表 2 名、磁碟 20 檔 | 00 |
| **Cell** | 可丟棄、受限的工作空間 | 執行不出 Cell，啟動時證明隔離 | 04, 05 |
| **Run** | 帶身分與明確生命週期的單一目標 | 非法轉換為可記錄值，不 panic | 03 |
| **Thread** | 共享一 Cell、一 provider session 的 Run 鏈 | 會話累積鍵於 thread root 而非 turn | 04 |
| **Ledger** | 有序、僅追加的完整事件記錄 | 先持久化再廣播，訂閱者永不見未落庫事件 | 02 |
| **Gate** | 執行因規則或人工停下的點，附帶理由 | UI 強制的 gate 只是建議；Gate 坐在副作用處 | 01, 06, 07, 08, 09 |
| **Dial** | 系統可提案調整、版本化、可升級的設定，旁邊放凍結清單 | 系統提案、人工升級、上限只降不升 | 10 |

### 十一大 BUILD 逐項拆解

| BUILD | 名稱 | 一句話目的 | 關鍵實作細節 | CHECK 通過條件 |
|-------|------|------------|--------------|----------------|
| **00** | **The Manifest** | 代碼若知模型廠商名，就把本季冠軍寫死在系統裡 | 每個 agent 一 JSON：binary、aliases、resume 方式、approval prompt 模式、working/idle/blocked 模式。載入順序：內建 → override 目錄，後蓋前。單檔獨立解析。兩手寫 adapter，其餘全 JSON。 | `cargo run --bin list-engines` 印 2；`ls manifests/*.json | wc -l` 印大得多。比率 = 下次換模型重寫成本。 |
| **01** | **The Boundary** | 一個 process 擁有所有副作用，否則你要查五個 process 誰寫了那行 | 三 process：shell（UI）、daemon（副作用）、update helper。Shell 只說 JSON-RPC 2.0 over Unix socket (0600) + getpeereid + Keychain token。Daemon 獨佔 SQLite、git、child process、network。 | `lsof -p $DAEMON_PID` 見 SQLite；`lsof -p $SHELL_PID` 不見。Socket `stat` 顯示 0600。 |
| **02** | **The Ledger** | 只存在 scrollback 的 run 是謠言，不可重播 | 事件先寫 append-only table 再廣播。全域 monotonic sequence + per-run sequence。序號來自 committed insert（非記憶體計數器）。冪等靠 `request_id`：重複請求回 `false` 不再廣播。 | 兩測試綠：重連走同一 code path、重試不重複廣播。 |
| **03** | **The State Table** | 非法轉換是可記錄的值，panic 是你選的停機 | 8 狀態 × 8 狀態 = 64 斷言的轉換表。`TransitionError { machine, from, to }` 可渲染。終態不可離開。關鍵防線：`Blocked → AwaitingApproval` 恢復時必重進隊列等人工。 | 完整狀態積測試綠；無 finished run 能再啟動。 |
| **04** | **The Worktree** | 改你 checkout branch 的 agent 讓你當保母，保母正是你想解僱的 | 每 run 獨立 worktree + branch。會話 ≠ 單 run；follow-up = 新 run 指向 parent，**所有累積鍵於 thread root**。Reclaim 只收乾淨且無額外 commit 的 tree，絕不 `--force`。 | 發起 run → follow-up → 兩 turn 回報同一 branch，你自己的 checkout `git status` 乾淨。 |
| **05** | **The Cage** | 沒試著闖的 sandbox 是設定檔，設定檔擋不住東西 | 兩族群兩規則：engine control 用 vendor 自帶 sandbox + 淨化環境；worker command 用**自建 profile**（獨立 process group、資源限制、proxy-only 網路、顯式可寫根目錄）。**從零建環境**（PATH、fake HOME、無 SSH_AUTH_SOCK、GIT_CONFIG_NOSYSTEM=1、空 global gitconfig）。**啟動探針證明**：`expect_denied` 以 `/bin/ls` 失敗為通過。任一探針失敗 → 拒絕啟動 run，無降級模式。Keychain 是縫隙：engine session symlink、.claude.json copy；worker 兩者皆無。Canary b2 證明兩族群未意外合併。 | ≥3 canary 通過；故意破壞 profile → `run.start` 被拒並命名失敗的 canary。 |
| **06** | **The Denier** | Agent 爆炸半徑 = 它能改且你撤不回的東西，全在機器外 | 純函數判 `program + args`：`git push`、`npm publish`、deploy 等外寫 → 擋下並寫入 Ledger。`git clone https`、`curl` 無 body/非變更 method → 放行。過度攔截 → 開發者註解掉 → 更糟。 | 兩測試綠：外寫被擋、本地操作（status/commit/clone）全過。 |
| **07** | **The Router** | 讓被監督者寫自己的預算是錯的 | **事實**（字數、命名檔數、附帶 check 指令、repo tracked 檔數、dirty 狀態）決定路由骨架；**模型意見**只能在事實同意且信心足時提案。直跑：短、原子、有 check。有界循環：短、原子、無 check。Swarm：語意暗示廣度/多步。信心門檻 0.7、直跑上限 60 字/3 檔、大 repo >5k tracked。`worth_planning` 門檻：事實說循序時跳過規劃呼叫。關鍵字 `each`、`across` 直接取消原子性。 | 三測試綠：router 非 passthrough。 |
| **08** | **The Compiler** | 模型提案計畫；你的代碼決定能不能跑，預設不准 | 純、全函數驗證，預設拒絕並點名規則。規則對應具體災難：cycle 不終止、orphan 白幹、雙 editor 衝突 scope、無 verifier 的 edit branch、過寬/深燒 token。詞彙寬容解析，歧義向**最受限**選項傾斜：未識 role → Editor（最嚴格：disjoint scope + verifier 路徑）。驗證在 merge **後**再跑一次。失敗節點標記 dependents unreachable。 | 三測試綠：惡意計畫（cycle、雙 editor 同 scope）被拒並具體理由渲染。 |
| **09** | **The Detector** | 迴圈與苦幹外觀相同，難點不在抓迴圈而在不誤報 | 三信號雙讀：同樣測試失敗兩次（卡住 / 故意紅綠重構）、4 分鐘無輸出（掛了 / 在編譯）、讀 20 檔 0 編輯（迷路 / 在研究）。**每個觸發必門於「明確缺乏進展」**，進展訊號可重置計數器。指紋雙層：精確 + 正規化（數字→#、路徑保留最後一段）。有界歷史 12 條。純函數（無時鐘、隨機、IO）。恢復階梯：nudge → replan → 從最後驗證點重啟 → 停下秀證據。15 測試中 5 個斷言「不觸發」。 | 三測試綠；誤報 fixture 通過。 |
| **10** | **The Evolution Guard** | 能自調參的系統能自擴籠子，所以先寫死不可碰的欄桿再讓它調 | Allow-list（5 欄位）+ Deny-list（15 子字串）雙重檢查，**允許清單優先**（合法欄位名可能含禁用子字串）。上限只降不升。系統觀察+提案，**升級唯人工**，自我升級 = 移除最後能說不的人。 | 三測試綠：候選政策試圖升 `max_turns` 在測試中被拒。 |

### 會自己產生自己的循環
- Repo 根目錄 `AGENTS.md` (36KB)、`PLAN.md`、`HANDOFF.md`、`HANDOFF-FABLE.md`、`docs/superpowers/plans/`、`specs/` —— 不是文件，是**下一輪模型的輸入格式**，由上一輪模型寫成。
- `crates/daemon/src/handoff.rs` 為切換 provider 時組裝 brief：免費（讀 ledger 不呼叫模型）、可重現、不依賴前一 process 存活。**拒絕讓離職模型自我總結**（不可驗證、費 token、需 live session）。
- 方法即產品：包含產生自身過程的 repo 是循環，不含的是制品。

### 它輸在哪（誠實清單）
1. 無 CI，GPUI 需 Metal toolchain，四步驟 gate 跑在筆電；徽章是宣稱非 CI 產出。
2. 測試數對不上：badge 606、實際屬性 604、舊 commit 576。
3. 僅 macOS 14+、Rust 1.97+、edition 2024、GPUI 釘 Zed git rev。
4. V1 無外寫：不能開 PR、推 branch、deploy，最後一哩路全手動。
5. 協議版本寫了不驗：`protocol_version` 四處寫入、零處比對。
6. 未出貨：v0.1.0，簽名/公證/更新通道待憑證。
7. Manifest 是螢幕刮取，有保存期；vendor 改狀態列規則失效、靜默失效。
8. Router 故意粗糙：17 關鍵字 substring matching，避開關鍵字的 10 步驟任務會被判為 atomic。
9. 閾值是帶版號的初稿。

### 地圖與推廣時程
- **核心 crate (03, 07-10) 零 IO** → 純守衛才能窮盡測試拒絕邏輯。
- **6 週推廣**：
  - Week 1: Manifest（agent 變資料，grep 廠商名為空）
  - Week 2: Ledger + Boundary（關 UI 10 分鐘重開歷史完整、無額外 catch-up）
  - Week 3: Worktree + State Table（三 follow-up 留主 checkout 乾淨、狀態積全走）
  - Week 4: Cage + Denier（故意破 sandbox → 拒啟動並點名 canary）
  - Week 5: Router + Compiler（惡意計畫被拒並具體理由顯示）
  - Week 6: Detector + Guard（誤報 fixture 過、候選政策升 max_turns 被測試擋下）

### 跑書 15 條鐵律
1. 註冊表不寫廠商名；agent 是檔案，加 agent = 寫文字。
2. 一 process 擁有所有副作用；一處審計。
3. 先持久化再廣播；重播與即時共用一通道。
4. 非法轉換回傳值；panic 是你選的停機。
5. 你 checkout 的 branch 絕不碰；reclaim 只收乾淨的，永不 `--force`。
6. 會話鍵於 thread 非 turn。
7. 環境從零建；過濾是永遠要維護的清單。
8. 啟動時用探針證明隔離。
9. **Fail closed**；無降級模式。
10. 外寫 spawn 前擋下並記錄拒絕。
11. 事實決定形狀；模型信心只是輸入之一。
12. 不確定性向下走階梯，不向上。
13. 預設拒絕計畫，點名失敗規則，歧義向最受限解析。
14. 停滯觸發門於「缺乏進展」；先寫誤報測試。
15. Allow-list + Deny-list，上限只降，人工升級。

### 五大預測（四個一年內可驗）
1. 2027 年前，前沿模型之間的路由將成為標準工作流。
2. Harness 代碼庫將超過模型整合代碼 10 倍以上。
3. 「模型無關」將成為 agent 工具的基本要求，而非差異化特性。
4. 能力邊界（allow/deny 清單）將成為安全審計的標準制品。
5. 自我擴展 Tier 2/3 將在生產環境保持「僅提案、人工升級」。

### 反方最強論點與反駁
- **論點**：廠商每季把 harness 功能內建到自家 CLI（sandbox、permission、resume、subagent、plan approval），若內建夠好且免費，獨立 harness 只是愛好。
- **反駁**：**廠商無法為競爭對手提供槽位**。Anthropic 不會在 Claude Code 內放 Kimi manifest；OpenAI 不會在事實指向 Gemini 時幫你路由。**內建 harness 本質上是 Harness 1.0（針對自家 worker）**，跨模型路由層必須由**不賣模型的人**建。窗口期就開在模型能力仍不均的當下。

### 結語
> Harness 是智力利用率所在。我們可以擁有可客製化、隨使用方式即時演進的 harness。既然智力豐富，建立這類 harness 將佔據多數護城河。


## 重點知識與概念拆解

| 概念名 | 一句白話解釋 |
|--------|--------------|
| **Agentic Harness** | 針對「你的工作流」量身裁剪的控制層，而非針對某個 AI 模型；模型像馬/電線/被測系統，Harness 是固定在你 repo、檢查、核准習慣上的韁繩/線束/測試床。 |
| **Abundance (智力豐富)** | 推理成本以年降 10 倍的速度暴跌（三年千倍），頂尖開源模型（K3）已逼近閉源前沿，模型選擇變成排程決策而非架構決策。 |
| **Unevenness (能力不均)** | 同一模型在不同基準極端分化：K3 寫代碼 Terminal-Bench 第一、數學 FrontierMath Tier 4 僅 39%，你不是在選可信智力，而是在選「你能接住的錯誤形狀」。 |
| **The Seam (縫隙/接縫)** | Harness 與模型唯一的接觸面，必須極薄：兩手寫 adapter + 20 個 JSON manifest，方言全塞進資料，換模型成本 = 寫一個文字檔。 |
| **Self-extension (自我擴展)** | 三層：Tier 1 數據（JSON manifest 熱載入）、Tier 2 提案（系統起草調參，人工升級）、Tier 3 證據（學習事實需證據鏈）。**核心：系統可增知識、提調參，不可自授新能力**。 |
| **Capability Boundary (能力邊界)** | 允許清單 5 欄位、拒絕清單 15 子字串（sandbox、capab、external_write…），上限只降不升，雙清單並行、允許優先，防止系統自擴籠子。 |
| **Slot (槽位)** | 命名的智力插槽，純資料宣告；代碼零廠商名，註冊表 2 名、磁碟 20 檔。 |
| **Cell (胞/隔離空間)** | 可丟棄的受限工作區：獨立 worktree、fake HOME、生成 profile、顯式可寫根；啟動時以探針證明隔離，非假設。 |
| **Run (執行單元)** | 帶身分與明確生命週期的單一目標；非法狀態轉換回傳錯誤值而非 panic。 |
| **Thread (執行緒/會話鏈)** | 共享一 Cell、一 provider session 的 Run 父子鏈；所有會話累積鍵於 thread root，非 turn。 |
| **Ledger (帳本/事件日誌)** | 僅追加、有序、全域序號 + per-run 序號；**先持久化再廣播**，重連與即時共用同一 code path。 |
| **Gate (閘門)** | 執行因規則或人工停下的點，理由附隨；真正的 gate 坐在副作用發生處，UI gate 只是建議。 |
| **Dial (可調鈕)** | 系統可提案、版本化、可升級的設定，旁邊放凍結清單；系統提案、人工升級、上限只降不升。 |
| **Fail Closed (失效關閉)** | 沙箱探針任一失敗 → 拒絕啟動 run，無警告橫幅、無降級模式、結構化拒絕帶診斷資訊。 |
| **Progress-Gated Detection (進展門控偵測)** | 迴圈/停滯/迷路觸發器**必須**門於「明確缺乏進展」；進展訊號可重置計數器，誤報測試佔測試檔 1/3。 |
| **Pure Guards (純守衛)** | 核心 crate (state、router、compiler、detector、policy) 零 IO、無時鐘、無隨機、無副作用 → 可窮盡測試每一個拒絕。 |


## 中英金句與解釋

| 原文 | 中譯 | 脈絡/解釋 |
|------|------|-----------|
| "The model is the commodity and the harness is the asset. Build the harness like you will replace the model twice this year. You will." | 「模型是商品，Harness 才是資產。像今年要換兩次模型一樣去建 Harness。你真的會換。」 | 前言核心主張：投資不會過時的控制層，而非綁定特定模型的整合代碼。 |
| "Intelligence got cheap and plural. Your control layer did not." | 「智力變得廉價且多元。你的控制層沒有。」 | 情境段落：點出痛點根源——模型更迭快，自建工具鏈卻拖累遷移。 |
| "When models converge on price and stay uneven on capability, the only place left to build is between them." | 「當模型在價格上收斂、在能力上保持不均，唯一還能建設的地方就在他們之間。」 | The Bet 核心推論：跨模型路由/控制層成唯一護城河。 |
| "Thin is a property of the seam, not the system." | 「薄是縫隙的屬性，不是系統的屬性。」 | Law 2：Harness 系統可厚（6 萬行），只有觸碰模型的介面必須薄。 |
| "Fungible intelligence leaves trust nowhere to live except the harness." | 「可互換的智力讓信任無處安放，只能住在 Harness 裡。」 | Law 3 推論：既然模型都會換、都不可靠，信任只能寄託在你建的控制層。 |
| "A harness here is fitted to the work, not to the worker." | 「這裡的 Harness 是針對『工作』裁剪，而非『工作者』。」 | 概念段：重新定義 Harness 一詞，強調綁定 repo/檢查/習慣，而非綁定某家模型。 |
| "You are not choosing a trustworthy intelligence. You are choosing which one is wrong in the shape you can catch." | 「你不是在選可信的智力。你是在選『哪一個會以你能接住的形狀犯錯』。」 | Unevenness 段：幻覺率 50%+ 是常態，Harness 的工作是接住特定形狀的錯。 |
| "Put dialect in data and the seam is a file format. Put it in code and the seam becomes your roadmap for the next two quarters." | 「把方言放進資料，縫隙就是檔案格式。放進代碼，縫隙就變成你未來兩季的路線圖。」 | The Seam 段：架構決策的經濟帳。 |
| "Self-extensible does not mean self-modifying. The system may grow what it knows and propose what it tunes. It may not grant itself a capability." | 「自我擴展不等於自我修改。系統可增長所知、提議調參，但不可授予自己新能力。」 | Self-extension 定義：劃清 Tier 2/3 的紅線。 |
| "Ceilings may fall and never rise. A policy that can raise max_turns can spend without limit." | 「上限只能降不能升。能升 max_turns 的政策就是能無限花錢。」 | Capability Boundary / Evolution Guard 核心防線設計哲學。 |
| "A run that exists only in a scrollback buffer is a run you cannot replay, and a run you cannot replay is a rumour." | 「只存在 scrollback buffer 的 run 是無法重播的，無法重播的 run 就是謠言。」 | BUILD 02 Ledger 存在理由。 |
| "An illegal transition is a value you can log, show, and persist, and the moment you make it a panic you have traded a bug report for an outage." | 「非法轉換是可記錄、可顯示、可持久化的值；把它變成 panic 的瞬間，你就用一份 bug report 換了一場停機。」 | BUILD 03 State Table 設計原則。 |
| "A sandbox you have not tried to break is a configuration file, and a configuration file has never stopped anything." | 「沒試著闖的 sandbox 是設定檔，設定檔從來擋不住任何東西。」 | BUILD 05 Cage 核心信條：啟動探針證明隔離，Fail closed。 |
| "The blast radius of an agent is the set of things it can change that you cannot undo, and every one of those lives outside your machine." | 「Agent 的爆炸半徑 = 它能改且你撤不回的東西，而那些全在你機器外面。」 | BUILD 06 Denier 畫線邏輯：本地可復原、外寫不可逆。 |
| "Letting a model choose how many workers to spend is letting the thing being supervised write its own budget." | 「讓模型決定花多少 worker，就是讓被監督者自己寫預算。」 | BUILD 07 Router 設計動機：事實決定骨架，模型只能在事實同意時提案。 |
| "Treat the plan as untrusted input, because it is." | 「把計畫當作不受信輸入，因為它就是。」 | BUILD 08 Compiler 原則：預設拒絕、純函數驗證、歧義向最受限解析。 |
| "Detection without a progress channel produces false positives, false positives train you to ignore the alarm, and an ignored alarm is no alarm." | 「無進展通道的偵測產生誤報，誤報訓練你忽略警報，被忽略的警報等於沒警報。」 | BUILD 09 Detector 核心洞見：進展門控是防誤報唯一解。 |
| "A system that can tune itself can widen its own cage, so write down the bars it may never touch before you let it tune anything." | 「能自調參的系統能自擴籠子，所以先寫死它永遠不能碰的欄桿，再讓它調參。」 | BUILD 10 Evolution Guard 存在理由。 |
| "A vendor cannot ship a slot for its competitor. Anthropic will not put a Kimi manifest in Claude Code. OpenAI will not route your objective to Gemini when the facts say Gemini is better at it." | 「廠商無法為競爭對手提供槽位。Anthropic 不會在 Claude Code 放 Kimi manifest。OpenAI 不會在事實指向 Gemini 時幫你路由。」 | The Case Against 反駁核心：跨模型路由層必須由不賣模型的人建。 |
| "Harness is where the utilisation of intelligence lies." | 「Harness 是智力利用率所在。」 | 結語：護城河不在模型，在控制層。 |


## 可參考資料

- **參考實作倉庫**：https://github.com/codejunkie99/autoharness（Rust、macOS-only、GPUI、參考實作）
- **Kimi K3 模型資訊**：2.8T 參數、16/896 experts、1M context、$3 in / $15 out、AA Intelligence Index 57
- **基準測試**：
  - Terminal-Bench（K3 88.3 vs Fable 5 84.6）
  - SWE Marathon（K3 42.0 vs Fable 5 35.0）
  - Frontend Code Arena（K3 1,679 vs Fable 5 1,631 vs GPT-5.6 Sol 1,618）
  - FrontierMath Tier 4（K3 ~39% vs 閉源 ~90%）
  - AA-Omniscience 幻覺率（K3 51%、Claude Fable 5 54.9%）
- **關鍵文件**（Repo 內）：
  - `AGENTS.md` (36 KB)、`PLAN.md`、`HANDOFF.md`、`HANDOFF-FABLE.md`
  - `docs/superpowers/plans/`、`docs/superpowers/specs/`
  - `crates/daemon/src/handoff.rs`（handoff brief 組裝邏輯）
  - `crates/engines/src/lib.rs`、`crates/pty/manifests/*.json`（Manifest）
  - `crates/protocol/src/lib.rs`、`crates/daemon/src/lib.rs`、`crates/daemon/src/auth.rs`（Boundary）
  - `crates/store/src/lib.rs`（Ledger）
  - `crates/core/src/lib.rs`（State Table）
  - `crates/daemon/src/worktree.rs`、`crates/engines/src/adapter.rs`（Worktree）
  - `crates/daemon/src/sandbox/canaries.rs`（Cage 探針）
  - `crates/daemon/src/sandbox/policy.rs`（Denier）
  - `crates/core/src/router.rs`（Router）
  - `crates/core/src/graph.rs`（Compiler）
  - `crates/core/src/detector.rs`（Detector）
  - `crates/core/src/policy.rs`（Evolution Guard）
- **作者**：Avid (@Av1dlive) X 貼文：https://x.com/Av1dlive/status/2085405823782842835
- **協作模型**：內容由作者筆記 + Kimi K3 Code 撰寫 + Opus 4.7 編輯潤飾
