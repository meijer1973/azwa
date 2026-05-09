# Pre-contact Internal Dry Run

## Summary
Current sprint: Sprint 33.P5 - Pre-contact validation-readiness: internal dry run.

Generated on: 2026-05-09.

This file defines the internal dry-run cases for the prepared D5/D6 stakeholder packets. It is not a stakeholder validation record and it does not authorize contact with policymakers.

Human reviewers should work in the Excel validation workbooks, not in raw CSV files. The CSV packet paths below are repository traceability references: they help the repository team verify that returned answers can be mapped back to `vraag_id`, packet routing and processing targets.

Repository check status: `completed`.

Human dry-run status: `pending_internal_reviewers`.

Gate effect: Blocks P7 send-readiness until human reviewers complete the cases; does not block P6 workflow integration.

## Automated Checks

| Check | Status |
| --- | --- |
| Packet index loads and contains prepared packets. | `pass` |
| All packet drafts remain prepared_not_sent. | `pass` |
| Required dry-run cases are resolvable to exact packet rows. | `pass` |
| Dry-run CSVs expose answer, evidence and not-my-domain fields. | `pass` |
| Packet sizes remain reviewable. | `pass` |

## Reviewer Roles

| Role | What to test |
| --- | --- |
| `policy_reviewer` | Plain-language policy meaning, safe wording and decision-risk clarity. |
| `finance_reviewer` | Funding-line, structural/project and double-counting questions. |
| `data_repository_reviewer` | Vraag_id preservation, answer-processing route and not-my-domain rerouting. |
| `subject_reviewer` | Whether a domain expert can answer from the filtered packet alone. |

## What The Human Reviewer Should Do

1. Open the workbook named in the case detail.
2. Go to the listed sheet and row.
3. Answer only that row using the workbook's dropdowns, short note fields and evidence fields. For D5 owner, party or action-holder fields, choose from the dropdown where possible and use `Anders, toelichten` only when the list is missing the right option.
4. If the row is outside the reviewer's domain, choose or write `niet mijn domein` and name the better owner if known.
5. Record whether the row was easy to understand, what evidence would be attached, and whether any dropdown option was missing.
6. Do not use the CSV as the human form. The repository team uses the CSV path only to check traceability and export shape.

The dry run tests usability and processability. It is not asking reviewers to validate all D5/D6 content and it does not create stakeholder evidence.

## Dry-run Cases

| Case | Packet | Vraag ID | Test | Expected route |
| --- | --- | --- | --- | --- |
| `P5-CASE-001` | `welzijn_sociale_basis` | `D5-SV-001` | Test whether a busy social-base reviewer can answer a D5 sociaal-verwijzen row without opening the full workbook. | `validation_log_or_decision_ticket` |
| `P5-CASE-002` | `wijkteams_slt_leads` | `D6-WIJK-001` | Test whether a Wijkteams/SLT reviewer can classify the D6 relation from the packet row and evidence fields. | `d6_validation_log_or_register_update` |
| `P5-CASE-003` | `finance_controller` | `D5-NNZ-004` | Test whether finance can evaluate a component-level budget question now that the separate D5 finance tab has been removed. | `validation_log_or_finance_ticket` |
| `P5-CASE-004` | `gemeente_almere_sociaal_domein_d6` | `D6-SLT-001` | Test whether a formal-decision interpretation can be answered only with an explicit evidence type and reference. | `d6_validation_log_or_decision_ticket` |
| `P5-CASE-005` | `zorgverzekeraar_zvw` | `D5-SV-001` | Test whether a reviewer can mark a row as not-my-domain and route it to the better owner without losing vraag_id traceability. | `reroute_or_validation_log_note` |

## Case Details

### P5-CASE-001 - d5_tab_answerability

Packet: `welzijn_sociale_basis` (Welzijn en sociale basis)

Human workbook: `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`

Repository CSV reference: `data/workagenda/precontact_packets/welzijn_sociale_basis.csv`

Vraag ID: `D5-SV-001`

Sheet: `Sociaal verwijzen` row `5`

Question: Capaciteit brede gesprek huisarts/eerstelijn

Reviewer role: `policy_or_subject_reviewer`

Expected processing route: `validation_log_or_decision_ticket`

What the reviewer does:

- Open `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`.
- Go to sheet `Sociaal verwijzen`, row `5`.
- Use the workbook dropdowns and evidence fields to answer just this row. Check whether owner/party/action-holder dropdowns are sufficient.
- Note whether wording, answer options or evidence instructions need improvement before stakeholder contact.

Pass criteria:

- Reviewer can find the indicated workbook sheet and row without repository help.
- Reviewer can understand what is being asked in the Excel workbook.
- Reviewer can choose an answer, mark unknown, or mark not-my-domain.
- Reviewer can name evidence type and evidence reference when claiming confirmation.
- Repository reviewer can map the Excel answer back to vraag_id and packet_id using the dry-run case reference.
- Repository team can route the answer to the expected processing route.

Failure triggers:

- Question requires a broad explanation instead of a choice or short correction.
- Reviewer cannot tell whether evidence is required.
- Reviewer needs raw CSV or repository JSON to answer the human-facing question.
- Not-my-domain answer has no clear reroute target.
- Answer would silently become a source claim instead of a validation record.

### P5-CASE-002 - d6_tab_answerability

Packet: `wijkteams_slt_leads` (Wijkteams / SLT-leads)

Human workbook: `docs/review/Almere_D6_validatieformats.xlsx`

Repository CSV reference: `data/workagenda/precontact_packets/wijkteams_slt_leads.csv`

Vraag ID: `D6-WIJK-001`

Sheet: `Wijkteams` row `7`

Question: D6-relatie: Welke beschrijving past bij Wijkteams Almere?

Reviewer role: `subject_reviewer`

Expected processing route: `d6_validation_log_or_register_update`

What the reviewer does:

- Open `docs/review/Almere_D6_validatieformats.xlsx`.
- Go to sheet `Wijkteams`, row `7`.
- Use the workbook dropdowns and evidence fields to answer just this row.
- Note whether wording, answer options or evidence instructions need improvement before stakeholder contact.

Pass criteria:

- Reviewer can find the indicated workbook sheet and row without repository help.
- Reviewer can understand what is being asked in the Excel workbook.
- Reviewer can choose an answer, mark unknown, or mark not-my-domain.
- Reviewer can name evidence type and evidence reference when claiming confirmation.
- Repository reviewer can map the Excel answer back to vraag_id and packet_id using the dry-run case reference.
- Repository team can route the answer to the expected processing route.

Failure triggers:

- Question requires a broad explanation instead of a choice or short correction.
- Reviewer cannot tell whether evidence is required.
- Reviewer needs raw CSV or repository JSON to answer the human-facing question.
- Not-my-domain answer has no clear reroute target.
- Answer would silently become a source claim instead of a validation record.

### P5-CASE-003 - finance_row

Packet: `finance_controller` (Finance/controller)

Human workbook: `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`

Repository CSV reference: `data/workagenda/precontact_packets/finance_controller.csv`

Vraag ID: `D5-NNZ-004`

Sheet: `Nu Niet Zwanger` row `8`

Question: Toegankelijke anticonceptiezorg en budget

Reviewer role: `finance_reviewer`

Expected processing route: `validation_log_or_finance_ticket`

What the reviewer does:

- Open `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`.
- Go to sheet `Nu Niet Zwanger`, row `8`.
- Use the workbook dropdowns and evidence fields to answer just this row. Check whether owner/party/action-holder dropdowns are sufficient.
- Note whether wording, answer options or evidence instructions need improvement before stakeholder contact.

Pass criteria:

- Reviewer can find the indicated workbook sheet and row without repository help.
- Reviewer can understand what is being asked in the Excel workbook.
- Reviewer can choose an answer, mark unknown, or mark not-my-domain.
- Reviewer can name evidence type and evidence reference when claiming confirmation.
- Repository reviewer can map the Excel answer back to vraag_id and packet_id using the dry-run case reference.
- Repository team can route the answer to the expected processing route.

Failure triggers:

- Question requires a broad explanation instead of a choice or short correction.
- Reviewer cannot tell whether evidence is required.
- Reviewer needs raw CSV or repository JSON to answer the human-facing question.
- Not-my-domain answer has no clear reroute target.
- Answer would silently become a source claim instead of a validation record.

### P5-CASE-004 - evidence_field

Packet: `gemeente_almere_sociaal_domein_d6` (Gemeente Almere sociaal domein - D6 validatie)

Human workbook: `docs/review/Almere_D6_validatieformats.xlsx`

Repository CSV reference: `data/workagenda/precontact_packets/gemeente_almere_sociaal_domein_d6.csv`

Vraag ID: `D6-SLT-001`

Sheet: `SLT` row `7`

Question: Formele betekenis: Wat regelt de SLT-besluitroute formeel voor D6?

Reviewer role: `policy_reviewer`

Expected processing route: `d6_validation_log_or_decision_ticket`

What the reviewer does:

- Open `docs/review/Almere_D6_validatieformats.xlsx`.
- Go to sheet `SLT`, row `7`.
- Use the workbook dropdowns and evidence fields to answer just this row.
- Note whether wording, answer options or evidence instructions need improvement before stakeholder contact.

Pass criteria:

- Reviewer can find the indicated workbook sheet and row without repository help.
- Reviewer can understand what is being asked in the Excel workbook.
- Reviewer can choose an answer, mark unknown, or mark not-my-domain.
- Reviewer can name evidence type and evidence reference when claiming confirmation.
- Repository reviewer can map the Excel answer back to vraag_id and packet_id using the dry-run case reference.
- Repository team can route the answer to the expected processing route.

Failure triggers:

- Question requires a broad explanation instead of a choice or short correction.
- Reviewer cannot tell whether evidence is required.
- Reviewer needs raw CSV or repository JSON to answer the human-facing question.
- Not-my-domain answer has no clear reroute target.
- Answer would silently become a source claim instead of a validation record.

### P5-CASE-005 - not_my_domain_reroute

Packet: `zorgverzekeraar_zvw` (Zorgverzekeraar/Zvw)

Human workbook: `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`

Repository CSV reference: `data/workagenda/precontact_packets/zorgverzekeraar_zvw.csv`

Vraag ID: `D5-SV-001`

Sheet: `Sociaal verwijzen` row `5`

Question: Capaciteit brede gesprek huisarts/eerstelijn

Reviewer role: `data_repository_reviewer`

Expected processing route: `reroute_or_validation_log_note`

What the reviewer does:

- Open `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`.
- Go to sheet `Sociaal verwijzen`, row `5`.
- Use the workbook dropdowns and evidence fields to answer just this row. Check whether owner/party/action-holder dropdowns are sufficient.
- Note whether wording, answer options or evidence instructions need improvement before stakeholder contact.

Pass criteria:

- Reviewer can find the indicated workbook sheet and row without repository help.
- Reviewer can understand what is being asked in the Excel workbook.
- Reviewer can choose an answer, mark unknown, or mark not-my-domain.
- Reviewer can name evidence type and evidence reference when claiming confirmation.
- Repository reviewer can map the Excel answer back to vraag_id and packet_id using the dry-run case reference.
- Repository team can route the answer to the expected processing route.

Failure triggers:

- Question requires a broad explanation instead of a choice or short correction.
- Reviewer cannot tell whether evidence is required.
- Reviewer needs raw CSV or repository JSON to answer the human-facing question.
- Not-my-domain answer has no clear reroute target.
- Answer would silently become a source claim instead of a validation record.

Expected reroute candidates:

- `welzijn_sociale_basis`
- `gemeente_almere_sociaal_domein_d5`

## Human Completion Required

- Select 2-4 internal reviewers before stakeholder contact.
- Have them complete the five dry-run cases in the human-facing Excel workbooks, using workbook path, sheet and row from this note.
- For D5 cases, test the owner/party/action-holder dropdowns and report whether an expected owner option is missing.
- Use CSV packet paths only as repository traceability/export references, not as the normal human entry surface.
- Record time-to-answer, confusing wording, missing dropdown options, evidence ambiguity and reroute clarity.
- Apply workbook or packet fixes before the P7 send-readiness gate.

## Next Step

Sprint 33.P6 can proceed with repository/workflow integration while this human dry run is pending. Sprint 33.P7 send-readiness remains blocked until internal reviewers complete these cases and any required packet fixes are made.
