# Validation Workbook Prefill Audit

## Summary
Sprint covered: Sprint 33.P2 - Pre-contact validation-readiness: prefill audit and current working views.

Generated on: 2026-05-09.

This audit checks whether the D5 and D6 validation workbooks are understandable before stakeholder contact. It checks current working views, answer/correction fields, evidence fields, broad questions and internal jargon. It does not validate the policy content.

## Bottom Line

The workbooks are usable as pre-contact drafts, but they still need packet cleanup before sending. D5 is stronger on row-level current working hypotheses and validation/evidence fields. D6 is stronger on short safe/unsafe wording blocks. The remaining work is to make those strengths consistent in the exported stakeholder packets.

## Headline Counts

| Check | Count |
| --- | ---: |
| Human-facing sheets audited | 25 |
| Validation rows covered by traceability map | 189 |
| Sheets missing a current working view | 2 |
| Sheets missing an assessment/selection field | 0 |
| Sheets missing a correction/toelichting field | 1 |
| Sheets missing an evidence field | 0 |
| Sheets with language cleanup flags | 2 |
| Sheets with broad-question flags | 2 |

## Workbook Findings

### D5 Workbook

Path: `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`

| Sheet | Status | Main cleanup need |
| --- | --- | --- |
| Overzicht D5 | needs cleanup | Add or clarify a short correction/toelichting field. |
| Laagdremp. steunpunten | ok | No immediate prefill cleanup flagged. |
| Sociaal verwijzen | ok | No immediate prefill cleanup flagged. |
| Mentale gezondheid | ok | No immediate prefill cleanup flagged. |
| Valpreventie | ok | No immediate prefill cleanup flagged. |
| Overgewicht volwassenen | ok | No immediate prefill cleanup flagged. |
| Kansrijke Start | ok | No immediate prefill cleanup flagged. |
| Integrale gezinspoli | ok | No immediate prefill cleanup flagged. |
| Nu Niet Zwanger | ok | No immediate prefill cleanup flagged. |
| Overgewicht kinderen | ok | No immediate prefill cleanup flagged. |
| Optionele ontwikkelagenda | ok | No immediate prefill cleanup flagged. |
| Monitoring cyclus | needs cleanup | Add a concise current working view before stakeholder contact. |
| D6 afhankelijkheden | needs cleanup | Add a concise current working view before stakeholder contact. |

### D6 Workbook

Path: `docs/review/Almere_D6_validatieformats.xlsx`

| Sheet | Status | Main cleanup need |
| --- | --- | --- |
| Inloopvoorzieningen | needs cleanup | Replace English/technical terms with plain Dutch policy language. |
| Wijkteams | ok | No immediate prefill cleanup flagged. |
| SLT | ok | No immediate prefill cleanup flagged. |
| JGZ Almere | ok | No immediate prefill cleanup flagged. |
| GGD Flevoland | ok | No immediate prefill cleanup flagged. |
| Gezonde School | needs cleanup | Narrow broad monitoring/owner questions before packet export. |
| Monitoring | ok | No immediate prefill cleanup flagged. |
| Samen Sterker | needs cleanup | Narrow broad monitoring/owner questions before packet export. |
| PGA-Zorgzaam-Flever | needs cleanup | Replace English/technical terms with plain Dutch policy language. |
| Digitaal-operationeel | ok | No immediate prefill cleanup flagged. |
| Informele steun | ok | No immediate prefill cleanup flagged. |
| Financiering | ok | No immediate prefill cleanup flagged. |

## Cross-workbook Findings

- The workbooks already avoid the biggest anti-pattern: they do not ask stakeholders to start from a blank sheet.
- D5 component sheets usually contain row-level `Huidige werkhypothese`, status, correction and evidence columns.
- D6 component sheets usually contain concise current working view, safe wording and unsafe wording blocks.
- Some D5 matrix tabs are operational control sheets rather than stakeholder-friendly tabs; they need current-view or instruction cleanup before packet export.
- Some D6 text still uses English or technical wording such as `evidence` or `social-base`; replace this with plain Dutch in outgoing packets.
- Monitoring rows still contain generic prompts that should be narrowed before sending to busy stakeholders.

## Required Before Sending

- Keep generated `vraag_id` values from the traceability map in outgoing packets.
- Add or preserve a concise current working view for each exported tab.
- Add a clear confirm/correct choice where the current workbook only has open text.
- Keep evidence fields visible in every packet.
- Replace internal or English technical terms in stakeholder-facing text.
- Narrow broad monitoring questions into concrete validation choices where possible.

## Next Step

Sprint 33.P3 should prepare targeted pre-contact agents. Use agents only for evidence-prefill audit, policymaker readability, D5-D6 dependency mapping, finance-risk precheck and the end-May handreiking watchlist. Do not start broad D5 or D6 research.
