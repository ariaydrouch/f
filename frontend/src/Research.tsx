import { useEffect, useRef, useState } from "react";
import { compact, get, inr } from "./api";
import { Bars } from "./charts";

const SECTIONS = [
  ["snapshot", "Snapshot"], ["trajectory", "Trajectory"], ["balance", "Balance sheet"], ["cash", "Cash quality"],
  ["promises", "Promised vs delivered"], ["bullbear", "Bull / Bear"],
] as const;

const SECTION_ALIAS: Record<string, string> = {
  business: "snapshot", financial: "snapshot", trajectory: "trajectory", balance: "balance", cash: "cash", promises: "promises", bull_bear: "bullbear",
};

function Card({ id, title, sub, children }: { id: string; title: string; sub?: string; children: any }) {
  return (
    <section id={`sec-${id}`} className="card">
      <div className="card-h"><h3>{title}</h3>{sub && <span className="muted small">{sub}</span>}</div>
      {children}
    </section>
  );
}

const Notes = ({ n }: { n: string[] }) => <ul className="notes">{n.map((x, i) => <li key={i}>{x}</li>)}</ul>;

function Delivery({ d }: { d: any }) {
  if (!d) return <div className="muted small">Next quarter not yet reported.</div>;
  return (
    <div className="deliv">
      <b>Delivered {d.quarter}:</b> revenue {d.revenue_yoy != null ? `${d.revenue_yoy > 0 ? "+" : ""}${d.revenue_yoy}% YoY` : "—"} · EBITDA margin {d.opm ?? "—"}%
      {d.opm_yoy_bps != null && ` (${d.opm_yoy_bps > 0 ? "+" : ""}${d.opm_yoy_bps} bp YoY)`} · PAT {d.pat_yoy != null ? `${d.pat_yoy > 0 ? "+" : ""}${d.pat_yoy}% YoY` : "—"}
    </div>
  );
}

export default function Research({ ticker, section, setTicker, meta }: { ticker: string | null; section: string | null; setTicker: (t: string) => void; meta: any }) {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState("");
  const [q, setQ] = useState("");
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ticker) return;
    setData(null); setErr("");
    get(`/api/research/${ticker}`).then(setData).catch((e) => setErr(e.message));
  }, [ticker]);

  useEffect(() => {
    if (!data || !section) return;
    const id = SECTION_ALIAS[section];
    setTimeout(() => document.getElementById(`sec-${id}`)?.scrollIntoView({ behavior: "smooth", block: "start" }), 120);
  }, [data, section]);

  const demo = meta.research_demo as string[];
  const go = (t: string) => { setTicker(t.trim().toUpperCase().replace(".NS", "")); setQ(""); };

  return (
    <div className="page" ref={ref}>
      <form className="pad" onSubmit={(e) => { e.preventDefault(); q && go(q); }}>
        <h2>Research any NSE company</h2>
        <div className="row gap" style={{ marginTop: 8 }}>
          <input className="input" placeholder="Ticker, e.g. PIDILITIND, DIXON, CDSL" value={q} onChange={(e) => setQ(e.target.value)} />
          <button className="btn">Go</button>
        </div>
        <div className="chips" style={{ marginTop: 8 }}>
          {[...demo, ...meta.portfolio.map((p: any) => p.ticker).filter((t: string) => !demo.includes(t)).slice(0, 4)].map((t) => (
            <button key={t} className={`chip ${ticker === t ? "on" : ""}`} onClick={() => go(t)}>{t}</button>
          ))}
        </div>
      </form>

      {!ticker && <p className="muted pad">Grounded only in primary data: filings and concall transcripts. No news, no broker notes.</p>}
      {err && <p className="down pad">Couldn't load {ticker}. {err}</p>}
      {ticker && !data && !err && <div className="pad"><div className="skeleton" style={{ height: 120 }} /><div className="skeleton" style={{ height: 160, marginTop: 10 }} /><p className="muted small" style={{ marginTop: 8 }}>Reading statements and concall transcripts…</p></div>}

      {data && (
        <>
          <div className="pad hero">
            <h2>{data.name}</h2>
            <p className="muted small">{data.basis} financials · {data.grounding}</p>
          </div>
          <div className="jump">
            {SECTIONS.map(([id, l]) => <button key={id} className="chip" onClick={() => document.getElementById(`sec-${id}`)?.scrollIntoView({ behavior: "smooth", block: "start" })}>{l}</button>)}
          </div>

          <Card id="snapshot" title="Snapshot" sub={`FY ${data.financial.year}`}>
            <div className="kpis">
              {data.financial.cards.map((c: any) => (
                <div key={c.k} className="kpi"><span className="muted small">{c.k}</span><b>{c.u === "Rs Cr" ? compact(c.v) : `${inr(c.v, c.u === "%" || c.u === "x" ? 1 : 2)}${c.u === "%" ? "%" : c.u === "x" ? "x" : ""}`}</b></div>
              ))}
            </div>
            <details>
              <summary className="muted small">What it does</summary>
              <p className="read">{data.business.about}</p>
              <p className="muted small">{data.business.note}</p>
            </details>
          </Card>

          <Card id="trajectory" title="Trajectory" sub="5-year direction">
            <Notes n={data.trajectory.notes} />
            <div className="lab">Revenue (Rs Cr)</div>
            <Bars labels={data.trajectory.cols} values={data.trajectory.series.Revenue} fmt={(n) => compact(n).replace(" Cr", "")} />
            <div className="lab">PAT (Rs Cr)</div>
            <Bars labels={data.trajectory.cols} values={data.trajectory.series.PAT} fmt={(n) => compact(n).replace(" Cr", "")} />
            <div className="lab">EBITDA margin (%)</div>
            <Bars labels={data.trajectory.cols} values={data.trajectory.series["EBITDA margin %"]} fmt={(n) => `${n}%`} />
          </Card>

          <Card id="balance" title="Balance sheet" sub={data.balance.year}>
            <div className="kpis">
              <div className="kpi"><span className="muted small">Borrowings</span><b>{compact(data.balance.borrowings)}</b></div>
              <div className="kpi"><span className="muted small">Net worth</span><b>{compact(data.balance.net_worth)}</b></div>
              <div className="kpi"><span className="muted small">Debt / equity</span><b>{data.balance.debt_to_equity ?? "—"}x</b></div>
              <div className="kpi"><span className="muted small">Debtor days</span><b>{data.balance.debtor_days ?? "—"}</b></div>
            </div>
            <Notes n={data.balance.notes} />
            <div className="lab">Cash conversion cycle (days)</div>
            <Bars labels={data.balance.cols} values={data.balance.ccc_trend} h={44} />
          </Card>

          <Card id="cash" title="Cash quality" sub="do profits become cash?">
            <Notes n={data.cash.notes} />
            <div className="lab">Operating cash flow / PAT (%)</div>
            <Bars labels={data.cash.cols} values={data.cash.cfo_to_pat_pct} fmt={(n) => `${n}%`} h={50} />
            <div className="lab">Free cash flow (Rs Cr)</div>
            <Bars labels={data.cash.cols} values={data.cash.fcf} fmt={(n) => compact(n).replace(" Cr", "")} h={50} />
          </Card>

          <Card id="promises" title="Promised vs delivered" sub="last concalls vs next reported quarter">
            {data.promises.calls.map((c: any, i: number) => (
              <div key={i} className="promise">
                <div className="row between"><b>{c.call} call</b><span className="muted small">{c.quarter_reported ? `on ${c.quarter_reported} results` : ""}</span></div>
                {c.error && <p className="muted small">Transcript unavailable from this host. <a className="link" href={c.transcript} target="_blank" rel="noreferrer">Open ↗</a></p>}
                {c.no_explicit_guidance && <p className="flag">Management says it gives no explicit guidance.</p>}
                {c.quotes.map((x: string, j: number) => <blockquote key={j}>“{x}”</blockquote>)}
                {!c.error && <Delivery d={c.delivered} />}
              </div>
            ))}
            {data.narrative_llm && <p className="read">{data.narrative_llm}</p>}
            <p className="muted small">Quotes are extracted verbatim from transcripts by pattern, not paraphrased.</p>
          </Card>

          <Card id="bullbear" title="Bull vs bear" sub="from the numbers above">
            <div className="bb">
              <div><h4 className="up">Bull</h4><ul>{data.bull_bear.bull.map((x: string, i: number) => <li key={i}>{x}</li>)}</ul></div>
              <div><h4 className="down">Bear</h4><ul>{data.bull_bear.bear.map((x: string, i: number) => <li key={i}>{x}</li>)}{!data.bull_bear.bear.length && <li className="muted">No red flags in the headline data.</li>}</ul></div>
            </div>
            <div className="row gap wrap" style={{ marginTop: 8 }}>
              {data.annual_reports.map((a: any) => <a key={a.url} className="btn ghost" href={a.url} target="_blank" rel="noreferrer">{a.label} ↗</a>)}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
