import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")


class Validator:
    def __init__(self, toc: List[Dict], spec: List[Dict]):
        self.toc = toc
        self.spec = spec

    def compare(self) -> Dict[str, pd.DataFrame]:
        toc_df = pd.DataFrame(self.toc)
        spec_df = pd.DataFrame(self.spec)

        toc_df["title_norm"] = toc_df["title"].str.lower().str.strip()
        spec_df["title_norm"] = spec_df["title"].str.lower().str.strip()

        spec_map = spec_df.set_index("section_id")
        rows = []

        for _, r in toc_df.iterrows():
            sid = r["section_id"]
            if sid in spec_map.index:
                ss = spec_map.loc[sid]
                if isinstance(ss, pd.DataFrame):
                    ss = ss.iloc[0]

                title_match = str(r["title_norm"]) == str(ss["title_norm"])
                page_match = (int(r["page"]) == int(ss["page"])) or \
                             abs(int(r["page"]) - int(ss["page"])) <= 1

                rows.append({
                    "section_id": sid,
                    "title_toc": r["title"],
                    "title_spec": ss["title"],
                    "page_toc": int(r["page"]),
                    "page_spec": int(ss["page"]),
                    "found_in_spec": True,
                    "match_title": bool(title_match),
                    "match_page": bool(page_match),
                    "match_overall": bool(title_match and page_match),
                })
            else:
                rows.append({
                    "section_id": sid,
                    "title_toc": r["title"],
                    "title_spec": None,
                    "page_toc": int(r["page"]),
                    "page_spec": None,
                    "found_in_spec": False,
                    "match_title": False,
                    "match_page": False,
                    "match_overall": False,
                })

        cmp_df = pd.DataFrame(rows)
        return {
            "comparison": cmp_df,
            "mismatches": cmp_df[(cmp_df["found_in_spec"]) & (~cmp_df["match_overall"])],
            "missing_in_spec": cmp_df[~cmp_df["found_in_spec"]],
            "missing_in_toc": spec_df[~spec_df["section_id"].isin(toc_df["section_id"])],
            "toc_df": toc_df,
            "spec_df": spec_df,
        }

    def to_excel(self, out_path: str, counts: Dict[str, int]) -> str:
        parts = self.compare()
        with pd.ExcelWriter(out_path, engine="openpyxl") as xls:
            for name, df in parts.items():
                df.to_excel(xls, sheet_name=name, index=False)

            summary = {
                "toc_total": [len(self.toc)],
                "spec_total": [len(self.spec)],
                "matched": [int(parts["comparison"]["match_overall"].sum())],
                "title_mismatch": [int(((parts["comparison"]["found_in_spec"]) & \
                                        (~parts["comparison"]["match_title"])).sum())],
                "page_mismatch": [int(((parts["comparison"]["found_in_spec"]) & \
                                       (~parts["comparison"]["match_page"])).sum())],
                "missing_in_spec": [len(parts["missing_in_spec"])],
                "missing_in_toc": [len(parts["missing_in_toc"])],
            }

            pd.DataFrame(summary).to_excel(xls, sheet_name="summary", index=False)
            pd.DataFrame([counts]).to_excel(xls, sheet_name="counts", index=False)
        logging.info(f" Excel report written to {out_path}")
        return out_path
