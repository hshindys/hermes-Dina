#!/bin/bash
# Jellyfin library scan — wrapper script for cron job
# Runs from the jellyfin-control directory where node_modules are available.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
JELLYFIN_DIR="/c/Users/hshin/AppData/Local/hermes/skills/jellyfin-control"

cd "$JELLYFIN_DIR"

export JF_URL="http://localhost:8096"
export JF_API_KEY="74e663d2d7244887ae8c312a0b024ff1"

node cli.js scan