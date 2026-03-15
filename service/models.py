from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, UUID4

class JobStatusEnum(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class StemNameEnum(str, Enum):
    VOCALS = "vocals"
    DRUMS = "drums"
    BASS = "bass"
    OTHER = "other"

# --- Common ---
class ApiError(BaseModel):
    error_code: str
    message: str
    details: Optional[str] = None
    retryable: bool
    request_id: Optional[str] = None
    job_id: Optional[str] = None
    schema_version: str = "1.0.0"

class JobStatus(BaseModel):
    job_id: str
    status: JobStatusEnum
    progress: float = Field(ge=0.0, le=1.0)
    message: Optional[str] = None
    warnings: List[str] = []

# --- Analysis ---
class TrackAnalysisRequest(BaseModel):
    request_id: UUID4
    file_path: str
    detect_sections: bool = True
    detect_key: bool = True
    detect_bpm: bool = True
    workspace_id: Optional[str] = None

class Section(BaseModel):
    label: str
    start_sec: float
    end_sec: float
    confidence: float

class AnalysisDiagnostics(BaseModel):
    bpm_windows_total: int = 0
    bpm_windows_valid: int = 0
    bpm_candidates: List[float] = []

class TrackAnalysisResponse(BaseModel):
    job_id: str
    status: str # "completed" | "failed"
    bpm: float # Precise measured value
    suggested_bpm: Optional[float] = None # Musical interpretation
    bpm_confidence: float
    bpm_confidence_label: Optional[str] = None
    key: str
    key_confidence: float
    duration_sec: float
    sample_rate_hz: int
    channels: int
    source_format: str
    analysis_version: str
    diagnostics: Optional[AnalysisDiagnostics] = None
    schema_version: str = "1.0.0"
    sections: List[Section] = []

# --- Stems ---
class StemSeparationRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    request_id: UUID4
    file_path: str
    model_id: str = "htdemucs"
    output_format: str = "wav24"
    target_bpm: Optional[float] = None
    key_shift: int = 0
    normalize_output: bool = True
    overwrite_existing: bool = False
    workspace_id: Optional[str] = None

class StemAsset(BaseModel):
    name: StemNameEnum
    file_path: str
    format: str
    peak_dbfs: Optional[float] = None

class StemSeparationResponse(BaseModel):
    model_config = {'protected_namespaces': ()}
    job_id: str
    status: str # "completed" | "failed"
    model_id: str
    processing_time_ms: int
    schema_version: str = "1.0.0"
    warnings: List[str] = []
    stems: List[StemAsset]
