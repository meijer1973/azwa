# Sprint 25.2 - Lokale bronversterking Almere

## Summary
Status: completed.

Sprint 25.2 heeft de publieke lokale bronbasis voor Almere versterkt. De sprint is afgesloten op de grens van wat met publieke bronnen verantwoord kan worden gevuld: ontbrekende niet-publieke informatie, lokale medewerkerskennis en formele besluitvragen zijn carry-over voor latere validatie en besluitvorming, geen blocker voor deze publieke bronversterkingsfase.

## Opgeleverd
- Nieuwe en bijgewerkte bronversterkingslaag: `data/extracted/local_source_strengthening_almere.json`.
- Publieke bronprobe en intakebeoordeling: `docs/internal/source-intake/phase25.2-public-source-assessment.md`.
- Eerste formele Documentwijzer-intake voor Visie Gezondheidsbeleid, Brede SPUK/GALA en Maatschappelijke Agenda.
- Page-markdownconversie voor de geselecteerde Documentwijzer-PDF's voordat ze in de pipeline zijn verwerkt.
- Eerste formele GGD/ZonMw-intake: GGD Flevoland tabellenboeken 2024 voor volwassenen en ouderen, GGD Valpreventie Gemeente Almere, en ZonMw Doorontwikkeling Zorgzaam Flevoland.
- Regeneratie van inventory, extracties, claims, site-viewmodels en intern dashboard.

## Belangrijkste guardrails
- Publieke bronnen gaan eerst; niet-publieke informatie wordt niet als blocker behandeld, maar als latere invulvraag.
- Interne researchdocumenten blijven signalen voor bronhiaten en mogen niet als bronfeit worden gepromoveerd.
- Generated claims uit de nieuwe Documentwijzer-, GGD- en ZonMw-bronnen blijven reviewmateriaal totdat ze voor bestuurlijke of public-facing tekst worden gebruikt.
- Publieke pagina's met contactpersonen, telefoonnummers of e-mailadressen mogen alleen via een geschoonde rol/geografie-extractie in de formele corpuslaag komen.

## Carry-over
- Sprint 25.3 vult per werkagenda-target de publieke nulmeting, capaciteit, dekking, doelgroep en bronstatus zo ver mogelijk in.
- De ontbrekende raadsbrief `Stand van zaken Gezondheidsbeleid (IZA en GALA)` van 2 februari 2025 gaat naar lokale validatie als publieke zoekslag uitgeput blijft.
- De MGN-rol/geografievraag gaat naar een geschoonde rolvalidatie, niet naar directe corpusintake van contactgegevens.
- Als publieke bronnen geen capaciteit, budget, eigenaar, schaalkeuze of prioritering geven, wordt dat een invulvraag voor lokale medewerkers of een besluitvraag voor later in de workflow.

## Controle
- Pipeline en dashboard zijn opnieuw gegenereerd na de intake.
- `python -m pytest tests/test_pipeline_graph.py` is uitgevoerd en gaf 7 geslaagde tests.
- Python compile- en JSON-controles zijn uitgevoerd.
- Een contactdetail-scan op gegenereerde outputs gaf geen matches.
