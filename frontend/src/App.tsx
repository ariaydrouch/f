import { useEffect, useState } from "react";
import { get, post } from "./api";
import Alerts, { Settings } from "./Alerts";
import Brief from "./Brief";
import Research from "./Research";

type Tab = "brief" | "alerts" | "research";

const EXAMPLES = ["what changed in 3 days", "did Titan deliver on what it promised?", "unusual volume", "Asian Paints debt and cash"];

export default function App() {
  const [meta, setMeta] = useState<any>(null);
  const h = window.location.hash.replace("#", "").split("/");
  const [tab, setTab] = useState<Tab>(h[0] === "alerts" || h[0] === "research" ? h[0] : "brief");
  const [ticker, setTicker] = useState<string | null>(h[0] === "research" && h[1] ? h[1].toUpperCase() : null);
  const [section, setSection] = useState<string | null>(null);
  const [s, setS] = useState<Settings | null>(null);
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    get("/api/meta").then((m) => {
      setMeta(m);
      const saved = localStorage.getItem("finn.settings");
      setS(saved ? JSON.parse(saved) : { vol: 2, move: 3, cats: m.default_watch });
    });
  }, []);
  useEffect(() => { if (s) localStorage.setItem("finn.settings", JSON.stringify(s)); }, [s]);

  const dig = (t: string, sec: string | null = null) => { setTicker(t); setSection(sec); setTab("research"); window.scrollTo(0, 0); };

  const ask = async (text: string) => {
    if (!text.trim()) return;
    setBusy(true);
    try {
      const r = await post("/api/ask", { q: text });
      if (r.intent === "research") dig(r.ticker, r.section);
      else if (r.intent === "alerts") setTab("alerts");
      else { localStorage.setItem("finn.hours", String(r.hours)); setTab("brief"); window.location.hash = `w${r.hours}`; }
    } finally { setBusy(false); setQ(""); }
  };

  if (!meta || !s) return <div className="boot">FINN</div>;
  return (
    <div className="app">
      <header className="top">
        <div className="logo">FINN<i /></div>
        <span className="muted small">{new Date().toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short" })} · {meta.portfolio.length} stocks</span>
      </header>
      <main key={tab === "brief" ? window.location.hash : tab}>
        {tab === "brief" && <Brief meta={meta} onDig={(t) => dig(t)} />}
        {tab === "alerts" && <Alerts meta={meta} s={s} setS={setS} onDig={(t) => dig(t)} />}
        {tab === "research" && <Research meta={meta} ticker={ticker} section={section} setTicker={(t) => { setTicker(t); setSection(null); }} />}
      </main>
      <div className="dock">
        <div className="examples">{EXAMPLES.map((e) => <button key={e} onClick={() => ask(e)}>{e}</button>)}</div>
        <form onSubmit={(e) => { e.preventDefault(); ask(q); }} className="ask">
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ask FINN anything about your stocks…" />
          <button disabled={busy}>{busy ? "…" : "→"}</button>
        </form>
        <nav className="tabs">
          {(["brief", "alerts", "research"] as Tab[]).map((t) => (
            <button key={t} className={tab === t ? "on" : ""} onClick={() => setTab(t)}>{t === "brief" ? "Brief" : t === "alerts" ? "Alerts" : "Research"}</button>
          ))}
        </nav>
      </div>
    </div>
  );
}
