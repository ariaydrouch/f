"""Pull side. Grounded only in primary-derived data: screener's standardised statements (from filings),
annual-report/concall links, and the raw concall transcripts (PDF). No news, no broker notes, no model memory."""
import io
import re
from concurrent.futures import ThreadPoolExecutor

import requests
from pypdf import PdfReader

from . import llm, screener
from .config import UA
from .store import cached

MONTH = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def _last(xs, n=1):
    v = [x for x in xs if x is not None]
    return v[-n] if len(v) >= n else None


def _cagr(a, b, yrs):
    if a is None or b is None or a <= 0 or b <= 0 or yrs <= 0:
        return None
    return round(((b / a) ** (1 / yrs) - 1) * 100, 1)


def _ann(d, table, key):
    t = d[table]
    r = t["rows"].get(key)
    return t["cols"], r or []


def _year_cols(d):
    cols = d["annual"]["cols"]
    return [i for i, c in enumerate(cols) if c != "TTM"]


# ---------- structured sections ----------
def business(d):
    return {"about": d["about"], "sector_note": None,
            "note": "Segment/revenue mix needs the annual report; links below. Run with an LLM key to auto-extract it."}


def financial(d):
    q = d["quarters"]["rows"]
    a = d["annual"]
    top = d["top"]
    ycols = _year_cols(d)
    li = ycols[-1]
    pick = lambda k: a["rows"].get(k, [None] * len(a["cols"]))
    return {
        "year": a["cols"][li],
        "cards": [
            {"k": "Revenue", "v": pick("Sales")[li], "u": "Rs Cr"},
            {"k": "EBITDA margin", "v": pick("OPM %")[li], "u": "%"},
            {"k": "PAT", "v": pick("Net Profit")[li], "u": "Rs Cr"},
            {"k": "EPS", "v": pick("EPS in Rs")[li], "u": "Rs"},
            {"k": "ROCE", "v": top.get("ROCE"), "u": "%"},
            {"k": "ROE", "v": top.get("ROE"), "u": "%"},
            {"k": "P/E", "v": top.get("Stock P/E"), "u": "x"},
            {"k": "Div yield", "v": top.get("Dividend Yield"), "u": "%"},
        ],
    }


def trajectory(d):
    a = d["annual"]
    ycols = _year_cols(d)[-6:]
    cols = [a["cols"][i] for i in ycols]
    series = {}
    for k, lab in [("Sales", "Revenue"), ("Net Profit", "PAT"), ("OPM %", "EBITDA margin %"), ("EPS in Rs", "EPS")]:
        r = a["rows"].get(k)
        if r:
            series[lab] = [r[i] for i in ycols]
    yrs = len(ycols) - 1
    notes = []
    s = series.get("Revenue", [])
    if len(s) > 1:
        c = _cagr(s[0], s[-1], yrs)
        if c is not None:
            notes.append(f"Revenue CAGR {c}% over {yrs}y")
    p = series.get("PAT", [])
    if len(p) > 1:
        c = _cagr(p[0], p[-1], yrs)
        if c is not None:
            notes.append(f"PAT CAGR {c}% over {yrs}y")
    m = series.get("EBITDA margin %", [])
    if len(m) > 1 and None not in (m[0], m[-1]):
        dm = m[-1] - m[0]
        notes.append(f"EBITDA margin {'expanded' if dm > 0 else 'compressed'} {abs(dm):.1f}pp ({m[0]:.0f}% to {m[-1]:.0f}%)")
    return {"cols": cols, "series": series, "notes": notes}


def balance(d):
    b = d["balance"]["rows"]
    bc = d["balance"]["cols"]
    ratios = d["ratios"]["rows"]
    i = len(bc) - 1
    eq = (b.get("Equity Capital", [0])[i] or 0) + (b.get("Reserves", [0])[i] or 0)
    debt = b.get("Borrowings", [None])[i]
    de = round(debt / eq, 2) if debt is not None and eq else None
    debt_hist = b.get("Borrowings", [])[-5:]
    cc = ratios.get("Cash Conversion Cycle", [])
    out = {
        "year": bc[i], "borrowings": debt, "net_worth": round(eq), "debt_to_equity": de,
        "debt_trend": debt_hist, "debtor_days": _last(ratios.get("Debtor Days", [])),
        "inventory_days": _last(ratios.get("Inventory Days", [])), "payable_days": _last(ratios.get("Days Payable", [])),
        "ccc": _last(cc), "ccc_trend": cc[-5:], "cols": bc[-5:],
    }
    notes = []
    if de is not None:
        notes.append("Effectively debt-free" if de < 0.1 else f"Debt/equity {de}x" + (" (leveraged)" if de > 1 else ""))
    if len(cc) >= 2 and None not in (cc[-1], cc[-2]) and abs(cc[-1] - cc[-2]) >= 3:
        notes.append(f"Cash conversion cycle {'lengthened' if cc[-1] > cc[-2] else 'shortened'} {abs(cc[-1]-cc[-2]):.0f} days YoY")
    out["notes"] = notes
    return out


def cash(d):
    cf = d["cashflow"]
    cols = cf["cols"]
    r = cf["rows"]
    pat = d["annual"]["rows"].get("Net Profit", [])
    acols = d["annual"]["cols"]
    cfo = r.get("Cash from Operating Activity", [])
    fcf = r.get("Free Cash Flow", [])
    n = min(5, len(cols))
    conv = []
    for c, v in zip(cols[-n:], cfo[-n:]):
        p = pat[acols.index(c)] if c in acols else None
        conv.append(round(v / p * 100) if v is not None and p else None)
    out = {"cols": cols[-n:], "cfo": cfo[-n:], "fcf": fcf[-n:], "cfo_to_pat_pct": conv, "notes": []}
    valid = [x for x in conv if x is not None]
    if valid:
        avg = sum(valid) / len(valid)
        out["notes"].append(f"Operating cash flow averaged {avg:.0f}% of PAT over {len(valid)}y: " +
                            ("profits convert well to cash." if avg >= 85 else "weak conversion, dig into working capital." if avg < 60 else "adequate conversion."))
    pos = [x for x in fcf if x is not None]
    if pos and all(x > 0 for x in pos):
        out["notes"].append("Free cash flow positive every year.")
    elif pos and sum(1 for x in pos if x < 0) >= 2:
        out["notes"].append("Free cash flow negative in multiple years: growth is consuming cash.")
    return out


# ---------- transcripts ----------
def _pdf_text(url: str) -> str:
    def load():
        r = requests.get(url, headers={"User-Agent": UA, "Referer": "https://www.screener.in/"}, timeout=30, allow_redirects=True)
        r.raise_for_status()
        rd = PdfReader(io.BytesIO(r.content))
        return {"text": "\n".join((p.extract_text() or "") for p in rd.pages)}

    return cached(f"pdf_{url}", 30 * 24 * 3600, load)["text"]


FUTURE = r"expect|aim|target|guid|outlook|confident|aspir|going forward|next (year|quarter|two|three)|FY ?'?\d\d|will (grow|be|see|deliver|invest|continue)|ambition|plan to|on track|range"
NUMERIC = r"\d+(\.\d+)?\s?(%|per ?cent|bps|basis points|crore|billion|million|x\b)|double[- ]digit|low[- ]teens|mid[- ]teens|high[- ]teens|single[- ]digit"
DISCLAIM = r"forward-looking|safe harbo|disclaimer|risks? (that|which)|replay|recording|please (note|refer)|moderator|audible"


def _sentences(text: str) -> list[str]:
    t = re.sub(r"\s+", " ", text)
    t = re.sub(r"Page \d+ of \d+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+(?=[A-Z])", t)]


def guidance_quotes(text: str, k: int = 3) -> dict:
    sents = _sentences(text)
    no_guid = next((s for s in sents if re.search(r"(don'?t|do not|does not|not) (provide|give)[^.]{0,60}guidance", s, re.I)), None)
    scored = []
    for s in sents:
        if not (70 <= len(s) <= 340) or re.search(DISCLAIM, s, re.I) or s.rstrip().endswith("?"):
            continue
        f, n = re.search(FUTURE, s, re.I), re.search(NUMERIC, s, re.I)
        if f and n:
            sc = 2 + bool(re.search(r"guid|target|aim|aspir|ambition|expect", s, re.I)) * 2 + bool(re.search(r"margin|growth|capex|revenue|EBITDA", s, re.I))
            scored.append((sc, s))
    scored.sort(key=lambda x: -x[0])
    clean = lambda s: re.sub(r"^[A-Z][\w\.]+(?: [A-Z][\w\.]+){1,3}: ", "", s)
    return {"quotes": [clean(s) for _, s in scored[:k]], "no_explicit_guidance": no_guid}


def _call_quarter(label: str, cols: list[str]) -> str | None:
    m = re.match(r"([A-Z][a-z]{2}) (\d{4})", label)
    if not m:
        return None
    mo, yr = MONTH[m.group(1)], int(m.group(2))
    target = {1: ("Dec", yr - 1), 2: ("Dec", yr - 1), 3: ("Dec", yr - 1), 4: ("Mar", yr), 5: ("Mar", yr), 6: ("Mar", yr),
              7: ("Jun", yr), 8: ("Jun", yr), 9: ("Jun", yr), 10: ("Sep", yr), 11: ("Sep", yr), 12: ("Sep", yr)}[mo]
    q = f"{target[0]} {target[1]}"
    return q if q in cols else None


def _delivered(d, qlabel):
    q = d["quarters"]
    cols, rows = q["cols"], q["rows"]
    if qlabel not in cols:
        return None
    i = cols.index(qlabel)
    sales = rows.get("Sales") or rows.get("Revenue") or []
    opm = rows.get("OPM %", [])
    pat = rows.get("Net Profit", [])
    g = lambda r, j: r[j] if 0 <= j < len(r) else None
    yoy = lambda r: round((r[i] / r[i - 4] - 1) * 100, 1) if i >= 4 and r[i] and r[i - 4] and r[i - 4] > 0 else None
    return {"quarter": qlabel, "revenue": g(sales, i), "revenue_yoy": yoy(sales), "opm": g(opm, i),
            "opm_yoy_bps": round((opm[i] - opm[i - 4]) * 100) if i >= 4 and opm[i] is not None and opm[i - 4] is not None else None,
            "pat": g(pat, i), "pat_yoy": yoy(pat)}


def promises_vs_delivery(d, n_calls: int = 4) -> dict:
    cols = d["quarters"]["cols"]
    calls = [c for c in d["concalls"] if "Transcript" in c["links"]][:n_calls + 1]

    def work(c):
        try:
            t = _pdf_text(c["links"]["Transcript"])
            return c, guidance_quotes(t), None
        except Exception as e:
            return c, None, str(e)[:80]

    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(work, calls))
    rows = []
    for c, g, err in res:
        q = _call_quarter(c["label"], cols)
        rows.append({"call": c["label"], "quarter_reported": q, "transcript": c["links"]["Transcript"], "error": err,
                     "quotes": g["quotes"] if g else [], "no_explicit_guidance": g["no_explicit_guidance"] if g else None})
    # promise made on call i is judged on the quarter reported on the next call
    chron = list(reversed(rows))
    for idx, r in enumerate(chron):
        nxt = chron[idx + 1] if idx + 1 < len(chron) else None
        r["judged_on"] = nxt["quarter_reported"] if nxt else None
        r["delivered"] = _delivered(d, r["judged_on"]) if r["judged_on"] else None
        r["quarter_delivered"] = _delivered(d, r["quarter_reported"]) if r["quarter_reported"] else None
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: bool(r["error"])):
        if r["quarter_reported"] in seen:
            continue
        seen.add(r["quarter_reported"])
        out.append(r)
    out.sort(key=lambda r: rows.index(r))
    return {"calls": out[:n_calls]}


def bull_bear(d, f, t, b, c) -> dict:
    bull, bear = [], []
    notes = " ".join(t["notes"])
    ser = t["series"]
    rev = ser.get("Revenue", [])
    cg = _cagr(rev[0], rev[-1], len(rev) - 1) if len(rev) > 1 else None
    if cg and cg >= 12:
        bull.append(f"Compounding: revenue CAGR {cg}% over {len(rev)-1}y.")
    if cg is not None and cg < 8:
        bear.append(f"Slow top line: revenue CAGR only {cg}% over {len(rev)-1}y.")
    m = ser.get("EBITDA margin %", [])
    if len(m) > 1 and None not in (m[0], m[-1]):
        if m[-1] - m[0] >= 2:
            bull.append(f"Operating leverage: margin up {m[-1]-m[0]:.1f}pp.")
        if m[-1] - m[0] <= -2:
            bear.append(f"Margin compression: down {m[0]-m[-1]:.1f}pp since {t['cols'][0]}.")
    roce = d["top"].get("ROCE")
    if roce and roce >= 20:
        bull.append(f"High return on capital: ROCE {roce:.0f}%.")
    if roce is not None and roce < 12:
        bear.append(f"Weak returns: ROCE {roce:.0f}%.")
    de = b.get("debt_to_equity")
    if de is not None and de < 0.2:
        bull.append("Balance sheet is clean: negligible debt.")
    if de is not None and de > 1 and "Financing Profit" not in d["quarters"]["rows"]:
        bear.append(f"Leverage: debt/equity {de}x.")
    cv = [x for x in c["cfo_to_pat_pct"] if x is not None]
    if cv and sum(cv) / len(cv) >= 90:
        bull.append(f"Earnings are real: operating cash ~{sum(cv)/len(cv):.0f}% of PAT.")
    if cv and sum(cv) / len(cv) < 60 and "Financing Profit" not in d["quarters"]["rows"]:
        bear.append(f"Cash conversion is weak: operating cash ~{sum(cv)/len(cv):.0f}% of PAT.")
    ccc = b.get("ccc_trend", [])
    if len(ccc) >= 3 and None not in (ccc[-1], ccc[-3]) and ccc[-1] - ccc[-3] > 10:
        bear.append(f"Working capital stretching: cash conversion cycle +{ccc[-1]-ccc[-3]:.0f} days in 2y.")
    pe = d["top"].get("Stock P/E")
    if pe and pe > 50:
        bear.append(f"Priced for perfection: P/E {pe:.0f}x.")
    if pe and pe < 18 and cg and cg > 10:
        bull.append(f"Growth at a modest price: P/E {pe:.0f}x.")
    return {"bull": bull[:4], "bear": bear[:4]}


def research(ticker: str, with_calls: bool = True) -> dict:
    d = screener.company(ticker)
    f, t, b, c = financial(d), trajectory(d), balance(d), cash(d)
    out = {
        "ticker": ticker, "name": d["name"], "basis": d.get("basis"),
        "business": business(d), "financial": f, "trajectory": t, "balance": b, "cash": c,
        "bull_bear": bull_bear(d, f, t, b, c),
        "annual_reports": d["annual_reports"][:3],
        "grounding": "Standardised statements derived from filings (screener.in), plus raw concall transcripts. No news or broker notes.",
    }
    if with_calls:
        try:
            out["promises"] = promises_vs_delivery(d)
        except Exception as e:
            out["promises"] = {"calls": [], "error": str(e)[:100]}
        pv = out["promises"]["calls"]
        txt = llm.chat(
            "strong",
            "You are an equity analyst. Using ONLY the provided data, write 3 crisp bullets (max 25 words each) on where "
            "management narrative and reported numbers agree or diverge. Quote numbers. No outside knowledge.",
            str({"promises": pv, "trajectory": t["notes"], "cash": c["notes"], "balance": b["notes"]})[:6000],
            max_tokens=300,
        )
        if txt:
            out["narrative_llm"] = txt
    return out
