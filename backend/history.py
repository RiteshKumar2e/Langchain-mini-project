"""
history.py
──────────
Lightweight append-only interaction log persisted as newline-delimited JSON (JSONL).

Design notes:
  • JSONL is human-readable, grep-able, and trivially parseable.
  • No database dependency — suitable for a local prototype.
  • In production this would be replaced by a proper database (Postgres/DynamoDB).
  • Each entry includes similarity scores on sources for evaluation purposes.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import settings
from logger import get_logger

log = get_logger(__name__)

_HISTORY_FILE = Path("history.jsonl")


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_entry(
    question: str,
    *,
    answer: str = "",
    sources: list[dict[str, Any]] | None = None,
    chunks_retrieved: int = 0,
    error: str | None = None,
) -> None:
    """Append one interaction (success or failure) to the JSONL log."""
    entry = {
        "timestamp": _now_iso(),
        "question": question,
        "answer": answer,
        "sources": sources or [],
        "chunks_retrieved": chunks_retrieved,
        "error": error,
    }
    try:
        with _HISTORY_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as exc:
        log.warning("Could not write history entry: %s", exc)


def get_recent(n: int = 10) -> list[dict[str, Any]]:
    """Return the last n entries from the history file (most recent last)."""
    if not _HISTORY_FILE.exists():
        return []
    try:
        lines = _HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        entries = [json.loads(line) for line in lines if line.strip()]
        return entries[-n:]
    except (OSError, json.JSONDecodeError) as exc:
        log.warning("Could not read history: %s", exc)
        return []


def clear() -> int:
    """Truncate the history file. Returns number of entries removed."""
    if not _HISTORY_FILE.exists():
        return 0
    lines = _HISTORY_FILE.read_text(encoding="utf-8").splitlines()
    count = sum(1 for line in lines if line.strip())
    _HISTORY_FILE.write_text("", encoding="utf-8")
    log.info("History cleared — %d entries removed", count)
    return count
