#!/usr/bin/env python3
"""Four-job CORE-004 review activation via the existing protected validator.

The PR path is ALWAYS read-only; live activation requires protected main.
No mathematical admission, certification or publication power is conferred.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ci import cda_review_job_admission as base

REGISTRY = Path(__file__).resolve().parents[1] / "governance/CDA_REVIEW_ADMISSION_004.json"
FIXED = {
    (35, "C06", "CDA-REV-C06-004", 31),
    (36, "C07", "CDA-REV-C07-004", 32),
    (37, "C08", "CDA-REV-C08-004", 33),
    (38, "C09", "CDA-REV-C09-004", 34),
}


def load_jobs():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema") != "GCL-CDA-REVIEW-ADMISSION/1" or data.get("campaign") != base.CAMPAIGN:
        base.fail("invalid source-locked CORE-004 registry")
    jobs = data.get("jobs")
    if not isinstance(jobs, list) or len(jobs) != 4:
        base.fail("expected four bounded CORE-004 jobs")
    found = {(j["issue"],j["chapter"],j["assignment_id"],j["pr"]) for j in jobs}
    if found != FIXED:
        base.fail("CORE-004 registry differs from authorized four-job identity")
    for job in jobs:
        if not isinstance(job["head"],str) or not base.re.fullmatch(r"[0-9a-f]{40}",job["head"]):
            base.fail("invalid frozen PR head")
    return jobs


def run(execute=False):
    cohort = load_jobs()
    states = []
    for job in cohort:  # All four source/field/label inputs checked before mutation
        issue, fields, pr, comments = base.read_job(job)
        states.append(base.validate_job(job, issue, fields, pr, comments))
    print(json.dumps([{"issue":j["issue"],"state":state}
                      for j,state in zip(cohort,states)],indent=2))
    if not execute:
        print("READ ONLY: no Issue Fields or labels changed")
        return
    if os.environ.get("GITHUB_REPOSITORY") != base.REPO:
        base.fail("wrong repository")
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        base.fail("not protected main")
    for job,state in zip(cohort,states):
        if state in {"admit","finish_fields"}:
            base.set_fields(job)
            base.add_labels(job)
        elif state == "finish_labels":
            base.add_labels(job)
        elif state == "finish_body":
            issue,_,_,_=base.read_job(job)
            base.update_body(job, issue)
        elif state in {"already_available","already_returned"}:
            continue
        else:
            base.fail(f"unexpected CORE-004 transition {state}")
    for job in cohort:
        issue, fields, pr, comments = base.read_job(job)
        if base.validate_job(job,issue,fields,pr,comments) not in {
            "already_available","already_returned"
        }:
            base.fail(f"#{job['issue']} protected readback failed")
    print("Protected CORE-004 readback PASS: 4 source-locked jobs")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--execute",action="store_true")
    args=parser.parse_args()
    run(execute=args.execute)
