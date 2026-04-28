# Phase 26 Sprint 26.2 - Deterministic Text Fixes

## Summary

Current sprint: Sprint 26.2. Sprint 25.6 remains parked as a policy-maker/stakeholder validation dependency and does not block repository-side text-quality cleanup. This sprint added deterministic filters before claim generation, so known format noise is no longer promoted into `claims_master.jsonl`.

## What Changed

- Added structural text cleanup in `src/build_structural_extractions.py`:
  - common mojibake/control-character repair;
  - TOC-line filtering;
  - Drupal article-link filtering;
  - voting-result capture outside claim input.
- Added candidate-level hard filters in `src/build_document_extractions.py`:
  - ministerial-letter letterhead removal;
  - residual mojibake skip;
  - voting-result skip;
  - Drupal article-link skip;
  - TOC fragment skip even when timeline-like years are present.
- Preserved voting results in `data/extracted/voting_records.json`.
- Added cleanup diagnostics in `data/logs/phase26_text_cleanup.json`.
- Added regression tests in `tests/test_phase26_text_cleanup.py`.

## Before / After

Before Sprint 26.2, after Sprint 26.1:

- Claims: 598.
- Rough publication claims: 195.
- `encoding_noise`: 4.
- `raw_letterhead`: 6.
- `bullet_or_heading_fragment`: 48.
- Voting-result claims present: 2.

After Sprint 26.2:

- Claims: 590.
- Rough publication claims: 159.
- `encoding_noise`: 0.
- `raw_letterhead`: 0.
- `bullet_or_heading_fragment`: 14.
- `unverified_extraction_length`: 45.
- `fragment_too_short`: 42.
- Voting-result claims in `claims_master.jsonl`: 0.
- Voting records preserved separately: 4.

The claim count drop is 8 claims, about 1.3 percent of the pre-sprint total, within the expected safe range.

## Verification

Regenerated manually from structural extraction through render/dashboard because `phase0_setup` currently rewrites `data/raw/manifest.json` from the older selected-source set and causes an upstream annotation/manifest mismatch if the full pipeline runner includes phase 0.

Commands run:

```bash
python src/build_structural_extractions.py
python src/build_document_extractions.py
python src/build_claims_top5.py
python src/build_current_interpretation.py
python src/build_workagenda_d5_operational_requirements.py
python src/build_local_source_strengthening_almere.py
python src/build_workagenda_nulmeting_capacity.py
python src/build_d6_governance_collaboration.py
python src/build_almere_d6_responsibility_register.py
python src/build_master_views.py
python src/build_quality_control.py
python src/build_site_view_models.py
python src/build_data_quality_audit.py
python src/render_site.py
python src/build_internal_review_dashboard.py
```

Results:

- QC: 0 blocking, 6 warning, 73 review items.
- Render: 132 HTML pages and 133 search index entries.

## Carry Forward

Sprint 26.3 should focus on the remaining rough categories that need claim-level structure rather than simple format filtering:

- sentence-boundary checks for mid-sentence starts and missing terminal punctuation;
- deduplication within document/topic/subtopic groups;
- claim-id reference verification after claim removal or consolidation.
