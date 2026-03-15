# RemixBuddy - Status Report & Handover

## Current Version: v0.2a verified architecture / v0.2c pending BPM method upgrade
**Date:** 15. März 2026

## Executive summary
RemixBuddy has moved from concept to a real working local system.

Verified:
- JUCE VST3 plugin builds and loads in FL Studio
- Local FastAPI backend runs on `127.0.0.1:17845`
- Plugin ↔ service communication works
- End-to-end analysis flow works:
  - file selected in plugin
  - `POST /jobs/analyze`
  - job polling via `GET /jobs/{id}`
  - result returned via `GET /jobs/{id}/result`
- BPM / key / duration are displayed in the plugin UI

Not yet accepted:
- BPM method for **full tracks** is still not accurate enough for producer-grade trust
- Current global librosa-based estimate can deviate from FL Studio / Edison reference on real tracks
- Therefore v0.3 (Demucs / stem separation) is still **blocked**

## Verified milestones

### v0.1 – Analysis Vertical Slice
Completed and validated.
- FastAPI service
- asynchronous worker
- contracts for analysis / job status / error handling
- local test script
- result retrieval

### v0.2 – Plugin Architecture
Completed and validated.
- JUCE 8 + CMake + VST3
- plugin loads in FL Studio
- drag/drop or file selection path
- HTTP connector to local service
- polling status in plugin UI
- result rendering in plugin UI

### v0.2a – Connector Hardening / debug visibility
Completed and validated.
- health endpoint handled correctly
- connector debug overlay added
- service offline issue was traced and resolved
- backend dependency issue (`pkg_resources`) was identified during live validation
- service restart requirement was confirmed for backend logic changes

## Current technical reality
Architecture now proven in practice:

FL Studio Plugin
→ local HTTP/JSON
→ FastAPI service
→ worker thread
→ librosa analysis
→ result JSON
→ plugin UI

This architecture is accepted as the working base.

## Current blocker
### BPM quality for full tracks
Current BPM analysis is good enough for architectural proof, but not yet accepted as product quality.

Observed problem case:
- Reference via FL Studio / Edison: ~`127.002 BPM`
- RemixBuddy result: `126.05 BPM`

Conclusion:
- Not a UI bug
- Not a contract bug
- Not a reload bug
- Not a plugin/service IPC bug
- It is a **method-level BPM estimation issue**

## Approved next step
### v0.2c – BPM Method Upgrade Pass
Before v0.3, the team must upgrade BPM estimation from a single global estimate to a more robust segmented method.

Approved direction:
1. split full track into windows (e.g. 10 seconds, 5 second hop)
2. estimate local BPM per window
3. discard or down-weight weak / unstable windows
4. cluster candidates
5. derive final BPM from stable dominant cluster

No Demucs work is approved until this pass is validated.

## Pending tasks (ordered)
1. **v0.2c BPM Method Upgrade**
2. Validate against real reference tracks from FL Studio / Edison
3. Freeze accepted BPM method
4. Only then open **v0.3 Stem Separation / Demucs**

## Known issues / technical debt
- Essentia is still skipped on Windows
- Job persistence is still in-memory only
- Build step cannot auto-copy `.vst3` into `C:\Program Files\Common Files\VST3` without admin rights
- Plugin UI currently shows the precise BPM value only; optional interpreted BPM is not surfaced yet
- BPM algorithm for full tracks is not yet trustworthy enough

## Local environment notes
- Project root: `D:\ASDZ-Projekte-2026\FL-Plugin`
- Backend service is started from:
  - `service\.venv\Scripts\python.exe -m service.main`
- If backend code changes, service restart is required
- `.venv` should not be included in ZIP snapshots
