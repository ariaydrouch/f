"""Generate the Hironaka-form tables in docs/tables.md and data/tables.json.

    python examples/make_tables.py [--workers 4] [--quick]

Tables
  1. N = 2, d = 1..7, matrix (species) grading
  2. N = 2, d = 1..18, all species equal
  3. d = 2, N = 2..6, all species equal
  4. d = 2, N = 2..5, matrix (bi)grading

Equal-grading series are cached in data/series_cache.json (N = 6 takes ~6 min
with 4 workers).  --quick skips N = 6 if it is not cached.
"""

import argparse
import json
import math
import os
import sys
import time

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import hilbert_series as hs  # noqa: E402

DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA, "series_cache.json")
x = sp.Symbol("x")


def krull_dim(N, d):
    return N if d == 1 else (d - 1) * N * N + 1


# ---------------------------------------------------------------- equal grading

def equal_series(N, d, cache, workers, quick):
    key = f"{N},{d}"
    if key not in cache:
        if quick and N >= 6:
            return None
        _, Zx = hs.hilbert_series(N, d, equal_x=True, workers=workers)
        num, den = sp.fraction(sp.cancel(sp.together(Zx)))
        cache[key] = {"num": hs._coeffs(num, x), "den": hs._coeffs(den, x)}
        with open(CACHE, "w") as f:
            json.dump(cache, f)
    c = cache[key]
    num = sum(v * x ** i for i, v in enumerate(c["num"]))
    den = sum(v * x ** i for i, v in enumerate(c["den"]))
    return hs.ReducedSeries(num / den, x)


def harris_tu(d):
    """Degree of the variety of symmetric d x d matrices of rank <= 3."""
    return 2 ** (d - 3) * math.comb(2 * d - 4, d - 2) // (d - 1) if d >= 3 else 1


def equal_row(rs, hf, **extra):
    return dict(degrees={str(k): v for k, v in hf.degrees.items()},
                numerator=hf.numerator, secondaries=hf.secondaries,
                numerator_degree=len(hf.numerator) - 1,
                palindromic=hf.palindromic, nonnegative=hf.nonnegative,
                e=str(rs.e), **extra)


def table_n2_equal(cache, workers, dmax):
    rows = []
    for d in range(1, dmax + 1):
        rs = equal_series(2, d, cache, workers, False)
        degrees = {1: 1, 2: 1} if d == 1 else {1: d, 2: 3 * d - 3}
        hf = hs.hironaka_form(rs, degrees=degrees)
        h = rs.series(len(hf.numerator))
        assert hs.admissible(hf, h), d
        if d <= 8:
            assert hs.hironaka_candidates(rs)[0].secondaries == hf.secondaries, d
        even = sum(hf.numerator[0::2])
        odd = sum(hf.numerator[1::2])
        rows.append(equal_row(rs, hf, d=d, even_sum=even, odd_sum=odd,
                              harris_tu=harris_tu(d)))
    return rows


def table_d2_equal(cache, workers, quick):
    rows = []
    for N in range(2, 7):
        rs = equal_series(N, 2, cache, workers, quick)
        if rs is None:
            continue
        best = hs.hironaka_candidates(rs)[0]
        h = rs.series(400)
        paper = hs.hironaka_form(rs, degrees=hs.PAPER_DEGREES_D2[N])
        row = dict(N=N, min=equal_row(rs, best),
                   paper=equal_row(rs, paper, admissible=hs.admissible(paper, h)))
        rows.append(row)
    return rows


# -------------------------------------------------------------- species grading

def species_row(N, d):
    xs, raw = hs.molien_weyl_raw(N, d)
    D = krull_dim(N, d)
    f = hs.species_form(raw, D)
    spec_num, spec_deg = f.specialise()
    row = dict(N=N, d=d, krull_dim=D, factors_count=f.num_factors,
               excess=f.num_factors - D, hironaka=f.num_factors == D and bool(f.admissible),
               secondaries=f.at_one(), terms=len(f.numerator),
               factors=[[list(a), m] for a, m in f.factors],
               specialised_degrees={str(k): v for k, v in spec_deg.items()},
               specialised_numerator=spec_num)
    if d == 2:
        row["numerator"] = [[list(m), c] for m, c in sorted(f.numerator.items())]
    row["orbits"] = [[list(m), c, n] for m, (c, n) in
                     sorted(f.orbits().items(), key=lambda t: (sum(t[0]), t[0]))]
    return row


# -------------------------------------------------------------------- markdown

def fmt_degrees(deg):
    return " ".join(f"{k}" + (f"^{v}" if v > 1 else "") for k, v in deg.items())


def fmt_coeffs(c):
    return "[" + ", ".join(str(v) for v in c) + "]"


def factor_types(factors):
    """Group species factors (alpha, m) by sorted alpha (S_d orbit)."""
    out = {}
    for a, m in factors:
        key = tuple(sorted((v for v in a if v), reverse=True))
        out[key] = out.get(key, 0) + m
    return out


def md_species_n2(rows):
    L = ["## 1. N = 2, d = 1..7, matrix grading", ""]
    L.append("Variables x_1..x_d, one per matrix.  Denominator factors grouped by type "
             "(the exponent pattern of x^alpha up to permuting the x_a; e.g. `(1,1)` means "
             "all (1 - x_a x_b), a < b, each with the multiplicity shown).  F = number of "
             "factors, D = Krull dimension.  Numerator terms grouped by S_d orbit: "
             "`rep : coefficient x orbit size`.")
    L.append("")
    L.append("| d | D | F | F - D | Hironaka (species-graded hsop) | P(1,..,1) | terms | orbits |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r['d']} | {r['krull_dim']} | {r['factors_count']} | {r['excess']} | "
                 f"{'yes' if r['hironaka'] else 'no'} | {r['secondaries']} | {r['terms']} | "
                 f"{len(r['orbits'])} |")
    L.append("")
    for r in rows:
        types = factor_types(r["factors"])
        L.append(f"### d = {r['d']}")
        L.append("")
        L.append("Denominator: " + ", ".join(
            f"`{t}` ({m} factors)" for t, m in types.items()))
        L.append("")
        L.append("Numerator (orbit rep : coefficient x orbit size):")
        L.append("")
        L.append("```")
        line = []
        for rep, c, n in r["orbits"]:
            line.append(f"{tuple(rep)}:{c:+d}x{n}")
        width, cur = 0, []
        for item in line:
            if width + len(item) > 100:
                L.append("  ".join(cur))
                cur, width = [], 0
            cur.append(item)
            width += len(item) + 2
        if cur:
            L.append("  ".join(cur))
        L.append("```")
        L.append("")
    return L


def grid(numerator):
    I = max(m[0] for m, _ in numerator)
    J = max(m[1] for m, _ in numerator)
    G = [[0] * (J + 1) for _ in range(I + 1)]
    for (i, j), c in numerator:
        G[i][j] = c
    return G


def md_species_d2(rows):
    L = ["## 4. d = 2, N = 2..5, matrix (bi)grading", ""]
    L.append("Variables x (first matrix), y (second).  Denominator lists every factor "
             "(1 - x^i y^j) as `(i,j)^m`.  Numerator as a grid: row i = power of x, "
             "column j = power of y (blank = 0).")
    L.append("")
    L.append("| N | D | F | F - D | bigraded hsop | P(1,1) | terms |")
    L.append("|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r['N']} | {r['krull_dim']} | {r['factors_count']} | {r['excess']} | "
                 f"{'yes' if r['hironaka'] else 'no'} | {r['secondaries']} | {r['terms']} |")
    L.append("")
    for r in rows:
        L.append(f"### N = {r['N']}")
        L.append("")
        L.append("Denominator: " + " ".join(
            f"({a[0]},{a[1]})" + (f"^{m}" if m > 1 else "") for a, m in r["factors"]))
        L.append("")
        L.append("Specialised to x = y: degrees " + fmt_degrees(
            {int(k): v for k, v in r["specialised_degrees"].items()}))
        L.append("")
        G = grid([(tuple(m), c) for m, c in r["numerator"]])
        w = max(max(len(str(c)) for row in G for c in row), len(str(len(G[0]) - 1))) + 1
        L.append("```")
        L.append("i\\j " + "".join(f"{j:>{w}}" for j in range(len(G[0]))))
        for i, row in enumerate(G):
            L.append(f"{i:>3} " + "".join(f"{(str(c) if c else ''):>{w}}" for c in row))
        L.append("```")
        L.append("")
    return L


def md_equal_n2(rows):
    L = ["## 2. N = 2, d = 1..18, all species equal", ""]
    L.append("Primary degrees 1^d 2^(3d-3) (1 2 for d = 1).  P_k = number of secondaries "
             "of degree k.  S = P(1) = 2^(d-2) Cat(d-2) = 2 HT(d), HT(d) = degree of the "
             "variety of symmetric d x d matrices of rank <= 3.  `even`/`odd` = sum of P_k "
             "over even/odd k.")
    L.append("")
    L.append("| d | D | S = P(1) | even | odd | HT(d) | deg P | e |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r['d']} | {sum(int(v) for v in r['degrees'].values())} | "
                 f"{r['secondaries']} | {r['even_sum']} | {r['odd_sum']} | {r['harris_tu']} | "
                 f"{r['numerator_degree']} | {r['e']} |")
    L.append("")
    L.append("Numerator coefficients P_0, P_1, ... :")
    L.append("")
    L.append("```")
    for r in rows:
        L.append(f"d={r['d']:>2}: {fmt_coeffs(r['numerator'])}")
    L.append("```")
    L.append("")
    return L


def md_equal_d2(rows):
    L = ["## 3. d = 2, N = 2..6, all species equal", ""]
    L.append("`min` = admissible choice with the smallest P(1) (a lower bound for the "
             "number of secondaries, attained whenever primaries of those degrees exist); "
             "`paper` = the denominators of arXiv:2503.20097 (Table 3).")
    L.append("")
    L.append("| N | D | choice | primary degrees | P(1) | deg P | palindromic | admissible |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        for name in ("min", "paper"):
            c = r[name]
            deg = {int(k): v for k, v in c["degrees"].items()}
            adm = "yes" if name == "min" else ("yes" if c["admissible"] else "no")
            L.append(f"| {r['N']} | {sum(deg.values())} | {name} | {fmt_degrees(deg)} | "
                     f"{c['secondaries']} | {c['numerator_degree']} | "
                     f"{'yes' if c['palindromic'] else 'no'} | {adm} |")
    L.append("")
    for r in rows:
        for name in ("min", "paper"):
            c = r[name]
            L.append(f"N={r['N']} {name}: {fmt_coeffs(c['numerator'])}")
            L.append("")
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--dmax-equal", type=int, default=18)
    ap.add_argument("--dmax-species", type=int, default=7)
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

    out = {}
    t = time.time()
    out["n2_species"] = [species_row(2, d) for d in range(1, args.dmax_species + 1)]
    print(f"table 1 done ({time.time() - t:.1f}s)", flush=True)
    out["n2_equal"] = table_n2_equal(cache, args.workers, args.dmax_equal)
    print(f"table 2 done ({time.time() - t:.1f}s)", flush=True)
    out["d2_equal"] = table_d2_equal(cache, args.workers, args.quick)
    print(f"table 3 done ({time.time() - t:.1f}s)", flush=True)
    out["d2_species"] = [species_row(N, 2) for N in range(2, 6)]
    print(f"table 4 done ({time.time() - t:.1f}s)", flush=True)

    with open(os.path.join(DATA, "tables.json"), "w") as f:
        json.dump(out, f)
    L = ["# Hironaka-form tables", "",
         "Generated by `examples/make_tables.py`; machine-readable copy in "
         "`data/tables.json`.  Patterns and their explanations: "
         "`docs/hilbert_series.md`, sections 10-11.", ""]
    L += md_species_n2(out["n2_species"])
    L += md_equal_n2(out["n2_equal"])
    L += md_equal_d2(out["d2_equal"])
    L += md_species_d2(out["d2_species"])
    with open(os.path.join(ROOT, "docs", "tables.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
