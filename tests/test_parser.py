import unittest
from parser import TOCParser, SectionParser, count_tables_figures

PDF_PATH = "USB_PD_R3_2 V1.1 2024-10.pdf"
DOC_TITLE = "USB PD Specification Rev X"


class TestParser(unittest.TestCase):
    def test_toc_extraction(self):
        toc_parser = TOCParser(PDF_PATH, DOC_TITLE)
        toc_data = [entry.__dict__ for entry in toc_parser.extract_toc()]
        self.assertTrue(len(toc_data) > 0, "TOC should have entries")
        first = toc_data[0]
        self.assertIn("section_id", first)
        self.assertIn("title", first)
        self.assertIn("page", first)

    def test_section_extraction(self):
        toc_parser = TOCParser(PDF_PATH, DOC_TITLE)
        toc_data = [entry.__dict__ for entry in toc_parser.extract_toc()]
        section_parser = SectionParser(PDF_PATH, DOC_TITLE)
        spec_data = [entry.__dict__ for entry in section_parser.extract_sections(
            [entry["section_id"] for entry in toc_data],
            toc_parser.toc_start_page,
            toc_parser.toc_end_page
        )]
        self.assertTrue(len(spec_data) > 0, "Spec should have entries")

    def test_count_tables_figures(self):
        toc_parser = TOCParser(PDF_PATH, DOC_TITLE)
        toc_parser.detect_toc_range()
        counts = count_tables_figures(PDF_PATH, toc_parser.toc_start_page, toc_parser.toc_end_page)
        self.assertIn("tables_in_body", counts)
        self.assertIn("figures_in_body", counts)
        self.assertGreaterEqual(counts["tables_in_body"], 0)
        self.assertGreaterEqual(counts["figures_in_body"], 0)
