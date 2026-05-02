# Phase 32 Sprint 32.2 - D5-validatieformats

## Summary
Sprint 32.2 is completed repository-side. It turned the D5 statusmatrix into constrained validation tickets and stakeholder packet formats.

## Outputs

- `data/workagenda/d5_validation_tickets.json`
- `docs/workagenda-d5-validation-tickets.md`
- `src/build_workagenda_d5_validation_tickets.py`
- `tests/test_workagenda_d5_validation_tickets.py`
- `data/workagenda/d5_validation_packets.json`
- `docs/workagenda-d5-validation-format.md`
- `data/workagenda/validation_packets/*.csv`
- `src/build_workagenda_d5_validation_packets.py`
- `tests/test_workagenda_d5_validation_packets.py`

## What Changed

The sprint created 47 constrained D5 validation tickets:

- 9 local status/capacity tickets;
- 9 governance/role tickets;
- 9 finance/controller tickets;
- 9 D6 dependency tickets;
- 9 decision/phasing tickets;
- 2 scope-choice tickets for conditional/optional workagenda items.

It then grouped the tickets into six stakeholder packet CSVs:

- D6-afhankelijkheden;
- Besluitvorming en fasering;
- Finance/controller en zorgverzekeraar;
- Gemeente Almere beleid en sociaal domein;
- JGZ / GGD Flevoland;
- Zorgverzekeraar / Zvw.

## Guardrail

These packet forms are not validation results. Blank answers remain unresolved and must not be filled by repository inference. Sprint 32.3 remains blocked until stakeholder answers, validation records, explicit policy decisions or relevant evidence documents are available.

## Carry Forward

Sprint 32.3 can process completed validation responses when they exist. Repository-side work can continue with Sprint 32.4 source-update watch, because Sprint 32.3 depends on external validation.
