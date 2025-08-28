"""Helpers for importing documents into the knowledge base."""
from pathlib import Path

import markdown
from docx import Document


def parse_docx(path: Path) -> str:
    """Return plain text from a .docx file."""
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def parse_md(path: Path) -> str:
    """Convert Markdown to HTML."""
    return markdown.markdown(path.read_text(encoding="utf-8"))
