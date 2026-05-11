# Werkagenda D5 statusmatrix v1

## Summary
Current sprint: Sprint 32.1 - D5-statusmatrix bouwen.

This is the first central D5 delivery-status matrix. It does not draft the workagenda and it does not validate local choices. It translates the existing D5 workagenda requirements and public-source nulmeting into red/yellow/gray steering rows.

Machine-readable version: `data/workagenda/d5_status_matrix.json`.

## Current Steering Summary

- D5 components tracked: 11.
- Required components: 9.
- Ready for workagenda drafting: 0.
- Risk counts: {"geel": 5, "grijs": 2, "rood": 4}.

No row is ready for drafting yet. The next sprint should turn these rows into constrained validation tickets and formats.

## Matrix

| D5 component | Required | Public foundation | Risk | Main blocker | Next action |
| --- | --- | --- | --- | --- | --- |
| Laagdrempelige steunpunten | Yes | deels | geel | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Welke bestaande Almeerse steunpunten tellen mee voor de werkagenda? |
| Sociaal verwijzen | Yes | sterk | geel | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Welke actuele Almeerse verwijzingsroute en brugfunctie bestaan al? |
| Valpreventie | Yes | sterk | geel | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Wat is het actuele aantal 65-plussers per peildatum? |
| Ketenaanpak overgewicht en obesitas volwassenen | Yes | deels | geel | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Welke GLI-capaciteit en leefstijl-/beweegcapaciteit zijn in Almere beschikbaar? |
| Kansrijke Start | Yes | zwak | rood | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Welke actuele coalitie Kansrijke Start bestaat in gemeente Almere en, waar relevant, op IZA/AZWA-regio Flevoland-schaal? |
| Integrale gezinspoli | Yes | zwak | rood | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Is er in Almere of Flevoland al een integrale gezinspoli of voorbereiding? |
| Nu Niet Zwanger | Yes | zwak | rood | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Wordt NNZ bestuurlijk op GGD-regio, IZA/AZWA-regio of gemeentelijke schaal georganiseerd? |
| Mentale gezondheidsnetwerken | Yes | deels | geel | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Welk MGN-transformatieplan is leidend voor gemeente Almere en, waar relevant, de IZA/AZWA-regio Flevoland? |
| Ketenaanpak overgewicht en obesitas kinderen | Yes | zwak | rood | finance, owner, decision, D6 dependency | Prepare constrained validation ticket: Wat is het actuele aantal jeugdigen per peildatum? |
| Ontwikkelagenda 1 nieuw: dementie, nicotinevrij, rookvrije start, multiproblematiek NPLV | Conditional | zwak | grijs | scope choice | Decide whether this optional/conditional item belongs in the gemeente Almere and IZA/AZWA-regio Flevoland workagenda scope. |
| Ontwikkelagenda 2 en overige initiatieven | Conditional | zwak | grijs | scope choice | Decide whether this optional/conditional item belongs in the gemeente Almere and IZA/AZWA-regio Flevoland workagenda scope. |

## Field Status Meaning

The machine-readable matrix scores each component on these fields:

- `huidige_situatie`
- `gewenste_situatie`
- `ingroeipad_2030`
- `aantallen_capaciteit`
- `financiering`
- `verantwoordelijkheid_governance`
- `monitoring_lerende_cyclus`
- `mijlpalen`
- `d6_afhankelijkheden`
- `open_besluiten_risicos`

Status codes come from `data/workagenda/d5_stuurmodel.json`: A source-answered, B source-suggested but validation needed, C local validation needed, D decision needed, E finance/controller needed, F insurer/Zvw confirmation needed, G ICT/privacy/data confirmation needed, H awaiting national guidance, I optional/not applicable, J unknown.

## Guardrails

- Treat the matrix as a steering layer only.
- Do not turn yellow or red rows into final workagenda text.
- Do not use finance or governance wording as confirmed until validation evidence exists.
- Keep D6 prerequisites visible as dependencies.
