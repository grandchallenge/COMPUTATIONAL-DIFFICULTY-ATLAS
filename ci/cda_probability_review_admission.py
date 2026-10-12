#!/usr/bin/env python3
"""Tranche-006 probability-branch admission reusing the protected tranche-002 contract.

This extends queue capacity *without modifying* the old six immutably returned
jobs or adding standalone authority. PR preflight is read-only; writes occur only
on protected main after exact registry merge.
"""
import argparse
import json
import os
from pathlib import Path

from ci import cda_review_job_admission as base

REGISTRY = Path(__file__).resolve().parents[1] / "governance/CDA_REVIEW_ADMISSION_006.json"


def load_jobs():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema") != "GCL-CDA-REVIEW-ADMISSION/1":
        base.fail("unexpected admission registry schema")
    if data.get("campaign") != base.CAMPAIGN:
        base.fail("wrong campaign")
    jobs = data.get("jobs")
    if not isinstance(jobs, list) or len(jobs) != 2:
        base.fail("expected exactly two PROBABILITY-006 review jobs")
    if {(j["issue"], j["chapter"], j["assignment_id"], j["pr"]) for j in jobs} != {
        (49, "C13", "CDA-REV-C13-006", 47),
        (50, "C14", "CDA-REV-C14-006", 48),
    }:
        base.fail("unrecognized issue/assignment map for tranche 006")
    if len({j["head"] for j in jobs}) != 2:
        base.fail("PROBABILITY-006 review jobs require two distinct frozen manuscript heads")
    return jobs


def run(execute=False):
    jobs = load_jobs()
    decisions = []
    for job in jobs:  # Full cohort immutable preflight before ANY field write
        issue, fields, pr, comments = base.read_job(job)
        decisions.append(base.validate_job(job, issue, fields, pr, comments))
    print(json.dumps([{"issue": j["issue"], "state": state}
                      for j, state in zip(jobs, decisions)], indent=2))
    if not execute:
        print("READ ONLY: no Issue Field or label writes")
        return
    if os.environ.get("GITHUB_REPOSITORY") != base.REPO:
        base.fail("wrong target repository")
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        base.fail("write attempted outside protected main")
    for job, decision in zip(jobs, decisions):
        if decision in {"admit", "finish_fields"}:
            base.set_fields(job)
            base.add_labels(job)
        elif decision == "finish_labels":
            base.add_labels(job)
        elif decision == "finish_body":
            issue, _, _, _ = base.read_job(job)
            base.update_body(job, issue)
        elif decision in {"already_available", "already_returned"}:
            continue
        else:
            base.fail(f"unrecognized projection step {decision}")
    for job in jobs:
        issue, fields, pr, comments = base.read_job(job)
        if base.validate_job(job, issue, fields, pr, comments) not in {
            "already_available", "already_returned"
        }:
            base.fail(f"#{job['issue']} failed full protected projection readback")
    print("Protected readback: both PROBABILITY-006 jobs are correctly admitted/returned")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true")
    args = p.parse_args()
    run(execute=args.execute)
