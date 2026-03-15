# RemixBuddy – API Contract Notes

## Current endpoint set
- `GET /health`
- `POST /jobs/analyze`
- `GET /jobs/{job_id}`
- `GET /jobs/{job_id}/result`

## Contract meanings
### Health
Used by plugin startup / connector state.
Should return service identity and version.

### Analyze request
Creates an asynchronous job from a file path and analysis flags.

### Job status
Used for:
- queued
- processing
- completed
- failed

### Result
Carries the final analysis output.

## BPM field semantics
### Accepted semantics
- `bpm`: precise measured BPM float
- `suggested_bpm`: optional interpreted / normalized BPM

### Rejected semantics
- using rounded integer BPM as the only source of truth
- hiding raw measurement from the producer

## Key caveat
The contract may be technically correct while the method behind the value is still wrong.
Contract correctness does not equal analysis correctness.
