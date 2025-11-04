# 🔍 Data Flow Diagram (DFD)

This diagram represents the flow of data through each stage of the **USB PD TOC & Specification Parser** project.

---

### 🔄 Workflow
1. **USB PD Specification PDF**  
   → Extracts text, TOC, and sections  

2. **PDF Text Extractor (pdfplumber / pytesseract)**  
   → Parses and structures TOC & section data  

3. **Parser Module (parser.py)**  
   → Formats and structures parsed data  

4. **Utils Module (utils.py)**  
   → Saves parsed data as JSONL files  

5. **Validator Module (validator.py)**  
   → Compares TOC & section data  
   → Generates validation report  

---

### 📊 Outputs
- `usb_pd_toc.jsonl`  
- `usb_pd_spec.jsonl`  
- `usb_pd_metadata.jsonl`  
- `validation_report.xlsx`  

---

### 🖼️ Diagram
Data Flow Diagram
<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/40759d6f-8b87-4e65-a9de-f7623fd09426" />

