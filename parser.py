import re
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from utils import normalize_title, parent_of, level_of
import pdfplumber
from PIL import Image
import pytesseract


@dataclass
class TOCEntry:
    doc_title: str
    section_id: str
    title: str
    page: int
    level: int
    parent_id: Optional[str]
    full_path: str
    tags: List[str] = field(default_factory=list)


@dataclass
class SectionEntry:
    doc_title: str
    section_id: str
    title: str
    page: int
    level: int
    parent_id: Optional[str]
    full_path: str
    tags: List[str] = field(default_factory=list)


class TOCParser:
    def __init__(self, pdf_path: str, doc_title: str = "USB PD Specification"):
        self.pdf_path = pdf_path
        self.doc_title = doc_title
        self.toc_start_page: Optional[int] = None
        self.toc_end_page: Optional[int] = None
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    def detect_toc_range(self) -> None:
        toc_start, toc_end = None, None
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                logging.info(f" Checking page {i+1}/{total_pages} for TOC...")
                text = page.extract_text() or ""
                if toc_start is None and re.search(r"Table of Contents", text,
                                                   re.IGNORECASE):
                    toc_start = i
                    continue
                if toc_start is not None and toc_end is None:
                    if re.search(r"List of (Tables|Figures)", text, re.IGNORECASE):
                        toc_end = i - 1
                        break
            if toc_start is None:
                raise ValueError("TOC start not found")
            if toc_end is None:
                toc_end = min(toc_start + 6, total_pages - 1)
        self.toc_start_page, self.toc_end_page = toc_start, toc_end

    def extract_toc(self) -> List[TOCEntry]:
        if self.toc_start_page is None:
            self.detect_toc_range()
        toc_entries: List[TOCEntry] = []
        pattern = re.compile(r"^\s*(\d+(?:\.\d+)*)\s+(.+?)\s+"
                             r"(?:\.{2,}\s*)?(\d+)$")
        with pdfplumber.open(self.pdf_path) as pdf:
            for i in range(self.toc_start_page, self.toc_end_page + 1):
                logging.info(f"Processing TOC page {i+1}/{len(pdf.pages)}...")
                text = pdf.pages[i].extract_text() or ""
                for line in text.split("\n"):
                    m = pattern.match(line.strip())
                    if m:
                        sid, title, page = m.groups()
                        toc_entries.append(TOCEntry(
                            doc_title=self.doc_title,
                            section_id=sid,
                            title=normalize_title(title),
                            page=int(page),
                            level=level_of(sid),
                            parent_id=parent_of(sid),
                            full_path=f"{sid} {normalize_title(title)}"
                        ))
        return toc_entries


class SectionParser:
    def __init__(self, pdf_path: str, doc_title: str = "USB PD Specification"):
        self.pdf_path = pdf_path
        self.doc_title = doc_title
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    def extract_sections(self, toc_ids: List[str], toc_start: int,
                         toc_end: int) -> List[SectionEntry]:
        pattern = re.compile(r"^(\d+(?:\.\d+)*)\s+([A-Za-z].+)$")
        caption_noise = re.compile(r"^(Table|Figure)\s+\d", re.IGNORECASE)
        sections: List[SectionEntry] = []
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                if toc_start <= i <= toc_end:
                    continue
                logging.info(f"Processing body page {i+1}/{total_pages}...")
                text = page.extract_text() or ""
                for line in text.split("\n"):
                    line = line.strip()
                    if caption_noise.match(line):
                        continue
                    m = pattern.match(line)
                    if m:
                        sid, title = m.groups()
                        if sid not in toc_ids:
                            continue
                        sections.append(SectionEntry(
                            doc_title=self.doc_title,
                            section_id=sid,
                            title=normalize_title(title),
                            page=i + 1,
                            level=level_of(sid),
                            parent_id=parent_of(sid),
                            full_path=f"{sid} {normalize_title(title)}"
                        ))
        return sections


def count_tables_figures(pdf_path: str, toc_start: int, toc_end: int) -> Dict[str, int]:
    tables, figures = 0, 0
    table_pattern = re.compile(r"^Table\s+\d+\.\d+\s+.+", re.IGNORECASE)
    figure_pattern = re.compile(r"\b(Figure)\s+(\d+[\-\.]?\d*)", re.IGNORECASE)

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            if toc_start <= i <= toc_end:
                continue
            logging.info(f"Scanning page {i+1}/{total_pages} for tables/figures...")
            text = page.extract_text() or ""
            if not text.strip():
                logging.info(f"   Page {i+1}: using OCR fallback...")
                im = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(im)

            for line in text.split("\n"):
                line = " ".join(line.split())
                if table_pattern.match(line):
                    tables += 1
                elif figure_pattern.search(line):
                    figures += 1

            grid_tables = page.extract_tables()
            if grid_tables:
                for g in grid_tables:
                    if len(g) >= 3:
                        tables += 1

    logging.info(f"Tables found: {tables} | Figures found: {figures}")
    return {"tables_in_body": tables, "figures_in_body": figures}
