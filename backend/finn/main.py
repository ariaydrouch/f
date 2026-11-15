import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import announcements, enrich, llm, prices, research
from .classify import ALL_CATEGORIES, DEFAULT_WATCH, LABELS
from .config import NAMES, PORTFOLIO, RESEARCH_DEMO, ROOT, SECTORS

app = FastAPI(title="FINN")


@app.get("/api/meta")
def meta():
    return {
        "portfolio": [{"ticker": t, "name": n, "sector": s} for t, n, s, _ in PORTFOLIO],
        "research_demo": RESEARCH_DEMO,
        "categories": [{"id": c, "label": LABELS[c]} for c in ALL_CATEGORIES],
        "default_watch": DEFAULT_WATCH,
        "llm": llm.available(),
    }


@app.get("/api/prices")
def prices_all():
    return prices.all_metrics()


@app.get("/api/digest")
def digest(hours: int = 24, tickers: str | None = None):
    tk = [t for t in tickers.split(",") if t in NAMES] if tickers else None
    items = announcements.window(max(1, min(hours, 24 * 30)), tk)
    pm = {m["ticker"]: m for m in prices.all_metrics()}
    for i in items:
        m = pm.get(i["ticker"])
        i["chg_pct"] = m["chg_pct"] if m else None
    return {
        "hours": hours, "count": len(items),
        "counts": {t: sum(1 for i in items if i["tier"] == t) for t in ("must", "notable", "routine")},
        "items": items,
    }


@app.get("/api/alerts")
def alerts(hours: int = 72, vol_mult: float = 2.0, move_pct: float = 3.0, cats: str = ",".join(DEFAULT_WATCH)):
    watch = set(cats.split(",")) if cats else set()
    out = []
    for m in prices.all_metrics():
        reasons = []
        if m["vol_mult"] and m["vol_mult"] >= vol_mult:
            reasons.append(f"Volume {m['vol_mult']}x its 20-day average")
        if abs(m["chg_pct"]) >= move_pct:
            reasons.append(f"Price {m['chg_pct']:+.1f}% on the day")
        if reasons:
            out.append({"kind": "market", "ticker": m["ticker"], "company": NAMES[m["ticker"]], "reasons": reasons,
                        "price": m["price"], "chg_pct": m["chg_pct"], "vol_mult": m["vol_mult"], "t": m["t"],
                        "score": 50 + 10 * len(reasons) + min(abs(m["chg_pct"]), 10)})
    for i in announcements.window(hours):
        if i["category"] in watch and i["priority"] >= 50:
            out.append({"kind": "filing", "ticker": i["ticker"], "company": i["company"], "reasons": [LABELS[i["category"]]],
                        "item": i, "score": i["priority"]})
    out.sort(key=lambda a: -a["score"])
    return {"count": len(out), "alerts": out}


@app.get("/api/enrich/{ticker}/{item_id}")
def enrich_item(ticker: str, item_id: str):
    ticker = ticker.upper()
    if ticker not in NAMES:
        raise HTTPException(404)
    for i in announcements.fetch(ticker):
        if i["id"] == item_id:
            return enrich.enrich(i)
    raise HTTPException(404)


@app.get("/api/research/{ticker}")
def research_ticker(ticker: str, calls: bool = True):
    try:
        return research.research(ticker.upper().replace(".NS", ""), with_calls=calls)
    except Exception as e:
        raise HTTPException(404, f"No data for {ticker}: {e}")


@app.get("/api/quote/{ticker}")
def quote(ticker: str):
    try:
        return prices.metrics(ticker.upper())
    except Exception:
        raise HTTPException(404)


class Ask(BaseModel):
    q: str


STOP = {"WHAT", "WHY", "SHOW", "THE", "AND", "FOR", "ABOUT", "TELL", "ME", "ON", "OF", "IS", "ARE", "HOW", "BULL", "BEAR", "CASE",
        "DID", "DO", "RESULTS", "GUIDANCE", "PROMISED", "PROMISE", "DEBT", "CASH", "ANY", "NEW", "TODAY", "ANALYSE", "ANALYZE", "RESEARCH", "DIG"}


def _find_ticker(q: str) -> str | None:
    ql = q.lower()
    for t, n in NAMES.items():
        if t.lower() in re.findall(r"[a-z&]+", ql) or n.lower() in ql or n.split()[0].lower() in ql:
            return t
    for tok in re.findall(r"\b[A-Z][A-Z&\-]{2,14}\b", q):
        if tok not in STOP:
            return tok
    return None


@app.post("/api/ask")
def ask(body: Ask):
    """Intent router: cheap rules first. Returns which card(s) the client should render."""
    q = body.q.strip()
    ql = q.lower()
    t = _find_ticker(q)
    section = None
    for key, rx in [("promises", r"promis|guid|deliver|narrative|said|management"), ("bull_bear", r"bull|bear|risk|thesis|case"),
                    ("balance", r"debt|leverage|balance|borrow"), ("cash", r"cash|fcf|conversion"),
                    ("trajectory", r"trend|trajectory|growth|margin|history"), ("financial", r"numbers|financial|snapshot|ratio|valuation"),
                    ("business", r"business|segment|what does")]:
        if re.search(rx, ql):
            section = key
            break
    if t and not re.search(r"digest|what changed|my portfolio", ql):
        return {"intent": "research", "ticker": t, "section": section}
    if re.search(r"unusual|volume|alert|spike|move", ql):
        return {"intent": "alerts"}
    m = re.search(r"(\d+)\s*(h|hour|d|day|week)", ql)
    hours = 24
    if m:
        hours = int(m.group(1)) * {"h": 1, "hour": 1, "d": 24, "day": 24, "week": 168}[m.group(2)]
    return {"intent": "digest", "hours": hours}


DIST = ROOT / "frontend" / "dist"
if DIST.exists():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")

    @app.get("/{path:path}")
    def spa(path: str):
        f = DIST / path
        return FileResponse(f if f.is_file() else DIST / "index.html")
