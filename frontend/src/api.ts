export const get = async <T = any>(path: string): Promise<T> => {
  const r = await fetch(path);
  if (!r.ok) throw new Error((await r.text()).slice(0, 160));
  return r.json();
};
export const post = async <T = any>(path: string, body: unknown): Promise<T> => {
  const r = await fetch(path, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
};

export const inr = (n: number | null | undefined, d = 0) =>
  n == null ? "—" : n.toLocaleString("en-IN", { maximumFractionDigits: d, minimumFractionDigits: d });

export const compact = (n: number | null | undefined) => {
  if (n == null) return "—";
  const a = Math.abs(n);
  if (a >= 1e5) return `${(n / 1e5).toFixed(2)} L Cr`;
  if (a >= 1e3) return `${(n / 1e3).toFixed(1)}k Cr`;
  return `${inr(n)} Cr`;
};

export const ago = (iso: string) => {
  const m = (Date.now() - new Date(iso).getTime()) / 60000;
  if (m < 60) return `${Math.max(1, Math.round(m))}m`;
  if (m < 60 * 24) return `${Math.round(m / 60)}h`;
  return `${Math.round(m / 1440)}d`;
};

export const signed = (n: number | null | undefined, d = 1) => (n == null ? "—" : `${n > 0 ? "+" : ""}${n.toFixed(d)}%`);
export const tone = (n: number | null | undefined) => (n == null || n === 0 ? "" : n > 0 ? "up" : "down");
