"""Per-announcement enrichment: what earns attention depends on the category."""
import re
from urllib.parse import quote_plus

from . import llm, screener

ALIASES = {
    "revenue": ["Sales", "Revenue"],
    "ebitda": ["Operating Profit", "Financing Profit"],
    "pbt": ["Profit before tax"],
    "pat": ["Net Profit"],
}
LABEL = {"revenue": "Revenue", "ebitda": "EBITDA", "pbt": "PBT", "pat": "PAT"}


def _row(rows, keys):
    for k in keys:
        if k in rows:
            return rows[k]
    return None


def _pct(a, b):
    if a is None or b in (None, 0):
        return None
    return round((a / abs(b) - 1) * 100, 1) if b > 0 else None


def results_card(ticker: str) -> dict:
    d = screener.company(ticker)
    q = d["quarters"]
    cols, rows = q["cols"], q["rows"]
    i = len(cols) - 1
    out = {"quarter": cols[i], "basis": d.get("basis"), "unit": "Rs Cr", "metrics": [], "source": "screener.in standardised quarterly financials"}
    bank = "Financing Profit" in rows
    for k, aliases in ALIASES.items():
        r = _row(rows, aliases)
        if not r:
            continue
        cur, qoq_base = r[i], r[i - 1] if i >= 1 else None
        yoy_base = r[i - 4] if i >= 4 else None
        out["metrics"].append({
            "key": k, "label": LABEL[k] + (" (fin. profit)" if bank and k == "ebitda" else ""),
            "value": cur, "qoq": _pct(cur, qoq_base), "yoy": _pct(cur, yoy_base),
            "prev_q": qoq_base, "prev_y": yoy_base,
        })
    m = {x["key"]: x for x in out["metrics"]}
    rv, eb = m.get("revenue"), m.get("ebitda")
    if rv and eb and not bank:
        mg = lambda e, r: e / r * 100 if e is not None and r else None
        cur, pq, py = mg(eb["value"], rv["value"]), mg(eb["prev_q"], rv["prev_q"]), mg(eb["prev_y"], rv["prev_y"])
        out["margin"] = {"value": round(cur, 1) if cur is not None else None,
                         "qoq_bps": round((cur - pq) * 100) if None not in (cur, pq) else None,
                         "yoy_bps": round((cur - py) * 100) if None not in (cur, py) else None}
    rev, pat = m.get("revenue"), m.get("pat")
    if rev and pat and rev["yoy"] is not None and pat["yoy"] is not None:
        diff = pat["yoy"] - rev["yoy"]
        out["read"] = (
            f"Revenue {rev['yoy']:+.1f}% YoY, PAT {pat['yoy']:+.1f}% YoY: "
            + ("profit growing faster than sales (operating leverage)." if diff > 5 else
               "profit lagging sales (margin pressure)." if diff < -5 else "profit tracking sales.")
        )
    return out


def mgmt_card(item: dict) -> dict:
    text = f"{item['title']}. {item.get('summary', '')}"
    m = re.search(r"(?:appoint\w*|approved|reappointed|named)\s+(?:of\s+)?((?:Shri|Mr\.?|Ms\.?|Dr\.?|Smt\.?)?\s*[A-Z][\w\.]+(?:\s+[A-Z][\w\.]+){0,3})\s+(?:as|to)\s+([^.,;]+)", text)
    name, role = (m.group(1).strip(), m.group(2).strip()) if m else (None, None)
    if not name:
        m = re.search(r"([A-Z][\w\.]+(?:\s+[A-Z][\w\.]+){1,3})\s+(?:resign|appointed|reappointed)", text)
        name = m and m.group(1)
    card = {"name": name, "role": role, "bio": None, "bio_note": None}
    if name:
        card["linkedin"] = "https://www.linkedin.com/search/results/people/?keywords=" + quote_plus(f"{name} {item['company']}")
        bio = llm.chat(
            "cheap",
            "You write 2-sentence professional backgrounds of Indian corporate executives for investors. "
            "If you do not reliably know the person, reply exactly UNKNOWN. Never invent employers or dates.",
            f"Person: {name}. Context: {text}",
            max_tokens=120,
        )
        if bio and "UNKNOWN" not in bio:
            card["bio"] = bio
            card["bio_note"] = "Model-written, unverified. Check LinkedIn."
        elif not llm.available():
            card["bio_note"] = "Set FINN_LLM_API_KEY to auto-write a background; use the LinkedIn link meanwhile."
    return card


def enrich(item: dict) -> dict:
    cat = item["category"]
    out = {"id": item["id"], "category": cat, "line": item.get("summary") or item["title"]}
    try:
        if cat == "results" and item["priority"] >= 80:
            out["results"] = results_card(item["ticker"])
        elif cat == "management_change":
            out["mgmt"] = mgmt_card(item)
    except Exception as e:
        out["error"] = str(e)[:120]
    return out
