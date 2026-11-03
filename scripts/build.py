# /// script
# requires-python = ">=3.11"
# dependencies = ["jinja2", "markdown-it-py", "pyyaml"]
# ///
"""Validate every note and build the static site into ``dist/``.

Usage:
    uv run scripts/build.py            # validate + build
    uv run scripts/build.py --check    # validate only, write nothing

The note format is described in ``AGENTS.md`` (section「筆記檔格式」).
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markdown_it import MarkdownIt
from markdown_it.token import Token

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "content" / "notes"
TOPICS_FILE = ROOT / "content" / "topics.yml"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"

SITE = {
    "title": "AI 閱讀筆記",
    "tagline": "把讀過、看過的 AI 與技術內容，整理成結構一致、可以搜尋的中文筆記。",
    "repo_url": "https://github.com/Ch1nYu/ai-reading-notes",
}

REQUIRED_KEYS = ("title", "type", "source_url", "source_site", "added", "topics", "summary")
ALLOWED_KEYS = {
    "title",
    "type",
    "source_url",
    "source_site",
    "language",
    "duration",
    "added",
    "topics",
    "summary",
    "abstract",
}
ALLOWED_H2 = ("完整摘要", "重點知識與概念拆解", "中英金句與解釋", "可參考資料")
QUOTES_H2 = "中英金句與解釋"
NOTE_TYPES = ("article", "video")
LANGUAGES = ("en", "zh")
TYPE_LABELS = {"article": "文章", "video": "影片"}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’\-]*")
SUMMARY_MAX = 200

MD = MarkdownIt("commonmark", {"linkify": False}).enable("table")


@dataclass
class Note:
    slug: str
    title: str
    type: str
    source_url: str
    source_site: str
    language: str | None
    duration: str | None
    added: str
    topics: list[dict[str, str]]
    summary: str
    abstract: str | None
    html: str
    toc: list[dict[str, Any]] = field(default_factory=list)
    reading_minutes: int = 1

    @property
    def type_label(self) -> str:
        return TYPE_LABELS[self.type]

    @property
    def url(self) -> str:
        return f"notes/{self.slug}/"


class Report:
    """Collects validation errors and warnings for one note."""

    def __init__(self, path: Path) -> None:
        self.label = path.relative_to(ROOT).as_posix()
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def emit(self) -> None:
        for message in self.errors:
            print(f"ERROR {self.label}: {message}")
        for message in self.warnings:
            print(f"WARN {self.label}: {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    return None, text


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def inline_text(token: Token) -> str:
    parts: list[str] = []
    for child in token.children or []:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
        elif child.type == "image":
            parts.append(child.content)
    return "".join(parts).strip()


def heading_titles(tokens: list[Token], tag: str) -> list[str]:
    titles: list[str] = []
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag == tag and token.level == 0:
            titles.append(inline_text(tokens[index + 1]))
    return titles


def validate_body(body: str, report: Report) -> None:
    tokens = MD.parse(body)
    h1s = heading_titles(tokens, "h1")
    if h1s:
        report.error("內文不可有 H1：" + "、".join(h1s))

    h2s = heading_titles(tokens, "h2")
    for title in h2s:
        if title not in ALLOWED_H2:
            report.error(f"H2 標題不在允許清單：{title}")
    positions = [ALLOWED_H2.index(title) for title in h2s if title in ALLOWED_H2]
    if len(set(positions)) != len(positions) or positions != sorted(positions):
        report.error("H2 區塊順序錯誤，應為：" + " → ".join(ALLOWED_H2))


def normalize_added(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        cleaned = value.strip()
        if not DATE_RE.match(cleaned):
            return None
        try:
            return date.fromisoformat(cleaned).isoformat()
        except ValueError:
            return None
    return None


def validate_frontmatter(
    data: Any, slug: str, topic_keys: set[str], report: Report
) -> dict[str, Any] | None:
    if not isinstance(data, dict):
        report.error("frontmatter 缺少或不是 key: value 對應表")
        return None

    for key in REQUIRED_KEYS:
        if key not in data or is_empty(data[key]):
            report.error(f"缺少必填欄位或內容為空：{key}")

    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        report.error("不允許的欄位：" + "、".join(unknown))

    if not SLUG_RE.match(slug):
        report.error(f"檔名不符規則（只能小寫英數字與連字號）：{slug}.md")

    note_type = data.get("type")
    if not is_empty(note_type) and note_type not in NOTE_TYPES:
        report.error(f"type 只能是 article 或 video：{note_type}")

    language = data.get("language")
    if not is_empty(language) and language not in LANGUAGES:
        report.error(f"language 只能是 en 或 zh：{language}")

    added = data.get("added")
    if not is_empty(added) and normalize_added(added) is None:
        report.error(f"added 不是有效的 YYYY-MM-DD：{added}")

    topics = data.get("topics")
    if not is_empty(topics):
        if not isinstance(topics, list):
            report.error("topics 必須是清單")
        elif not 1 <= len(topics) <= 3:
            report.error(f"topics 需要 1 到 3 個分類：{topics}")
        else:
            bad = [str(topic) for topic in topics if str(topic) not in topic_keys]
            if bad:
                report.error("topics 含未知分類：" + "、".join(bad))

    source_url = data.get("source_url")
    if not is_empty(source_url) and not str(source_url).startswith(("http://", "https://")):
        report.error(f"source_url 必須以 http:// 或 https:// 開頭：{source_url}")

    summary = data.get("summary")
    if isinstance(summary, str) and len(summary) > SUMMARY_MAX:
        report.warn(f"summary 超過 {SUMMARY_MAX} 字（目前 {len(summary)} 字）")

    return data


def make_html_block(content: str) -> Token:
    token = Token("html_block", "", 0)
    token.content = content
    token.block = True
    token.map = [0, 0]
    token.level = 0
    return token


def render_body(body: str) -> tuple[str, list[dict[str, Any]]]:
    tokens = MD.parse(body)
    toc: list[dict[str, Any]] = []
    counter = 0
    current_h2: str | None = None

    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag in ("h2", "h3"):
            counter += 1
            heading_id = f"s-{counter}"
            token.attrSet("id", heading_id)
            text = inline_text(tokens[index + 1])
            level = 2 if token.tag == "h2" else 3
            toc.append({"level": level, "id": heading_id, "text": text})
            if token.tag == "h2":
                current_h2 = text
        elif token.type == "link_open":
            href = token.attrGet("href") or ""
            if href.startswith("http"):
                token.attrSet("target", "_blank")
                token.attrSet("rel", "noopener")
        elif token.type == "table_open" and current_h2 == QUOTES_H2:
            token.attrSet("class", "table--quotes")

    wrapped: list[Token] = []
    for token in tokens:
        if token.type == "table_open":
            wrapped.append(make_html_block('<div class="table-wrap">\n'))
            wrapped.append(token)
        elif token.type == "table_close":
            wrapped.append(token)
            wrapped.append(make_html_block("</div>\n"))
        else:
            wrapped.append(token)

    return MD.renderer.render(wrapped, MD.options, {}), toc


def reading_minutes(*parts: str | None) -> int:
    text = "\n".join(part for part in parts if part)
    cjk = len(CJK_RE.findall(text))
    words = len(LATIN_WORD_RE.findall(text))
    return max(1, math.ceil(cjk / 400 + words / 200))


def load_topics() -> dict[str, dict[str, str]]:
    data = yaml.safe_load(read_text(TOPICS_FILE))
    if not isinstance(data, dict):
        raise SystemExit("ERROR content/topics.yml: 應為 key: value 對應表")
    topics: dict[str, dict[str, str]] = {}
    for key, value in data.items():
        meta = value if isinstance(value, dict) else {}
        topics[str(key)] = {
            "label": str(meta.get("label") or key),
            "description": str(meta.get("description") or ""),
        }
    return topics


def load_notes(topic_map: dict[str, dict[str, str]]) -> tuple[list[Note], int]:
    reports: list[Report] = []
    notes: list[Note] = []
    topic_keys = set(topic_map)

    for path in sorted(NOTES_DIR.glob("*.md")):
        report = Report(path)
        reports.append(report)
        raw_frontmatter, body = split_frontmatter(read_text(path))
        if raw_frontmatter is None:
            report.error("找不到 frontmatter（檔案開頭需為 --- 區塊）")
            continue
        try:
            data = yaml.safe_load(raw_frontmatter)
        except yaml.YAMLError as error:
            report.error(f"frontmatter 無法解析：{error}")
            continue

        frontmatter = validate_frontmatter(data, path.stem, topic_keys, report)
        validate_body(body, report)
        if frontmatter is None or report.errors:
            continue

        html, toc = render_body(body)
        summary = str(frontmatter["summary"]).strip()
        abstract = frontmatter.get("abstract")
        abstract_text = str(abstract).strip() if not is_empty(abstract) else None
        note_topics = [
            {"key": str(key), "label": topic_map[str(key)]["label"]}
            for key in frontmatter["topics"]
        ]
        notes.append(
            Note(
                slug=path.stem,
                title=str(frontmatter["title"]).strip(),
                type=str(frontmatter["type"]),
                source_url=str(frontmatter["source_url"]).strip(),
                source_site=str(frontmatter["source_site"]).strip(),
                language=None if is_empty(frontmatter.get("language")) else str(frontmatter["language"]),
                duration=None if is_empty(frontmatter.get("duration")) else str(frontmatter["duration"]),
                added=normalize_added(frontmatter["added"]) or str(frontmatter["added"]),
                topics=note_topics,
                summary=summary,
                abstract=abstract_text,
                html=html,
                toc=toc,
                reading_minutes=reading_minutes(body, summary, abstract_text),
            )
        )

    for report in reports:
        report.emit()

    error_count = sum(len(report.errors) for report in reports)
    notes.sort(key=lambda note: (-date.fromisoformat(note.added).toordinal(), note.title))
    return notes, error_count


def build_topic_list(topic_map: dict[str, dict[str, str]], notes: list[Note]) -> list[dict[str, Any]]:
    counts = {key: 0 for key in topic_map}
    for note in notes:
        for topic in note.topics:
            counts[topic["key"]] = counts.get(topic["key"], 0) + 1
    return [
        {
            "key": key,
            "label": meta["label"],
            "description": meta["description"],
            "count": counts.get(key, 0),
        }
        for key, meta in topic_map.items()
    ]


def build_site(notes: list[Note], topics: list[dict[str, Any]]) -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )

    common = {
        "site": SITE,
        "topics": topics,
        "notes_total": len(notes),
        "build_date": date.today().isoformat(),
    }
    counts = {
        "article": sum(1 for note in notes if note.type == "article"),
        "video": sum(1 for note in notes if note.type == "video"),
    }

    index_html = env.get_template("index.html").render(
        **common, root="", notes=notes, counts=counts
    )
    write_text(DIST_DIR / "index.html", index_html)

    note_template = env.get_template("note.html")
    for position, note in enumerate(notes):
        page_html = note_template.render(
            **common,
            root="../../",
            note=note,
            prev=notes[position - 1] if position > 0 else None,
            next=notes[position + 1] if position + 1 < len(notes) else None,
        )
        write_text(DIST_DIR / "notes" / note.slug / "index.html", page_html)

    shutil.copytree(STATIC_DIR, DIST_DIR / "static")
    write_text(DIST_DIR / ".nojekyll", "")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="驗證筆記並建置靜態網站")
    parser.add_argument("--check", action="store_true", help="只驗證，不輸出檔案")
    args = parser.parse_args(argv)

    if not NOTES_DIR.is_dir():
        print(f"ERROR content/notes: 找不到筆記資料夾 {NOTES_DIR}", file=sys.stderr)
        return 1

    topic_map = load_topics()
    notes, error_count = load_notes(topic_map)
    if error_count:
        return 1
    if args.check:
        return 0

    build_site(notes, build_topic_list(topic_map, notes))
    print(f"built {len(notes)} notes -> dist/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
