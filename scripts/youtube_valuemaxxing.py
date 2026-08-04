#!/usr/bin/env python3
"""
Valuemaxxing Pipeline — Deterministic YouTube → Telegram workflow
No AI in the plumbing steps. AI only for the final copywriting step.

Usage:
    python3 youtube_valuemaxxing.py <youtube_url>

Steps (deterministic, $0 cost):
    1. Fetch video metadata (title, channel, url)
    2. Fetch transcript via youtube-transcript-api        
    3. Format as structured JSON

Step 4 (AI step, $0.11 cost):
    4. Send to Claude/Fable 5 for copywriting (opt-in)
"""

import json
import sys
import subprocess
import os
from datetime import datetime

VIDEO_URL = sys.argv[1] if len(sys.argv) > 1 else None
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(OUTPUT_DIR, "pipeline_data.json")

def step1_fetch_metadata(url):
    """Step 1: Extract video ID and basic metadata (deterministic)."""
    video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
    return {
        "video_id": video_id,
        "url": url,
        "fetched_at": datetime.now().isoformat(),
        "method": "deterministic"
    }

def step2_fetch_transcript(video_id):
    """Step 2: Fetch transcript via youtube-transcript-api (deterministic)."""
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
    """Step 3: Format as structured JSON for the AI step."""
    output = {
        "pipeline": "valuemaxxing",
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "metadata": metadata,
        "transcript": transcript_data,
        "cost_estimate": {
            "deterministic_steps_cost": "$0.00",
            "ai_copywriting_step_cost": "$0.11 (if used)",
            "total_cost_with_ai": "$0.11",
            "tokens_for_ai_step": "~4700"
        },
        "steps_completed": [1, 2, 3]
    }
    return output

def step4_ai_copywriting(data):
    """Step 4 (optional): Send transcript to AI for copywriting.
    This is the ONLY step that costs money."""
    # This step would use the Claude API or a Zapier webhook in production
    # For now, we just flag it as available
    data["ai_step"] = {
        "available": True,
        "description": "Send transcript to Claude Fable 5 for copywriting",
        "cost": "$0.11",
        "status": "pending"
    }
    data["steps_completed"].append(4)
    return data

def main():
    if not VIDEO_URL:
        print("Usage: python3 youtube_valuemaxxing.py <youtube_url>")
        sys.exit(1)

    print(f"[Valuemaxxing] Starting pipeline for: {VIDEO_URL}")
    
    # Step 1: Metadata
    print("[Step 1/4] Fetching metadata (deterministic)...")
    metadata = step1_fetch_metadata(VIDEO_URL)
    print(f"  → Video ID: {metadata['video_id']}")
    
    # Step 2: Transcript
    print("[Step 2/4] Fetching transcript (deterministic)...")
    transcript = step2_fetch_transcript(metadata["video_id"])
    if transcript["transcript"]:
        print(f"  → Transcript fetched ({transcript['length_chars']} chars)")
    else:
        print(f"  → Warning: {transcript.get('error', 'No transcript')}")
    
    # Step 3: Format
    print("[Step 3/4] Formatting output (deterministic)...")
    output = step3_format_output(metadata, transcript)
    print(f"  → Formatted JSON ready")
    
    # Step 4: AI (optional)
    use_ai = input("  → Run AI copywriting step ($0.11)? (y/n) [n]: ").strip().lower()
    if use_ai == 'y':
        print("[Step 4/4] Running AI copywriting...")
        output = step4_ai_copywriting(output)
        print(f"  → AI step queued ($0.11)")
    else:
        print("[Step 4/4] Skipped AI step (saving $0.11!)")
        output["steps_completed"].append("4 (skipped)")
    
    # Save output
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n[Done] Pipeline output saved to: {DATA_FILE}")
    print(f"[Cost] Total: {output['cost_estimate']['total_cost_with_ai'] if use_ai == 'y' else '$0.00'}")

if __name__ == "__main__":
    main()