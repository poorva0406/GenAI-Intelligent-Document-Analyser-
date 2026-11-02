"""Project entry point.

    python run.py check      # environment diagnostics
    python run.py app        # launch Streamlit (available from Phase 7)
"""
from __future__ import annotations

import subprocess
import sys

from core.config import ConfigError, get_settings
from core.env_check import format_report, run_checks
from core.logging_setup import setup_logging


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    try:
        settings = get_settings()
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return 2
    setup_logging(settings.log_level)
    settings.ensure_dirs()
    if cmd == "check":
        res = run_checks(settings.ollama_base_url)
        print(format_report(res))
        return 0 if all(r.ok for r in res if r.required) else 1
    if cmd == "app":
        return subprocess.call([sys.executable, "-m", "streamlit", "run", "app/main.py"])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
