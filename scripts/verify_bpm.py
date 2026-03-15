import sys
import os
import librosa
import numpy as np

# Add project root to path
sys.path.append(os.getcwd())

from service.worker import segmented_tempo_estimation, normalize_bpm

def test_file(file_path):
    print(f"Testing file: {file_path}")
    if not os.path.exists(file_path):
        print("Error: File not found")
        return

    # Load audio
    print("Loading audio (this may take a few seconds)...")
    y, sr = librosa.load(file_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"Duration: {duration:.2f}s, SR: {sr}Hz")

    # Run segmented analysis
    print("Running segmented BPM analysis...")
    precise_bpm, valid_wins, total_wins, candidates = segmented_tempo_estimation(y, sr)
    
    # Run global analysis for comparison
    print("Running global BPM analysis (old method)...")
    tempo_global, _ = librosa.beat.beat_track(y=y, sr=sr)
    global_bpm = float(tempo_global[0]) if isinstance(tempo_global, (np.ndarray, list)) else float(tempo_global)

    # Output results
    print("\n--- RESULTS ---")
    print(f"Global BPM (Old):   {global_bpm:.3f}")
    print(f"Segmented BPM (New): {precise_bpm:.3f}")
    print(f"Windows:            {valid_wins} valid / {total_wins} total")
    
    # Histogram of candidates
    if candidates:
        print(f"Top 10 candidates: {candidates[:10]}")
        
    suggested_bpm, label, score = normalize_bpm(precise_bpm)
    print(f"Suggested BPM:     {suggested_bpm} (Confidence: {label} / {score})")
    print("----------------\n")

if __name__ == "__main__":
    track_path = r"C:\Users\lunat\Desktop\YT-Begin\7 Thomas Schumacher - Ficken #3 (Original Mix).mp3"
    test_file(track_path)
