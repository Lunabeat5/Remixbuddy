# GEMINI.md - RemixBuddy Project Rules & Strategy

## Project Overview
RemixBuddy is a hybrid VST3 plugin system for stem extraction and audio analysis.
- **Frontend:** VST3 Plugin (C++17, JUCE 8, CMake)
- **Backend:** Local Processing Service (Python 3.11, FastAPI, Demucs, Librosa/Essentia)
- **Communication:** IPC via HTTP/JSON on `127.0.0.1:17845`

## Core Mandates & Constraints
- **Target Platform:** Windows 10/11 x64 (MSVC 2022).
- **Performance:** UI must remain responsive (< 200ms latency). Heavy processing (AI) must run in the background service.
- **Hardware:** **CPU-fallback is mandatory.** GPU (CUDA) acceleration is optional.
- **Data Handling:** Audio files are passed via file paths; no raw audio streaming over IPC in MVP.
- **Storage:** 
  - Results: `%LOCALAPPDATA%\RemixBuddy\jobs\<job_id>\`
  - Models (Dev): `<ProjectRoot>/runtime/models/`

## Implementation Strategy

### Phase 1: Foundation (Current Focus)
- **Monorepo Setup:** Create folders for plugin, service, contracts, and runtime.
- **JUCE Setup:** Add JUCE 8 as a Git submodule in `libs/JUCE`.
- **Python Setup:** Create local `.venv` in `service/` and `requirements.txt`.
- **IPC:** Define JSON schemas for Health Check and Job submission.

### Phase 2: Audio Analysis MVP
- Implement file loading in JUCE UI.
- Service-side BPM, Key, and Structure detection.

### Phase 3: Stem Separation MVP
- Integrate Demucs v4 (CPU-first, CUDA-optional).
- Job queuing and status polling.

## Directory Structure
```
remixbuddy/
├── contracts/        # API/IPC Schemas (JSON)
├── libs/             # External libraries (JUCE as submodule)
├── plugin/           # C++/JUCE VST3 source
├── service/          # Python backend (.venv, requirements.txt)
├── runtime/          # Models and temporary processing data
└── scripts/          # Build and setup scripts
```

## Licensing
- **JUCE:** Personal/Development license.
- **Rubber Band:** Evaluation/GPL version for MVP.
- **Demucs:** MIT/Open Source.
