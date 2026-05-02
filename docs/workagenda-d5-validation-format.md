# Werkagenda D5 validation format

## Summary
Current sprint: Sprint 32.2 - D5-validatie voorbereiden.

This is the practical handoff format for D5 validation. It groups the constrained ticket set into stakeholder packets and writes CSV forms that can be opened as spreadsheets or converted into Excel/form tooling.

Machine-readable packet index: `data/workagenda/d5_validation_packets.json`.

## How To Use

Send only the relevant packet to each stakeholder group. Ask them to fill `answer`, add a short correction if needed, choose or name the evidence type, and provide an evidence path or document reference. Blank answers remain unresolved.

## Packet Overview

| Packet | Purpose | Tickets | CSV form |
| --- | --- | ---: | --- |
| D6-afhankelijkheden | D6 preconditions needed for D5 execution. | 9 | `data/workagenda/validation_packets/d6_afhankelijkheden.csv` |
| Besluitvorming en fasering | Decision owner, phasing toward 2027-2030 and governance escalation. | 9 | `data/workagenda/validation_packets/besluitvorming_en_fasering.csv` |
| Finance/controller en zorgverzekeraar | Funding line, structural/project status, double-counting risk and insurer/Zvw confirmation. | 9 | `data/workagenda/validation_packets/finance_controller_en_zorgverzekeraar.csv` |
| Gemeente Almere beleid en sociaal domein | Local status, capacity, ownership, local coverage and social-domain implementation. | 5 | `data/workagenda/validation_packets/gemeente_almere_beleid_en_sociaal_domein.csv` |
| JGZ / GGD Flevoland | JGZ, GGD, prevention, monitoring and public-health role validation. | 6 | `data/workagenda/validation_packets/jgz_ggd_flevoland.csv` |
| Zorgverzekeraar / Zvw | Zvw, contracting, insurer role and care-professional funding questions. | 9 | `data/workagenda/validation_packets/zorgverzekeraar_zvw.csv` |

## Completion Rule

Sprint 32.2 is repository-side complete when these packet forms exist, remain constrained, and keep evidence gates visible. Sprint 32.3 remains blocked until completed stakeholder answers or explicit policy decisions are available.

## Guardrails

- These packet forms are not validation results.
- Do not fill blank answers from repository inference.
- Do not use finance, governance or D6 dependency answers unless evidence is recorded.
- Keep unresolved answers as validation, finance, decision or dependency tickets.
