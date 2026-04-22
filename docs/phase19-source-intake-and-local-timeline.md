# Phase 19: Source Intake and Local Timeline Enrichment

## Scope

This milestone extends the formal source intake for timeline-relevant web pages and promotes selected pipeline-backed dates into the public executive timeline.

## What Changed

- Added two new raw HTML sources to the formal corpus:
  - `nat_sociaalwerknl_financiering_iza_azwa_2025`
  - `mun_almere_raad_vergaderschema_2026`
- Updated `data/raw/manifest.json` and `src/build_document_inventory.py` so both sources flow through inventory, structural extraction, document extraction, claims, interpretation, QC, and site generation.
- Marked the original VNG Wegwijzer intake URL as `pending_replacement` because the recorded URL returned `404` on `2026-04-22`.
- Added explicit Dutch site labels for the newer web-source document types.

## Extraction Improvements

- Improved table-driven extraction by adding row-level candidates from extracted tables in `src/build_document_extractions.py`.
- Increased the auto-extraction capacity for `timeline_and_status` from `2` to `3` items.
- Added timeline keyword support for quarter-based and local-governance phrases such as:
  - `q2`
  - `q3`
  - `tweede kwartaal`
  - `derde kwartaal`
  - `politieke markt`
  - `gemeenteraadsverkiezingen`
  - `benoeming raad`
  - `afscheid raad`
- Added a dedicated claim topic for local schedule moments:
  - `timeline.local_governance_calendar`

## Timeline Promotions

Promoted these pipeline-backed moments into `config/timeline_curation.json`:

- `2026-03-18` Gemeenteraadsverkiezingen 2026 in Almere
- `2026-03-31` Afscheid van de raad 2022-2026
- `2026-04-01` Benoeming van de raad 2026-2030
- `Q3 2026` Aanvullend regioplan volgens Sociaal Werk Nederland in Q3 2026 gereed

The Sociaal Werk Nederland entry is intentionally flagged for human review in the site layer because it is a lower-authority commentary source rather than a formal national instrument.

## Human-Facing Source Notes

The site now distinguishes between:

- official local planning sources such as the Raad van Almere schedule
- lower-authority commentary sources such as Sociaal Werk Nederland

This keeps the public timeline explicit about what is a formal local moment and what is only a policy signal awaiting stronger confirmation.

## Verification

- `python src/run_pipeline.py --all`
- `python -m unittest discover -s tests -p "test_*.py"`

## Result

The public timeline now contains the newly ingested local Almere governance moments, keeps `2026` chronologically ordered, and includes a guarded Q3 2026 regioplan signal with explicit human-review wording.
