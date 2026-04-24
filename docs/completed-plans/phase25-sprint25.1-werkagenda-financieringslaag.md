# Sprint 25.1 - Werkagenda- en financieringslaag

## Summary
Status: completed.

Sprint 25.1 heeft een eerste operationele D5-werkagendalaag toegevoegd. De laag maakt de werkagenda-targets, verplichte velden, financieringsstreams, reviewvragen en guardrails zichtbaar zonder Almeerse conceptinvulling als vastgesteld besluit te presenteren.

## Opgeleverd
- Nieuwe generator: `src/build_workagenda_d5_operational_requirements.py`.
- Nieuwe datalaag: `data/extracted/workagenda_d5_operational_requirements.json`.
- `data/extracted/claims/d5_d6_master.json` gebruikt de werkagendalaag nu voor D5-basisfunctionaliteiten, ontwikkelagenda 1 en optionele/overige initiatieven.
- `docs/internal/review-dashboard.html` heeft een interne `Werkagenda`-tab met targets, status, financieringshints en reviewvragen.

## Belangrijkste guardrails
- `almere_local_decisions.json` blijft leidend voor menselijke lokale keuzes; zolang `decision_count` nul is, mag conceptinvulling niet klinken als vastgesteld Almeers beleid.
- Interne documenten zoals `conceptinvulling_werkagenda_azwa_almere.md` en `Samenvatting werkagenda.docx` zijn research-signalen, geen publieke bronfeiten.
- AZWA-D5/SPUK, Zvw/verzekeraar, GALA/SPUK, PGA/IZA-transformatie en reguliere gemeentelijke middelen blijven gescheiden om dubbeltelling te voorkomen.

## Open vervolgpunten
- Sprint 25.2 moet de genoemde primaire lokale en rolbronnen verder versterken.
- Sprint 25.3 moet de nulmeting en lokale capaciteit per basisfunctionaliteit vullen.
- Exacte budgetverdeling, prioritering 2027-2030, collegebesluitvorming en lokale eigenaarschap blijven review- of besluitpunten.
