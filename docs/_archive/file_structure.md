# Job Output File Structure

Each stem separation job writes to `jobs/<job_id>/`:

- `input/original.wav` — normalized WAV copy of the provided file (reuse even if input already WAV).  
- `demucs_output/` — temporary CLI output (Demucs creates `demucs_output/htdemucs/<track_name>/...`).  
- `stems/{drums,bass,vocals,other}.wav` — final validated stems moved into place.  
- `meta/manifest.json` — JSON manifest listing stem paths, job ID, and timestamp.  
- `meta/run_log.json` — command + stdout/stderr log for the Demucs invocation (used for debugging).

All directories are created deterministically to allow test automation without guessing paths.
