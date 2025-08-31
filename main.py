import json
import logging
from parser import TOCParser, SectionParser, count_tables_figures
from validator import Validator
from utils import Reporter

logging.basicConfig(level=logging.INFO, format="%(message)s")


def main() -> None:
    pdf_path = "USB_PD_R3_2 V1.1 2024-10.pdf"
    doc_title = "USB PD Specification Rev X"

    logging.info(" Step 1: Extracting TOC...")
    toc_parser = TOCParser(pdf_path, doc_title)
    toc_data = toc_parser.extract_toc()
    Reporter.write_jsonl("usb_pd_toc.jsonl", toc_data)
    logging.info(f" TOC extracted ({len(toc_data)} entries)")

    logging.info(" Step 2: Extracting spec sections...")
    section_parser = SectionParser(pdf_path, doc_title)
    spec_data = section_parser.extract_sections(
        [entry.section_id for entry in toc_data],
        toc_parser.toc_start_page,
        toc_parser.toc_end_page
    )
    Reporter.write_jsonl("usb_pd_spec.jsonl", spec_data)
    logging.info(f" Spec extracted ({len(spec_data)} entries)")

    logging.info(" Step 3: Counting tables & figures...")
    counts = count_tables_figures(pdf_path, toc_parser.toc_start_page,
                                  toc_parser.toc_end_page)
    logging.info(f" Tables: {counts['tables_in_body']} | Figures: "
                 f"{counts['figures_in_body']}")

    logging.info(" Step 4: Writing metadata...")
    metadata = {
        "doc_title": doc_title,
        "pdf_path": pdf_path,
        "total_pages": len(toc_data) + len(spec_data),
        "toc_start": toc_parser.toc_start_page,
        "toc_end": toc_parser.toc_end_page,
        **counts
    }
    with open("usb_pd_metadata.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps(metadata, ensure_ascii=False) + "\n")
    logging.info(" Metadata saved")

    logging.info(" Step 5: Validating and writing Excel report...")
    validator = Validator(toc_data, spec_data)
    validator.to_excel("validation_report.xlsx", counts)
    logging.info("\n Done! All outputs generated successfully.")


if __name__ == "__main__":
    main()
