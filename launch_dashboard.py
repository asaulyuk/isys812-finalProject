"""
Start the Streamlit dashboard from the project folder (works on Mac and Windows).

Run from a terminal:
  python launch_dashboard.py

Double-clicking this file may open it in an editor. Prefer:
  Run_dashboard_Windows.bat (PC)  or  Run_dashboard_Mac.command (Mac), from Finder / Explorer.
"""
from __future__ import annotations

import os
import subprocess
import sys

from project_paths import PROJECT_ROOT


def main() -> None:
    os.chdir(PROJECT_ROOT)
    raise SystemExit(
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_dashboard_app.py"]
        ).returncode
    )


if __name__ == "__main__":
    main()
