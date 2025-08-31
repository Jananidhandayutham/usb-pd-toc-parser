# 📄 USB PD TOC & Specification Parser

This project extracts the Table of Contents (TOC) and Actual Sections from the USB Power Delivery Specification PDF, saves them in .jsonl format, generates a metadata file, and produces a Validation Report in .xlsx format comparing TOC entries with actual document sections.

It outputs:
- **usb_pd_toc.jsonl** → Parsed TOC entries  
- **usb_pd_spec.jsonl** → Extracted actual sections  
- **usb_pd_metadata.jsonl** → Metadata about the PDF and extraction  
- **validation_report.xlsx** → Comparison report between TOC and actual sections  

---

## 🚀 Features
✅ Automatically detects TOC start and end pages  
✅ Extracts section IDs, titles, page numbers, and hierarchy  
✅ Counts tables and figures in body pages  
✅ Generates metadata file for the PDF and extraction  
✅ Saves output in JSONL and Excel formats  
✅ Compares TOC entries with actual sections to validate:  
   - Title matches  
   - Page matches  
   - Overall match status  
✅ Refactored code using dataclasses for TOC and Section entries  
✅ Full object-oriented design for maintainability  
✅ Full unit tests for parser, utils, and validator modules  
✅ Enhanced logging for each step  
✅ Improved error handling and OCR fallback for scanned pages  
✅ Code readability improvements, line lengths ≤88 chars for linting  

---

## 🛠️ Requirements
Install the dependencies:
```bash
pip install pdfplumber pandas pillow pytesseract openpyxl
```

> **Note:** pytesseract requires Tesseract OCR installed on your system.

---

## 📂 Project Structure
```
project/
│── main.py                   # Main script
│── parser.py                 # TOC & Section extraction logic
│── utils.py                  # Helper functions & JSONL writer
│── validator.py              # Validation logic & Excel report
│── tests/                    # Unit tests folder
│   ├── test_parser.py
│   ├── test_utils.py
│   └── test_validator.py
│── usb_pd_toc.jsonl           # Extracted TOC data
│── usb_pd_spec.jsonl          # Extracted actual sections
│── usb_pd_metadata.jsonl      # Metadata about extraction
│── validation_report.xlsx     # Validation comparison report
│── README.md                  # Project documentation
```

---

## ▶️ How to Run
Make sure the PDF file (e.g., `USB_PD_R3_2 V1.1 2024-10.pdf`) is in the same directory as `main.py`, then execute:

```bash
python main.py
```

---

## ▶️ How to Run Tests
To run all unit tests with detailed output:

```bash
python -m unittest discover -s tests -v
```

This will run tests for:
- Parser (`test_parser.py`)
- Utils (`test_utils.py`)
- Validator (`test_validator.py`)

**Sample output:**
```
test_normalize_title (test_utils.TestUtils) ... ok
test_parent_of (test_utils.TestUtils) ... ok
test_section_extraction (test_parser.TestParser) ... ok
...
----------------------------------------------------------------------
Ran 7 tests in 20.123s

OK
```

✅ Confirms that all tests passed successfully.

---

## 📊 Output Files

### `usb_pd_toc.jsonl` – Contains structured TOC entries
```json
{
  "doc_title": "USB PD Sample Document",
  "section_id": "1.1",
  "title": "Overview",
  "page": 34,
  "level": 2,
  "parent_id": "1",
  "full_path": "1.1 Overview",
  "tags": []
}
```

### `usb_pd_spec.jsonl` – Contains actual sections found in the PDF
```json
{
  "doc_title": "USB PD Sample Document",
  "section_id": "1.1",
  "title": "Overview",
  "page": 34,
  "level": 2,
  "parent_id": "1",
  "full_path": "1.1 Overview",
  "tags": []
}
```

### `usb_pd_metadata.jsonl` – Contains PDF metadata and extraction info
```json
{
  "doc_title": "USB PD Sample Document",
  "pdf_path": "USB_PD_R3_2 V1.1 2024-10.pdf",
  "total_pages": 1014,
  "toc_start": 12,
  "toc_end": 18,
  "tables_in_body": 35,
  "figures_in_body": 28
}
```

### `validation_report.xlsx` – Excel report comparing TOC with actual sections
| section_id | title_toc     | title_spec    | page_toc | page_spec | found_in_spec | match_title | match_page | match_overall |
|------------|---------------|---------------|----------|-----------|---------------|-------------|------------|---------------|
| 1          | Introduction  | Introduction  | 34       | 34        | True          | True        | True       | True          |
| 2.1        | Overview      | Overview      | 53       | 53        | True          | True        | True       | True          |
| 2.5.3      | Cable Plugs   | Cable Plugs   | 65       | 65        | True          | True        | True       | True          |

---

## 📌 Notes
- The project uses OCR fallback for pages where text cannot be directly extracted.  
- All JSONL outputs are structured for further automation or analysis.  
- Content coverage validation ensures that TOC sections match extracted sections.  
- Unit tests ensure the reliability of parser, utils, and validator modules.  
