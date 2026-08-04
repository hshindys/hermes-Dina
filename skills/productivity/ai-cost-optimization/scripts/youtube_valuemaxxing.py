#!/usr/bin/env python3
"""
Valuemaxxing Pipeline — Deterministic YouTube → Telegram workflow.
No AI in the plumbing steps. AI only for the final copywriting step.

Usage (Hermes venv on Windows):
    /c/Users/hshin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe youtube_valuemaxxing.py <youtube_url>
"""

import json, sys, subprocess, os
from datetime import datetime

VIDEO_URL = sys.argv[1] if len(sys.argv) > 1 else None
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(OUTPUT_DIR, "pipeline_data.json")

def step1_fetch_metadata(url):
    video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
    return {"video_id": video_id, "url": url, "fetched_at": datetime.now().isoformat()}

def step2_fetch_transcript(video_id):
    try:
        result = subprocess.run(
            ["/c/Users/hshin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe",
             "-m", "youtube_transcript_api", video_id],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return {"transcript": result.stdout.strip()[:5000], "length_chars": len(result.stdout)}
        return {"transcript": None, "error": "Transcript not available", "length_chars": 0}
    except Exception as e:
        return {"transcript": None, "error": str(e), "length_chars": 0}

def step3_format_output(metadata, transcript_data):
    return {
        "pipeline": "valuemaxxing", "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "metadata": metadata, "transcript": transcript_data,
        "cost_estimate": {
            "deterministic_steps_cost": "$0.00",
            "ai_copywriting_step_cost": "$0.11 (if used)",
            "total_cost_with_ai": "$0.11", "tokens_for_ai_step": "~4700"
        }, "steps_completed": [1, 2, 3]
    }

def step4_ai_copywriting(data):
    data["ai_step"] = {
        "available": True, "description": "Send transcript to Claude Fable 5 for copywriting",
        "cost": "$0.11", "status": "pending"
    }
    data["steps_completed"].append(4)
    return data

def main():
    if not VIDEO_URL:
        print("Usage: python3 youtube_valuemaxxing.py <youtube_url>")
        sys.exit(1)
    print(f"[Valuemaxxing] Pipeline started for: {VIDEO_URL}")
    metadata = step1_fetch_metadata(VIDEO_URL)
    print(f"[1/4] Metadata: {metadata['video_id']}")
    transcript = step2_fetch_transcript(metadata["video_id"])
    print(f"[2/4] Transcript: {transcript.get('length_chars', 0)} chars")
    output = step3_format_output(metadata, transcript)
    print(f"[3/4] Output formatted")
    use_ai = input("  Run AI copywriting ($0.11)? (y/n) [n]: ").strip().lower()
    if use_ai == 'y':
        output = step4_ai_copywriting(output)
        print(f"[4/4] AI step queued ($0.11)")
    else:
        print("[4/4] AI step skipped ($0.00 saved)")
        output["steps_completed"].append("4 (skipped)")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"[Done] Saved to {DATA_FILE}")
    print(f"[Cost] Total: {output['cost_estimate']['total_cost_with_ai'] if use_ai == 'y' else '$0.00'}")

if __name__ == "__main__":
    main()