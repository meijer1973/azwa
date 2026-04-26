# Sprint 25.3 - Nulmeting en capaciteit werkagenda

## Summary
Status: completed.

Sprint 25.3 heeft de D5-werkagenda-structuur zo ver mogelijk gevuld met publieke nulmetings- en capaciteitsinformatie. Waar publieke bronnen geen bestaand aanbod, capaciteit, fte, wachttijden, wijkspreiding, budget, eigenaar of besluitstatus geven, zijn deze velden expliciet als lokale invul- of besluitvragen vastgelegd.

## Opgeleverd
- Nieuwe generator: `src/build_workagenda_nulmeting_capacity.py`.
- Nieuwe datalaag: `data/extracted/workagenda_nulmeting_capacity.json`.
- Dashboardweergave onder de Werkagenda-tab met publieke indicatoren, indicatieve berekeningen en lokale invulvelden.
- Pipeline-registratie voor de Sprint 25.3-laag.

## Publieke basis
- Werkagenda-targets uit `data/extracted/workagenda_d5_operational_requirements.json`.
- Publieke bronversterking uit `data/extracted/local_source_strengthening_almere.json`.
- GGD Flevoland 2024-tabellenboeken voor volwassenen en ouderen.
- CBS KWB 2025 Almere-denominator, live geverifieerd op 26 april 2026.

## Belangrijkste guardrails
- De GGD-percentages en CBS-berekeningen zijn publieke prefill en blijven indicatief totdat lokale medewerkers de interpretatie valideren.
- De CBS-denominator is geverifieerd maar nog niet als formele manifestbron opgenomen; voeg die toe als de laag public-facing of auditkritisch wordt.
- Publieke bronnen vullen de structuur; ontbrekende lokale capaciteit of besluitvorming wordt niet verzonnen.

## Carry-over
- Sprint 25.4 moet D6-rollen, schaalniveaus, samenwerking en monitoring expliciet maken.
- Lokale medewerkers moeten aanbod, capaciteit, wachttijden, wijkspreiding, budget, eigenaar en besluitstatus aanvullen waar publieke bronnen stil zijn.
- Onopgeloste prioritering, budget, eigenaarschap en schaalkeuzes gaan na lokale validatie naar besluitvorming.

## Controle
- `python -m pytest tests/test_pipeline_graph.py` is uitgevoerd en gaf 7 geslaagde tests.
- Python compile- en JSON-controles zijn uitgevoerd.
