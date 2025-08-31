# 📘 USB PD TOC & Specification Parser

This project extracts the **Table of Contents (TOC)** and **Actual Sections** from the USB Power Delivery Specification PDF, saves them in `.jsonl` format, and generates a **Validation Report** in `.xlsx` format comparing TOC entries with actual document sections.

---

## 🚀 Features
- ✅ Extracts section IDs, titles, page numbers, and hierarchy  
- ✅ Saves output in JSONL and Excel formats  
- ✅ Generates metadata file for the PDF and extraction  
- ✅ Compares TOC entries with actual sections to validate:
  - Title matches  
  - Page matches  
  - Overall match status  
- ✅ Refactored code using dataclasses for TOC and Section entries  
- ✅ Full object-oriented design for maintainability  
- ✅ Tables and Figures counting included for body pages  
- ✅ Full unit tests for parser, utils, and validator (`tests/` folder)  
- ✅ Enhanced logging for each step  
- ✅ Metadata generation in `usb_pd_metadata.jsonl`  
- ✅ Improved error handling and OCR fallback for scanned pages  
- ✅ Code readability improvements (line lengths < 88 chars for linting)  

---

## ⚙️ Requirements
Install dependencies:

```bash
pip install pdfplumber pandas pillow pytesseract openpyxl
