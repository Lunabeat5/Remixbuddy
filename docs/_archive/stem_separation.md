# Stem Separation Feature

## Overview
- Triggers local stem separation via Demucs (model: `htdemucs`).  
- Intended as a proof of concept that runs entirely on the host machine using the CLI binary.

## Model details
- `htdemucs` balances practicality and quality for drums/bass/vocals/other.  
- The backend simply invokes `demucs -n htdemucs -o <output> <input.wav>`.

## CLI usage
```bash
demucs -n htdemucs -o ./demo-output ./input/audio.wav
```

## Input / output
- Input: arbitrary WAV/MP3 tracked via `TrackAnalysisRequest`. MP3s are normalized/converted to WAV before separation.  
- Output: deterministic folder structure `jobs/<job_id>/stems/` containing `drums.wav`, `bass.wav`, `vocals.wav`, `other.wav`.

## Expected results
- Provides four stems that can be inspected or consumed by downstream tools.  
- The GUI will surface stem file paths and status (idle/running/success/failure).

## Runtime requirements
- FFmpeg must be installed and reachable via `PATH` before running Demucs. The worker verifies this by calling `ffmpeg -version` and will mark the job as **FAILED** with the message `FFmpeg not installed or not in PATH` if the binary is unavailable.
- Windows deployments must use a full shared FFmpeg build (e.g., the shared builds from gyan.dev or BtbN) so the Demucs loader can access `ffmpeg`/`ffprobe`; stripped-down static builds can omit codecs required by the CLI.
- With FFmpeg available, Demucs no longer falls back to torchaudio decoding, eliminating dependencies on `torchcodec`.

## Limitations
- Demucs may leak instruments between stems (especially vocals vs. other) and cannot guarantee perfect isolation.  
- Quality is tied to Demucs’s pretrained weights; no fine-tuning is performed.  
- Separation may be slow on CPU-heavy machines (`demucs` uses internal chunking).
