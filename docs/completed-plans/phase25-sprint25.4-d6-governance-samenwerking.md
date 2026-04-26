# Sprint 25.4 - D6 governance en samenwerking

## Summary
Status: completed.

Sprint 25.4 heeft de D6-governance en samenwerking uitgewerkt als publieke prefill- en validatielaag. De laag maakt per D6-dimensie zichtbaar welke publieke claims beschikbaar zijn, welke actorrollen als publieke rolhypothese of bronstatus kunnen worden gebruikt, en welke verantwoordelijkheidssloten lokaal moeten worden bevestigd.

## Opgeleverd
- Bijgewerkte generator: `src/build_d6_governance_collaboration.py`.
- Bijgewerkte datalaag: `data/extracted/d6_governance_collaboration.json`.
- Dashboardweergave onder de D6 Governance-tab met dimensies, actorrollen, verantwoordelijkheidsprefill en besluitvragen.
- Pipeline-registratie voor de Sprint 25.4-laag.

## Publieke basis
- Claims uit `data/extracted/claims/claims_master.jsonl`.
- Regionale rollen en schaalguardrails uit `data/curated/regional_roles_and_splits_almere_flevoland.json`.
- Nulmeting en capaciteit uit `data/extracted/workagenda_nulmeting_capacity.json`.

## Belangrijkste guardrails
- Publieke bronnen vullen de structuur; niet-publieke rolverdeling, mandaat, budget, monitoring en schaalkeuzes blijven lokale validatie of latere besluitvorming.
- IZA/AZWA-regio, GGD-regio, zorgkantoorregio en lokale uitvoering blijven strikt gescheiden.
- Actorrollen zijn geen bestuurlijk besluit tenzij een bronpassage of lokale validatie dat expliciet bevestigt.
- De laag is intern werkmateriaal en geen public-facing beleidsbron.

## Carry-over
- Lokale medewerkers moeten bevestigen welke lokale teams, wijkverbanden, inloopvoorzieningen, sociale-basispartners en aanspreekpunten meetellen.
- Formele mandaat-, budget-, monitorings- en schaalkeuzes moeten na lokale validatie naar besluitvorming wanneer publieke bronnen geen vastgesteld antwoord geven.
- Sprint 25.5 kan de Almere/Flevoland-bronbasis verder aanvullen rond AZWA, IZA, GALA, preventie, sociaal domein en gezondheid.

## Controle
- `python src/build_d6_governance_collaboration.py` is uitgevoerd.
- Python compile-controle voor de D6-generator en het interne dashboard is uitgevoerd.
