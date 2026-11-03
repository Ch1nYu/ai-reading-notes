# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Convert one summarizer note folder into ``content/notes/<slug>.md``.

Usage:
    uv run scripts/import_note.py SRC_DIR --slug SLUG --title TITLE \
        --topics a,b [--out content/notes] [--force]

The output format is described in ``AGENTS.md`` (section「筆記檔格式」).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

ALLOWED_H2 = ("完整摘要", "重點知識與概念拆解", "中英金句與解釋", "可參考資料")
SUMMARY_TITLES = ("一句話總結", "一句總結")
EMPTY_VALUES = {"", "—", "-", "–"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
SITE_RE = re.compile(r"\[([^\[\]]+)\]\s*$")
LINK_URL_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
README_FIELD_RE = re.compile(r"^\s*[-*]\s*\*\*(?P<key>[^*]+)\*\*\s*[:：]\s*(?P<value>.*)$")
HEADER_ABSTRACT_RE = re.compile(r"^\*{0,2}簡要說明\*{0,2}\s*[:：]\s*(?P<value>.*)$")
HEADER_FIELD_RE = re.compile(r"^\*{0,2}(?P<key>[^*：:]+?)\*{0,2}\s*[:：]\s*(?P<value>.*)$")
H2_RE = re.compile(r"^##\s+(?P<title>\S.*)$")
NUMBER_PREFIX_RE = re.compile(r"^\d+(?:[.、)]\s*|\s+)")
TRAILING_PAREN_RE = re.compile(r"\s*[（(][^（()）]*[)）]\s*$")


class ImportNoteError(Exception):
    """Raised for every recoverable import failure."""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_readme(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = README_FIELD_RE.match(line)
        if match:
            fields[match.group("key").strip()] = match.group("value").strip()
    return fields


def parse_notes_header(text: str) -> dict[str, str]:
    """Parse the ``>`` blockquote below the H1 into label -> value pairs."""
    fields: dict[str, str] = {}
    seen_header = False
    for line in text.splitlines():
        stripped = line.strip()
        if not seen_header:
            if stripped.startswith("# "):
                seen_header = True
            continue
        if not stripped.startswith(">"):
            if stripped:
                break
            continue
        content = stripped.lstrip(">").strip()
        if not content:
            continue
        abstract = HEADER_ABSTRACT_RE.match(content)
        if abstract:
            fields["簡要說明"] = abstract.group("value").strip()
            continue
        for segment in content.split("｜"):
            match = HEADER_FIELD_RE.match(segment.strip())
            if match:
                fields[match.group("key").strip()] = match.group("value").strip()
    return fields


def parse_manifest(path: Path) -> tuple[str | None, str | None]:
    """Return (display_url, first source_acquired_at) or (None, None)."""
    if not path.is_file():
        return None, None
    try:
        data = json.loads(read_text(path))
    except (json.JSONDecodeError, OSError):
        return None, None
    display_url = data.get("display_url")
    acquired_at = None
    for artifact in data.get("artifacts") or []:
        provenance = artifact.get("provenance") or {}
        if provenance.get("source_acquired_at"):
            acquired_at = provenance["source_acquired_at"]
            break
    return display_url, acquired_at


def pick(*values: str | None) -> str | None:
    for value in values:
        if value is not None and value.strip():
            return value.strip()
    return None


def normalize_language(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned in EMPTY_VALUES:
        return None
    lowered = cleaned.lower()
    if lowered.startswith("en") or "英" in cleaned:
        return "en"
    if "zh" in lowered or "中" in cleaned:
        return "zh"
    return None


def normalize_duration(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned in EMPTY_VALUES:
        return None
    return cleaned


def normalize_h2_title(text: str) -> str:
    title = NUMBER_PREFIX_RE.sub("", text.strip())
    while True:
        stripped = TRAILING_PAREN_RE.sub("", title)
        if stripped == title:
            break
        title = stripped
    return title.strip()


def h2_positions(lines: list[str]) -> list[int]:
    positions: list[int] = []
    in_fence = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and H2_RE.match(line):
            positions.append(index)
    return positions


def extract_summary(lines: list[str], positions: list[int]) -> str:
    for index in positions:
        match = H2_RE.match(lines[index])
        if match and normalize_h2_title(match.group("title")) in SUMMARY_TITLES:
            paragraph: list[str] = []
            for line in lines[index + 1 :]:
                if not line.strip() or line.startswith("#"):
                    break
                paragraph.append(line.strip())
            if paragraph:
                return " ".join(" ".join(paragraph).split())
    raise ImportNoteError("notes.md 找不到「一句話總結」段落內容")


def build_body(lines: list[str], positions: list[int]) -> str:
    summary_index = None
    for index in positions:
        match = H2_RE.match(lines[index])
        if match and normalize_h2_title(match.group("title")) in SUMMARY_TITLES:
            summary_index = index
            break
    if summary_index is None:
        raise ImportNoteError("notes.md 找不到「一句話總結」區塊")
    body_positions = [index for index in positions if index > summary_index]
    if not body_positions:
        raise ImportNoteError("notes.md 在一句話總結之後沒有任何 H2 區塊")

    kept: list[str] = []
    for order, index in enumerate(body_positions):
        end = body_positions[order + 1] if order + 1 < len(body_positions) else len(lines)
        match = H2_RE.match(lines[index])
        title = normalize_h2_title(match.group("title"))
        if title not in ALLOWED_H2:
            continue
        kept.append(f"## {title}")
        kept.extend(lines[index + 1 : end])

    cleaned: list[str] = []
    in_fence = False
    for line in kept:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            cleaned.append(line)
            continue
        if not in_fence and line.strip() == "---":
            continue
        cleaned.append(line)

    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    if not cleaned:
        raise ImportNoteError("notes.md 的四個固定區塊都沒有內容")

    collapsed: list[str] = []
    blank_run = 0
    for line in cleaned:
        if line.strip():
            blank_run = 0
            collapsed.append(line)
            continue
        blank_run += 1
        if blank_run >= 3:
            continue
        collapsed.append("")
    return "\n".join(collapsed) + "\n"


def load_topic_keys(topics_path: Path) -> set[str]:
    if not topics_path.is_file():
        raise ImportNoteError(f"找不到主題分類檔：{topics_path}")
    try:
        data = yaml.safe_load(read_text(topics_path))
    except yaml.YAMLError as error:
        raise ImportNoteError(f"無法解析 {topics_path}：{error}") from error
    if not isinstance(data, dict):
        raise ImportNoteError(f"{topics_path} 格式不正確，應為 key: value 對應表")
    return {str(key) for key in data}


def parse_topics(raw: str, allowed: set[str]) -> list[str]:
    topics = [item.strip() for item in raw.split(",") if item.strip()]
    if not 1 <= len(topics) <= 3:
        raise ImportNoteError("--topics 需要 1 到 3 個以逗號分隔的分類")
    unknown = [topic for topic in topics if topic not in allowed]
    if unknown:
        raise ImportNoteError(
            "--topics 含未知分類：" + ", ".join(unknown) + "（可用：" + ", ".join(sorted(allowed)) + "）"
        )
    return topics


def source_site_from_dir(src_dir: Path) -> str | None:
    match = SITE_RE.search(src_dir.name.strip())
    if match and match.group(1).strip():
        return match.group(1).strip()
    return None


def host_of(url: str) -> str | None:
    hostname = urlparse(url).hostname
    if not hostname:
        return None
    return hostname.removeprefix("www.")


def resolve_added(readme: dict[str, str], acquired_at: str | None) -> str:
    processed = readme.get("處理時間")
    if processed:
        match = DATE_RE.search(processed)
        if match:
            return match.group(1)
    if acquired_at:
        match = DATE_RE.search(acquired_at)
        if match:
            return match.group(1)
    return date.today().isoformat()


def build_frontmatter(
    *,
    title: str,
    note_type: str,
    source_url: str,
    source_site: str,
    language: str | None,
    duration: str | None,
    added: str,
    topics: list[str],
    summary: str,
    abstract: str | None,
) -> str:
    fields: dict[str, object] = {
        "title": title,
        "type": note_type,
        "source_url": source_url,
        "source_site": source_site,
    }
    if language:
        fields["language"] = language
    if duration:
        fields["duration"] = duration
    fields["added"] = added
    fields["topics"] = topics
    fields["summary"] = summary
    if abstract:
        fields["abstract"] = abstract
    return yaml.safe_dump(fields, allow_unicode=True, sort_keys=False, width=10**9)


def convert(src_dir: Path, slug: str, title: str, topics_raw: str) -> str:
    notes_path = src_dir / "notes.md"
    if not notes_path.is_file():
        raise ImportNoteError(f"找不到 {notes_path}")

    notes_text = read_text(notes_path)
    readme_path = src_dir / "README.md"
    readme = parse_readme(read_text(readme_path)) if readme_path.is_file() else {}
    header = parse_notes_header(notes_text)
    display_url, acquired_at = parse_manifest(src_dir / "manifest.json")

    topics_path = Path(__file__).resolve().parent.parent / "content" / "topics.yml"
    topics = parse_topics(topics_raw, load_topic_keys(topics_path))

    note_type = "video" if "影片" in (readme.get("類型") or "") or "影片" in (header.get("類型") or "") else "article"

    header_source = header.get("來源") or ""
    header_url_match = LINK_URL_RE.search(header_source)
    source_url = pick(readme.get("來源 URL"), header_url_match.group(1) if header_url_match else None, display_url)
    if not source_url:
        raise ImportNoteError("找不到來源網址（README、notes 標頭與 manifest 都沒有）")

    source_site = source_site_from_dir(src_dir) or host_of(source_url)
    if not source_site:
        raise ImportNoteError("無法判斷 source_site")

    language = normalize_language(pick(readme.get("語言"), header.get("語言")))
    duration = None
    if note_type == "video":
        duration = normalize_duration(pick(readme.get("時長"), header.get("時長"), header.get("時間")))

    added = resolve_added(readme, acquired_at)
    lines = notes_text.split("\n")
    positions = h2_positions(lines)
    summary = extract_summary(lines, positions)
    body = build_body(lines, positions)
    abstract = header.get("簡要說明") or None

    frontmatter = build_frontmatter(
        title=title,
        note_type=note_type,
        source_url=source_url,
        source_site=source_site,
        language=language,
        duration=duration,
        added=added,
        topics=topics,
        summary=summary,
        abstract=abstract,
    )
    return f"---\n{frontmatter}---\n\n{body}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="把整理工具產生的筆記資料夾轉成 content/notes/<slug>.md",
    )
    parser.add_argument("src_dir", type=Path, help="整理工具輸出的資料夾")
    parser.add_argument("--slug", required=True, help="輸出檔名（不含 .md）")
    parser.add_argument("--title", required=True, help="筆記標題")
    parser.add_argument("--topics", required=True, help="逗號分隔的 1–3 個主題 key")
    parser.add_argument("--out", type=Path, default=Path("content/notes"), help="輸出資料夾")
    parser.add_argument("--force", action="store_true", help="覆寫既有檔案")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if not SLUG_RE.match(args.slug):
            raise ImportNoteError("--slug 只能用小寫英數字和連字號，例如 kv-cache-handbook")
        src_dir = args.src_dir
        if not src_dir.is_dir():
            raise ImportNoteError(f"找不到資料夾：{src_dir}")

        target = args.out / f"{args.slug}.md"
        if target.exists() and not args.force:
            raise ImportNoteError(f"{target} 已存在，改用 --force 覆寫")

        content = convert(src_dir, args.slug, args.title, args.topics)
        args.out.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    except ImportNoteError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
