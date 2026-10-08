# Computational Difficulty Atlas — Execution Protocol

Status: normative controller protocol

## Recovery authority

After any interruption, recover project execution state from branch `state/cda-controller`.

Read in this order:

1. `governance/ACTIVE_TRANSACTION.yaml`
2. `governance/CURRENT_HANDOFF.md`

Do not reconstruct live execution state from chat history.

## Separation of concerns

- `main`: accepted project state.
- candidate branches: bounded proposed changes.
- `state/cda-controller`: live transaction and recovery state.
- GitHub issues: bounded review/work evidence.
- pull requests: candidate integration surfaces.

## Exact-head rule

Any review or acceptance disposition binds to one exact candidate commit SHA.

If the candidate head changes after review, the review is not automatically transferable. The changed scope must be re-evaluated.

## Stop conditions

A bounded transaction may stop only for:

- a genuine external dependency;
- a validation failure requiring new work;
- an explicit review or governance gate;
- successful completion and durable readback.

Progress-only chat handoffs are not authoritative state.

## Visual publication rule

A figure is not publication-ready merely because it renders.

Publication readiness requires:
- mathematical review;
- pedagogical review;
- typography review at intended scale;
- grayscale/accessibility check;
- reproducible source and provenance.
