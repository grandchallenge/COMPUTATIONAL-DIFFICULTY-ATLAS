#!/usr/bin/env python3
"""Replay missed CDA direct-editorial RESULT/1 events from durable issue comments.

This is a repair path for missed issue_comment delivery. It applies exactly the
same projector contract as the event-driven workflow and emits at most one
projection candidate. It does not mutate GitHub itself.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ci.cda_direct_return_projector import REPO, evaluate


def reconcile(issue: dict, fields: list[dict], comments: list[dict]) -> dict:
    if issue.get("state") != "open":
        return {"project": False, "reason": "not_open_issue"}

    ordered = sorted(
        comments,
        key=lambda c: (
            str(c.get("created_at") or ""),
            int(c.get("id") or 0),
        ),
    )

    examined = 0
    rejected: list[dict] = []
    for comment in ordered:
        body = comment.get("body")
        if not isinstance(body, str) or not body.startswith("RESULT/1\n"):
            continue
        examined += 1
        event = {
            "action": "created",
            "repository": {"full_name": REPO},
            "issue": issue,
            "comment": comment,
        }
        result = evaluate(event, fields)
        if result.get("project") is True:
            return {
                **result,
                "replayed": True,
                "examined_result_comments": examined,
            }
        rejected.append(
            {
                "comment_id": comment.get("id"),
                "reason": result.get("reason"),
            }
        )

    return {
        "project": False,
        "reason": "no_conforming_result",
        "examined_result_comments": examined,
        "rejected": rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", type=Path, required=True)
    parser.add_argument("--issue-fields", type=Path, required=True)
    parser.add_argument("--comments", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = reconcile(
        json.loads(args.issue.read_text(encoding="utf-8")),
        json.loads(args.issue_fields.read_text(encoding="utf-8")),
        json.loads(args.comments.read_text(encoding="utf-8")),
    )
    args.output.write_text(
        json.dumps(result, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
