# GUI Stem Separation Integration

## Overview
The new **Stem Separation** panel lives below the existing tempo diagnostics and shows the current status of the Demucs-based backend job. It exposes the \ Separate Stems\ action, the fixed metadata (model, device, chunk length), the output path, the four stem files, and any error text in a compact status block.

## Panel Layout
- **Separate Stems** button launches a POST to /jobs/separate with the currently selected audio file. The button is disabled while a job is running and whenever no file is selected.
- **Status** text mirrors the backend job state (idle / queued / running / success / failed) and shows the human-readable message returned by /jobs/{job_id}.
- **Model / Device / Chunk Length** labels document that the panel runs htdemucs on cpu with 8?s internal chunks.
- **Output** label displays the jobs/<job_id>/stems folder once the job completes.
- **Stems** list prints one line per stem (drums, bass, vocals, other) with the absolute path to each generated WAV file.
- **Error** label appears in red whenever the backend signals failure, showing the backend message (e.g., missing dependencies or Demucs errors).

## Backend Interaction
1. The GUI submits a JSON payload with equest_id, ile_path, and model_id to /jobs/separate through ServiceConnector::submitStemJob.
2. The panel keeps the returned job_id and starts polling /jobs/{job_id} over the existing timer loop.
3. Once the status becomes completed, the GUI pulls /jobs/{job_id}/stems to populate the output folder and stem list.
4. Failures (status ailed or missing stem data) clear the job ID, show the error label, and re-enable the button so the user can retry.

## Job Polling and Diagnostics
- Polling runs inside the same 1?s timer that already refreshes analysis jobs, so no new thread is required.
- While a stem job is active, the status label dynamically shows the latest backend message and automatically switches to **success** / **failed** when the job finishes.
- The panel still surfaces the four expected stems and the manifest folder even if the backend warns (warnings are ignored in the current UI but kept in the service connector for future diagnostics).

## User Expectations
- After the backend job succeeds, the user immediately sees the jobs/<job_id>/stems folder path and the list of generated WAV files.
- If the job fails, the red error label shows one short reason (e.g., Stem separation failed. or the backend message). The button becomes enabled again for retries.
- The task remains lightweight: no waveforms, players, or BPM measurements per stem were added—this panel merely surfaces the backend output and status.
