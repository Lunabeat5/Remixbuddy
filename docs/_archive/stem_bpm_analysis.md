# Stem-Based BPM Analysis (v0.3 / M1.1)

## Overview
- M1.1 introduces the first stem-aware analysis step: after a successful stem separation job, the backend now reuses the existing BPM engine to analyze the `drums` stem and report it alongside the full-mix BPM.
- The drums analysis is identical to the `librosa`-based engine already powering v0.2 for full mixes, ensuring consistent terminology, confidence, and tempo-family reasoning.

## Backend behavior
- After `StemSeparationResponse` finishes, the manifest at `jobs/<job_id>/meta/manifest.json` now records the original source file.  
- When an analysis job runs, the service scans `jobs/job_sep_*` folders for a manifest whose `source_file_abs` matches the requested track. If a matching job exists, it loads `jobs/<job_id>/stems/drums.wav` and calls `estimate_bpm` (same helper used for the full mix) to compute precise BPM and confidence.  
- The resulting drum metrics are attached to `TrackAnalysisResponse.drum_bpm*` fields and the diagnostics block (`drum_bpm`, `drum_bpm_confidence`, `drum_bpm_confidence_label`, `drum_bpm_message`). If the drums stem is missing, corrupt, or cannot be read, the backend fails closed by leaving `drum_bpm` empty and capturing the failure description in `drum_bpm_message`.
- No caching is introduced; every analysis attempt rescan the `jobs` tree so the backend stays stateless and always picks the latest stem job if multiple exist.

## GUI surface
- The Analysis section now shows “Drum BPM” right below the full-mix BPM (with its confidence) so users can compare them side by side.  
- When drums analysis is unavailable, the label reads “Drum BPM: unavailable” and the diagnostics text explains why (`drum_bpm_message`).  
- The UI continues to reuse the existing layout, colors, and fonts; the visibility change is simply an extra value line inside the Tempo block.

## Missing stems and communication
- If no `drums.wav` is found under any `job_sep_` directory that matches the requested file, the service logs “Drum BPM analysis skipped: …” and returns `drum_bpm_message` explaining why (e.g., “Drum stem not found for this track”).  
- The UI surfaces that message in both the displayed label and the diagnostics list, so users immediately see when a stem-derived BPM is unavailable without having to inspect logs.
