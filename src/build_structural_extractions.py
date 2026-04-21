from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
TEXT_DIR = REPO_ROOT / "data" / "intermediate" / "text"
CHUNKS_DIR = REPO_ROOT / "data" / "intermediate" / "chunks"
TABLES_DIR = REPO_ROOT / "data" / "intermediate" / "tables"
MARKDOWN_DIRECTORIES = [
    REPO_ROOT / "sources markdown canonical",
    REPO_ROOT / "sources markdown",
    REPO_ROOT / "sources markdown context",
]


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def locate_markdown_source(entry: dict) -> Path:
    selected_name = Path(entry["selected_source_file"]).name
    candidates = []
    if selected_name.lower().endswith(".pdf"):
        candidates.append(selected_name[:-4] + ".md")
    else:
        candidates.append(Path(selected_name).stem + ".md")

    source_prefix = f"{entry['source_number']:02d}-"
    for base_dir in MARKDOWN_DIRECTORIES:
        for candidate in candidates:
            path = base_dir / candidate
            if path.exists():
                return path
        matches = sorted(base_dir.glob(source_prefix + "*.md"))
        if matches:
            matches.sort(key=lambda item: (len(item.name), item.name), reverse=True)
            return matches[0]

    raise FileNotFoundError(f"No markdown source found for {entry['document_id']}")


def clean_lines(lines: list[str]) -> list[str]:
    cleaned = [line.rstrip() for line in lines]
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return cleaned


def normalize_text(text: str) -> str:
    lines = clean_lines(text.splitlines())
    return "\n".join(lines).strip()


def split_long_text(text: str, target_size: int = 1800) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    current: list[str] = []
    current_size = 0
    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        if current and current_size + paragraph_size + 2 > target_size:
            chunks.append("\n\n".join(current))
            current = [paragraph]
            current_size = paragraph_size
        else:
            current.append(paragraph)
            current_size += paragraph_size + (2 if current_size else 0)
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def parse_pdf_markdown(markdown_text: str) -> list[dict]:
    pages: list[dict] = []
    current_page_number: int | None = None
    current_lines: list[str] = []

    for line in markdown_text.splitlines():
        match = re.match(r"^## Page (\d+)", line)
        if match:
            if current_page_number is not None:
                page_text = normalize_text("\n".join(current_lines))
                pages.append(
                    {
                        "page_number": current_page_number,
                        "text": page_text,
                        "char_count": len(page_text),
                    }
                )
            current_page_number = int(match.group(1))
            current_lines = []
            continue
        if current_page_number is not None:
            current_lines.append(line)

    if current_page_number is not None:
        page_text = normalize_text("\n".join(current_lines))
        pages.append(
            {
                "page_number": current_page_number,
                "text": page_text,
                "char_count": len(page_text),
            }
        )

    return pages


def parse_html_markdown(markdown_text: str) -> list[dict]:
    sections: list[dict] = []
    heading_stack: list[tuple[int, str]] = []
    current_lines: list[str] = []
    seen_first_heading = False

    def flush_section() -> None:
        section_text = normalize_text("\n".join(current_lines))
        if section_text:
            sections.append(
                {
                    "section_path": [heading for _, heading in heading_stack] or ["Document"],
                    "text": section_text,
                    "char_count": len(section_text),
                }
            )

    for line in markdown_text.splitlines():
        if line.startswith("#"):
            if seen_first_heading:
                flush_section()
                current_lines.clear()
            seen_first_heading = True
            level = len(line) - len(line.lstrip("#"))
            heading = line[level:].strip()
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, heading))
        elif seen_first_heading:
            if line.startswith("- Original file:") or line.startswith("- Source URL:") or line.startswith("- Converted from:"):
                continue
            current_lines.append(line)

    if seen_first_heading:
        flush_section()

    return sections


def looks_like_table_block(block: str) -> bool:
    if not block.strip():
        return False
    if re.search(r"\b[Tt]abel\b", block):
        return True
    if "Jaartal" in block:
        return True
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    digit_lines = sum(1 for line in lines if re.search(r"\d", line))
    short_lines = sum(1 for line in lines if len(line) <= 80)
    return len(lines) >= 4 and digit_lines >= 3 and short_lines >= 3


def is_table_anchor(block: str) -> bool:
    lowered = block.lower()
    return "jaartal" in lowered or bool(re.search(r"\b[tT]abel\b", block))


def is_table_continuation(block: str) -> bool:
    if looks_like_table_block(block):
        return True
    if len(block) <= 80 and not block.rstrip().endswith((".", ":", ";")):
        return True
    if len(block) <= 120 and re.search(r"\d", block):
        return True
    return False


def collect_table_candidates(blocks: list[str]) -> list[str]:
    tables: list[str] = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if is_table_anchor(block) or looks_like_table_block(block):
            collected = [block]
            j = i + 1
            while j < len(blocks) and is_table_continuation(blocks[j]):
                collected.append(blocks[j])
                j += 1
            merged = "\n\n".join(item.strip() for item in collected if item.strip())
            if merged:
                tables.append(merged)
            i = j
        else:
            i += 1
    return tables


def guess_table_type(raw_table: str) -> str:
    lowered = raw_table.lower()
    if any(token in lowered for token in ("financ", "budget", "middelen", "besparing", "kosten")):
        return "financial"
    if any(token in lowered for token in ("monitor", "indicator", "voortgang", "evaluatie")):
        return "monitoring"
    if any(token in lowered for token in ("gemeente", "regio", "samenwerking", "governance")):
        return "governance"
    return "unknown"


def extract_table_label(raw_table: str) -> str | None:
    match = re.search(r"\b(Tabel(?:\s+[A-Z]?\d+(?:\.\d+)?)?)\b", raw_table, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def build_pdf_outputs(entry: dict, markdown_path: Path, markdown_text: str) -> tuple[dict, list[dict], list[dict]]:
    pages = parse_pdf_markdown(markdown_text)
    text_payload = {
        "document_id": entry["document_id"],
        "source_file_path": entry["file_path"],
        "source_markdown_path": markdown_path.relative_to(REPO_ROOT).as_posix(),
        "source_format": "pdf",
        "extraction_method": "markdown_pdf_v1",
        "page_count": len(pages),
        "pages": pages,
    }

    chunks: list[dict] = []
    chunk_index = 1
    for page in pages:
        for piece in split_long_text(page["text"]):
            section_path = [f"Page {page['page_number']}"]
            chunks.append(
                {
                    "document_id": entry["document_id"],
                    "chunk_id": f"{entry['document_id']}_chunk_{chunk_index:04d}",
                    "page_start": page["page_number"],
                    "page_end": page["page_number"],
                    "section_heading": section_path[-1],
                    "section_path": section_path,
                    "text": piece,
                    "char_count": len(piece),
                }
            )
            chunk_index += 1

    tables: list[dict] = []
    table_index = 1
    for page in pages:
        blocks = [block.strip() for block in re.split(r"\n\s*\n", page["text"]) if block.strip()]
        for block in collect_table_candidates(blocks):
                section_path = [f"Page {page['page_number']}"]
                tables.append(
                    {
                        "document_id": entry["document_id"],
                        "table_id": f"{entry['document_id']}_table_{table_index:03d}",
                        "page": page["page_number"],
                        "section_path": section_path,
                        "table_label": extract_table_label(block),
                        "raw_table": block,
                        "table_type_guess": guess_table_type(block),
                    }
                )
                table_index += 1

    return text_payload, chunks, tables


def build_html_outputs(entry: dict, markdown_path: Path, markdown_text: str) -> tuple[dict, list[dict], list[dict]]:
    sections = parse_html_markdown(markdown_text)
    text_payload = {
        "document_id": entry["document_id"],
        "source_file_path": entry["file_path"],
        "source_markdown_path": markdown_path.relative_to(REPO_ROOT).as_posix(),
        "source_format": "html",
        "extraction_method": "markdown_html_v1",
        "section_count": len(sections),
        "sections": sections,
    }

    chunks: list[dict] = []
    chunk_index = 1
    for section in sections:
        for piece in split_long_text(section["text"]):
            chunks.append(
                {
                    "document_id": entry["document_id"],
                    "chunk_id": f"{entry['document_id']}_chunk_{chunk_index:04d}",
                    "page_start": None,
                    "page_end": None,
                    "section_heading": section["section_path"][-1],
                    "section_path": section["section_path"],
                    "text": piece,
                    "char_count": len(piece),
                }
            )
            chunk_index += 1

    tables: list[dict] = []
    table_index = 1
    for section in sections:
        blocks = [block.strip() for block in re.split(r"\n\s*\n", section["text"]) if block.strip()]
        for block in collect_table_candidates(blocks):
                tables.append(
                    {
                        "document_id": entry["document_id"],
                        "table_id": f"{entry['document_id']}_table_{table_index:03d}",
                        "page": None,
                        "section_path": section["section_path"],
                        "table_label": extract_table_label(block),
                        "raw_table": block,
                        "table_type_guess": guess_table_type(block),
                    }
                )
                table_index += 1

    return text_payload, chunks, tables


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    manifest = load_manifest()

    for entry in manifest:
        markdown_path = locate_markdown_source(entry)
        markdown_text = markdown_path.read_text(encoding="utf-8", errors="ignore")
        source_format = Path(entry["file_path"]).suffix.lower()

        if source_format == ".pdf":
            text_payload, chunks, tables = build_pdf_outputs(entry, markdown_path, markdown_text)
        else:
            text_payload, chunks, tables = build_html_outputs(entry, markdown_path, markdown_text)

        write_json(TEXT_DIR / f"{entry['document_id']}.json", text_payload)
        write_json(CHUNKS_DIR / f"{entry['document_id']}.json", chunks)
        write_json(TABLES_DIR / f"{entry['document_id']}.json", tables)

    print(f"Wrote structural extraction files for {len(manifest)} documents")


if __name__ == "__main__":
    main()
