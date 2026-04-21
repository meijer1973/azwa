# AZWA Corpus

This repository contains the AZWA / D5-D6 source corpus and the working materials for building a structured extraction pipeline.

## Current Source Layout

- `sources/`: original downloaded files plus earlier working copies
- `sources markdown/`: Markdown conversions of the original files
- `sources canonical/`: curated raw files recommended as the primary evidence set
- `sources markdown canonical/`: curated Markdown files recommended as the default basis for JSON extraction work
- `sources context/`: supporting context files that are useful for interpretation but weaker as primary evidence
- `sources markdown context/`: Markdown versions of the context set

## Curation Artifacts

- `source-curation.md`: human-readable recommendation for canonical vs context material
- `source-curation.json`: machine-readable version of the curation decision

## Working Principle

The repository is being prepared for a three-layer architecture:

1. source-faithful document extraction
2. append-only normalized claims
3. computed municipality views, including Almere

The canonical source folders are the best starting point for that pipeline.
