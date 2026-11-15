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
    row["numerator"] = [[list(m), c] for m, c in
                        sorted(f.numerator.items(), key=lambda t: (sum(t[0]), [-u for u in t[0]]))]
    row["orbits"] = [[list(m), c, n] for m, (c, n) in
                     sorted(f.orbits().items(), key=lambda t: (sum(t[0]), t[0]))]
    return row


# ------------------------------------------------- forms quoted in arXiv:2503.20097

def _sym_factors(d):
    e = lambda *idx: tuple(sum(1 for i in idx if i == a) for a in range(d))
    return ([[list(e(a)), 1] for a in range(d)] + [[list(e(a, a)), 1] for a in range(d)]
            + [[list(e(a, b)), 1] for a in range(d) for b in range(a + 1, d)])


def _paper_n2_d4():
    num = {(0, 0, 0, 0): 1, (2, 2, 2, 2): -1}
    for a in range(4):
        num[tuple(0 if i == a else 1 for i in range(4))] = 1
        num[tuple(2 if i == a else 1 for i in range(4))] = -1
    return [[list(m), c] for m, c in num.items()]


PAPER_N2_SPECIES = {   # d: (equation, factors, numerator)
    1: ("(3.5) with N = 2", [[[1], 1], [[2], 1]], [[[0], 1]]),
    2: ("(3.14)", _sym_factors(2), [[[0, 0], 1]]),
    3: ("(3.24)", _sym_factors(3), [[[0, 0, 0], 1], [[1, 1, 1], 1]]),
    4: ("(3.35)-(3.36)", _sym_factors(4), _paper_n2_d4()),
}
PAPER_N2_EQUAL = {     # d: (equation, numerator, degrees)
    1: ("(3.5) with N = 2", [1], {"1": 1, "2": 1}),
    4: ("(3.39)", [1, 0, 1, 4, 1, 0, 1], {"1": 4, "2": 9}),
}
PAPER_D2_EQUAL_EQ = {2: "(3.14) with x = y", 3: "(3.40) with x = y", 4: "(3.46)-(3.47)",
                     5: "(3.48)-(3.49)", 6: "(3.51)-(3.52)"}
PAPER_D2_SPECIES = {   # N: (equation, factors, numerator)
    2: ("(3.14)", _sym_factors(2), [[[0, 0], 1]]),
    3: ("(3.40)", [[[1, 0], 1], [[0, 1], 1], [[2, 0], 1], [[1, 1], 1], [[0, 2], 1],
                   [[3, 0], 1], [[2, 1], 1], [[1, 2], 1], [[0, 3], 1], [[2, 2], 1]],
        [[[0, 0], 1], [[3, 3], 1]]),
}


def same_species_form(f1, n1, f2, n2):
    key = lambda fs: sorted((tuple(a), m) for a, m in fs)
    return key(f1) == key(f2) and {tuple(m): c for m, c in n1} == {tuple(m): c for m, c in n2}


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
            f"  denominator: {equal_den({int(k): v for k, v in degrees.items()})}",
            f"  max numerator degree: {max(k for k, c in enumerate(numerator) if c)}", ""]


def max_degrees(numerator, names):
    total = max(sum(m) for m, c in numerator)
    each = ", ".join(f"{n} {max(m[i] for m, c in numerator)}" for i, n in enumerate(names))
    return f"max numerator degree: total {total}; in each matrix: {each}"


VARS = ["x", "y", "z", "w", "u", "v", "t"]


def poly_terms(numerator, names):
    out = []
    for m, c in numerator:
        mon = mono(m, names)
        if mon == "1":
            out.append(str(c))
        else:
            out.append(("+ " if c > 0 else "- ") + ("" if abs(c) == 1 else f"{abs(c)} ") + mon)
    return out


def species_lines(factors, numerator, names, inline, fname=None):
    L = ["  denominator: " + " ".join(
        f"(1-{mono(a, names)})" + (f"^{m}" if m > 1 else "") for a, m in factors)]
    L.append("  " + max_degrees(numerator, names))
    numerator = sorted(numerator, key=lambda t: (sum(t[0]), [-u for u in t[0]]))
    terms = poly_terms(numerator, names)
    if inline:
        L.append("  numerator:   " + " ".join(terms))
    else:
        with open(os.path.join(DATA, fname), "w") as f:
            f.write("\n".join(terms) + "\n")
        L.append(f"  numerator:   {len(terms)} terms, one per line in data/{fname}")
    return L


def paper_species_lines(paper, ours_f, ours_n, names):
    if paper is None:
        return ["paper: not given in arXiv:2503.20097"]
    eq, pf, pn = paper
    same = same_species_form(pf, pn, ours_f, ours_n)
    return ([f"paper, eq. {eq}" + (" (identical to ours):" if same else " (DIFFERENT):")]
            + species_lines(pf, pn, names, True))


def md_species_n2(rows, inline_max=5):
    L = ["## 1. N = 2, d = 1..7, matrix grading", "",
         "One variable per matrix: x, y, z, w, u, v, t.", ""]
    for r in rows:
        d = r["d"]
        names = VARS[:d]
        L += [f"### d = {d}", "", "```", "ours:"]
        L += species_lines(r["factors"], r["numerator"], names, d <= inline_max,
                           f"n2_d{d}_numerator.txt")
        L += [""] + paper_species_lines(PAPER_N2_SPECIES.get(d), r["factors"], r["numerator"], names)
        L += ["```", ""]
    return L


def md_equal_n2(rows):
    L = ["## 2. N = 2, d = 1..18, all species equal", "",
         "Numerator coefficients from degree 0 upwards.", "", "```"]
    for r in rows:
        L += equal_block(f"d = {r['d']}, ours (P(1) = {r['secondaries']})",
                         r["numerator"], r["degrees"])
        if r["d"] in PAPER_N2_EQUAL:
            eq, pn, pd = PAPER_N2_EQUAL[r["d"]]
            same = pn == r["numerator"] and pd == r["degrees"]
            L += equal_block(f"d = {r['d']}, paper, eq. {eq}"
                             + (" (identical to ours)" if same else " (DIFFERENT)"), pn, pd)
        else:
            L += [f"d = {r['d']}, paper: not given in arXiv:2503.20097", ""]
    L += ["```", ""]
    return L


def md_equal_d2(rows):
    L = ["## 3. d = 2, N = 2..6, all species equal", "",
         "Numerator coefficients from degree 0 upwards.  `ours` = the admissible choice "
         "with the fewest secondaries.  Both forms are the same Z(x).", "", "```"]
    for r in rows:
        L += equal_block(f"N = {r['N']}, ours (P(1) = {r['min']['secondaries']})",
                         r["min"]["numerator"], r["min"]["degrees"])
        same = r["paper"]["degrees"] == r["min"]["degrees"]
        L += equal_block(f"N = {r['N']}, paper, eq. {PAPER_D2_EQUAL_EQ[r['N']]} "
                         f"(P(1) = {r['paper']['secondaries']})"
                         + (" (identical to ours)" if same else ""),
                         r["paper"]["numerator"], r["paper"]["degrees"])
    L += ["```", ""]
    return L


def grid_lines(numerator):
    I = max(m[0] for m, _ in numerator)
    J = max(m[1] for m, _ in numerator)
    G = [[0] * (J + 1) for _ in range(I + 1)]
    for (i, j), c in numerator:
        G[i][j] = c
    w = max(max(len(str(c)) for row in G for c in row), len(str(J))) + 1
    L = ["  numerator (row i = power of x, column j = power of y):",
         "  i\\j" + "".join(f"{j:>{w}}" for j in range(J + 1))]
    for i, row in enumerate(G):
        L.append(f"  {i:>3}" + "".join(f"{c:>{w}}" for c in row))
    return L


def bigraded_lines(factors, numerator):
    num = [(tuple(m), c) for m, c in numerator]
    return (["  denominator: " + " ".join(
        f"(1-{mono(a, ['x', 'y'])})" + (f"^{m}" if m > 1 else "") for a, m in factors)]
        + ["  " + max_degrees(num, ["x", "y"])] + grid_lines(num))


def md_species_d2(rows):
    L = ["## 4. d = 2, N = 2..5, matrix grading", ""]
    for r in rows:
        L += [f"### N = {r['N']}", "", "```", "ours:"]
        L += bigraded_lines(r["factors"], r["numerator"])
        L.append("")
        paper = PAPER_D2_SPECIES.get(r["N"])
        if paper is None:
            L.append("paper: not given in arXiv:2503.20097")
        else:
            eq, pf, pn = paper
            same = same_species_form(pf, pn, r["factors"], r["numerator"])
            L.append(f"paper, eq. {eq}" + (" (identical to ours):" if same else " (DIFFERENT):"))
            L += bigraded_lines(pf, pn)
        L += ["```", ""]
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
