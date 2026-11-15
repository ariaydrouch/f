import statistics
from concurrent.futures import ThreadPoolExecutor

import requests

from .config import PORTFOLIO, UA
from .store import cached


def _fetch(ticker: str) -> list[dict]:
    r = requests.get(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}.NS",
        params={"range": "6mo", "interval": "1d"},
        headers={"User-Agent": UA},
        timeout=12,
    )
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    rows = []
    for t, c, v in zip(res["timestamp"], q["close"], q["volume"]):
        if c is None:
            continue
        rows.append({"t": t, "c": round(c, 2), "v": v or 0})
    return rows


def history(ticker: str) -> list[dict]:
    return cached(f"px_{ticker}", 3 * 3600, lambda: _fetch(ticker), snapshot=f"px_{ticker}.json")


def metrics(ticker: str, lookback: int = 20) -> dict:
    h = history(ticker)
    last, prev = h[-1], h[-2]
    base = [x["v"] for x in h[-lookback - 1 : -1] if x["v"]]
    avg = statistics.mean(base) if base else 0
    return {
        "ticker": ticker,
        "price": last["c"],
        "t": last["t"],
        "chg_pct": round((last["c"] / prev["c"] - 1) * 100, 2),
        "volume": last["v"],
        "avg_volume": int(avg),
        "vol_mult": round(last["v"] / avg, 2) if avg else None,
        "spark": [x["c"] for x in h[-30:]],
        "chg_30d_pct": round((last["c"] / h[-31]["c"] - 1) * 100, 1) if len(h) > 31 else None,
    }


def all_metrics() -> list[dict]:
    def one(t):
        try:
            return metrics(t)
        except Exception:
            return None

    with ThreadPoolExecutor(8) as ex:
        return [m for m in ex.map(one, [p[0] for p in PORTFOLIO]) if m]
