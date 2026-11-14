#!/usr/bin/env python3
"""Worked examples: which primary invariants exist (see docs/hilbert_series.md, 5.7).

Example A  (N = 3, d = 2): the lowest-terms Molien-Weyl fraction suggests
           primaries that cannot exist; the true minimum has 2 secondaries.
Example B  (N = 2, d = 4): the single-trace invariants that the multigraded
           series suggests are never a system of primary invariants; a mixed
           choice is, and it attains the minimum P(1) = 8.
"""
import itertools
import os
import random
import sys

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import hilbert_series as h  # noqa: E402

x = sp.Symbol("x")


def matrices(N, d, prefix):
    return [sp.Matrix(N, N, lambda i, j: sp.Symbol(f"{prefix}{a}_{i}{j}")) for a in range(d)]


def tr_word(Ms, word):
    P = sp.eye(Ms[0].shape[0])
    for a in word:
        P = P * Ms[a]
    return sp.expand(P.trace())


def example_a():
    print("=" * 72)
    print("Example A: N = 3, d = 2")
    _, Z = h.hilbert_series(3, 2, equal_x=True)
    rs = h.ReducedSeries(Z, x)
    hh = rs.series(8)
    print("lowest-terms Molien-Weyl output:", sp.factor(Z))
    naive = {1: 2, 2: 4, 3: 4}
    hf = h.hironaka_form(rs, degrees=naive)
    print(f"as (1-x)^2 (1-x^2)^4 (1-x^3)^4:  P = {hf.numerator_str()},  P(1) = {hf.secondaries}")
    print(f"  h_2 = {hh[2]}; two degree-1 primaries already give 3 quadratics, so at most "
          f"{hh[2] - 3} degree-2 primaries fit -> 4 is impossible (P_2 = {hf.numerator[2]})")
    best = h.hironaka_candidates(rs)[0]
    print(f"fewest admissible secondaries: {best}  (P(1) = {best.secondaries})")

    X, Y = matrices(3, 2, "m")
    words = [(0,), (1,), (0, 0), (0, 1), (1, 1), (0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1),
             (0, 0, 1, 1)]
    theta = [tr_word([X, Y], w) for w in words]
    vars_ = sorted(set().union(*[t.free_symbols for t in theta]), key=str)
    random.seed(1)
    pt = {v: sp.Rational(random.randint(-9, 9), random.randint(1, 9)) for v in vars_}
    J = sp.Matrix([[sp.diff(t, v).subs(pt) for v in vars_] for t in theta])
    print(f"Jacobian rank of the 10 traces Tr X, Tr Y, Tr X^2, Tr XY, Tr Y^2, Tr X^3, Tr X^2Y, "
          f"Tr XY^2, Tr Y^3, Tr X^2Y^2 at a random point: {J.rank()} (= D = 10, algebraically "
          f"independent; that they form an hsop is Teranishi's theorem)")


def example_b():
    print("=" * 72)
    print("Example B: N = 2, d = 4  (matrices W, X, Y, Z)")
    Zg, Zx = h.hilbert_series(2, 4)
    den = sp.fraction(sp.factor(Zg))[1]
    nbin = 2 * 4 + 6
    print("multigraded denominator:", den)
    print(f"  = prod_a (1-x_a)(1-x_a^2) prod_(a<b) (1-x_a x_b): {nbin} binomials, "
          f"but D = (d-1)N^2+1 = 13")
    rs = h.ReducedSeries(Zx, x)
    print("singly graded Hironaka form (fewest admissible secondaries):", h.hironaka_form(rs))

    names = "WXYZ"
    pairs = [(a, b) for a in range(4) for b in range(a, 4)]
    E = sp.Matrix([[0, 1], [0, 0]])
    F = sp.Matrix([[0, 0], [1, 0]])
    H = sp.Matrix([[1, 0], [0, -1]])
    O = sp.zeros(2)
    print("\nEvery choice of 4 traces + 9 of the 10 single traces Tr(AB) fails:")
    for drop in pairs:
        a, b = drop
        Ms = [O] * 4
        if a == b:
            Ms[a] = H
        else:
            Ms[a], Ms[b] = E, F
        vals = {p: (Ms[p[0]] * Ms[p[1]]).trace() for p in pairs}
        kept_zero = all(vals[p] == 0 for p in pairs if p != drop) and all(M.trace() == 0 for M in Ms)
        print(f"  drop Tr({names[a]}{names[b]}): all 13 kept invariants vanish: {kept_zero}; "
              f"Tr({names[a]}{names[b]}) = {vals[drop]} != 0  -> point outside the nullcone")

    print("\nMixed choice m11 = Tr(WZ) + Tr(XY) with the other 8 Tr(AB):")
    M = sp.zeros(4)
    M[0, 3] = M[3, 0] = 1
    M[1, 2] = M[2, 1] = -1
    print(f"  common zeros have Gram matrix c*M, M = {M.tolist()}, det M = {M.det()} -> rank 4;")
    print("  Gram matrices of 4 vectors in C^3 have rank <= 3, so c = 0 and every invariant")
    print("  vanishes: an hsop with degrees 1^4 2^9, P(1) = e * 2^9 = 8 = the minimum.")
    random.seed(2)
    for _ in range(3):
        R = sp.Matrix(4, 4, lambda i, j: 0)
        for i, j in itertools.combinations_with_replacement(range(4), 2):
            R[i, j] = R[j, i] = random.randint(-5, 5)
        print(f"  random combination: kernel spanned by a symmetric matrix with det {R.det()} "
              f"({'hsop' if R.det() else 'not hsop'})")


if __name__ == "__main__":
    example_a()
    example_b()
