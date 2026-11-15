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

def fmt_coeffs(c):
    return ", ".join(str(v) for v in c)


def mono(alpha, names):
    parts = []
    for v, n in zip(alpha, names):
        if v:
            parts.append(n if v == 1 else f"{n}^{v}")
    return " ".join(parts) or "1"


def equal_den(deg):
    return " ".join(("(1-x)" if k == 1 else f"(1-x^{k})") + (f"^{m}" if m > 1 else "")
                    for k, m in sorted(deg.items()))


def equal_block(label, numerator, degrees):
    return [f"{label}",
            f"  numerator:   {fmt_coeffs(numerator)}",
            f"  denominator: {equal_den({int(k): v for k, v in degrees.items()})}", ""]


def md_species_n2(rows):
    L = ["## 1. N = 2, d = 1..7, matrix grading", "",
         "Numerator in monomial symmetric functions: `m[2,1,1]` = sum of all distinct "
         "permutations of x1^2 x2 x3.", ""]
    for r in rows:
        d = r["d"]
        names = [f"x{a + 1}" for a in range(d)]
        den = {}
        for alpha, m in r["factors"]:
            key = tuple(sorted((v for v in alpha if v), reverse=True))
            den.setdefault(key, set()).add(m)
        L.append(f"### d = {d}")
        L.append("")
        L.append("```")
        L.append("denominator: " + " ".join(
            f"(1-{mono(k + (0,) * (d - len(k)), names)})" + (f"^{max(ms)}" if max(ms) > 1 else "")
            for k, ms in den.items()) + ("   (each over all permutations of the x's)" if d > 1 else ""))
        L.append("numerator:")
        for rep, c, n in r["orbits"]:
            L.append(f"  {'m[' + ','.join(str(v) for v in rep if v) + ']' if any(rep) else '1'}: {c}")
        L.append("```")
        L.append("")
    return L


def md_equal_n2(rows):
    L = ["## 2. N = 2, d = 1..18, all species equal", "",
         "Numerator coefficients from degree 0 upwards.", "", "```"]
    for r in rows:
        L += equal_block(f"d = {r['d']}", r["numerator"], r["degrees"])
    L += ["```", ""]
    return L


def md_equal_d2(rows):
    L = ["## 3. d = 2, N = 2..6, all species equal", "",
         "Numerator coefficients from degree 0 upwards.", "", "```"]
    for r in rows:
        L += equal_block(f"N = {r['N']}", r["min"]["numerator"], r["min"]["degrees"])
    L += ["```", ""]
    return L


def md_species_d2(rows):
    L = ["## 4. d = 2, N = 2..5, matrix grading", "",
         "Numerator grid: row i = power of x, column j = power of y.", ""]
    for r in rows:
        L.append(f"### N = {r['N']}")
        L.append("")
        L.append("```")
        L.append("denominator: " + " ".join(
            f"(1-{mono(a, ['x', 'y'])})" + (f"^{m}" if m > 1 else "") for a, m in r["factors"]))
        L.append("numerator:")
        num = [(tuple(m), c) for m, c in r["numerator"]]
        I = max(m[0] for m, _ in num)
        J = max(m[1] for m, _ in num)
        G = [[0] * (J + 1) for _ in range(I + 1)]
        for (i, j), c in num:
            G[i][j] = c
        w = max(max(len(str(c)) for row in G for c in row), len(str(J))) + 1
        L.append("i\\j" + "".join(f"{j:>{w}}" for j in range(J + 1)))
        for i, row in enumerate(G):
            L.append(f"{i:>3}" + "".join(f"{c:>{w}}" for c in row))
        L.append("```")
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
    L = ["# Hironaka-form tables", ""]
    L += md_species_n2(out["n2_species"])
    L += md_equal_n2(out["n2_equal"])
    L += md_equal_d2(out["d2_equal"])
    L += md_species_d2(out["d2_species"])
    with open(os.path.join(ROOT, "docs", "tables.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
