# RemixBuddy – Current Roadmap

## Completed
### v0.1
- contracts
- FastAPI service
- worker
- result polling
- analysis flow

### v0.2
- JUCE plugin architecture
- VST3 build
- plugin ↔ service HTTP communication
- plugin UI result rendering

### v0.2a
- health check hardening
- debug visibility
- dependency fix
- end-to-end architectural validation in FL Studio

## In progress
### v0.2c – BPM Method Upgrade Pass
Goal:
- robust BPM estimation for full tracks
- producer-trustworthy BPM output

Required before acceptance:
- segmented BPM estimation plan
- implementation
- validation against real reference tracks
- delta comparison against FL Studio / Edison

## Blocked
### v0.3 – Stem Separation / Demucs
Blocked until v0.2c is accepted.

## Later
### v0.4
- waveform UI
- remix pack export
- better persistence / job tracking

### v0.5
- quality-improved key detection
- section detection improvement
- producer UX refinements
