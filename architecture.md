# 🧩 System Architecture Diagram

This diagram illustrates the complete workflow of the **USB PD TOC & Specification Parser** project, from input PDF to output data.

---

### ⚙️ Overview
The system processes the USB Power Delivery (PD) Specification PDF, extracts the Table of Contents and document sections, validates their alignment, and outputs structured JSONL and Excel reports.

---

### 🧠 Architecture Flow
**Hardware**
- **Computer / System**
  - **Input:** USB PD Specification PDF  
  - **Output:** Processed Data (JSONL + Excel)

**Software**
- **pdfplumber / pytesseract**
  - **Input:** PDF file  
  - **Output:** Extracted text + TOC + Sections  
- **Parser Module (parser.py)**
  - **Input:** Extracted text  
  - **Output:** Parsed TOC and section data  
- **Utils Module (utils.py)**
  - **Input:** Parsed entries  
  - **Output:** JSONL formatted files  
- **Validator Module (validator.py)**
  - **Input:** TOC + Section JSONL files  
  - **Output:** Validation report (.xlsx)  

**Storage**
- `usb_pd_toc.jsonl`
- `usb_pd_spec.jsonl`
- `usb_pd_metadata.jsonl`
- `validation_report.xlsx`

---

### 🖼️ Diagram
<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/fdc0ea4e-2e05-4f3e-89e4-0315ccb6ee57" />

