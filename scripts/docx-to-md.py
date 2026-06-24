#!/usr/bin/env python3
"""
Извлекает текст из .docx и сохраняет как .md для пайплайна TZ → OpenAPI.
Использует только stdlib (docx = zip + XML). Зависимости не нужны.

Usage:
  python scripts/docx-to-md.py input/my-spec.docx
  python scripts/docx-to-md.py input/my-spec.docx -o input/my-spec.md
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def _tag(local: str) -> str:
    return f"{{{W_NS}}}{local}"


def paragraph_text(p: ET.Element) -> str:
    parts: list[str] = []
    for node in p.iter():
        tag = node.tag.split("}")[-1] if "}" in node.tag else node.tag
        if tag == "t" and node.text:
            parts.append(node.text)
        elif tag == "tab":
            parts.append("\t")
        elif tag == "br":
            parts.append("\n")
    return "".join(parts).strip()


def cell_text(tc: ET.Element) -> str:
    paragraphs = [paragraph_text(p) for p in tc.findall("w:p", NS)]
    text = " ".join(p for p in paragraphs if p).strip()
    return re.sub(r"\s+", " ", text.replace("|", "\\|"))


def table_to_markdown(tbl: ET.Element) -> str:
    rows: list[list[str]] = []
    for tr in tbl.findall("w:tr", NS):
        row = [cell_text(tc) for tc in tr.findall("w:tc", NS)]
        if any(cell.strip() for cell in row):
            rows.append(row)

    if not rows:
        return ""

    width = max(len(r) for r in rows)
    normalized = [r + [""] * (width - len(r)) for r in rows]

    lines = [
        "| " + " | ".join(normalized[0]) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    for row in normalized[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def docx_to_markdown(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        try:
            xml_bytes = archive.read("word/document.xml")
        except KeyError as exc:
            raise ValueError(f"Not a valid docx: {path}") from exc

    root = ET.fromstring(xml_bytes)
    body = root.find("w:body", NS)
    if body is None:
        raise ValueError(f"No document body in {path}")

    lines: list[str] = []
    for child in body:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "p":
            text = paragraph_text(child)
            lines.append(text if text else "")
        elif tag == "tbl":
            lines.append("")
            lines.append(table_to_markdown(child))
            lines.append("")

    out: list[str] = []
    prev_blank = False
    for line in lines:
        blank = not line.strip()
        if blank and prev_blank:
            continue
        out.append(line)
        prev_blank = blank

    header = (
        f"# {path.stem}\n\n"
        f"> Авто-конвертация из `{path.name}`. "
        f"Проверьте таблицы и диаграммы; при расхождениях сверяйтесь с исходным docx.\n\n"
    )
    return header + "\n".join(out).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert DOCX TZ to Markdown")
    parser.add_argument("input", type=Path, help="Path to .docx file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output .md path (default: same name with .md extension)",
    )
    args = parser.parse_args()

    src = args.input.resolve()
    if not src.exists():
        print(f"Error: file not found: {src}", file=sys.stderr)
        return 1
    if src.suffix.lower() != ".docx":
        print("Error: input must be .docx", file=sys.stderr)
        return 1

    dst = (args.output or src.with_suffix(".md")).resolve()

    try:
        content = docx_to_markdown(src)
    except (ValueError, zipfile.BadZipFile) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")
    print(f"OK: {dst}")
    print(f"Lines: {len(content.splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
