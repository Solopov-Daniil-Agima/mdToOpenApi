#!/usr/bin/env python3
"""
Извлекает текст из PDF и сохраняет как .md для пайплайна TZ → OpenAPI.

Требует: pip install pypdf

Usage:
  python scripts/pdf-to-md.py input/spec.pdf
  python scripts/pdf-to-md.py input/spec.pdf -o input/spec.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

def pdf_to_markdown(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "Модуль pypdf не установлен. Выполните: pip install pypdf"
        ) from exc

    reader = PdfReader(str(path))
    pages: list[str] = []

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append(f"## Страница {i}\n\n{text}")

    body = "\n\n---\n\n".join(pages) if pages else "_Текст не извлечён (возможно, скан без OCR)._"

    # Collapse excessive blank lines
    body = re.sub(r"\n{3,}", "\n\n", body)

    header = (
        f"# {path.stem}\n\n"
        f"> Авто-конвертация из `{path.name}`. "
        f"PDF без текстового слоя может потребовать OCR. Проверьте таблицы вручную.\n\n"
    )
    return header + body.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert PDF TZ to Markdown")
    parser.add_argument("input", type=Path, help="Path to .pdf file")
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
    if src.suffix.lower() != ".pdf":
        print("Error: input must be .pdf", file=sys.stderr)
        return 1

    dst = (args.output or src.with_suffix(".md")).resolve()

    try:
        content = pdf_to_markdown(src)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")
    print(f"OK: {dst}")
    print(f"Pages/lines: {len(content.splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
