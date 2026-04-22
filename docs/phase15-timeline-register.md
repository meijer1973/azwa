## Phase 15: Timeline Register And Year-Based Timeline View

This milestone upgrades the timeline from a flat page list to a dedicated register plus a richer public view.

Added data output:
- `data/site/timeline_register.json`

Updated site output:
- `data/site/site_timeline_view.json`
- `dist/timeline/index.html`

What changed:
- the timeline now has a dedicated register of source-backed time references
- future references are no longer limited to a few handpicked milestones; they now include linked source basis and related possible besluitvragen or opvolgacties where relevant
- the public timeline groups entries by year
- the current year (`2026`) opens by default
- links from elsewhere on the site can now open collapsed timeline years automatically through hash-target reveal logic

The register contains both:
- source moments such as key national documents
- time references and implementation horizons such as:
  - Q4 2025 national D5 framework
  - Q1 2026 governance and D6 structure references
  - early 2027 mid-term review
  - decision window before 1 July 2027
  - 2027-2028 start package period
  - 2028 update and D6 implementation horizon
  - 2029 local Almere horizon
  - 2030 national rollout horizon

Verification:
- `python -m unittest discover -s tests -p "test_*.py"`
- `python src/run_pipeline.py --all --dry-run`
