#!/usr/bin/env python3
"""Wrapper: run novel-writing-session.py next (jump to next unwritten chapter).
Used by cron job 'Dina: Writing Check-in — Chron Progress'."""
import os, sys, subprocess

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "novel-writing-session.py")
result = subprocess.run([sys.executable, SCRIPT, "next"], text=True)
sys.exit(result.returncode)
