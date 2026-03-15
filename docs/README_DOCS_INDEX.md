# RemixBuddy – Documentation Index

This folder is the updated documentation snapshot after the first implementation rounds.

## Canonical documents

### Product / concept
- `remixbuddy_concept_v1.docx` — original concept and product framing
- `PRODUCT_DECISIONS.md` — current product and technical decisions (living document)
- `ROADMAP_CURRENT.md` — current roadmap with milestone order and gating

### Engineering / implementation
- `remixbuddy_engineering_spec_v4.docx` — original engineering spec used to start implementation
- `ENGINEERING_ADDENDUM_v0.2a.md` — implementation-era updates and corrections to the spec
- `API_CONTRACT_NOTES.md` — current meaning of fields and endpoint behavior

### Status / release / handover
- `status_report.md` — current project status and handover summary
- `v0.1_release_notes.md` — release notes for analysis vertical slice v0.1
- `v0.2a_release_notes.md` — release notes for plugin/service vertical slice v0.2a
- `LESSONS_LEARNED.md` — important implementation lessons and pitfalls
- `BPM_VALIDATION_PROTOCOL.md` — current BPM validation method and reference cases

## Current truth

As of this snapshot:
- Architecture **works**: FL Studio plugin ↔ FastAPI service ↔ analysis worker
- Analysis flow **works end to end**
- BPM for loops/tracks is **not fully accepted yet**
- Next approved technical focus is **BPM Method Upgrade Pass** before any Demucs/v0.3 work

## Local project path
- `D:\ASDZ-Projekte-2026\FL-Plugin`

## Important rule
No new milestone is opened before the current slice is locally validated on real material.
