"""Bundle a fallback snapshot so the demo still renders if Yahoo/screener are unreachable."""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from finn import prices, screener  # noqa: E402
from finn.config import PORTFOLIO, RESEARCH_DEMO  # noqa: E402
from finn.store import save_snapshot  # noqa: E402

tickers = sorted({p[0] for p in PORTFOLIO} | set(RESEARCH_DEMO))


def one(t):
    try:
        save_snapshot(f"px_{t}.json", prices._fetch(t))
        save_snapshot(f"scr_{t}.json", screener._load(t))
        return t, "ok"
    except Exception as e:
        return t, f"FAILED {e}"


with ThreadPoolExecutor(4) as ex:
    for t, s in ex.map(one, tickers):
        print(t, s)
