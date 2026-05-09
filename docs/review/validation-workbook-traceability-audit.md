# Validation Workbook Traceability Audit

## Summary
Sprint covered: Sprint 33.P1 - Pre-contact validation-readiness: add IDs, routing and traceability.

Generated on: 2026-05-03.

This audit checks whether the current D5 and D6 Excel validation workbooks can be traced back into the repository before contact with policymakers. The workbooks remain pre-validation instruments, not source evidence, final policy truth or stakeholder validation results.

## Bottom Line

Repository-side traceability is now available through:

`data/workagenda/validation_workbook_traceability_map.json`

The map assigns stable generated `vraag_id` values, component IDs, stakeholder packages, answer types, evidence requirements, repo-update effects and deadlines to the validation rows found in both workbooks.

The Excel workbooks themselves are **not yet send-ready as raw stakeholder packets**, because most validation rows do not visibly contain all traceability metadata columns. Before sending, filtered packets should either include the generated IDs/metadata as visible or protected columns, or be exported from the traceability map so returned answers cannot lose their row identity.

## Scope Checked

| Workbook | Path | Mapped validation rows | Result |
| --- | --- | ---: | --- |
| D5 validatieformat werkagenda Almere | `docs/review/D5_validatieformat_werkagenda_Almere_v0.5.xlsx` | 154 | Traceability map created; workbook still lacks visible per-row metadata fields. |
| Almere D6 validatieformats | `docs/review/Almere_D6_validatieformats.xlsx` | 91 | Traceability map created; workbook still lacks visible per-row metadata fields. |
| Total |  | 245 | All generated IDs are unique. |

## Required Traceability Fields

The traceability map provides these fields per validation row:

| Field | Purpose |
| --- | --- |
| `vraag_id` | Stable row identity for returned answers. |
| `component_id` | Links the answer to a D5 or D6 component. |
| `stakeholderpakket` | Indicates who should answer. |
| `antwoordtype` | Indicates whether the row is a dropdown, role matrix, finance matrix, dependency matrix or similar. |
| `validatiestatus_default` | Starts returned answers as not yet asked unless later validation changes that. |
| `bewijstype_verplicht` | Marks that an answer needs evidence or an explicit no-evidence note. |
| `repo_update_effect` | Tells the team whether the answer updates a validation log, finance matrix, decision register, dependency map, status matrix or D6 register. |
| `deadline` | Keeps the question tied to the pre-contact send-readiness workflow. |

## Workbook Coverage Finding

The workbooks already contain useful human-facing fields:

- current working hypotheses;
- validation or status fields on many D5 sheets;
- evidence type or evidence reference fields;
- stakeholder packet overview tabs;
- safe provisional wording in the D6 workbook.

The workbooks do **not** consistently expose the repository traceability fields per row:

| Gap | Effect |
| --- | --- |
| No visible `vraag_id` per row | Returned answers can be ambiguous if rows are moved, copied or filtered. |
| No visible `component_id` per row | Import depends on sheet identity unless the traceability map is used. |
| No per-row `stakeholderpakket` | Packet routing is sheet-level, not row-level. |
| No explicit `antwoordtype` | Processing route must be inferred from sheet type unless map is used. |
| No explicit `repo_update_effect` | Returned answers could be applied inconsistently without the map. |
| D6 sheets mostly lack `validatiestatus` and `deadline` columns | Follow-up tracking must be added in packets or validation logs. |

## Import Rule

Returned answers must not be copied into policy text or source claims directly.

| Answer type | Processing route |
| --- | --- |
| Public source found | Add source, ingest, rerun/check evidence layer. |
| Stakeholder confirmation | Add to validation log. |
| Finance/controller confirmation | Add to finance matrix and validation log. |
| Formal decision | Add to decision register and evidence log. |
| Conflicting answers | Mark review needed. |
| Unknown or not my domain | Keep unresolved or reroute. |

## Sprint 33.P1 Result

Sprint 33.P1 is complete at repository-map level:

- D5 and D6 workbook rows have generated stable IDs in the traceability map.
- Row-level stakeholder routing exists in the map.
- Row-level answer type, evidence requirement, repo-update effect and default deadline exist in the map.
- Duplicate generated IDs: 0.

Sprint 33.P1 does **not** make the workbooks ready to send by itself. Send-readiness still requires Sprint 33.P2-P7:

- current working view audit;
- visible or protected metadata in outgoing packets;
- targeted pre-contact checks;
- filtered stakeholder packets;
- internal dry run;
- response-processing workflow;
- send-readiness gate.

## Next Step

Sprint 33.P2 should audit the human-facing current working views and language. It should check whether every relevant tab has concise Dutch wording, no internal repository terms, no blank broad questions and clear evidence instructions.
