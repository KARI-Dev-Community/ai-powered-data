#!/usr/bin/env python3
"""Run all scheduled scrapers for data-moat agents."""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRAPER = PROJECT_ROOT / "scrapers" / "google-maps" / "scraper.py"

def run_scraper(path: Path) -> bool:
    print(f"Running: {path}")
    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )
        print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timed out: {path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Failed: {path}: {e}", file=sys.stderr)
        return False


def main():
    if not SCRAPER.exists():
        print(f"Scraper not found: {SCRAPER}", file=sys.stderr)
        sys.exit(1)

    success = run_scraper(SCRAPER)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
