# BPM Decision Logic (v0.3 / M1.2)

## What M1.2 adds
- Introduces a lightweight decision layer that consumes the existing full-mix BPM, drum stem BPM, and suggested BPM to derive a single `working_bpm` value, along with a source and a short explanation.  
- The working BPM is bundled with every `TrackAnalysisResponse` so both the service API and GUI can show the interpreted tempo without introducing a new analysis engine.

## Decision rules
1. **Suggested first:** if the BPM engine produces a non-zero suggested BPM, it becomes the working BPM (`working_bpm_source = "suggested"`). This respects the musical correction already computed by the engine.  
2. **Drum / full-mix alignment:** when suggested BPM is missing, the logic compares the full-mix BPM with the drum stem BPM. If the drum BPM confidence is at least 0.35 and the drum/full ratio is close to either 2.0 or 0.5 (±0.2 tolerance), the working BPM copies the drum value with a reason such as “double-time alignment with full mix.”  
3. **Fallback:** when neither rule applies, the working BPM simply mirrors the full-mix BPM with `working_bpm_source = "full_mix"`, preserving the previously accepted signal.
4. **Fail-safe:** if the service cannot produce any BPM, the working BPM remains empty and the UI shows “Working BPM: -” while diagnostics explain why.

## What `working_bpm` means
- It is the tempo the system recommends for downstream work (export, metadata, etc.).  
- The related `working_bpm_reason` string tells the user whether the result came from the suggested correction, a drum/full relationship, or the baseline full mix.  
- `working_bpm_source` is a short tag (`suggested`, `drum`, `full_mix`, `none`) that can be used for filtering/analytics.

## Drum BPM availability and fallbacks
- If the drum stem is missing or unreadable, the service leaves `drum_bpm_available = false`, logs a sentence such as “Drum BPM analysis skipped: Drum stem not found for this track,” and the decision rules ignore the drum-specific branch.  
- The UI surfaces that message next to “Drum BPM” and via diagnostics, so users immediately know why the drum signal was unused.

## GUI surface
- The Analysis section now lists: full mix BPM, drum BPM (with optional confidence), suggested BPM, and the derived “Working BPM”.  
- Below “Working BPM” a compact metadata line shows `Source: … | Reason: …` so the user can understand how the tempo was chosen without extra clicks.  
- The diagnostics pane echoes the same information with `Working BPM: … (source)` and “Decision: …” lines for quick inspection.
