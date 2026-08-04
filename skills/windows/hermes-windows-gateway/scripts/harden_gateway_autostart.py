#!/usr/bin/env python3
"""Harden the Hermes gateway Scheduled Task so it survives Windows reboots.

Idempotent + password-free. What it does:
  1. Reads the CURRENT \\Hermes_Gateway task to capture your real SID and
     existing action paths (no guessing).
  2. Patches the launcher VBS to WAIT for the gateway (Wait=True) so the task's
     RestartOnFailure guards the gateway process itself, not the wrapper.
  3. Rebuilds the task XML with a BootTrigger + LogonTrigger, HighestAvailable,
     and the existing RestartOnFailure (999 / PT1M).
  4. Backs up the original task XML before re-registering.

Run from a shell that has Task Scheduler write access (Admin not required for a
task owned by your own account, but HighestAvailable needs a UAC-elevatable token).

Usage:
    python scripts/harden_gateway_autostart.py            # apply
    python scripts/harden_gateway_autostart.py --dry-run  # print XML only
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

TASK_NAME = r"\Hermes_Gateway"
HOMEDIR = os.environ.get(
    "HERMES_HOME",
    os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\unknown\AppData\Local"), "hermes"),
)
VBS_PATH = os.path.join(HOMEDIR, "gateway-service", "Hermes_Gateway.vbs")
BACKUP_PATH = os.path.join(HOMEDIR, "gateway-service", "Hermes_Gateway.backup.xml")
NEW_XML_PATH = os.path.join(HOMEDIR, "gateway-service", "Hermes_Gateway.new.xml")
NS = "http://schemas.microsoft.com/windows/2004/02/mit/task"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def patch_vbs() -> bool:
    if not os.path.exists(VBS_PATH):
        print(f"[!] VBS not found at {VBS_PATH}; skipping VBS patch", file=sys.stderr)
        return False
    with open(VBS_PATH, encoding="utf-8") as f:
        src = f.read()
    if "Wait=True" in src or ", True)" in src:
        print("[ok] VBS already waits for the gateway; no change needed")
        return False
    # Flip the trailing False -> True on the gateway run line.
    new = src.replace(', False)\n', ', True)\n').replace(", False)", ", True)")
    if new == src:
        print("[!] Could not locate the gateway run line in VBS", file=sys.stderr)
        return False
    with open(VBS_PATH, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"[ok] Patched VBS to wait: {VBS_PATH}")
    return True


def get_current_sid() -> str:
    r = run(["schtasks", "/query", "/tn", TASK_NAME, "/xml"])
    if r.returncode != 0:
        print(f"[!] Cannot read current task: {r.stderr.strip()}", file=sys.stderr)
        return ""
    try:
        root = ET.fromstring(r.stdout)
        uid = root.find(f".//{{{NS}}}Principals/{{{NS}}}Principal/{{{NS}}}UserId")
        return uid.text if uid is not None else ""
    except ET.ParseError:
        return ""


def build_xml(sid: str) -> str:
    sid_line = f"      <UserId>{sid}</UserId>\n" if sid else ""
    # NOTE: raw string below because the URI is "\Hermes_Gateway" (literal \U).
    return rf'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="{NS}">
  <RegistrationInfo>
    <Description>Hermes Agent Gateway - Messaging Platform Integration</Description>
    <URI>\Hermes_Gateway</URI>
  </RegistrationInfo>
  <Principals>
    <Principal id="Author">
{uid_line}      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Count>999</Count>
      <Interval>PT1M</Interval>
    </RestartOnFailure>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
  </Settings>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>PT30S</Delay>
    </BootTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <Delay>PT30S</Delay>
    </LogonTrigger>
  </Triggers>
  <Actions Context="Author">
    <Exec>
      <Command>wscript.exe</Command>
      <Arguments>//B //Nologo "{VBS_PATH}"</Arguments>
    </Exec>
  </Actions>
</Task>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.dry_run:
        patch_vbs()

    sid = get_current_sid()
    xml = build_xml(sid)

    if args.dry_run:
        print(xml)
        return

    # Back up existing task, then re-register from a UTF-16 file.
    run(["schtasks", "/query", "/tn", TASK_NAME, "/xml", ">", BACKUP_PATH])
    with open(NEW_XML_PATH, "w", encoding="utf-16") as f:
        f.write(xml)
    r = run(["schtasks", "/create", "/tn", TASK_NAME, "/xml", NEW_XML_PATH, "/f"])
    if r.returncode == 0:
        print(f"[ok] Task {TASK_NAME} re-registered. Verify: hermes gateway status")
    else:
        print(f"[!] Re-register failed ({r.returncode}): {r.stderr.strip()}", file=sys.stderr)
        print(f"    Backup at: {BACKUP_PATH}")
        sys.exit(1)


if __name__ == "__main__":
    main()
