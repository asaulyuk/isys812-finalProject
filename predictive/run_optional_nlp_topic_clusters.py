"""
Compatibility wrapper for optional NLP topic clustering script.

Keeps legacy command/path working:
  python predictive/run_optional_nlp_topic_clusters.py

Actual implementation lives at:
  predictive/predictive/run_optional_nlp_topic_clusters.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_THIS_FILE = Path(__file__).resolve()
_IMPL_PATH = _THIS_FILE.parent / "predictive" / "run_optional_nlp_topic_clusters.py"

if not _IMPL_PATH.is_file():
    raise FileNotFoundError(f"Missing implementation script: {_IMPL_PATH}")

_SPEC = importlib.util.spec_from_file_location("run_optional_nlp_topic_clusters_impl", _IMPL_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Could not load module from: {_IMPL_PATH}")

_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

# Re-export implementation symbols so notebooks importing this path still work.
for _name in dir(_MODULE):
    if _name.startswith("__"):
        continue
    globals()[_name] = getattr(_MODULE, _name)


if __name__ == "__main__":
    _MODULE.main()
