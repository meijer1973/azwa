## Phase 14: Supporting Pages And Traceability

This milestone extends the public executive site beyond the first five primary pages.

Added generated site layers:
- `Thema's` overview and detail pages
- `Referentie` overview, topic index, and topic detail pages
- `Bronnen` overview and source detail pages

Key implementation choices:
- the site continues to be generated from the existing claim, interpretation, and Almere layers
- public wording stays careful: derived agenda items remain `mogelijke besluitvragen` and `mogelijke opvolgacties`
- source traceability now prefers internal source detail pages where available, with the original external URL still visible on the source page itself
- logical clickability is treated as a regression concern and is now covered in site-generation tests

Quality improvements in this phase:
- broader Dutch view-model generation for themes, topics, and sources
- clearer public labels for source classifications and document types
- cleaner topic labels for previously raw topic identifiers
- deduplicated evidence presentation on public detail pages where repeated source-topic combinations added no new value

Verification:
- `python -m unittest discover -s tests -p "test_*.py"`
- `python src/run_pipeline.py --all --dry-run`
