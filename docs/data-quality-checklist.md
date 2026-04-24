# Data Quality Checklist

## Purpose
This checklist is the working guide for applying the six quality perspectives in the repository:

- Norm
- Time
- Money
- Governance
- Locality
- Execution

It supports Sprint 24.1 of the long-term roadmap in [phase24-data-quality-roadmap.md](C:/Projects/azwa/docs/phase24-data-quality-roadmap.md).

## Where The Information Is Saved
- Canonical taxonomy: [config/data_quality_perspectives.json](C:/Projects/azwa/config/data_quality_perspectives.json)
- Human checklist: [data-quality-checklist.md](C:/Projects/azwa/docs/data-quality-checklist.md)
- Generated downstream labels: `data/site/*.json` and related generated view-model folders under [data/site](C:/Projects/azwa/data/site)

The rule of thumb is simple:
- `config/` stores machine-readable definitions
- `docs/` stores human-readable working guidance
- `data/site/` stores generated outputs that reuse the taxonomy

## Classification Rule
Before improving a source, claim, or site text block, first decide which of these four content classes it belongs to:

- `source_fact`
  Use when the statement is directly grounded in a source, source quote, explicit table item, or verified source-backed timeline moment.

- `interpretation`
  Use when the statement is a synthesis, best-current reading, or interpretive layer built from multiple grounded sources.

- `local_gap`
  Use when national or regional direction is visible, but explicit local adoption or local documentation is not yet visible in Almere or Flevoland sources.

- `human_choice_question`
  Use when the source base raises a real choice, sequencing question, or interpretation issue that should stay with human reviewers or policymakers.

## Perspective Checklist

### 1. Norm
Check:
- Is this required, allowed, expected, agreed, or only suggested?
- What is the authority level of the source?
- Is the wording on the site stronger than the source justifies?

Common quality problems:
- FAQ or commentary sounds binding
- Lower-authority text is not explicitly attributed
- Agreement text and guidance text are mixed together

Editorial rule:
- Attribute lower-authority sources explicitly in public-facing summaries.

### 2. Time
Check:
- Is there an explicit date, deadline, quarter, year, or expected publication moment?
- Is the timing formal, expected, or inferred?
- Is the item chronologically sorted?
- Does the item belong on the public timeline or only in an internal review queue?

Common quality problems:
- Mixed chronology within a year
- Expected moments shown as hard deadlines
- Local internal timing invented from national milestones

Editorial rule:
- Keep external source-backed moments separate from internal planning.

### 3. Money
Check:
- Does the source define a funding route, budget window, allocation condition, or reporting rule?
- Is there actual evidence for carry-over, reservation, co-financing, or redistribution?
- Is a financial interpretation being overstated as fact?

Common quality problems:
- Rumored rules presented as settled
- Budget categories merged too quickly
- Practical funding guidance treated as norm text

Editorial rule:
- Financial rumors stay out of public-facing conclusions until source-backed.

### 4. Governance
Check:
- Who decides?
- Who coordinates?
- Who owns implementation?
- Who must approve or account?
- Which regional role is meant: formal mandate, coordination, execution, or review signal?

Common quality problems:
- Actor labels are too vague
- Decision, coordination, and execution are blended together
- Regional governance is described without saying which party actually acts
- `mandaatgemeente` is treated as if it also means practical task owner or project lead

Editorial rule:
- Keep ownership, coordination, and approval distinct.
- For Almere/Flevoland regional roles, first check [regional-roles-and-splits-almere-flevoland.md](C:/Projects/azwa/docs/regional-roles-and-splits-almere-flevoland.md).

### 5. Locality
Check:
- Is this explicitly about Almere?
- Is it explicitly about Flevoland?
- Is it only nationally relevant but not yet publicly adopted locally?
- Is a local implication inferred rather than visible in a local source?
- Which regional split is meant: IZA/AZWA-regio, GGD-regio, zorgkantoorregio, ROAZ/subregio, province, or subregional project?

Common quality problems:
- National goals are presented as if Almere already adopted them
- Regional context is mistaken for local policy
- Local documentation gaps are hidden instead of shown
- Flevoland as province, IZA/AZWA-regio Flevoland, GGD Flevoland, and zorgkantoorregio 't Gooi are collapsed into one vague `regio`
- Zeewolde is included or excluded without saying which regional split is being used

Editorial rule:
- Frame these as adoption or documentation gaps, not as failures of the database.
- Do not write `de regio` or `Flevolandse structuur` where Almere's role depends on the regional split. Name the relevant scale in plain language.

### 6. Execution
Check:
- What must be organized, clarified, sequenced, or prepared?
- Does the source actually support that follow-up?
- Is the wording drifting into invented implementation advice?

Common quality problems:
- Generator invents staffing or milestones
- Site language sounds like a formal instruction instead of a possible follow-up
- Action pages imply an owner that the source does not explicitly provide

Editorial rule:
- Use careful wording like “possible follow-up action” unless the source clearly establishes the action.

## Review Pass Sequence
When reviewing a source or page, use this order:

1. Confirm the content class.
2. Label the relevant quality perspectives.
3. Check whether the source authority is described correctly.
4. Check whether dates and money logic are source-backed.
5. Check whether local adoption is explicit or only inferred.
6. Check whether the public wording stays neutral and grounded.

## Minimum Acceptance Standard
An item is good enough for the public site when:

- the source or interpretation status is clear;
- the relevant perspectives are labeled;
- lower-authority wording is attributed where needed;
- local gaps are framed clearly;
- no invented policy advice is added;
- click-through traceability still works.
