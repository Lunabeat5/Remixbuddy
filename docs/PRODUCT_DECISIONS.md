# RemixBuddy – Product Decisions (Living Document)

## Roles
- René = Product Owner / Producer-side decision maker
- External team = implementation team
- Buddy / AI support = architecture, specification, review support

## Global rules
1. No hallucinated decisions. Unknown stays unknown until verified.
2. No new milestone before the current slice is locally validated.
3. Architecture decisions beat convenience.
4. Producer trust is more important than cosmetic “smartness”.

## Confirmed architecture decisions
- Local-first product
- Hybrid runtime:
  - JUCE VST3 plugin = thin DAW client
  - FastAPI Python service = heavy analysis / DSP backend
- Windows 10/11 x64 only for v1
- VST3 only for v1
- CMake + JUCE 8 for plugin
- Python backend in project-local `.venv`
- HTTP/JSON on loopback (`127.0.0.1:17845`) for plugin ↔ service communication

## Dependency / environment decisions
- CPU fallback is mandatory
- GPU acceleration is optional and reserved mainly for future stem separation
- `.venv` is not shipped in project ZIP snapshots
- `requirements.txt` is canonical for backend dependencies

## Milestone gating decisions
### Accepted
- v0.1 analysis vertical slice
- v0.2 plugin architecture
- v0.2a connector hardening / integration validation

### Not accepted yet
- BPM quality for complete tracks
- v0.3 Demucs integration

## BPM decisions
### Rejected strategies
- hard integer rounding as primary BPM output
- UI smoothing that hides wrong BPM values
- claiming “stabilized” without comparison against real reference material

### Current BPM output rules
- `bpm` = precise measured BPM float
- `suggested_bpm` = optional interpreted value (not primary truth)
- producer trust requires that the measured value remains visible

### Current BPM engineering direction
- move from single global estimate to segmented tempo estimation
- validate against FL Studio / Edison reference on real tracks

## Validation decisions
- FL Studio / Edison may be used as practical producer reference
- one successful test is not enough; multiple real tracks are required
- the problematic track `7 Thomas Schumacher - Ficken #3 (Original Mix).mp3` is an official BPM regression case
