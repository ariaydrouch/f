# FINN: a financial investment agent for the daily investor (mobile-first)

Built for the ENAM AI Engineer Build Challenge. FINN filters a firehose of filings and prices down to the few things that matter (push), and answers on-demand research grounded only in primary sources (pull).

## Run it

```bash
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
python3 -m uvicorn finn.main:app --app-dir backend --port 8000   # serves API + the built app
```

Open http://localhost:8000 on a phone or in a mobile-width browser. For frontend dev, run `npm run dev` in `frontend/` (proxies `/api` to :8000).

Optional LLM (any OpenAI-compatible endpoint): `FINN_LLM_API_KEY`, `FINN_LLM_BASE_URL`, `FINN_LLM_CHEAP_MODEL`, `FINN_LLM_STRONG_MODEL`. The app works without it.

Tests: `python3 -m pytest backend/tests`. Refresh the offline fallback snapshot: `python3 scripts/refresh_snapshot.py`.

## Interaction model

One screen of judgment, one command bar.
- **Brief (push):** a time-windowed digest (24h / 3d / 7d / 14d). Must-reads first, notable next, routine filings collapsed behind one line. Tap an item to expand an enrichment that depends on its type: results become a Revenue / EBITDA / PBT / PAT table with QoQ and YoY; management changes show the person, role and a LinkedIn lookup.
- **Alerts (push):** you set what "unusual" means (volume multiple, daily move %, filing categories you care about) and FINN shows what trips those wires.
- **Research (pull):** any NSE ticker. Snapshot, 5-year trajectory, balance sheet, cash quality, bull/bear, and "promised vs delivered" built from the last four concall transcripts.
- **Ask bar:** a persistent command bar routes natural language ("did Titan deliver on what it promised?") to the right view and section.

## Architecture and decisions

| Concern | Choice |
|---|---|
| Prices/volume | Yahoo chart API (EOD), 20-day average volume for the spike test |
| Announcements | BSE API first; falls back to BSE filings as surfaced by screener.in (BSE blocks many datacentre IPs) |
| Fundamentals | screener.in standardised statements, plus concall transcript PDFs via the links screener exposes |
| Classification | Rule taxonomy + priority score (0-100). Free, instant, testable. Titles are often generic ("Reg 30 (LODR)"), so rules read the one-line summary too |
| LLM use | Optional and routed by tier: cheap model for bio/short text, strong model only for narrative-vs-numbers synthesis. All calls disk-cached |
| Cost | Zero LLM calls on the default path. Fetches are TTL-cached; transcript PDFs are cached for 30 days |
| Reliability | Every fetch falls back: live, then stale cache, then bundled snapshot in `data/snapshot` |

**Primary-source discipline.** Pull-side numbers come from standardised statements derived from filings and from raw transcripts. No news, broker notes or model memory. Guidance quotes are extracted verbatim by pattern, never paraphrased, and when management says it gives no guidance (TCS does) FINN says so rather than inventing some.

## What I deliberately left out
- Parsing the results filing PDF itself. The headline numbers come from screener's standardised quarterly table, which is the same data but can lag the filing by hours.
- Real-time push notifications (web push / email). Alerts are evaluated on demand against EOD data.
- Segment / revenue mix from annual reports, and bank-specific views (banks show financing profit instead of EBITDA).
- Auth, per-user portfolios, persistence beyond localStorage.

## Next
1. Parse the results PDF with a cheap model for exact figures and exceptional items; diff against screener to catch restatements.
2. Score management credibility across quarters (promise hit-rate), as in ENAM's Wave 2 "earnings call analyzer".
3. Web push for tripwires; a per-user portfolio.
4. LLM promise extraction from transcripts, constrained to quoted spans, with a verification pass.
