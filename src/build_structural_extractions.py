from __future__ import annotations

import json
import re
from html import unescape
from html.parser import HTMLParser
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "manifest.json"
TEXT_DIR = REPO_ROOT / "data" / "intermediate" / "text"
CHUNKS_DIR = REPO_ROOT / "data" / "intermediate" / "chunks"
TABLES_DIR = REPO_ROOT / "data" / "intermediate" / "tables"
EXTRACTED_DIR = REPO_ROOT / "data" / "extracted"
LOG_DIR = REPO_ROOT / "data" / "logs"
VOTING_RECORDS_PATH = EXTRACTED_DIR / "voting_records.json"
TEXT_CLEANUP_LOG_PATH = LOG_DIR / "phase26_text_cleanup.json"
MARKDOWN_DIRECTORIES = [
    REPO_ROOT / "data" / "intermediate" / "source_markdown",
    REPO_ROOT / "sources markdown canonical",
    REPO_ROOT / "sources markdown",
    REPO_ROOT / "sources markdown context",
]

MOJIBAKE_REPLACEMENTS = {
    "\x07": "",
    "â€œ": "“",
    "â€": "”",
    "â€˜": "‘",
    "â€™": "’",
    "â€“": "–",
    "â€”": "—",
    "â€¦": "…",
    "â€¢": "•",
    "Ã©": "é",
    "Ã«": "ë",
    "Ã¨": "è",
    "Ã¡": "á",
    "Ã ": "à",
    "Ã¶": "ö",
    "Ã¼": "ü",
}

TOC_LINE_PATTERN = re.compile(r"^\d+(?:\.\d+)+\s+[A-ZÀ-Ö][^.]{4,}\s+\d{1,3}$")
DRUPAL_ARTICLE_LINK_PATTERN = re.compile(r"^\[######|\]\(/article/")
VOTING_RESULT_PATTERN = re.compile(
    r"\b(?:motie|amendement)\b.{0,160}\b(?:is\s+)?met\s+\d+\s+stemmen",
    re.IGNORECASE,
)
WETTEN_ACTION_TEXTS = {
    "toon relaties in lido",
    "maak een permanente link",
    "toon wetstechnische informatie",
    "vergelijk met andere versie tekst regeling",
    "druk de regeling af",
    "sla de regeling op",
    "druk het regelingonderdeel af",
    "sla het regelingonderdeel op",
}


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def source_file_path(entry: dict) -> Path:
    return REPO_ROOT / entry["file_path"]


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


def locate_structural_source(entry: dict) -> tuple[str, Path]:
    source_path = source_file_path(entry)
    source_format = source_path.suffix.lower()

    if source_format == ".pdf":
        return "markdown_pdf", locate_markdown_source(entry)

    try:
        return "markdown_html", locate_markdown_source(entry)
    except FileNotFoundError:
        if source_format == ".html" and source_path.exists():
            return "raw_html", source_path
        raise


def clean_lines(lines: list[str]) -> list[str]:
    cleaned = [line.rstrip() for line in lines]
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return cleaned


def repair_mojibake(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    repaired = text
    for bad, good in MOJIBAKE_REPLACEMENTS.items():
        count = repaired.count(bad)
        if count:
            counts[repr(bad)] = count
            repaired = repaired.replace(bad, good)
    return repaired, counts


def is_toc_line(line: str) -> bool:
    return bool(TOC_LINE_PATTERN.fullmatch(normalize_inline_text(line)))


def is_drupal_article_link(line: str) -> bool:
    return bool(DRUPAL_ARTICLE_LINK_PATTERN.search(line.strip()))


def is_voting_result_text(text: str) -> bool:
    return bool(VOTING_RESULT_PATTERN.search(normalize_inline_text(text)))


def is_structural_noise_line(line: str) -> bool:
    return is_toc_line(line) or is_drupal_article_link(line) or is_voting_result_text(line)


def is_wetten_action_text(text: str) -> bool:
    normalized = normalize_inline_text(text).lower().strip(" -")
    return normalized in WETTEN_ACTION_TEXTS


def voting_records_from_text(entry: dict, text: str) -> list[dict]:
    records = []
    seen: set[str] = set()
    for line in text.splitlines():
        cleaned = normalize_inline_text(line)
        if not cleaned or cleaned in seen:
            continue
        if not is_voting_result_text(cleaned):
            continue
        seen.add(cleaned)
        records.append(
            {
                "document_id": entry["document_id"],
                "source_file_path": entry["file_path"],
                "source_url": entry.get("source_url"),
                "record_text": cleaned,
                "record_type": "voting_result",
            }
        )
    return records


def normalize_text(text: str) -> str:
    lines = clean_lines(text.splitlines())
    return "\n".join(lines).strip()


def normalize_inline_text(text: str) -> str:
    text = unescape(text).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


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
        if current_page_number is not None and not is_structural_noise_line(line):
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

    def should_skip_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if line.startswith("- Original file:") or line.startswith("- Source URL:") or line.startswith("- Converted from:"):
            return True
        if is_structural_noise_line(line):
            return True
        if stripped.startswith(("Laatst bewerkt op:", "###### Pagina delen:", "###### Tags:")):
            return True
        if "Ga terug naar de overzichtspagina" in stripped:
            return True
        if "Ga direct naar het overzicht van de beleidsterreinen" in stripped:
            return True
        if "Scroll naar beneden voor een overzicht van de informatiepagina's" in stripped:
            return True
        if stripped in {"---", "â–¼", "▼"}:
            return True
        if "searchbytag?search=" in stripped:
            return True
        return False

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
            if should_skip_line(line):
                continue
            current_lines.append(line)

    if seen_first_heading:
        flush_section()

    return sections


def title_from_html(html_text: str) -> str | None:
    match = re.search(r"<title>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return normalize_inline_text(match.group(1))


def should_skip_html_block(text: str) -> bool:
    stripped = normalize_inline_text(text)
    if not stripped:
        return True
    if stripped in {"...", "- ..."}:
        return True
    if is_wetten_action_text(stripped):
        return True
    if stripped.startswith("- ") and stripped.count("- ") >= 3 and not any(token in stripped for token in (".", ":", ";")):
        return True
    if is_structural_noise_line(stripped):
        return True
    if stripped.startswith(("Laatst bewerkt op:", "Pagina delen", "Tags:")):
        return True
    if "Ga terug naar de overzichtspagina" in stripped:
        return True
    if "Ga direct naar het overzicht van de beleidsterreinen" in stripped:
        return True
    if "Scroll naar beneden voor een overzicht van de informatiepagina's" in stripped:
        return True
    if stripped in {"Menu", "Zoek opnieuw", "Documenten zoeken", "Lees voor"}:
        return True
    return False


class RawHTMLSectionParser(HTMLParser):
    SKIP_TAGS = {"script", "style", "noscript", "svg"}
    BLOCK_TAGS = {"p", "li", "dd", "dt", "blockquote", "summary"}
    NON_SUBSTANTIVE_HEADINGS = {
        "menu",
        "service",
        "over deze site",
        "deel deze pagina",
        "hoort bij",
        "primaire navigatie",
        "berichten over uw buurt",
        "dienstverlening",
        "beleid regelgeving",
        "contactgegevens overheden",
        "alle onderwerpen",
        "zie ook",
        "contact met de gemeente",
        "bezoekadres",
        "postadres",
        "volg ons",
        "inhoudsopgave",
    }

    def __init__(self, document_title: str | None) -> None:
        super().__init__(convert_charrefs=False)
        self.document_title = document_title
        self.sections: list[dict] = []
        self.heading_stack: list[tuple[int, str]] = []
        self.current_lines: list[str] = []
        self.skip_depth = 0
        self.heading_level: int | None = None
        self.heading_buffer: list[str] = []
        self.block_tag: str | None = None
        self.block_prefix = ""
        self.block_buffer: list[str] = []

    def current_section_path(self) -> list[str]:
        if self.heading_stack:
            return [heading for _, heading in self.heading_stack]
        if self.document_title:
            return [self.document_title]
        return ["Document"]

    def flush_section(self) -> None:
        if self.heading_stack and self.heading_stack[-1][1].strip().lower() in self.NON_SUBSTANTIVE_HEADINGS:
            self.current_lines = []
            return
        section_text = normalize_text("\n".join(self.current_lines))
        if section_text:
            self.sections.append(
                {
                    "section_path": self.current_section_path(),
                    "text": section_text,
                    "char_count": len(section_text),
                }
            )
        self.current_lines = []

    def append_block(self, text: str) -> None:
        cleaned = normalize_inline_text(text)
        if should_skip_html_block(cleaned):
            return
        if self.block_prefix:
            cleaned = f"{self.block_prefix}{cleaned}"
        self.current_lines.append(cleaned)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lower_tag = tag.lower()
        if lower_tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if re.fullmatch(r"h[1-6]", lower_tag):
            self.flush_section()
            self.heading_level = int(lower_tag[1])
            self.heading_buffer = []
            return
        if lower_tag in self.BLOCK_TAGS:
            self.block_tag = lower_tag
            self.block_prefix = "- " if lower_tag == "li" else ""
            self.block_buffer = []
            return
        if lower_tag == "br":
            if self.heading_level is not None:
                self.heading_buffer.append("\n")
            elif self.block_tag is not None:
                self.block_buffer.append("\n")

    def handle_endtag(self, tag: str) -> None:
        lower_tag = tag.lower()
        if lower_tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if self.heading_level is not None and lower_tag == f"h{self.heading_level}":
            heading = normalize_inline_text("".join(self.heading_buffer))
            if heading:
                while self.heading_stack and self.heading_stack[-1][0] >= self.heading_level:
                    self.heading_stack.pop()
                self.heading_stack.append((self.heading_level, heading))
            self.heading_level = None
            self.heading_buffer = []
            return
        if self.block_tag is not None and lower_tag == self.block_tag:
            self.append_block("".join(self.block_buffer))
            self.block_tag = None
            self.block_prefix = ""
            self.block_buffer = []

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.heading_level is not None:
            self.heading_buffer.append(data)
        elif self.block_tag is not None:
            self.block_buffer.append(data)

    def close(self) -> list[dict]:
        super().close()
        self.flush_section()
        return self.sections


def parse_raw_html(html_text: str, document_title: str | None) -> list[dict]:
    parser = RawHTMLSectionParser(document_title or title_from_html(html_text))
    parser.feed(html_text)
    return parser.close()


def strip_html_tags(html_fragment: str) -> str:
    text = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html_fragment)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return normalize_text(text)


def parse_raw_html_tables(html_text: str, document_title: str | None) -> list[dict]:
    tables: list[dict] = []
    section_path = [document_title or title_from_html(html_text) or "Document"]
    for table_html in re.findall(r"(?is)<table[^>]*>(.*?)</table>", html_text):
        rows = []
        for row_html in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", table_html):
            cells = [
                normalize_inline_text(strip_html_tags(cell_html))
                for cell_html in re.findall(r"(?is)<t[hd][^>]*>(.*?)</t[hd]>", row_html)
            ]
            cells = [cell for cell in cells if cell]
            if cells:
                rows.append(" | ".join(cells))
        raw_table = normalize_text("\n".join(rows))
        if raw_table:
            tables.append(
                {
                    "section_path": section_path,
                    "raw_table": raw_table,
                }
            )
    return tables


def is_structural_heading_block(block: str) -> bool:
    stripped = block.strip()
    if not stripped:
        return True
    if stripped in {"Inhoud", "Woordenlijst", "Voorwoord"}:
        return True
    if re.fullmatch(r"H\d+\s+.+", stripped):
        return True
    if re.fullmatch(r"\d+\s+\|\s+.+", stripped):
        return True
    return False


def looks_like_bullet_list(block: str) -> bool:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if len(lines) < 3:
        return False
    bullet_lines = sum(1 for line in lines if re.match(r"^[-*•]\s+", line))
    return bullet_lines >= 3 and bullet_lines >= max(3, len(lines) // 2)


def looks_like_numeric_series_block(block: str) -> bool:
    if is_structural_heading_block(block) or looks_like_bullet_list(block):
        return False

    compact = " ".join(line.strip() for line in block.splitlines() if line.strip())
    year_tokens = len(re.findall(r"\b(?:19|20)\s?\d{2}\b", compact))
    percent_tokens = len(re.findall(r"\b\d+(?:[.,]\d+)?\s*%\b", compact))
    number_tokens = len(re.findall(r"\b\d+(?:[.,]\d+)?\b", compact))
    all_caps_tokens = len(re.findall(r"\b[A-Z][A-Z0-9+&/\-]{2,}\b", compact))

    if year_tokens >= 2 and number_tokens >= 4:
        return True
    if percent_tokens >= 2:
        return True
    if len(compact) <= 80 and number_tokens >= 4:
        return True
    if len(compact) <= 90 and all_caps_tokens >= 2 and number_tokens >= 2:
        return True
    return False


def looks_like_table_block(block: str) -> bool:
    if not block.strip():
        return False
    if is_structural_heading_block(block):
        return False
    if looks_like_bullet_list(block):
        return False
    if re.search(r"\b[Tt]abel\b", block):
        return True
    if "Jaartal" in block:
        return True
    if looks_like_numeric_series_block(block):
        return True
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    digit_lines = sum(1 for line in lines if re.search(r"\d", line))
    short_lines = sum(1 for line in lines if len(line) <= 80)
    return len(lines) >= 4 and digit_lines >= 3 and short_lines >= 3


def is_table_anchor(block: str) -> bool:
    lowered = block.lower()
    return "jaartal" in lowered or bool(re.search(r"\b[tT]abel\b", block)) or looks_like_numeric_series_block(block)


def is_table_continuation(block: str) -> bool:
    if is_structural_heading_block(block):
        return False
    if looks_like_bullet_list(block):
        return False
    if looks_like_table_block(block):
        return True
    if len(block) <= 80 and re.fullmatch(r"[A-Z0-9 +%&/\-.,()]+", block.strip()):
        return True
    if len(block) <= 80 and not block.rstrip().endswith((".", ":", ";")) and re.search(r"[\d%]", block):
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


def build_html_outputs(entry: dict, source_path: Path, source_text: str, source_kind: str) -> tuple[dict, list[dict], list[dict]]:
    if source_kind == "raw_html":
        sections = parse_raw_html(source_text, entry.get("title"))
        extracted_tables = parse_raw_html_tables(source_text, entry.get("title"))
        extraction_method = "raw_html_v1"
        source_markdown_path = None
    else:
        sections = parse_html_markdown(source_text)
        extracted_tables = []
        extraction_method = "markdown_html_v1"
        source_markdown_path = source_path.relative_to(REPO_ROOT).as_posix()

    text_payload = {
        "document_id": entry["document_id"],
        "source_file_path": entry["file_path"],
        "source_markdown_path": source_markdown_path,
        "source_content_path": source_path.relative_to(REPO_ROOT).as_posix(),
        "source_format": "html",
        "extraction_method": extraction_method,
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

    seen_tables = {table["raw_table"] for table in tables}
    for extracted_table in extracted_tables:
        if extracted_table["raw_table"] in seen_tables:
            continue
        tables.append(
            {
                "document_id": entry["document_id"],
                "table_id": f"{entry['document_id']}_table_{table_index:03d}",
                "page": None,
                "section_path": extracted_table["section_path"],
                "table_label": extract_table_label(extracted_table["raw_table"]),
                "raw_table": extracted_table["raw_table"],
                "table_type_guess": guess_table_type(extracted_table["raw_table"]),
            }
        )
        table_index += 1

    return text_payload, chunks, tables


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    manifest = load_manifest()
    cleanup_log = {
        "run_id": "phase26_text_cleanup_v1",
        "generated_on": date.today().isoformat(),
        "documents": [],
    }
    voting_records: list[dict] = []

    for entry in manifest:
        source_kind, source_path = locate_structural_source(entry)
        source_text = source_path.read_text(encoding="utf-8", errors="ignore")
        source_text, mojibake_counts = repair_mojibake(source_text)
        records = voting_records_from_text(entry, source_text)
        voting_records.extend(records)
        source_format = source_file_path(entry).suffix.lower()

        if source_format == ".pdf":
            text_payload, chunks, tables = build_pdf_outputs(entry, source_path, source_text)
        else:
            text_payload, chunks, tables = build_html_outputs(entry, source_path, source_text, source_kind)

        write_json(TEXT_DIR / f"{entry['document_id']}.json", text_payload)
        write_json(CHUNKS_DIR / f"{entry['document_id']}.json", chunks)
        write_json(TABLES_DIR / f"{entry['document_id']}.json", tables)
        if mojibake_counts or records:
            cleanup_log["documents"].append(
                {
                    "document_id": entry["document_id"],
                    "mojibake_replacements": mojibake_counts,
                    "voting_record_count": len(records),
                }
            )

    write_json(
        VOTING_RECORDS_PATH,
        {
            "run_id": "phase26_voting_records_v1",
            "generated_on": date.today().isoformat(),
            "record_count": len(voting_records),
            "records": voting_records,
        },
    )
    write_json(TEXT_CLEANUP_LOG_PATH, cleanup_log)
    print(f"Wrote structural extraction files for {len(manifest)} documents")
    print(f"Wrote {len(voting_records)} voting record(s)")


if __name__ == "__main__":
    main()
