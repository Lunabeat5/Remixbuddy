# Stem Separation API

## POST `/jobs/separate`
- **Description:** Accepts `StemSeparationRequest` with `file_path`, enqueues a Demucs job, returns a job ID.  
- **Request example:**
  ```json
  {
    "request_id": "uuid",
    "file_path": "C:/input/song.mp3",
    "model_id": "htdemucs"
  }
  ```
- **Successful response:** `202 Accepted` with `{"job_id":"job_sep_abcd","status":"accepted"}`.
- **Failure cases:** missing file, Demucs not installed, CLI error → `JobStatusEnum.FAILED` updates, client must poll `/jobs/{job_id}` to see failure message.

## GET `/jobs/{job_id}`
- **Returns:** current `JobStatus` (queued/processing/completed/failed) and optional message.
- **Failure:** `404` if job ID unknown; `202` if job still running.

## GET `/jobs/{job_id}/stems`
- **Returns:** `StemSeparationResponse` once job completes.
- **Response example:**
  ```json
  {
    "job_id": "job_sep_abcd",
    "status": "completed",
    "model_id": "htdemucs",
    "processing_time_ms": 12345,
    "stems": [
      {"name":"drums","file_path":"jobs/job_sep_abcd/stems/drums.wav","format":"wav"},
      ...
    ]
  }
  ```
- **Failure cases:** `202` if not ready, `404` if job never existed.
