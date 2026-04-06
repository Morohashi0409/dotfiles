#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


META_PREFIXES = (
    "- Article type:",
    "- Target template:",
    "- Source:",
    "- Reference structure:",
)

IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
STANDALONE_MARKDOWN_LINK_RE = re.compile(r"^\[([^\]]+)\]\((https?://[^)]+)\)\s*$")
STANDALONE_URL_RE = re.compile(r"^\s*(https?://\S+)\s*$")
QUOTE_SOURCE_RE = re.compile(r"^\s*(出典|引用元)\s*:\s*(.+?)\s*$")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
HEADING_RE = re.compile(r"^(#{2,3})\s+(.*)$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    raw_meta, body = parts
    meta_lines = raw_meta.splitlines()[1:]
    data: dict[str, str] = {}
    for line in meta_lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data, body


def resolve_output_dir(article_path: Path, out_dir: Path | None) -> Path:
    if out_dir is not None:
        return out_dir
    parts = article_path.parts
    if "articles" in parts:
        idx = parts.index("articles")
        base = Path(*parts[:idx + 1]).parent / "publish-kit" / article_path.stem
        return base
    return article_path.parent / f"{article_path.stem}-note-kit"


def extract_title(frontmatter: dict[str, str], lines: list[str], article_path: Path) -> tuple[str, int | None]:
    if frontmatter.get("title"):
        return frontmatter["title"], None
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            return line[2:].strip(), idx
    return article_path.stem, None


def clean_inline_markup(text: str) -> str:
    text = INLINE_CODE_RE.sub(r"**\1**", text)
    text = MARKDOWN_LINK_RE.sub(r"\1（\2）", text)
    return text


def nonempty(iterable: Iterable[str]) -> list[str]:
    return [item for item in iterable if item.strip()]


def build_package(article_path: Path, cover_image: str | None) -> dict:
    raw = article_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(raw)
    lines = body.splitlines()
    title, title_idx = extract_title(frontmatter, lines, article_path)

    body_lines: list[str] = []
    images: list[dict[str, str]] = []
    embeds: list[dict[str, str]] = []
    quote_sources: list[dict[str, str]] = []
    heading_h2 = ""
    heading_h3 = ""

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if title_idx is not None and idx == title_idx:
            idx += 1
            continue

        if stripped.startswith(META_PREFIXES):
            idx += 1
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading_level, heading_text = heading_match.groups()
            if heading_level == "##":
                heading_h2 = heading_text.strip()
                heading_h3 = ""
            else:
                heading_h3 = heading_text.strip()
            body_lines.append(line)
            idx += 1
            continue

        quote_source_match = QUOTE_SOURCE_RE.match(line)
        if quote_source_match:
            label, source_text = quote_source_match.groups()
            quote_sources.append(
                {
                    "label": label,
                    "text": source_text.strip(),
                    "section_h2": heading_h2,
                    "section_h3": heading_h3,
                }
            )
            idx += 1
            continue

        standalone_md_link = STANDALONE_MARKDOWN_LINK_RE.match(line)
        if standalone_md_link:
            link_text, url = standalone_md_link.groups()
            embeds.append(
                {
                    "url": url,
                    "label": link_text,
                    "section_h2": heading_h2,
                    "section_h3": heading_h3,
                }
            )
            body_lines.append(url)
            idx += 1
            continue

        standalone_url = STANDALONE_URL_RE.match(line)
        if standalone_url:
            url = standalone_url.group(1)
            embeds.append(
                {
                    "url": url,
                    "label": "",
                    "section_h2": heading_h2,
                    "section_h3": heading_h3,
                }
            )
            body_lines.append(url)
            idx += 1
            continue

        image_match = IMAGE_RE.search(line)
        if image_match:
            alt = image_match.group("alt").strip()
            image_path = image_match.group("path").strip()
            caption = ""
            next_idx = idx + 1
            if next_idx < len(lines):
                next_line = lines[next_idx].strip()
                if next_line.startswith("*") and next_line.endswith("*"):
                    caption = next_line.strip("*").strip()
                    idx += 1
                elif not next_line and next_idx + 1 < len(lines):
                    after_blank = lines[next_idx + 1].strip()
                    if after_blank.startswith("*") and after_blank.endswith("*"):
                        caption = after_blank.strip("*").strip()
                        idx += 2
            images.append(
                {
                    "alt": alt,
                    "path": str((article_path.parent / image_path).resolve())
                    if not Path(image_path).is_absolute()
                    else image_path,
                    "original_path": image_path,
                    "caption": caption,
                    "section_h2": heading_h2,
                    "section_h3": heading_h3,
                }
            )
            idx += 1
            continue

        body_lines.append(clean_inline_markup(line))
        idx += 1

    cleaned_lines: list[str] = []
    previous_blank = False
    for line in body_lines:
        blank = not line.strip()
        if blank and previous_blank:
            continue
        cleaned_lines.append(line.rstrip())
        previous_blank = blank

    paragraphs = nonempty(
        line.strip()
        for line in cleaned_lines
        if not line.startswith("#")
        and not line.startswith("- ")
        and not re.match(r"^\d+\.\s", line)
    )
    lead_excerpt = " ".join(paragraphs[:2])[:180]

    return {
        "source_file": str(article_path.resolve()),
        "title": title,
        "cover_image": cover_image or "",
        "lead_excerpt": lead_excerpt,
        "body_for_note": "\n".join(cleaned_lines).strip() + "\n",
        "images": images,
        "embeds": embeds,
        "quote_sources": quote_sources,
    }


def write_outputs(data: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    body_path = output_dir / "body_for_note.md"
    manifest_path = output_dir / "manifest.json"
    checklist_path = output_dir / "publication_checklist.md"

    body_path.write_text(data["body_for_note"], encoding="utf-8")
    manifest_path.write_text(
        json.dumps(
            {
                key: value
                for key, value in data.items()
                if key != "body_for_note"
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        f"# {data['title']}",
        "",
        "## Publish Summary",
        "",
        f"- Source file: `{data['source_file']}`",
        f"- Cover image: `{data['cover_image'] or '(not set)'}`",
        f"- Lead excerpt: {data['lead_excerpt'] or '(empty)'}",
        "",
        "## Inline Images",
        "",
    ]

    if data["images"]:
        for idx, image in enumerate(data["images"], start=1):
            lines.extend(
                [
                    f"{idx}. `{image['path']}`",
                    f"   - alt: {image['alt'] or '(empty)'}",
                    f"   - caption: {image['caption'] or '(none)'}",
                    f"   - section: {image['section_h2'] or '(top)'} / {image['section_h3'] or '-'}",
                ]
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Standalone Embeds", ""])
    if data["embeds"]:
        for idx, embed in enumerate(data["embeds"], start=1):
            lines.extend(
                [
                    f"{idx}. `{embed['url']}`",
                    f"   - label: {embed['label'] or '(none)'}",
                    f"   - section: {embed['section_h2'] or '(top)'} / {embed['section_h3'] or '-'}",
                ]
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Quote Sources", ""])
    if data["quote_sources"]:
        for idx, source in enumerate(data["quote_sources"], start=1):
            lines.extend(
                [
                    f"{idx}. {source['text']}",
                    f"   - section: {source['section_h2'] or '(top)'} / {source['section_h3'] or '-'}",
                ]
            )
    else:
        lines.append("- none")

    checklist_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a note-ready publish package from a markdown article")
    parser.add_argument("article", help="Absolute path to the source markdown article")
    parser.add_argument("--cover-image", help="Absolute path to the cover image", default=None)
    parser.add_argument("--out-dir", help="Output directory for the publish kit", default=None)
    args = parser.parse_args()

    article_path = Path(args.article).expanduser().resolve()
    out_dir = resolve_output_dir(article_path, Path(args.out_dir).expanduser().resolve() if args.out_dir else None)

    package = build_package(article_path, args.cover_image)
    write_outputs(package, out_dir)

    print(json.dumps({"output_dir": str(out_dir), "title": package["title"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
