# Sprint 24.2 Audit

## Purpose
Sprint 24.2 turns the six quality perspectives into a saved internal audit of the current claim layer and site-data layer.

This sprint does not change the public site text yet. It creates an internal baseline that shows where the current data is still too broad, too rough, or too weakly mapped to the quality framework.

## Saved Outputs
- Canonical machine-readable audit: `data/extracted/data_quality_audit.json`
- Generator script: `src/build_data_quality_audit.py`
- Pipeline stage: `phase24_data_quality_audit`

The audit output is intentionally stored under `data/extracted/` rather than `data/site/`, because it is an internal quality-control product and not a public publication layer.

## What The Audit Checks
- claim coverage across `Norm`, `Time`, `Money`, `Governance`, `Locality`, and `Execution`
- perspective coverage of detail view-models
- broad rest buckets such as `timeline.other`
- claims that are useful in substance but too rough for publication
- rough claims that already leak into site drill-downs and overview models

## Snapshot On 2026-04-24
- `376` claims across `44` interpreted topics
- `356` claims mapped to at least one perspective
- `20` claims still without a strong perspective mapping
- `5` broad `*.other` rest topics
- `6` high-volume catch-all topics
- `199` claims flagged as textually rough for publication
- `12` site JSON files already carrying rough claims into public-facing drill-downs or summaries

## Main Findings

### 1. Broad rest buckets still absorb too much meaning
The largest rest categories are:
- `timeline.other` with `32` current claims
- `governance_and_finance.other` with `28` current claims
- `monitoring.other` with `27` current claims
- `d5.other` with `18` current claims
- `d6.other` with `4` current claims

These topics still mix different policy meanings into one bucket. That makes both the reference layer and the public site less precise than they should be.

### 2. One large catch-all topic remains outside the rest buckets
`municipal.implementation_translation` currently carries `72` current claims and `10` historical claims.

This topic is useful, but it is too large to stay as one combined translation bucket for long. It is a good candidate for later splitting by `Locality`, `Governance`, and `Execution`.

### 3. Rough claim text is a real site-data problem
The main rough-text issue types are:
- `102` `long_raw_excerpt`
- `59` `english_summary`
- `29` `bullet_or_heading_fragment`
- `26` `fragment_too_short`
- `6` `raw_letterhead`

This confirms that the current problem is not only “a few bad claims.” It is a recurring quality pattern in the extraction layer.

### 4. Rough evidence already leaks into public-facing models
The worst-affected site-data files currently include:
- `data/site/site_home_view.json`
- `data/site/site_updates_view.json`
- `data/site/site_almere_view.json`
- `data/site/action_view_models/act_d5_werkagenda_expliciteren.json`
- `data/site/action_view_models/act_monitoring_afstemmen.json`
- `data/site/decision_view_models/dec_d5_prioritering.json`

In practice this means some public drill-downs still carry English evidence lines, long raw extraction blocks, or overly rough fragments.

### 5. Perspective mapping is mostly in place, but one gap remains visible
The audit finds `20` claims without a strong perspective mapping. The main affected topic is:
- `governance_and_finance.other`

That topic needs structural cleanup rather than only better wording.

## Immediate Follow-On Use
This audit points directly to the next cleanup sprints:
- `26.2` for claim-text cleanup
- `27.x` for splitting broad rest buckets
- `28.3` for moving rough drill-down content behind cleaner public summaries

## Working Rule
Use this audit as the internal baseline for future data-quality work. Do not expose it directly on the public site.
