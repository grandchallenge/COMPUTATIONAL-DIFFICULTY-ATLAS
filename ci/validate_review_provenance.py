#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "reviews/CDA_REV_001_RECEIPT.json"
ADJUDICATION = ROOT / "reviews/CDA_REV_001_ADJUDICATION.md"
METADATA = ROOT / "figures/metadata/F1_1.yaml"
CAPTION = ROOT / "figures/F1_1_CAPTION.md"

SHA = re.compile(r"^[0-9a-f]{40}$")
TICK = chr(96)


def scalar(lines: list[str], key: str) -> str:
    prefix = f"  {key}: "
    values = [line[len(prefix):].strip() for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise ValueError(f"expected one metadata scalar {key}, found {values}")
    return values[0]


def validate() -> list[str]:
    errors: list[str] = []
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))

    if receipt.get("schema") != "CDA-REVIEW-RECEIPT/1":
        errors.append("review receipt schema mismatch")
    head = str(receipt.get("input_head") or "")
    if not SHA.fullmatch(head):
        errors.append("review receipt input_head is not a 40-hex SHA")
    if receipt.get("assignment_id") != "CDA-REV-001":
        errors.append("review receipt assignment mismatch")
    if receipt.get("issue_number") != 2:
        errors.append("review receipt issue mismatch")
    if receipt.get("result_comment_id") != 6072199152:
        errors.append("review receipt comment mismatch")
    if receipt.get("disposition") != "APPROVE_WITH_CORRECTIONS":
        errors.append("review receipt disposition mismatch")

    authority = receipt.get("authority_effect") or {}
    for key in (
        "review_adjudicated",
        "editorial_accepted",
        "publication_authorized",
        "certification_authorized",
    ):
        if authority.get(key) is not False:
            errors.append(f"review receipt authority inflation: {key}")

    adjudication = ADJUDICATION.read_text(encoding="utf-8")
    for needle in (
        f"reviewed input head: {TICK}{head}{TICK}",
        f"RESULT/1 comment: {TICK}{receipt['result_comment_id']}{TICK}",
        f"disposition: {TICK}{receipt['disposition']}{TICK}",
    ):
        if needle not in adjudication:
            errors.append(f"adjudication provenance mismatch: {needle}")

    meta_lines = METADATA.read_text(encoding="utf-8").splitlines()
    try:
        if scalar(meta_lines, "assignment_id") != receipt["assignment_id"]:
            errors.append("figure metadata assignment mismatch")
        if scalar(meta_lines, "input_head") != head:
            errors.append("figure metadata input_head mismatch")
        if scalar(meta_lines, "disposition") != receipt["disposition"]:
            errors.append("figure metadata disposition mismatch")
        if int(scalar(meta_lines, "comment_id")) != receipt["result_comment_id"]:
            errors.append("figure metadata comment mismatch")
    except (ValueError, TypeError) as exc:
        errors.append(f"figure metadata provenance parse failure: {exc}")

    caption = CAPTION.read_text(encoding="utf-8")
    if f"exact head {TICK}{head}{TICK}" not in caption:
        errors.append("figure caption exact-head review evidence mismatch")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("PASS: CDA-REV-001 provenance is internally consistent and authority-neutral")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
