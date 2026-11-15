import hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import requests

from . import screener
from .classify import classify, tier
from .config import BSE_CODES, NAMES, PORTFOLIO, UA
from .store import cached

IST = timezone(timedelta(hours=5, minutes=30))


def _bse_live(ticker: str) -> list[dict]:
    """BSE's own feed. Often blocks datacentre IPs (Akamai); we fall through to screener when it does."""
    end = datetime.now(IST)
    start = end - timedelta(days=14)
    r = requests.get(
        "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w",
        params={"pageno": 1, "strCat": -1, "strPrevDate": start.strftime("%Y%m%d"), "strScrip": BSE_CODES[ticker],
                "strSearch": "P", "strToDate": end.strftime("%Y%m%d"), "strType": "C", "subcategory": -1},
        headers={"User-Agent": UA, "Referer": "https://www.bseindia.com/", "Origin": "https://www.bseindia.com"},
        timeout=10,
    )
    r.raise_for_status()
    out = []
    for x in r.json()["Table"]:
        ts = datetime.fromisoformat(x["NEWS_DT"]).replace(tzinfo=IST).isoformat()
        att = x.get("ATTACHMENTNAME")
        out.append({
            "title": (x.get("HEADLINE") or x.get("NEWSSUB") or "").strip(),
            "ts": ts,
            "url": f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{att}" if att else "",
            "summary": (x.get("MORE") or "").strip()[:240],
            "bse_cat": x.get("CATEGORYNAME"),
        })
    return out


def _raw(ticker: str) -> tuple[list[dict], str]:
    try:
        return _bse_live(ticker), "bse"
    except Exception:
        pass
    return screener.company(ticker)["announcements"], "screener"


def fetch(ticker: str) -> list[dict]:
    raw, src = cached(f"ann_{ticker}", 900, lambda: list(_raw(ticker)))
    items = []
    for a in raw:
        cat, score = classify(a["title"], a.get("summary", ""))
        items.append({
            "id": hashlib.sha1((ticker + a["ts"] + a["title"]).encode()).hexdigest()[:12],
            "ticker": ticker, "company": NAMES[ticker], "source": src, **a,
            "category": cat, "priority": score, "tier": tier(score),
        })
    return items


def window(hours: int, tickers: list[str] | None = None) -> list[dict]:
    tickers = tickers or [p[0] for p in PORTFOLIO]
    cutoff = datetime.now(IST) - timedelta(hours=hours)

    def one(t):
        try:
            return fetch(t)
        except Exception:
            return []

    with ThreadPoolExecutor(8) as ex:
        items = [i for lst in ex.map(one, tickers) for i in lst]
    items = [i for i in items if datetime.fromisoformat(i["ts"]) >= cutoff]
    items.sort(key=lambda i: (i["priority"], i["ts"]), reverse=True)
    return items
