import { useEffect, useState } from "react";
import { ago, get, inr, signed, tone } from "./api";
import { Spark } from "./charts";

const WINDOWS = [
  { l: "24h", h: 24 }, { l: "3d", h: 72 }, { l: "7d", h: 168 }, { l: "14d", h: 336 },
];

export function Tag({ cat, label }: { cat: string; label: string }) {
  return <span className={`tag tag-${cat.replace("&", "n")}`}>{label}</span>;
}

function Enrichment({ it, onDig }: { it: any; onDig: (t: string) => void }) {
  const [e, setE] = useState<any>(null);
  useEffect(() => { get(`/api/enrich/${it.ticker}/${it.id}`).then(setE).catch(() => setE({})); }, [it.id]);
  if (!e) return <div className="skeleton" style={{ height: 70 }} />;
  const r = e.results;
  return (
    <div className="enrich">
      {r && (
        <>
          <div className="enrich-h">{r.quarter} · {r.basis} · Rs Cr</div>
          <table className="res">
            <thead><tr><th></th><th>Value</th><th>QoQ</th><th>YoY</th></tr></thead>
            <tbody>
              {r.metrics.map((m: any) => (
                <tr key={m.key}>
                  <td>{m.label}</td><td>{inr(m.value)}</td>
                  <td className={tone(m.qoq)}>{signed(m.qoq)}</td><td className={tone(m.yoy)}>{signed(m.yoy)}</td>
                </tr>
              ))}
              {r.margin && (
                <tr><td>EBITDA margin</td><td>{r.margin.value}%</td>
                  <td className={tone(r.margin.qoq_bps)}>{r.margin.qoq_bps > 0 ? "+" : ""}{r.margin.qoq_bps} bp</td>
                  <td className={tone(r.margin.yoy_bps)}>{r.margin.yoy_bps > 0 ? "+" : ""}{r.margin.yoy_bps} bp</td></tr>
              )}
            </tbody>
          </table>
          {r.read && <p className="read">{r.read}</p>}
        </>
      )}
      {e.mgmt && (
        <div className="mgmt">
          {e.mgmt.name && <div className="mgmt-name">{e.mgmt.name}{e.mgmt.role && <span> · {e.mgmt.role}</span>}</div>}
          {e.mgmt.bio && <p className="read">{e.mgmt.bio}</p>}
          {e.mgmt.bio_note && <p className="muted small">{e.mgmt.bio_note}</p>}
          {e.mgmt.linkedin && <a className="link" href={e.mgmt.linkedin} target="_blank" rel="noreferrer">Find on LinkedIn ↗</a>}
        </div>
      )}
      <div className="row gap">
        <button className="btn" onClick={() => onDig(it.ticker)}>Research {it.ticker} →</button>
        {it.url && <a className="btn ghost" href={it.url} target="_blank" rel="noreferrer">Filing ↗</a>}
      </div>
    </div>
  );
}

function Item({ it, labels, onDig }: { it: any; labels: Record<string, string>; onDig: (t: string) => void }) {
  const [open, setOpen] = useState(false);
  const line = it.summary || it.title;
  return (
    <div className={`item tier-${it.tier}`} onClick={() => setOpen(!open)}>
      <div className="row between">
        <div className="row gap6"><b className="tk">{it.ticker}</b><Tag cat={it.category} label={labels[it.category]} /></div>
        <div className="row gap6 muted small">
          {it.chg_pct != null && <span className={tone(it.chg_pct)}>{signed(it.chg_pct)}</span>}
          <span>{ago(it.ts)}</span>
        </div>
      </div>
      <p className="line">{line}</p>
      {open && <Enrichment it={it} onDig={onDig} />}
    </div>
  );
}

export default function Brief({ meta, onDig }: { meta: any; onDig: (t: string) => void }) {
  const [hours, setHours] = useState(() => Number(localStorage.getItem("finn.hours") ?? 168));
  const [data, setData] = useState<any>(null);
  const [px, setPx] = useState<any[]>([]);
  const [showRoutine, setShowRoutine] = useState(false);
  const labels: Record<string, string> = Object.fromEntries(meta.categories.map((c: any) => [c.id, c.label]));

  useEffect(() => { get("/api/prices").then(setPx).catch(() => {}); }, []);
  useEffect(() => {
    localStorage.setItem("finn.hours", String(hours));
    setData(null);
    get(`/api/digest?hours=${hours}`).then(setData);
  }, [hours]);

  const by = (t: string) => data?.items.filter((i: any) => i.tier === t) ?? [];
  return (
    <div className="page">
      <div className="strip">
        {px.map((m) => (
          <button key={m.ticker} className="tile" onClick={() => onDig(m.ticker)}>
            <div className="row between"><b>{m.ticker}</b><span className={`small ${tone(m.chg_pct)}`}>{signed(m.chg_pct)}</span></div>
            <Spark data={m.spark} w={86} h={22} />
            <div className="muted small">₹{inr(m.price, 0)}{m.vol_mult && m.vol_mult >= 1.5 ? <b className="amber"> · {m.vol_mult}x vol</b> : ""}</div>
          </button>
        ))}
      </div>

      <div className="row between pad">
        <h2>What changed</h2>
        <div className="seg">
          {WINDOWS.map((w) => (
            <button key={w.h} className={hours === w.h ? "on" : ""} onClick={() => setHours(w.h)}>{w.l}</button>
          ))}
        </div>
      </div>

      {!data ? (
        <>{[0, 1, 2].map((i) => <div key={i} className="skeleton" style={{ height: 84, margin: "0 16px 10px" }} />)}</>
      ) : (
        <>
          <p className="summary pad">
            <b>{data.counts.must}</b> must-read · <b>{data.counts.notable}</b> notable · <span className="muted">{data.counts.routine} routine filings tucked away</span>
          </p>
          <div className="list">
            {by("must").map((i: any) => <Item key={i.id} it={i} labels={labels} onDig={onDig} />)}
            {by("notable").length > 0 && <div className="sect">Notable</div>}
            {by("notable").map((i: any) => <Item key={i.id} it={i} labels={labels} onDig={onDig} />)}
            {data.counts.must + data.counts.notable === 0 && <p className="muted pad">Nothing material in this window. That is the signal.</p>}
            {by("routine").length > 0 && (
              <button className="collapse" onClick={() => setShowRoutine(!showRoutine)}>
                {showRoutine ? "Hide" : "Show"} {by("routine").length} routine filings
              </button>
            )}
            {showRoutine && by("routine").map((i: any) => (
              <div key={i.id} className="routine row between">
                <span><b>{i.ticker}</b> {i.summary || i.title}</span><span className="muted small">{ago(i.ts)}</span>
              </div>
            ))}
          </div>
          {data.items[0]?.source && <p className="muted small pad foot">Source: {data.items[0].source === "bse" ? "BSE corporate announcements" : "BSE filings via screener.in"} · classified by rules</p>}
        </>
      )}
    </div>
  );
}
