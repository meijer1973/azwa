# Phase 16 - Timeline curation and executive timeline UI

This phase upgrades the timeline in two ways:

1. A curated source file now exists at `config/timeline_curation.json`.
2. The public timeline now opens with the current year first and keeps each entry compact until a reader opens the detail block.

## What changed

- Added `config/timeline_curation.json` as the curated input for:
  - corpus document moments
  - claim-based future references
  - external website-only or web-discovered timeline signals
- Expanded the 2026 timeline with:
  - BZK monitoring signal on tasks / means / execution
  - stand januari 2026 gemeentefonds
  - BO IZA/AZWA doorbraakmiddelen
  - Monitor Digitale Zorg 2025
  - expected meicirculaire gemeentefonds 2026
  - transformatieplan and SPUK timing references
- Reordered the page so `2026` appears first and is open by default.
- Changed timeline entries into nested `details` blocks so the top-level scan stays short.
- Updated regression tests to check:
  - `2026` renders before later years
  - timeline entries are collapsible
  - key 2026 items like the meicirculaire and BO IZA/AZWA moment are present

## Source model

The site now uses two timeline layers:

- `config/timeline_curation.json`
  Curated maintenance file for important dated moments.
- `data/site/timeline_register.json`
  Generated register used by the site.

This split makes it easier to add website-only milestones without forcing them into the main document corpus first.

## Verification

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py"
python src/run_pipeline.py --all --dry-run
```
