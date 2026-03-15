import time
import logging
import os
import traceback
import librosa
import numpy as np
from typing import Dict
from service.models import (
    JobStatus, 
    JobStatusEnum, 
    TrackAnalysisResponse, 
    Section,
    TrackAnalysisRequest
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("remixbuddy.worker")

def normalize_bpm(raw_bpm: float) -> tuple[float, str, float]:
    """
    Normalizes raw BPM to musical standards (integer rounding, half/double time).
    Returns: (suggested_bpm, confidence_label, confidence_score)
    """
    # 1. Round to nearest integer (electronic music standard)
    rounded_bpm = round(raw_bpm)
    diff = abs(raw_bpm - rounded_bpm)
    
    # 2. Range correction (focus on 90-175 BPM for electronic/pop)
    if rounded_bpm < 90:
        rounded_bpm *= 2
        range_adjusted = True
    elif rounded_bpm > 176:
        rounded_bpm /= 2
        range_adjusted = True
    else:
        range_adjusted = False
        
    # 3. Confidence Logic
    if diff < 0.1 and not range_adjusted:
        label = "high"
        score = 0.95
    elif diff < 0.3:
        label = "medium"
        score = 0.85
    else:
        label = "low"
        score = 0.65
        
    return float(rounded_bpm), label, score

def segmented_tempo_estimation(y, sr, window_sec=10.0, step_sec=5.0):
    """
    High-resolution segmented tempo estimation.
    Uses small hop_length and parabolic interpolation on ACF peaks.
    """
    # Use smaller hop_length for higher temporal resolution
    hop_length = 128 
    
    # 1. Compute global onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    
    # 2. Setup Windowing
    frames_per_sec = sr / hop_length
    win_frames = int(window_sec * frames_per_sec)
    step_frames = int(step_sec * frames_per_sec)
    
    # Target BPM range [60, 200]
    min_lag = int(60 * sr / (200 * hop_length))
    max_lag = int(60 * sr / (60 * hop_length))
    
    tempos = []
    total_windows = 0
    avg_onset = np.mean(onset_env)
    threshold = avg_onset * 0.4 

    for start in range(0, len(onset_env) - win_frames, step_frames):
        total_windows += 1
        win_env = onset_env[start : start + win_frames]
        
        if np.mean(win_env) < threshold:
            continue
            
        acf = librosa.autocorrelate(win_env, max_size=max_lag + 1)
        
        if len(acf) > min_lag:
            # Find integer peak
            relative_peak_idx = np.argmax(acf[min_lag:max_lag])
            peak_lag = relative_peak_idx + min_lag
            
            # 3. Parabolic Interpolation for sub-frame precision
            # Only if not at the boundaries of the search range
            if 0 < relative_peak_idx < (max_lag - min_lag - 1):
                y_0 = acf[peak_lag - 1]
                y_1 = acf[peak_lag]
                y_2 = acf[peak_lag + 1]
                
                # Formula for vertex of parabola through 3 points
                p = 0.5 * (y_0 - y_2) / (y_0 - 2 * y_1 + y_2)
                refined_lag = peak_lag + p
            else:
                refined_lag = float(peak_lag)
                
            if refined_lag > 0:
                bpm_val = (60.0 * sr) / (refined_lag * hop_length)
                tempos.append(bpm_val)

    if not tempos:
        return 0.0, 0, total_windows, []

    # 4. Aggregate
    final_bpm = np.median(tempos)
    return float(final_bpm), len(tempos), total_windows, [round(t, 3) for t in tempos]

def analyze_track_task(job_id: str, request: TrackAnalysisRequest, jobs_db: Dict[str, JobStatus], results_db: Dict[str, TrackAnalysisResponse]):
    """
    Background task for audio analysis using librosa.
    """
    try:
        jobs_db[job_id].status = JobStatusEnum.PROCESSING
        jobs_db[job_id].progress = 0.1
        jobs_db[job_id].message = "Loading audio file..."

        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"Audio file not found: {request.file_path}")

        # 1. Load Audio
        y, sr = librosa.load(request.file_path, sr=None, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)
        
        jobs_db[job_id].progress = 0.3
        jobs_db[job_id].message = "Analyzing tempo (BPM) via segments..."

        # 2. Segmented BPM Detection
        precise_bpm, valid_wins, total_wins, candidates = segmented_tempo_estimation(y, sr)
        
        # Apply normalization logic ONLY for suggested_bpm
        suggested_bpm, bpm_label, bpm_score = normalize_bpm(precise_bpm)

        jobs_db[job_id].progress = 0.6
        jobs_db[job_id].message = "Analyzing musical key..."

        # 3. Key Detection (Simple Chroma-based approach)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_avg = np.mean(chroma, axis=1)
        key_map = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_idx = int(np.argmax(chroma_avg))
        detected_key = key_map[key_idx]

        # 4. Structure Detection (Skeleton/Dummy for v0.1)
        sections = []
        if request.detect_sections:
            jobs_db[job_id].progress = 0.8
            jobs_db[job_id].message = "Detecting sections..."
            # For v0.1 we just provide a placeholder "Full Track" section
            sections.append(Section(label="Full Track", start_sec=0.0, end_sec=duration, confidence=1.0))

        # 5. Prepare Response
        from service.models import AnalysisDiagnostics
        diagnostics = AnalysisDiagnostics(
            bpm_windows_total=total_wins,
            bpm_windows_valid=valid_wins,
            bpm_candidates=candidates[:50] # Limit to top 50 for JSON size
        )

        response = TrackAnalysisResponse(
            job_id=job_id,
            status="completed",
            bpm=round(precise_bpm, 3), # Precise float as primary value
            suggested_bpm=suggested_bpm,
            bpm_confidence=bpm_score,
            bpm_confidence_label=bpm_label,
            key=detected_key,
            key_confidence=0.75, # Placeholder confidence
            duration_sec=duration,
            sample_rate_hz=sr,
            channels=1, # librosa.load(mono=True)
            source_format=os.path.splitext(request.file_path)[1][1:].upper(),
            analysis_version="librosa-0.10.1-segmented",
            diagnostics=diagnostics,
            sections=sections
        )

        results_db[job_id] = response
        jobs_db[job_id].status = JobStatusEnum.COMPLETED

        results_db[job_id] = response
        jobs_db[job_id].status = JobStatusEnum.COMPLETED
        jobs_db[job_id].progress = 1.0
        jobs_db[job_id].message = "Analysis complete."
        logger.info(f"Job {job_id} completed successfully.")

    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        logger.error(traceback.format_exc())
        jobs_db[job_id].status = JobStatusEnum.FAILED
        jobs_db[job_id].message = str(e)
