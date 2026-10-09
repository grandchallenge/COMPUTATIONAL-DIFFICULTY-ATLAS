#!/usr/bin/env python3
"""Project a valid CDA direct-editorial RESULT/1 into operational RETURNED state.

This module validates transport, issue binding, assignment identity, campaign,
and exact reviewed head. It does not adjudicate the review or grant acceptance,
merge, publication, certification, or release authority.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = "grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS"
CAMPAIGN = "COMPUTATIONAL-DIFFICULTY-ATLAS"
DIRECT_LABEL = "gcl-pickup:direct-editorial"
MARKER = "RESULT/1\n"
SHA = re.compile(r"^[0-9a-f]{40}$")
ASSIGNMENT = re.compile(r"^ASSIGNMENT_ID:[ \t]*([A-Z0-9-]+)[ \t]*$", re.M)
TARGET_HEAD = re.compile(r"^TARGET_HEAD:[ \t]*([0-9a-f]{40})[ \t]*$", re.M)
RETURN_FIELD = re.compile(r"^([a-z_]+):[ \t]*(.*)$", re.M)
DISPOSITIONS = {
    "APPROVE",
    "APPROVE_WITH_CORRECTIONS",
    "REQUEST_CHANGES",
    "BLOCKED",
}


def field_map(fields: list[dict]) -> dict[str, object]:
    result: dict[str, object] = {}
    for entry in fields:
        option = entry.get("single_select_option") or {}
        result[str(entry.get("issue_field_name"))] = option.get(
            "name", entry.get("value")
        )
    return result


def evaluate(event: dict, fields: list[dict]) -> dict:
    def skip(reason: str) -> dict:
        return {"project": False, "reason": reason}

    issue = event.get("issue") or {}
    comment = event.get("comment") or {}
    actor = comment.get("user") or {}
    repo = (event.get("repository") or {}).get("full_name")

    if repo != REPO:
        return skip("wrong_repository")
    if event.get("action") != "created":
        return skip("not_created")
    if "pull_request" in issue or issue.get("state") != "open":
        return skip("not_open_issue")
    labels = {x.get("name") for x in issue.get("labels", [])}
    if DIRECT_LABEL not in labels:
        return skip("not_direct_editorial")

    body = comment.get("body") or ""
    if not body.startswith(MARKER):
        return skip("not_result")
    if not comment.get("id") or not actor.get("login"):
        return skip("missing_authenticated_comment")

    operational = field_map(fields)
    if operational.get("GCL Campaign") != CAMPAIGN:
        return skip("wrong_campaign")
    if operational.get("GCL State") == "RETURNED":
        return skip("already_returned")
    if operational.get("GCL State") != "AVAILABLE":
        return skip("state_not_available")

    issue_body = issue.get("body") or ""
    assignment_match = ASSIGNMENT.search(issue_body)
    head_match = TARGET_HEAD.search(issue_body)
    if not assignment_match:
        return skip("missing_issue_assignment")
    if not head_match:
        return skip("missing_issue_target_head")

    returned = dict(RETURN_FIELD.findall(body))
    for required in ("assignment_id", "reviewer_role", "input_head", "disposition"):
        if not returned.get(required, "").strip():
            return skip(f"missing_{required}")

    assignment = returned["assignment_id"].strip()
    if assignment != assignment_match.group(1):
        return skip("wrong_assignment")

    input_head = returned["input_head"].strip()
    if not SHA.fullmatch(input_head):
        return skip("invalid_input_head")
    if input_head != head_match.group(1):
        return skip("wrong_input_head")

    disposition = returned["disposition"].strip()
    if disposition not in DISPOSITIONS:
        return skip("invalid_disposition")

    return {
        "project": True,
        "issue_number": issue["number"],
        "comment_id": comment["id"],
        "authenticated_actor": actor["login"],
        "assignment_id": assignment,
        "reviewer_role": returned["reviewer_role"].strip(),
        "input_head": input_head,
        "disposition": disposition,
        "state_to_write": "RETURNED",
        "review_adjudicated": False,
        "editorial_accepted": False,
        "publication_authorized": False,
        "certification_authorized": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--issue-fields", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = evaluate(
        json.loads(args.event.read_text(encoding="utf-8")),
        json.loads(args.issue_fields.read_text(encoding="utf-8")),
    )
    args.output.write_text(
        json.dumps(result, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
