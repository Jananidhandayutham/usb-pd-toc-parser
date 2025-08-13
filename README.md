# 📄 USB PD TOC & Specification Parser

This project extracts the Table of Contents (TOC) and Actual Sections from the USB Power Delivery Specification PDF, saves them in .jsonl format, and generates a Validation Report in .xlsx format comparing TOC entries with actual document sections.

It outputs:
- **usb_pd_toc.jsonl** → Parsed TOC entries  
- **usb_pd_spec.jsonl** → Extracted actual sections  
- **validation_report.xlsx** → Comparison report between TOC and actual sections  

---

## 🚀 Features
✅ Automatically detects TOC start and end pages  
✅ Extracts section IDs, titles, page numbers, and hierarchy  
✅ Saves output in JSONL and Excel formats  
✅ Compares TOC entries with actual sections to validate:  
   - Title matches  
   - Page matches  
   - Overall match status  


---

## 🛠️ Requirements
Install the dependencies:
```bash
pip install pdfplumber pandas
```

---

## 📂 Project Structure
```
project/
│── main.py                  # Main script
│── usb_pd_toc.jsonl          # Extracted TOC data
│── usb_pd_spec.jsonl         # Extracted actual sections
│── validation_report.xlsx    # Validation comparison report
│── README.md                 # Project documentation
```

---

## ▶️ How to Run
```bash
python main.py
```
Make sure the PDF file (e.g., `USB_PD_R3_2 V1.1 2024-10.pdf`) is in the same directory as `main.py`.

---

## 📊 Output Files
1. **usb_pd_toc.jsonl** – Contains structured TOC entries  
2. **usb_pd_spec.jsonl** – Contains actual sections found in the PDF  
3. **validation_report.xlsx** – Excel report comparing TOC with actual sections  

---

## 📌 Example Output (TOC Entry)
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

## 📊 Sample Output (Validation Report)
|  section_id |  title_toc   |  title_actual |  page_toc |  page_actual |  found_in_actual  |  match_title |  match_page |  match_overall |
| ----------- | ------------ | ------------- | --------- | ------------ | ----------------- | ------------ | ----------- | -------------- |
| 1           | Introduction | Introduction  | 34        | 34           | True              | True         | True        | True           |
| 2.1         | Overview     | Overview      | 53        | 53           | True              | True         | True        | True           |
| 2.5.3       | Cable Plugs  | Cable Plugs   | 65        | 65           | True              | True         | True        | True           |
