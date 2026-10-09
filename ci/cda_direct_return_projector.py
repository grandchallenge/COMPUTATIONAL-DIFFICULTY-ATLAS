#!/usr/bin/env python3
"""Project a valid CDA direct-editorial RESULT/1 into operational RETURNED state.

This module validates transport, issue binding, queue labels/fields, assignment
identity, reviewer role, campaign, pickup mode, and exact reviewed head. It does
not adjudicate the review or grant acceptance, merge, publication,
certification, or release authority.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = "grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS"
CAMPAIGN = "COMPUTATIONAL-DIFFICULTY-ATLAS"
PICKUP_MODE = "DIRECT_EDITORIAL_NO_CLAIM"
DIRECT_LABEL = "gcl-pickup:direct-editorial"
MARKER = "RESULT/1\n"
SHA = re.compile(r"^[0-9a-f]{40}$")
ASSIGNMENT = re.compile(r"^ASSIGNMENT_ID:[ \t]*([A-Z0-9-]+)[ \t]*$", re.M)
TARGET_HEAD = re.compile(r"^TARGET_HEAD:[ \t]*([0-9a-f]{40})[ \t]*$", re.M)
ISSUE_CAMPAIGN = re.compile(r"^CAMPAIGN:[ \t]*([^\r\n]+)[ \t]*$", re.M)
ISSUE_ROLE = re.compile(r"^ROLE:[ \t]*([^\r\n]+)[ \t]*$", re.M)
ISSUE_PICKUP = re.compile(r"^PICKUP_MODE:[ \t]*([^\r\n]+)[ \t]*$", re.M)
RETURN_FIELD = re.compile(r"^([a-z_]+):[ \t]*(.*)$", re.M)

ROLE_LABELS = {
    "gcl-role:reconnaissance": "RECON",
    "gcl-role:source-audit": "SOURCE",
    "gcl-role:adversarial": "ADVERSARIAL",
    "gcl-role:constructive": "CONSTRUCTIVE",
    "gcl-role:verify": "VERIFY",
    "gcl-role:lead": "LEAD",
    "gcl-role:support": "SUPPORT",
    "gcl-role:synthesis": "SYNTHESIS",
}
COLLAB_LABELS = {
    "gcl-collab:blind": "BLIND",
    "gcl-collab:cooperative": "COOPERATIVE",
    "gcl-collab:staged": "STAGED",
    "gcl-collab:lead-support": "LEAD_SUPPORT",
}
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


def one_mapped_label(
    labels: set[str],
    prefix: str,
    mapping: dict[str, str],
) -> tuple[str, str] | None:
    found = sorted(x for x in labels if x.startswith(prefix))
    if len(found) != 1 or found[0] not in mapping:
        return None
    return found[0], mapping[found[0]]


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

    labels = {str(x.get("name")) for x in issue.get("labels", []) if x.get("name")}
    if "gcl-job" not in labels:
        return skip("missing_job_label")

    pickup_labels = {x for x in labels if x.startswith("gcl-pickup:")}
    if pickup_labels != {DIRECT_LABEL}:
        return skip("pickup_label_mismatch")

    operational = field_map(fields)
    if operational.get("GCL Campaign") != CAMPAIGN:
        return skip("wrong_campaign")
    if operational.get("GCL State") == "RETURNED":
        return skip("already_returned")
    if operational.get("GCL State") != "AVAILABLE":
        return skip("state_not_available")

    state_labels = {x for x in labels if x.startswith("gcl-state:")}
    if state_labels != {"gcl-state:available"}:
        return skip("state_label_mismatch")

    role = one_mapped_label(labels, "gcl-role:", ROLE_LABELS)
    if role is None:
        return skip("role_label_mismatch")
    if operational.get("GCL Role") != role[1]:
        return skip("role_field_mismatch")

    collaboration = one_mapped_label(labels, "gcl-collab:", COLLAB_LABELS)
    if collaboration is None:
        return skip("collaboration_label_mismatch")
    if operational.get("GCL Collaboration") != collaboration[1]:
        return skip("collaboration_field_mismatch")

    body = comment.get("body") or ""
    if not body.startswith(MARKER):
        return skip("not_result")
    if not comment.get("id") or not actor.get("login"):
        return skip("missing_authenticated_comment")

    issue_body = issue.get("body") or ""
    assignment_match = ASSIGNMENT.search(issue_body)
    head_match = TARGET_HEAD.search(issue_body)
    campaign_match = ISSUE_CAMPAIGN.search(issue_body)
    role_match = ISSUE_ROLE.search(issue_body)
    pickup_match = ISSUE_PICKUP.search(issue_body)

    if not assignment_match:
        return skip("missing_issue_assignment")
    if not head_match:
        return skip("missing_issue_target_head")
    if not campaign_match or campaign_match.group(1).strip() != CAMPAIGN:
        return skip("issue_campaign_mismatch")
    if not role_match:
        return skip("missing_issue_role")
    if not pickup_match or pickup_match.group(1).strip() != PICKUP_MODE:
        return skip("issue_pickup_mode_mismatch")

    returned = dict(RETURN_FIELD.findall(body))
    for required in ("assignment_id", "reviewer_role", "input_head", "disposition"):
        if not returned.get(required, "").strip():
            return skip(f"missing_{required}")

    assignment = returned["assignment_id"].strip()
    if assignment != assignment_match.group(1):
        return skip("wrong_assignment")

    reviewer_role = returned["reviewer_role"].strip()
    if reviewer_role != role_match.group(1).strip():
        return skip("wrong_reviewer_role")

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
        "reviewer_role": reviewer_role,
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
