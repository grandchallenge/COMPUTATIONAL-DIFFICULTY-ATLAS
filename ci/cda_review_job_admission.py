#!/usr/bin/env python3
"""Fail-closed admission of protected CDA direct-editorial review jobs.

A protected merge of governance/CDA_REVIEW_ADMISSION_002.json is the activation
authority. PR validation is read-only. A GitHub Action running on protected main
can admit these exact jobs, then read back Issue Fields and lifecycle labels.
It cannot review, adjudicate, merge manuscript PRs, certify or publish results.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

REPO = "grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS"
CAMPAIGN = "COMPUTATIONAL-DIFFICULTY-ATLAS"
REGISTRY = Path(__file__).resolve().parents[1] / "governance/CDA_REVIEW_ADMISSION_002.json"
ROLE = "INDEPENDENT_MATHEMATICAL_EDITORIAL_VERIFY"
PICKUP = "DIRECT_EDITORIAL_NO_CLAIM"
BASE_LABELS = {"gcl-job", "gcl-role:verify", "gcl-collab:cooperative"}
AVAILABLE_LABELS = BASE_LABELS | {"gcl-state:available", "gcl-pickup:direct-editorial"}
FIELDS = {
    "GCL State": (47953501, "AVAILABLE"),
    "GCL Campaign": (47953502, CAMPAIGN),
    "GCL Role": (47953503, "VERIFY"),
    "GCL Collaboration": (47953504, "COOPERATIVE"),
    "GCL Phase": (47953505, "SHARED"),
}
FIELD_VALUES = {key: value for key, (_, value) in FIELDS.items()}


def fail(reason):
    raise ValueError(reason)


def api(method, route, payload=None):
    cmd = ["gh", "api", "--method", method, f"repos/{REPO}/{route}"]
    if payload is not None:
        cmd += ["--input", "-"]
    result = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                            text=True, capture_output=True, check=False)
    if result.returncode:
        fail(f"gh api {method} {route}: {result.stderr.strip()}")
    # Some successful GitHub mutating endpoints return 204 / an empty body.
    # A state-changing success is determined by the subsequent readback, not by
    # assuming every write returned JSON.
    if not result.stdout.strip():
        if method == "GET":
            fail(f"gh api GET {route}: empty response")
        return None
    return json.loads(result.stdout)


def labels_of(issue):
    return {x["name"] for x in issue.get("labels", [])}


def map_fields(data):
    fields = {}
    for x in data:
        name = x.get("issue_field_name")
        value = (x.get("single_select_option") or {}).get("name", x.get("value"))
        if not name or name in fields:
            fail("unknown or repeated Issue Field")
        fields[name] = value
    return fields


def exact_line(body, key, expected):
    # Reject *all* duplicate keys, including a correct value plus a hostile one.
    values = re.findall(rf"^{re.escape(key)}:[ \t]*(.*?)[ \t]*$", body, re.M)
    if len(values) != 1 or values[0].strip() != expected:
        fail(f"missing/duplicate/mismatched body binding {key}")


def validate_job(job, issue, field_rows, pr):
    number, assignment, head = job["issue"], job["assignment_id"], job["head"]
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        fail("invalid frozen head SHA")
    if issue.get("number") != number or issue.get("state") != "open" or "pull_request" in issue:
        fail(f"#{number} is not the expected open non-PR issue")
    body = issue.get("body") or ""
    staged_state = "STATE: STAGED_PENDING_AUTHORIZED_QUEUE_ADMISSION"
    ready_state = "STATE: AVAILABLE"
    state_lines = [line.strip() for line in body.splitlines()
                   if re.match(r"^STATE:", line)]
    if len(state_lines) != 1 or state_lines[0] not in {staged_state, ready_state}:
        fail(f"#{number} ambiguous issue body lifecycle STATE")
    state_staged = state_lines[0] == staged_state
    state_ready = state_lines[0] == ready_state
    for key, val in {
        "ASSIGNMENT_ID": assignment,
        "CAMPAIGN": CAMPAIGN,
        "ROLE": ROLE,
        "PICKUP_MODE": PICKUP,
        "TARGET_PR": f"#{job['pr']}",
        "TARGET_HEAD": head,
        "TARGET_CHAPTER": job["chapter"],
        "PROTECTED_OR_RELEASE_MUTATION_AUTHORIZED": "NO",
    }.items():
        exact_line(body, key, val)
    if pr.get("number") != job["pr"] or pr.get("state") != "open":
        fail(f"#{number} target PR missing/open state changed")
    if (pr.get("head") or {}).get("sha") != head:
        fail(f"#{number} stale target PR head; immutable packet requires re-approval")
    labs = labels_of(issue)
    if labs == BASE_LABELS:
        label_state = "staged"
    elif labs == AVAILABLE_LABELS:
        label_state = "available"
    elif labs > BASE_LABELS and labs < AVAILABLE_LABELS:
        label_state = "partial_labels"
    else:
        fail(f"#{number} unexpected labels {sorted(labs)}")
    fields = map_fields(field_rows)
    if label_state == "staged" and state_staged and not fields:
        return "admit"
    # Only already-correct subsets may be replayed after an interrupted field write.
    if label_state == "staged" and state_staged and fields != FIELD_VALUES and all(
        name in FIELD_VALUES and value == FIELD_VALUES[name]
        for name, value in fields.items()
    ):
        return "finish_fields"
    if fields == FIELD_VALUES and label_state in {"staged", "partial_labels"} and state_staged:
        return "finish_labels"  # safe replay of interrupted label writes
    if fields == FIELD_VALUES and label_state == "available" and state_staged:
        return "finish_body"
    if fields == FIELD_VALUES and label_state == "available" and state_ready:
        return "already_available"
    fail(f"#{number} partial/hostile Issue Field state {fields}")


def read_job(job):
    number = job["issue"]
    return (api("GET", f"issues/{number}"),
            api("GET", f"issues/{number}/issue-field-values"),
            api("GET", f"pulls/{job['pr']}"))


def load_registry():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema") != "GCL-CDA-REVIEW-ADMISSION/1" or data.get("campaign") != CAMPAIGN:
        fail("wrong registry identity")
    jobs = data["jobs"]
    if len(jobs) != 6:
        fail("unexpected cohort size")
    if len({j["issue"] for j in jobs}) != len(jobs):
        fail("duplicate issue in immutable registry")
    if len({j["assignment_id"] for j in jobs}) != len(jobs):
        fail("duplicate assignment")
    return jobs


def set_fields(job):
    number = job["issue"]
    existing = map_fields(api("GET", f"issues/{number}/issue-field-values"))
    if any(k not in FIELD_VALUES or v != FIELD_VALUES[k] for k, v in existing.items()):
        fail("partial field state inconsistent with protected registry")
    # Single-field POST mirrors the already exercised direct-return projector contract.
    for field_name, (field_id, value) in FIELDS.items():
        if field_name in existing:
            continue
        api("POST", f"issues/{number}/issue-field-values",
            {"issue_field_values": [{"field_id": field_id, "value": value}]})
    actual = map_fields(api("GET", f"issues/{number}/issue-field-values"))
    if actual != FIELD_VALUES:
        fail("field write failed readback; do NOT add available labels")


def add_labels(job):
    number = job["issue"]
    for name in ("gcl-pickup:direct-editorial", "gcl-state:available"):
        api("POST", f"issues/{number}/labels", {"labels": [name]})
    issue, fields, pr = read_job(job)
    if validate_job(job, issue, fields, pr) != "finish_body":
        fail(f"#{number} failed final label+field readback")
    update_body(job, issue)


def update_body(job, issue):
    number = job["issue"]
    old = "STATE: STAGED_PENDING_AUTHORIZED_QUEUE_ADMISSION"
    new = "STATE: AVAILABLE"
    body = issue.get("body") or ""
    if body.count(old) != 1:
        fail(f"#{number} stage body does not match immutable release transition")
    body = body.replace(old, new)
    body = body.replace("This issue is **STAGED, NOT AVAILABLE**.",
                        "This issue is available only when authoritative GCL Issue Fields and lifecycle labels agree.")
    api("PATCH", f"issues/{number}", {"body": body})
    new_issue, fields, pr = read_job(job)
    if validate_job(job, new_issue, fields, pr) != "already_available":
        fail(f"#{number} failed post-release body+field readback")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true",
                        help="protected-main activation only; default read-only")
    options = parser.parse_args()
    jobs = load_registry()
    states = []
    for job in jobs:  # full-cohort preflight before ANY mutation
        issue, fields, pr = read_job(job)
        states.append(validate_job(job, issue, fields, pr))
    print(json.dumps([{"issue": j["issue"], "state": s}
                      for j, s in zip(jobs, states)], indent=2))
    if not options.execute:
        print("READ-ONLY PREFLIGHT; no Issue Fields or labels changed")
        return
    if os.environ.get("GITHUB_REPOSITORY") != REPO:
        fail("wrong repository environment")
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        fail("no activation from non-protected main")
    for job, state in zip(jobs, states):
        if state in {"admit", "finish_fields"}:
            set_fields(job)
            add_labels(job)
        elif state == "finish_labels":
            add_labels(job)
        elif state == "finish_body":
            issue, _, _ = read_job(job)
            update_body(job, issue)
        elif state == "already_available":
            continue
    for job in jobs:
        issue, fields, pr = read_job(job)
        assert validate_job(job, issue, fields, pr) == "already_available"
    print("Protected review-job admission readback: 6/6 AVAILABLE")


if __name__ == "__main__":
    main()
