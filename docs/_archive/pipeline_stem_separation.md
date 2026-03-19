# Stem Separation Pipeline

1. **Input validation**
   - API accepts a file path via `StemSeparationRequest`.  
   - Job fails if the path does not exist or is unreadable.
2. **WAV normalization**
   - Non-WAV files (MP3, etc.) are loaded with `librosa` and re-exported as 16-bit WAV under `jobs/<job_id>/input/original.wav`.
3. **Demucs execution**
   - `subprocess.run(["demucs","-n","htdemucs","-o",<demucs_output>,<wav>])` captures stdout/stderr.  
   - CLI handles its own chunking; we simply wait for completion.
4. **Output extraction**
   - Demucs writes `.../htdemucs/<track_name>/{drums,bass,vocals,other}.wav`.  
   - Each stem is moved into `jobs/<job_id>/stems/<stem>.wav` and validated by `soundfile.info`.
5. **Validation**
   - The worker raises an error if any stem is missing or unreadable, setting job status to `FAILED`.
6. **Manifest/log creation**
   - `meta/manifest.json` records the stems and job metadata; `meta/run_log.json` captures CLI command, stdout/stderr, and timestamps.
