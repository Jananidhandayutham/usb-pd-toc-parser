import re
from typing import Optional, List
import json
from dataclasses import asdict, is_dataclass


def normalize_title(title: str) -> str:
    t = re.sub(r"\.{2,}", " ", title)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def parent_of(section_id: str) -> Optional[str]:
    return section_id.rsplit(".", 1)[0] if "." in section_id else None


def level_of(section_id: str) -> int:
    return section_id.count(".") + 1


class Reporter:
    @staticmethod
    def write_jsonl(path: str, data: List) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for entry in data:
                if is_dataclass(entry):
                    entry = asdict(entry)
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
