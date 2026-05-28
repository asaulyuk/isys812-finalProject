#!/bin/bash
# ========== macOS ONLY — double-click in Finder (not in Cursor) ==========
# Windows users: use Run_dashboard_Windows.bat in File Explorer instead.

cd "$(dirname "$0")"
DIR="$(pwd)"
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd \"${DIR}\" && python3 launch_dashboard.py"
end tell
EOF
