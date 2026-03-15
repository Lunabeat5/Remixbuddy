import requests
import time
import sys
import uuid

BASE_URL = "http://127.0.0.1:17845"

def test_flow(file_path):
    print(f"--- Starting Analysis Test for: {file_path} ---")
    
    # 1. Check Health
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {r.json()}")
    except Exception as e:
        print(f"Error: Service not running? {e}")
        return

    # 2. Submit Job
    payload = {
        "request_id": str(uuid.uuid4()),
        "file_path": file_path,
        "detect_sections": True,
        "detect_key": True,
        "detect_bpm": True
    }
    
    r = requests.post(f"{BASE_URL}/jobs/analyze", json=payload)
    if r.status_code != 202:
        print(f"Failed to submit job: {r.text}")
        return
    
    job_id = r.json()["job_id"]
    print(f"Job submitted! ID: {job_id}")

    # 3. Poll Status
    while True:
        r = requests.get(f"{BASE_URL}/jobs/{job_id}")
        status_data = r.json()
        status = status_data["status"]
        progress = status_data["progress"]
        message = status_data.get("message", "")
        
        print(f"Status: {status} | Progress: {progress*100:.1f}% | Message: {message}")
        
        if status == "completed":
            break
        if status == "failed":
            print(f"Job failed! Reason: {message}")
            return
        
        time.sleep(1)

    # 4. Get Result
    r = requests.get(f"{BASE_URL}/jobs/{job_id}/result")
    result = r.json()
    print("\n--- Final Result ---")
    print(f"BPM: {result['bpm']} (Confidence: {result['bpm_confidence']})")
    print(f"Key: {result['key']} (Confidence: {result['key_confidence']})")
    print(f"Duration: {result['duration_sec']:.2f}s")
    print(f"Format: {result['source_format']}")
    print(f"Sections: {len(result['sections'])}")
    print("---------------------")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_analysis_v01.py <path_to_audio_file>")
    else:
        test_flow(sys.argv[1])
