#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


DEFAULT_THRESHOLDS = {
    "minimum_pages": 3,
    "minimum_characters": 3500,
    "minimum_digit_count": 400,
    "minimum_percent_items": 15,
    "minimum_money_terms": 45,
}

REQUIRED_TERMS = [
    "基本面分析",
    "估值面分析",
    "研究判断与方法论",
    "经营现金流",
    "毛利率",
    "净利润",
    "PE",
    "观察条件",
    "失效条件",
    "不构成投资建议",
]

FORBIDDEN_TERMS = ["买入", "卖出", "目标价", "保证收益", "确定性收益"]
MOJIBAKE_TERMS = ["\x00", "锟", "�"]


def extract_text(pdf: Path) -> tuple[str, int]:
    reader = PdfReader(str(pdf))
    return "\n".join(page.extract_text() or "" for page in reader.pages), len(reader.pages)


def metrics(pdf: Path) -> dict:
    text, pages = extract_text(pdf)
    return {
        "pdf": str(pdf),
        "bytes": pdf.stat().st_size,
        "pages": pages,
        "characters": len(text),
        "digit_count": len(re.findall(r"\d", text)),
        "percent_items": len(re.findall(r"\d+(?:\.\d+)?%", text)),
        "money_terms": len(re.findall(r"(?:亿元|亿美元|元|USD|RMB|人民币|美元)", text)),
        "missing_required_terms": [term for term in REQUIRED_TERMS if term not in text],
        "forbidden_hits": [term for term in FORBIDDEN_TERMS if term in text],
        "mojibake_hits": [term for term in MOJIBAKE_TERMS if term in text],
    }


def find_quality_check(pdf: Path, explicit: Path | None = None) -> Path | None:
    if explicit:
        return explicit if explicit.exists() else None
    candidates = [
        pdf.with_name(f"{pdf.stem}_quality_check.md"),
    ]
    if "_截至" in pdf.stem:
        candidates.append(pdf.with_name(f"{pdf.stem.split('_截至', 1)[0]}_quality_check.md"))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    nearby = list(pdf.parent.glob("*quality_check.md"))
    if len(nearby) == 1:
        return nearby[0]
    return None


def quality_check_status(pdf: Path, explicit: Path | None = None) -> str:
    path = find_quality_check(pdf, explicit)
    if not path:
        return "MISSING"
    text = path.read_text(encoding="utf-8", errors="replace")
    tail = text.split("## 最终结论")[-1]
    if "**PASS**" in tail or "PASS" in tail:
        return "PASS"
    return "NOT_PASS"


def thresholds_from_golden(golden: Path | None) -> dict:
    if not golden:
        return dict(DEFAULT_THRESHOLDS)
    base = metrics(golden)
    return {
        "minimum_pages": max(DEFAULT_THRESHOLDS["minimum_pages"], base["pages"] - 1),
        "minimum_characters": max(DEFAULT_THRESHOLDS["minimum_characters"], int(base["characters"] * 0.65)),
        "minimum_digit_count": max(DEFAULT_THRESHOLDS["minimum_digit_count"], int(base["digit_count"] * 0.38)),
        "minimum_percent_items": max(DEFAULT_THRESHOLDS["minimum_percent_items"], int(base["percent_items"] * 0.22)),
        "minimum_money_terms": max(DEFAULT_THRESHOLDS["minimum_money_terms"], int(base["money_terms"] * 0.55)),
    }


def check(pdf: Path, quality_check: Path | None = None, golden: Path | None = None) -> dict:
    if not pdf.exists():
        return {"status": "FAIL", "pdf": str(pdf), "failures": ["pdf_missing"]}
    current = metrics(pdf)
    thresholds = thresholds_from_golden(golden)
    quality_status = quality_check_status(pdf, quality_check)

    failures = []
    if current["pages"] < thresholds["minimum_pages"]:
        failures.append("pages_below_depth_floor")
    if current["characters"] < thresholds["minimum_characters"]:
        failures.append("characters_below_depth_floor")
    if current["digit_count"] < thresholds["minimum_digit_count"]:
        failures.append("digit_density_below_depth_floor")
    if current["percent_items"] < thresholds["minimum_percent_items"]:
        failures.append("percent_items_below_depth_floor")
    if current["money_terms"] < thresholds["minimum_money_terms"]:
        failures.append("money_terms_below_depth_floor")
    if current["missing_required_terms"]:
        failures.append("missing_required_depth_terms")
    if current["forbidden_hits"]:
        failures.append("forbidden_terms_detected")
    if current["mojibake_hits"]:
        failures.append("mojibake_detected")
    if quality_status != "PASS":
        failures.append("quality_check_not_pass")

    return {
        "status": "PASS" if not failures else "NEEDS_REVIEW",
        "pdf": str(pdf),
        "quality_check_status": quality_status,
        "metrics": current,
        "thresholds": thresholds,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="+", type=Path)
    parser.add_argument("--quality-check", type=Path)
    parser.add_argument("--golden", type=Path, help="Optional local benchmark PDF for stricter relative thresholds.")
    args = parser.parse_args()

    results = [check(pdf, args.quality_check, args.golden) for pdf in args.pdf]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(item["status"] == "PASS" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
