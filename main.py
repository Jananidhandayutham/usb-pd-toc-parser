import pdfplumber
import re
import json
import pandas as pd

pdf_path = "USB_PD_R3_2 V1.1 2024-10.pdf"


toc_start_page = None
toc_end_page = None

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue

        if toc_start_page is None and re.search(r"Table Of Contents", text, re.IGNORECASE):
            toc_start_page = i
            continue

        if toc_start_page is not None and re.search(r"List of Figures", text, re.IGNORECASE):
            toc_end_page = i
            break

if toc_start_page is None:
    raise ValueError("Could not find TOC start page")
if toc_end_page is None:
    toc_end_page = toc_start_page + 6

print(f" Detected TOC pages: {toc_start_page} to {toc_end_page}")


structured_data = []
toc_pattern = re.compile(r"^\s*(\d+(?:\.\d+)*?)\s+(.+?)\s+(?:\.+\s*)?(\d+)$")

with pdfplumber.open(pdf_path) as pdf:
    for i in range(toc_start_page, toc_end_page + 1):
        text = pdf.pages[i].extract_text()
        if not text:
            continue

        for line in text.split("\n"):
            line = line.strip()
            match = toc_pattern.match(line)
            if match:
                section_id = match.group(1)
                title = re.sub(r"\.{2,}", "", match.group(2)).strip()
                page_number = int(match.group(3))
                level = section_id.count(".") + 1
                parent_id = ".".join(section_id.split(".")[:-1]) if "." in section_id else None

                structured_data.append({
                    "doc_title": "USB PD Sample Document",
                    "section_id": section_id,
                    "title": title,
                    "page": page_number,
                    "level": level,
                    "parent_id": parent_id,
                    "full_path": f"{section_id} {title}",
                    "tags": []
                })

with open("usb_pd_toc.jsonl", "w", encoding="utf-8") as f:
    for entry in structured_data:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print(f" TOC JSONL saved to usb_pd_toc.jsonl")


toc_section_ids = {entry["section_id"] for entry in structured_data}
actual_sections = []
actual_pattern = re.compile(r"^(\d+(?:\.\d+)*?)\s+([A-Za-z].+)$")

with pdfplumber.open(pdf_path) as pdf:
    total_pages = len(pdf.pages)
    for i, page in enumerate(pdf.pages):
        if toc_start_page <= i <= toc_end_page:
            continue 

        print(f"Processing page {i+1} of {total_pages}...")

        text = page.extract_text()
        if not text:
            continue

        for line in text.split("\n"):
            line = line.strip()
            match = actual_pattern.match(line)
            if match:
                section_id = match.group(1)
                if section_id not in toc_section_ids:
                    continue  

                title = re.sub(r"\.{2,}", "", match.group(2)).strip()
                level = section_id.count(".") + 1
                parent_id = ".".join(section_id.split(".")[:-1]) if "." in section_id else None

                actual_sections.append({
                    "doc_title": "USB PD Sample Document",
                    "section_id": section_id,
                    "title": title,
                    "page": i + 1,
                    "level": level,
                    "parent_id": parent_id,
                    "full_path": f"{section_id} {title}",
                    "tags": []
                })

with open("usb_pd_spec.jsonl", "w", encoding="utf-8") as f:
    for entry in actual_sections:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print(f" Actual spec JSONL saved to usb_pd_spec.jsonl")


toc_df = pd.DataFrame(structured_data)
actual_df = pd.DataFrame(actual_sections)

rows = []
for _, toc_row in toc_df.iterrows():
    sid = toc_row["section_id"]
    title_toc = toc_row["title"]
    page_toc = toc_row["page"]

    match_row = actual_df[actual_df["section_id"] == sid]
    if not match_row.empty:
        title_actual = match_row.iloc[0]["title"]
        page_actual = match_row.iloc[0]["page"]
        found_in_actual = True
        match_title = title_toc.strip() == title_actual.strip()
        match_page = page_toc == page_actual
        match_overall = match_title and match_page
    else:
        title_actual = None
        page_actual = None
        found_in_actual = False
        match_title = False
        match_page = False
        match_overall = False

    rows.append({
        "section_id": sid,
        "title_toc": title_toc,
        "title_actual": title_actual,
        "page_toc": page_toc,
        "page_actual": page_actual,
        "found_in_actual": found_in_actual,
        "match_title": match_title,
        "match_page": match_page,
        "match_overall": match_overall
    })

final_df = pd.DataFrame(rows)
final_df.to_excel("validation_report.xlsx", index=False)
print("Validation report saved to validation_report.xlsx")
