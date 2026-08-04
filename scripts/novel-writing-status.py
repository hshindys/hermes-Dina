#!/usr/bin/env python3
"""Wrapper: run novel-writing-session.py status (chapter progress).
Used by cron job 'Dina: Novel Writing Session — Chron'."""
import os, sys, subprocess

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "novel-writing-session.py")
result = subprocess.run([sys.executable, SCRIPT, "status"], text=True)
sys.exit(result.returncode)
