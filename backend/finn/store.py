import hashlib
import json
import time
from pathlib import Path

from .config import CACHE, SNAPSHOT


def _path(key: str) -> Path:
    h = hashlib.sha1(key.encode()).hexdigest()[:16]
    safe = "".join(c if c.isalnum() else "_" for c in key)[:40]
    return CACHE / f"{safe}_{h}.json"


def cached(key: str, ttl: int, fn, snapshot: str | None = None):
    """Return fresh cache, else call fn; on failure fall back to stale cache, then bundled snapshot."""
    p = _path(key)
    if p.exists() and time.time() - p.stat().st_mtime < ttl:
        return json.loads(p.read_text())
    try:
        val = fn()
        p.write_text(json.dumps(val))
        return val
    except Exception:
        if p.exists():
            return json.loads(p.read_text())
        if snapshot:
            sp = SNAPSHOT / snapshot
            if sp.exists():
                return json.loads(sp.read_text())
        raise


def save_snapshot(name: str, val):
    (SNAPSHOT / name).write_text(json.dumps(val))
