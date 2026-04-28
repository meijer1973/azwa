# Phase 26 Sprint 26.1 - Rough-Claim Audit Recalibration

## Summary

Current sprint: Sprint 26.1. Sprint 25.6 is parked as a policy-maker/stakeholder validation dependency and is not a blocker for repository-side data-quality cleanup. This sprint recalibrated the rough-claim audit without changing claim content: claim length is no longer enough by itself to mark a claim rough.

## What Changed

- Replaced the audit issue code `long_raw_excerpt` with `unverified_extraction_length`.
- Added a stricter length rule: a claim must be long and also show at least one extraction signal:
  - lowercase fragment start outside a small whitelist;
  - missing terminal punctuation;
  - table/column merge fingerprint.
- Increased `statement_excerpt` review context from 220 to 400 characters.
- Kept dashboard/QC compatibility for both the old and new rough issue names where needed.
- Added regression tests for long well-formed claims, lowercase fragments, table-merge fingerprints, and excerpt length.

## Audit Result

Baseline before this sprint:

- Rough publication claims: 293.
- `long_raw_excerpt`: 164.

After recalibration:

- Rough publication claims: 195.
- `unverified_extraction_length`: 48.
- Remaining issue counts:
  - `english_summary`: 59.
  - `raw_letterhead`: 6.
  - `fragment_too_short`: 42.
  - `bullet_or_heading_fragment`: 48.
  - `encoding_noise`: 4.

## Verification

- `python src/build_data_quality_audit.py` passed and regenerated `data/extracted/data_quality_audit.json`.
- `python src/build_internal_review_dashboard.py` passed and regenerated `docs/internal/review-dashboard.html`.
- `python -m pytest tests/test_data_quality_audit.py` passed.

Attempted broader scoped pipeline verification with:

```bash
python src/run_pipeline.py --from-stage phase24_data_quality_audit --force
```

That command did not reach the audit stage because upstream inventory rebuild failed on an existing annotation/manifest mismatch. The generated manifest churn from that failed attempt was reverted and is not part of this sprint.

## Carry Forward

Sprint 26.2 should now address the real remaining text/extraction problems deterministically: English summaries, letterhead fragments, encoding noise, table-of-contents/navigation fragments, and list/heading fragments. Sprint 26.3 can then focus on sentence boundaries, deduplication, and location/evidence cleanup.
