"""
history.py
──────────
Local history persistence layer.

Each QA interaction is appended as a JSON line to `history.jsonl`.
The module exposes helpers used by the API router:

  • log_entry(question, answer, sources, error)
  • get_recent(n)
  • clear()
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from logger import get_logger

log = get_logger(__name__)

HISTORY_FILE = Path("history.jsonl")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_entry(
    question: str,
    answer: str = "",
    sources: list[dict] | None = None,
    error: str | None = None,
) -> None:
    """Append one interaction to the history file."""
    entry: dict[str, Any] = {
        "timestamp": _timestamp(),
        "question": question,
        "answer": answer,
        "sources": sources or [],
        "error": error,
    }
    try:
        with HISTORY_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as exc:
        log.warning("Could not write history entry: %s", exc)


def get_recent(n: int = 10) -> list[dict]:
    """Return the last *n* entries from history (most recent last)."""
    if not HISTORY_FILE.exists():
        return []
    try:
        lines = HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        entries = [json.loads(line) for line in lines if line.strip()]
        return entries[-n:]
    except (OSError, json.JSONDecodeError) as exc:
        log.warning("Could not read history: %s", exc)
        return []


def clear() -> int:
    """Delete all history entries. Returns the number of entries removed."""
    if not HISTORY_FILE.exists():
        return 0
    try:
        lines = HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        count = sum(1 for l in lines if l.strip())
        HISTORY_FILE.unlink()
        log.info("History cleared (%d entries removed).", count)
        return count
    except OSError as exc:
        log.warning("Could not clear history: %s", exc)
        return 0
