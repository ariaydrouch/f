import { useEffect, useState } from "react";
import { ago, get, signed, tone } from "./api";
import { Tag } from "./Brief";

export type Settings = { vol: number; move: number; cats: string[] };

function Stepper({ label, value, step, min, max, unit, onChange }: any) {
  return (
    <div className="stepper">
      <span className="muted small">{label}</span>
      <div className="row gap">
        <button onClick={() => onChange(Math.max(min, +(value - step).toFixed(1)))}>−</button>
        <b>{value}{unit}</b>
        <button onClick={() => onChange(Math.min(max, +(value + step).toFixed(1)))}>+</button>
      </div>
    </div>
  );
}

export default function Alerts({ meta, s, setS, onDig }: { meta: any; s: Settings; setS: (s: Settings) => void; onDig: (t: string) => void }) {
  const [data, setData] = useState<any>(null);
  const labels: Record<string, string> = Object.fromEntries(meta.categories.map((c: any) => [c.id, c.label]));
  useEffect(() => {
    setData(null);
    const t = setTimeout(() => get(`/api/alerts?hours=168&vol_mult=${s.vol}&move_pct=${s.move}&cats=${encodeURIComponent(s.cats.join(","))}`).then(setData), 250);
    return () => clearTimeout(t);
  }, [s]);
  const toggle = (c: string) => setS({ ...s, cats: s.cats.includes(c) ? s.cats.filter((x) => x !== c) : [...s.cats, c] });
  return (
    <div className="page">
      <div className="pad"><h2>Your tripwires</h2><p className="muted small">You decide what “unusual” means. FINN watches every close and filing.</p></div>
      <div className="panel">
        <Stepper label="Volume above avg ×" value={s.vol} step={0.5} min={1} max={10} unit="x" onChange={(v: number) => setS({ ...s, vol: v })} />
        <Stepper label="Daily price move ±" value={s.move} step={0.5} min={0.5} max={15} unit="%" onChange={(v: number) => setS({ ...s, move: v })} />
        <div className="muted small" style={{ margin: "10px 0 6px" }}>Filings I care about</div>
        <div className="chips">
          {meta.categories.filter((c: any) => c.id !== "unclassified").map((c: any) => (
            <button key={c.id} className={`chip ${s.cats.includes(c.id) ? "on" : ""}`} onClick={() => toggle(c.id)}>{c.label}</button>
          ))}
        </div>
      </div>
      <div className="row between pad"><h2>Triggered</h2><span className="muted small">{data ? `${data.count} now` : ""}</span></div>
      <div className="list">
        {!data && <div className="skeleton" style={{ height: 80 }} />}
        {data?.alerts.map((a: any, i: number) => (
          <div key={i} className={`item alert ${a.kind}`} onClick={() => onDig(a.ticker)}>
            <div className="row between">
              <div className="row gap6"><b className="tk">{a.ticker}</b>{a.kind === "market" ? <span className="tag tag-mkt">Market</span> : <Tag cat={a.item.category} label={labels[a.item.category]} />}</div>
              <span className="muted small">{a.kind === "filing" ? ago(a.item.ts) : "EOD"}</span>
            </div>
            {a.kind === "market" ? (
              <p className="line">{a.reasons.join(" · ")} <span className={tone(a.chg_pct)}>({signed(a.chg_pct)})</span></p>
            ) : (
              <p className="line">{a.item.summary || a.item.title}</p>
            )}
          </div>
        ))}
        {data?.count === 0 && <p className="muted pad">Quiet. Loosen a threshold to see what it would have caught.</p>}
      </div>
    </div>
  );
}
