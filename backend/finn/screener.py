"""screener.in adapter: standardised financials, announcements, concall/AR links."""
import re

import requests
from bs4 import BeautifulSoup

from .config import UA
from .store import cached

BASE = "https://www.screener.in"


def num(s):
    if s is None:
        return None
    s = str(s).replace(",", "").replace("%", "").replace("₹", "").strip()
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _get(url: str) -> str:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"screener {r.status_code} for {url}")
    return r.text


def _table(soup, sec_id: str) -> dict:
    t = soup.select_one(f"#{sec_id} table")
    if not t:
        return {}
    rows = [[c.get_text(" ", strip=True) for c in r.select("th,td")] for r in t.select("tr")]
    cols = rows[0][1:]
    out = {"cols": cols, "rows": {}}
    for r in rows[1:]:
        if len(r) < 2 or not r[0]:
            continue
        label = re.sub(r"\s*\+$", "", r[0]).strip()
        out["rows"][label] = [num(x) for x in r[1:]]
    return out


def _parse(html: str) -> dict:
    s = BeautifulSoup(html, "lxml")
    top = {}
    for li in s.select("#top-ratios li"):
        n = li.select_one(".name")
        v = li.select_one(".value .number") or li.select_one(".number")
        if n and v:
            top[n.get_text(strip=True)] = num(v.get_text(strip=True))
    about = s.select_one(".about")
    cid = None
    el = s.select_one("[data-url*='/concalls/add-']")
    if el:
        m = re.search(r"add-(\d+)", el["data-url"])
        cid = m and m.group(1)
    anns = []
    for li in s.select("#company-announcements-tab li"):
        a = li.select_one("a")
        tm = li.select_one("time")
        if not a or not tm:
            continue
        small = li.select_one(".smaller")
        title = a.get_text(" ", strip=True)
        title = title.replace(small.get_text(" ", strip=True), "").strip() if small else title
        summ = ""
        if small:
            summ = small.get_text(" ", strip=True).split(" - ", 1)[-1] if " - " in small.get_text() else ""
        anns.append({"title": title, "ts": tm["datetime"], "url": a["href"], "summary": summ})
    concalls = []
    for li in s.select(".concalls li"):
        d = li.select_one("div")
        links = {a.get_text(strip=True): a["href"] for a in li.select("a")}
        if d and links:
            concalls.append({"label": d.get_text(strip=True), "links": links})
    ars = [
        {"label": a.get_text(" ", strip=True), "url": a["href"]}
        for a in s.select("#documents .documents")
        if a.select_one("h3") and "Annual" in a.select_one("h3").get_text()
        for a in a.select("a")
    ]
    name = s.select_one("h1")
    return {
        "name": name.get_text(strip=True) if name else None,
        "about": about.get_text(" ", strip=True) if about else "",
        "top": top,
        "company_id": cid,
        "quarters": _table(s, "quarters"),
        "annual": _table(s, "profit-loss"),
        "balance": _table(s, "balance-sheet"),
        "cashflow": _table(s, "cash-flow"),
        "ratios": _table(s, "ratios"),
        "announcements": anns,
        "concalls": concalls,
        "annual_reports": ars,
    }


def _load(ticker: str) -> dict:
    last = None
    for suffix in ("/consolidated/", "/"):
        try:
            d = _parse(_get(f"{BASE}/company/{ticker}{suffix}"))
            if d["quarters"] and d["annual"]:
                d["basis"] = "consolidated" if "consol" in suffix else "standalone"
                return d
        except Exception as e:
            last = e
    raise RuntimeError(f"screener data unavailable for {ticker}: {last}")


def company(ticker: str) -> dict:
    return cached(f"scr_{ticker}", 6 * 3600, lambda: _load(ticker), snapshot=f"scr_{ticker}.json")
