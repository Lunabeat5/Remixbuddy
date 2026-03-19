# Stem Separation Limitations

## Model limitations
- `htdemucs` prioritizes four stems (drums, bass, vocals, other). Bleeding between vocals/other is common.  
- Isolation quality varies by genre; aggressive stereo mixes or heavy mastering may degrade results.

## Audio quality
- Source bitrate/sample rate can influence separation sharpness; we convert EVERYTHING to WAV, so lossy input may already hurt quality.  
- The CLI produces 44.1 kHz outputs; no resampling back to the original format is currently implemented.

## Performance constraints
- Demucs leverages chunking internally but still benefits from GPU. CPU runs can be slow (tens of seconds for long tracks).  
- The backend logs processing time (`processing_time_ms`) to help identify slow jobs.

## Known edge cases
- Jobs fail if any of the four stems is missing after Demucs completes.  
- If `demucs` binary is unavailable or the CLI returns non-zero, the job marks `FAILED` with stderr shown.  
- Multi-channel (surround) inputs may be coerced to mono via `librosa`, so multi-channel detail is lost.
- Stem separation now requires FFmpeg on the system `PATH`; missing FFmpeg causes an immediate failure with the message `FFmpeg not installed or not in PATH` so Demucs never falls back to torchaudio/torchcodec. Windows deployments should use a full shared FFmpeg build (shared libs) to satisfy the CLI’s dependency on `ffmpeg`/`ffprobe`.
