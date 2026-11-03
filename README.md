# AI 閱讀筆記

把讀過、看過的 AI 與技術文章和影片，整理成結構一致、可以搜尋的中文筆記網站。

**網站**：<https://ch1nyu.github.io/ai-reading-notes/>

## 特色

- 每篇筆記都有固定結構：一句話總結、導讀、完整摘要、概念拆解表、中英金句和延伸資料
- 首頁支援全文搜尋（按 `/` 快速聚焦）、依文章或影片篩選、依主題篩選，篩選狀態會同步到網址，方便分享
- 筆記頁有側邊目錄、閱讀進度條、預估閱讀時間，以及上一篇和下一篇導覽
- 深色模式和手機版排版；前端不用任何 JS 框架或套件

## 本機使用

需要 [uv](https://docs.astral.sh/uv/)。

```sh
uv run scripts/build.py                        # 建置到 dist/
uv run python -m http.server 8000 -d dist      # 預覽 http://localhost:8000/
```

推送到 `main` 後，GitHub Actions 會自動建置並發布到 GitHub Pages。

## 給 AI 協作者

專案規則都寫在 [`AGENTS.md`](AGENTS.md)（`CLAUDE.md` 直接引用它）。新增筆記的流程寫在 [`.claude/skills/add-note/SKILL.md`](.claude/skills/add-note/SKILL.md)。
