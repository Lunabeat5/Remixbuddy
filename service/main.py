import uuid
from typing import Dict
from fastapi import FastAPI, BackgroundTasks, HTTPException
from service.models import (
    TrackAnalysisRequest, 
    StemSeparationRequest, 
    JobStatus, 
    JobStatusEnum,
    TrackAnalysisResponse,
    StemSeparationResponse,
    ApiError
)
from service.worker import analyze_track_task, run_stem_separation_task

app = FastAPI(title="RemixBuddy Processing Service", version="1.0.0")

# In-memory DB for MVP
jobs: Dict[str, JobStatus] = {}
results: Dict[str, TrackAnalysisResponse] = {} # Extension for v0.1: Separate results store
stem_jobs: Dict[str, JobStatus] = {}
stem_results: Dict[str, StemSeparationResponse] = {}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "RemixBuddy", "version": "1.0.0"}

@app.post("/jobs/analyze", status_code=202)
async def create_analysis_job(request: TrackAnalysisRequest, background_tasks: BackgroundTasks):
    job_id = f"job_an_{uuid.uuid4().hex[:8]}"
    jobs[job_id] = JobStatus(job_id=job_id, status=JobStatusEnum.QUEUED, progress=0.0, message="Job queued.")
    
    background_tasks.add_task(analyze_track_task, job_id, request, jobs, results)
    return {"job_id": job_id, "status": "accepted"}

@app.post("/jobs/separate", status_code=202)
async def create_stem_job(request: StemSeparationRequest, background_tasks: BackgroundTasks):
    job_id = f"job_sep_{uuid.uuid4().hex[:8]}"
    stem_jobs[job_id] = JobStatus(job_id=job_id, status=JobStatusEnum.QUEUED, progress=0.0, message="Stem job queued.")
    
    background_tasks.add_task(run_stem_separation_task, job_id, request, stem_jobs, stem_results)
    return {"job_id": job_id, "status": "accepted"}

@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    if job_id in jobs:
        return jobs[job_id]
    if job_id in stem_jobs:
        return stem_jobs[job_id]
    raise HTTPException(status_code=404, detail="Job not found")

@app.get("/jobs/{job_id}/result", response_model=TrackAnalysisResponse)
async def get_job_result(job_id: str):
    if job_id not in results:
        # Check if job exists but isn't done
        if job_id in jobs:
            status = jobs[job_id].status
            if status == JobStatusEnum.FAILED:
                 raise HTTPException(status_code=500, detail=f"Job failed: {jobs[job_id].message}")
            raise HTTPException(status_code=202, detail=f"Result not ready yet. Status: {status}")
        raise HTTPException(status_code=404, detail="Job not found")
    return results[job_id]

@app.get("/jobs/{job_id}/stems", response_model=StemSeparationResponse)
async def get_stem_result(job_id: str):
    if job_id not in stem_jobs:
        raise HTTPException(status_code=404, detail="Stem job not found")

    status = stem_jobs[job_id].status
    if status == JobStatusEnum.COMPLETED:
        return stem_results[job_id]
    if status == JobStatusEnum.FAILED:
        raise HTTPException(status_code=500, detail=f"Stem job failed: {stem_jobs[job_id].message}")
    raise HTTPException(status_code=202, detail=f"Stem job not ready yet. Status: {status}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=17845)
