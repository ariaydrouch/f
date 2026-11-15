export function Spark({ data, w = 64, h = 24, color }: { data: number[]; w?: number; h?: number; color?: string }) {
  if (!data?.length) return null;
  const min = Math.min(...data), max = Math.max(...data), r = max - min || 1;
  const pts = data.map((v, i) => `${(i / (data.length - 1)) * w},${h - 2 - ((v - min) / r) * (h - 4)}`).join(" ");
  const up = data[data.length - 1] >= data[0];
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      <polyline points={pts} fill="none" stroke={color ?? (up ? "var(--up)" : "var(--down)")} strokeWidth="1.6" strokeLinejoin="round" />
    </svg>
  );
}

export function Bars({ labels, values, fmt, h = 64 }: { labels: string[]; values: (number | null)[]; fmt?: (n: number) => string; h?: number }) {
  const nums = values.filter((v): v is number => v != null);
  const max = Math.max(...nums.map(Math.abs), 1);
  return (
    <div className="bars" style={{ height: h + 28 }}>
      {values.map((v, i) => (
        <div key={i} className="bar-col">
          <span className="bar-val">{v == null ? "—" : fmt ? fmt(v) : Math.round(v)}</span>
          <div className="bar-track" style={{ height: h }}>
            <div className={`bar ${v != null && v < 0 ? "neg" : ""} ${i === values.length - 1 ? "last" : ""}`} style={{ height: `${v == null ? 0 : Math.max(4, (Math.abs(v) / max) * 100)}%` }} />
          </div>
          <span className="bar-lab">{labels[i]?.replace(/ 20(\d\d)/, " '$1")}</span>
        </div>
      ))}
    </div>
  );
}
