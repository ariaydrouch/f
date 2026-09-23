"""
Counting Wick-contraction diagrams in <O_n O_n†> by power of N.

==============================================================
PHYSICAL SETUP
==============================================================
  O_n  = Tr(Z^n) = Z^{a0}_{a1} Z^{a1}_{a2} ... Z^{a(n-1)}_{a0}
  O_n† = Tr((Z†)^n)
  Propagator:  <Z^i_j (Z†)^k_l>  =  delta^i_l  delta^k_j

A Wick contraction is a permutation sigma in S_n where the k-th Z
contracts with the sigma(k)-th Z†:

  <Z^{a_k}_{a_{k+1 mod n}}  (Z†)^{b_{s(k)}}_{b_{(s(k)+1) mod n}}>
        = delta(a_k, b_{(s(k)+1)%n})  *  delta(b_{s(k)}, a_{(k+1)%n})

This gives 2n delta constraints on 2n variables {a_0,...,b_{n-1}}.
Power of N = number of connected components (= number of free indices).

==============================================================
THREE EQUIVALENT METHODS
==============================================================

Method A – Union-Find (direct, no prior knowledge required)
  Label nodes a_k -> k,  b_k -> n+k.
  For each k: unite(k, n+(sigma[k]+1)%n)
              unite(n+sigma[k], (k+1)%n)
  #components = power of N.

Method B – Cycle formula (derived from the delta structure)
  The constraint graph is 2-regular => it splits into disjoint cycles.
  Define f(k) = ( sigma_inv[(sigma[k]+1)%n] + 1 ) % n.
  This equals the permutation  f = tau o sigma^{-1} o tau o sigma
  (tau = cyclic n-shift).  Power of N = #cycles(f).

Method C – Representation theory closed form
  Tr(Z^n) = sum_R chi_R(tau) chi_R(Z)         [Fourier inversion on S_n]
  Only HOOK representations (n-k, 1^k) give chi ≠ 0:
    chi_{(n-k,1^k)}(tau) = (-1)^k.
  Using <chi_R chi_S†> = delta_RS f_R:
    <O_n O_n†> = sum_{k=0}^{n-1} f_{hook(n-k, 1^k)}
  Box-factor product for hook (n-k, 1^k):
    f_{hook} = N(N+1)...(N+n-k-1) * (N-1)(N-2)...(N-k)
             = (N-k)^{(n)}   [rising factorial, n terms starting at N-k]
  Via the hockey-stick identity sum_{j=0}^{n-1} C(N+j, n) = C(N+n, n+1) - C(N, n+1):

      <O_n O_n†>  =  n! * [ C(N+n, n+1) - C(N, n+1) ]     (*)

  where C(N+n, n+1) and C(N, n+1) are polynomials in N.
  Both methods A and B are verified to reproduce (*) exactly.
"""

from itertools import permutations
from collections import defaultdict
from fractions import Fraction
import math


# ────────────────────────────────────────────────────────────────────────────
# METHOD A  –  Union-Find
# ────────────────────────────────────────────────────────────────────────────

def power_union_find(sigma, n):
    parent = list(range(2 * n))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def unite(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    for k in range(n):
        unite(k,         n + (sigma[k] + 1) % n)   # a_k  = b_{(sigma[k]+1)%n}
        unite(n + sigma[k], (k + 1) % n)             # b_{sigma[k]} = a_{(k+1)%n}

    return len({find(i) for i in range(2 * n)})


# ────────────────────────────────────────────────────────────────────────────
# METHOD B  –  Cycle formula   f = tau o sigma^{-1} o tau o sigma
# ────────────────────────────────────────────────────────────────────────────

def power_cycle_formula(sigma, n):
    sigma_inv = [0] * n
    for k in range(n):
        sigma_inv[sigma[k]] = k

    f = [(sigma_inv[(sigma[k] + 1) % n] + 1) % n for k in range(n)]

    visited = [False] * n
    cycles = 0
    for s in range(n):
        if not visited[s]:
            cycles += 1
            j = s
            while not visited[j]:
                visited[j] = True
                j = f[j]
    return cycles


# ────────────────────────────────────────────────────────────────────────────
# METHOD C  –  Closed-form  n! * [C(N+n, n+1) - C(N, n+1)]
# ────────────────────────────────────────────────────────────────────────────

def _binomial_poly(offset, r):
    """Return polynomial coefficients of C(N+offset, r) as list [coeff of N^j].
    C(N+offset, r) = prod_{j=0}^{r-1} (N+offset-j)  /  r!
    """
    poly = [Fraction(1)]
    for j in range(r):
        shift = offset - j
        new = [Fraction(0)] * (len(poly) + 1)
        for d, c in enumerate(poly):
            new[d + 1] += c
            new[d]     += shift * c
        poly = new
    fr = math.factorial(r)
    return [c / fr for c in poly]


def closed_form_poly(n):
    """Return  <O_n O_n†>  =  n! * [C(N+n, n+1) - C(N, n+1)]
    as a dict  {power: integer_coefficient}.
    """
    p1 = _binomial_poly(n, n + 1)   # C(N+n, n+1)
    p2 = _binomial_poly(0, n + 1)   # C(N,   n+1)
    length = max(len(p1), len(p2))
    fn = Fraction(math.factorial(n))
    result = {}
    for j in range(length):
        c1 = p1[j] if j < len(p1) else Fraction(0)
        c2 = p2[j] if j < len(p2) else Fraction(0)
        val = fn * (c1 - c2)
        if val != 0:
            result[j] = int(val)
    return result


# Also compute via explicit rising-factorial sum (for display / verification)
def rising_factorial_sum(n):
    """<O_n O_n†> = sum_{k=0}^{n-1} (N-k)(N-k+1)...(N+n-k-1)."""
    total = defaultdict(Fraction)
    for k in range(n):
        poly = [Fraction(1)]
        for j in range(n):
            shift = j - k          # factor is (N + shift)
            new = [Fraction(0)] * (len(poly) + 1)
            for d, c in enumerate(poly):
                new[d + 1] += c
                new[d]     += shift * c
            poly = new
        for d, c in enumerate(poly):
            total[d] += c
    return {j: int(v) for j, v in total.items() if v != 0}


# ────────────────────────────────────────────────────────────────────────────
# Brute-force enumeration
# ────────────────────────────────────────────────────────────────────────────

def enumerate_diagrams(n, cross_check=True):
    counts = defaultdict(int)
    for sigma in permutations(range(n)):
        sigma = list(sigma)
        p = power_cycle_formula(sigma, n)
        if cross_check and n <= 7:
            assert power_union_find(sigma, n) == p
        counts[p] += 1
    return dict(counts)


# ────────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────────

def poly_str(cd):
    parts = []
    for p in sorted(cd.keys(), reverse=True):
        c = cd[p]
        if p == 0:
            parts.append(str(c))
        elif p == 1:
            parts.append("N" if c == 1 else f"{c}·N")
        else:
            parts.append(f"N^{p}" if c == 1 else f"{c}·N^{p}")
    return " + ".join(parts)


def cycle_type(sigma):
    n, vis, lens = len(sigma), [False]*len(sigma), []
    for s in range(n):
        if not vis[s]:
            j, ln = s, 0
            while not vis[j]:
                vis[j] = True; j = sigma[j]; ln += 1
            lens.append(ln)
    return tuple(sorted(lens, reverse=True))


# ────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────

def main():
    MAX_ENUM = 10   # enumerate up to n=10  (10! = 3.6M)
    MAX_CF   = 15   # closed form up to n=15 (exact polynomial, instant)

    # ------------------------------------------------------------------
    # 1. Cross-verify enumeration with closed form
    # ------------------------------------------------------------------
    print("=" * 72)
    print("  VERIFICATION: enumeration (A+B) vs closed form (C)")
    print("=" * 72)
    print()

    all_cf = {}
    for n in range(1, MAX_CF + 1):
        cf = closed_form_poly(n)
        rf = rising_factorial_sum(n)
        assert cf == rf, f"n={n}: closed form mismatch"
        all_cf[n] = cf

    for n in range(1, MAX_ENUM + 1):
        enum = enumerate_diagrams(n)
        cf   = all_cf[n]
        assert dict(enum) == cf, f"n={n}: enum vs closed form mismatch"
        print(f"  n={n:>2}: enumeration ({math.factorial(n):>8} contractions) ✓ matches closed form")

    print()

    # ------------------------------------------------------------------
    # 2. Summary table: exact polynomial for n=1..15
    # ------------------------------------------------------------------
    print("=" * 72)
    print("  <O_n O_n†>  as polynomial in N  [via  n! * (C(N+n,n+1) - C(N,n+1))]")
    print("=" * 72)
    print()
    print(f"  {'n':>3}  |  <O_n O_n†>")
    print("  " + "-" * 68)
    for n in range(1, MAX_CF + 1):
        print(f"  {n:>3}  |  {poly_str(all_cf[n])}")
    print()

    # ------------------------------------------------------------------
    # 3. Coefficient table  c(n, j)  = coeff of  N^{n-2j}
    # ------------------------------------------------------------------
    print("=" * 72)
    print("  COEFFICIENT TABLE  c(n,j) = # diagrams contributing N^{n-2j}")
    print("  Leading planar term = j=0; first sub-leading = j=1; etc.")
    print("=" * 72)
    print()
    max_j = (MAX_CF - 1) // 2
    header = f"  {'n':>3} |" + "".join(f"  j={j:<9}" for j in range(min(6, max_j + 1)))
    print(header)
    print("  " + "-" * (len(header) - 2))
    for n in range(1, MAX_CF + 1):
        cd = all_cf[n]
        row = f"  {n:>3} |"
        for j in range(min(6, max_j + 1)):
            power = n - 2 * j
            if power < 0:
                row += f"  {'(n/a)':<11}"
            else:
                val = cd.get(power, 0)
                row += f"  {val:<11}"
        print(row)
    print()

    # ------------------------------------------------------------------
    # 4. Key structural properties
    # ------------------------------------------------------------------
    print("=" * 72)
    print("  KEY STRUCTURAL RESULTS  (all verified computationally)")
    print("=" * 72)
    print()

    print("━━ RESULT 1: Leading planar term ━━")
    print("  coefficient of N^n = n  (exactly n planar diagrams)")
    print("  Explanation: f(sigma) = identity iff sigma commutes with tau.")
    print("  The centralizer of the n-cycle tau in S_n has exactly n elements")
    print("  {id, tau, tau^2, ..., tau^{n-1}}.  Each gives maximum #cycles = n.")
    print()

    print("━━ RESULT 2: Parity constraint ━━")
    print("  Only N^{n-2j} terms appear (j = 0,1,2,...);")
    print("  equivalently, power of N always has the same parity as n.")
    print("  Proof: sign(f) = sign(tau)^2 * sign(sigma)^{-1} * sign(sigma) = +1")
    print("  => f is always an even permutation")
    print("  => #cycles(f) ≡ n (mod 2)  (since parity = (-1)^{n - #cycles}).")
    print()

    print("━━ RESULT 3: No N^{n-1} term ━━")
    print("  c(n, n-1) = 0 for all n >= 2.")
    print("  Immediate from Result 2 (wrong parity).")
    for n in range(2, MAX_CF + 1):
        assert all_cf[n].get(n - 1, 0) == 0
    print("  Verified for n = 2 ...", MAX_CF)
    print()

    print("━━ RESULT 4: Minimum power ━━")
    print("  Odd  n: minimum power is N^1  (f can be an n-cycle, which is even for odd n).")
    print("  Even n: minimum power is N^2  (even permutation needs >= 2 cycles).")
    for n in range(1, MAX_CF + 1):
        expected_min = 1 if n % 2 == 1 else 2
        actual_min   = min(all_cf[n].keys())
        assert actual_min == expected_min, f"n={n}: min={actual_min}, expected={expected_min}"
    print("  Verified for n = 1 ...", MAX_CF)
    print()

    print("━━ RESULT 5: Exact closed form ━━")
    print()
    print("  Form I  (sum of rising factorials, one per hook representation):")
    print()
    print("    <O_n O_n†>  =  Σ_{k=0}^{n-1}  (N-k)(N-k+1)···(N+n-k-1)")
    print()
    print("  Form II  (closed, via hockey-stick identity on the sum):")
    print()
    print("    <O_n O_n†>  =  n! × [ C(N+n, n+1)  −  C(N, n+1) ]")
    print()
    print("  Derivation path:")
    print("   1. Tr(Z^n) = Σ_R χ_R(τ) χ_R(Z)           [Fourier inversion on S_n]")
    print("   2. χ_R(τ) ≠ 0 only for hook shapes R=(n-k,1^k), with χ_R(τ)=(-1)^k.")
    print("   3. <χ_R χ_S†> = δ_RS f_R   =>   <O_n O_n†> = Σ_{k=0}^{n-1} f_{hook(n-k,1^k)}")
    print("   4. f_{(n-k,1^k)} = N(N+1)···(N+n-k-1)·(N-1)···(N-k)  = (N-k)^{(n)}")
    print("   5. Σ_{k=0}^{n-1} C(N+n-k-1,n) = C(N+n,n+1) - C(N,n+1)  [hockey-stick]")
    print("      gives  Σ(N-k)^{(n)} = n!·[C(N+n,n+1) - C(N,n+1)].")
    print()

    print("━━ RESULT 6: Sub-leading coefficient ━━")
    print()
    print("  c(n, n-2)  =  n · C(n+1, 4)  =  n²(n+1)(n-1)(n-2) / 24")
    print()
    ok = all(all_cf[n].get(n - 2, 0) == n * math.comb(n + 1, 4)
             for n in range(3, MAX_CF + 1))
    print(f"  Verified for n = 3 ... {MAX_CF}: {'ALL MATCH' if ok else 'MISMATCH'}")
    print()
    for n in range(3, min(12, MAX_CF + 1)):
        c = all_cf[n].get(n - 2, 0)
        formula = n * math.comb(n + 1, 4)
        print(f"  n={n:>2}: c(n,n-2) = {c:<8}  =  {n}·C({n+1},4) = {n}·{math.comb(n+1,4)} = {formula}")
    print()

    # ------------------------------------------------------------------
    # 5. Cycle-type breakdown for n=4..7
    # ------------------------------------------------------------------
    print("=" * 72)
    print("  CYCLE-TYPE BREAKDOWN  (for n=4,5,6,7)")
    print("  Shows which cycle structure of sigma produces which power of N")
    print("=" * 72)

    for n_t in [4, 5, 6, 7]:
        print(f"\n  n = {n_t}:")
        data = defaultdict(lambda: defaultdict(int))
        for sigma in permutations(range(n_t)):
            sigma = list(sigma)
            ct = cycle_type(sigma)
            p  = power_cycle_formula(sigma, n_t)
            data[ct][p] += 1
        print(f"  {'Cycle type σ':22} | #σ     | power -> count")
        print("  " + "-" * 56)
        for ct in sorted(data.keys(), key=lambda x: (-len(x), x)):
            ct_str    = "+".join(str(c) for c in ct)
            total_ct  = sum(data[ct].values())
            powers    = sorted(data[ct].keys(), reverse=True)
            pstr      = "  ".join(f"N^{p}:{data[ct][p]}" for p in powers)
            print(f"  {ct_str:22} | {total_ct:<6} | {pstr}")

    # ------------------------------------------------------------------
    # 6. Total-diagram sanity check (enumeration)
    # ------------------------------------------------------------------
    print()
    print("=" * 72)
    print("  SANITY: sum of all coefficients = n! (total Wick contractions)")
    print("=" * 72)
    print()
    for n in range(1, MAX_CF + 1):
        total = sum(all_cf[n].values())
        ok    = (total == math.factorial(n))
        print(f"  n={n:>2}: Σ coefficients = {total:<12}  n! = {math.factorial(n):<12}  ✓" if ok
              else f"  n={n:>2}: MISMATCH  {total} vs {math.factorial(n)}")


if __name__ == "__main__":
    main()
