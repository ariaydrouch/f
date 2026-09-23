"""
Complete from-scratch derivation and analysis for <O_n O_n†>.

Contents
--------
Part 1 : What the indices look like — tau explained
Part 2 : Wick contraction mechanics — explicit for n=2,3
Part 3 : Why power of N = connected components (union-find)
Part 4 : The cycle formula f = tau sigma^{-1} tau sigma
Part 5 : Derivation of Form I  (sum of rising factorials)
Part 6 : Derivation of Form II (n! [C(N+n,n+1) - C(N,n+1)])
Part 7 : Does non-planar dominate at large N?  Normalization analysis.
"""

from itertools import permutations
from collections import defaultdict
from fractions import Fraction
import math


# ──────────────────────────────────────────────────────────────────────────────
# PART 1 : INDEX STRUCTURE OF O_n = Tr(Z^n)
# ──────────────────────────────────────────────────────────────────────────────

def part1():
    print("=" * 70)
    print("PART 1 : Index structure of  O_n = Tr(Z^n)")
    print("=" * 70)
    print("""
  O_n = Tr(Z^n) = Z^{a0}_{a1} Z^{a1}_{a2} ... Z^{a(n-1)}_{a0}

  Label the n copies of Z as Z_0, Z_1, ..., Z_{n-1}.
  Write out every index explicitly:

     Z_k  has  upper index  a_k
                lower index  a_{(k+1) mod n}

  So Z_0 has upper a_0, lower a_1.
     Z_1 has upper a_1, lower a_2.
     ...
     Z_{n-1} has upper a_{n-1}, lower a_0.

  The lower index of Z_k equals the upper index of Z_{k+1 mod n}.
  That is the meaning of "trace" — the indices cycle around.

  The function  tau(k) = (k+1) mod n  is just this cyclic shift.
  It has nothing deep about it: it is just the bookkeeping of which
  index slot connects to which in the trace.

  Examples:
""")
    for n in [2, 3, 4]:
        print(f"    n={n}:", end="")
        factors = []
        for k in range(n):
            factors.append(f"Z^{{a{k}}}_{{a{(k+1)%n}}}")
        print("  " + " ".join(factors))
    print()


# ──────────────────────────────────────────────────────────────────────────────
# PART 2 : WICK CONTRACTIONS EXPLICITLY FOR n=2 AND n=3
# ──────────────────────────────────────────────────────────────────────────────

def part2():
    print("=" * 70)
    print("PART 2 : Wick contractions written out explicitly")
    print("=" * 70)
    print("""
  Propagator:  <Z^i_j  (Z†)^k_l>  =  delta^i_l  delta^k_j

  So contracting Z^i_j with (Z†)^k_l gives  delta^i_l * delta^k_j:
    - the upper index of Z (=i) must equal the lower index of Z† (=l)
    - the upper index of Z† (=k) must equal the lower index of Z (=j)

  A Wick contraction for <O_n O_n†> is a choice of which Z contracts
  with which Z†.  With n Z's and n Z†'s there are n! choices.
  Label each choice by a permutation sigma in S_n:
    Z_k  contracts with  (Z†)_{sigma(k)}.
""")

    def show_contractions(n):
        print(f"  ─── n={n}  ({math.factorial(n)} permutations) ───")
        a = [f"a{k}" for k in range(n)]
        b = [f"b{k}" for k in range(n)]

        for sigma in permutations(range(n)):
            sigma = list(sigma)

            # Build the equality constraints
            constraints = []
            for k in range(n):
                # Z_k: upper=a_k, lower=a_{k+1 mod n}
                # (Z†)_{sigma[k]}: upper=b_{sigma[k]}, lower=b_{(sigma[k]+1) mod n}
                # Contraction: delta(a_k, b_{(sigma[k]+1)%n}) * delta(b_{sigma[k]}, a_{(k+1)%n})
                c1 = f"{a[k]}={b[(sigma[k]+1)%n]}"
                c2 = f"{b[sigma[k]]}={a[(k+1)%n]}"
                constraints.append(f"[{c1}, {c2}]")

            # Count free variables via union-find
            parent = list(range(2 * n))
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]; x = parent[x]
                return x
            def unite(x, y):
                px, py = find(x), find(y)
                if px != py: parent[px] = py

            for k in range(n):
                unite(k,          n + (sigma[k]+1)%n)
                unite(n+sigma[k], (k+1)%n)

            power = len({find(i) for i in range(2*n)})

            sigma_str = str(sigma).replace(" ", "")
            print(f"    sigma={sigma_str}:  {', '.join(constraints)}")
            print(f"              -> N^{power}  ({power} free variables)")
        print()

    show_contractions(2)
    show_contractions(3)


# ──────────────────────────────────────────────────────────────────────────────
# PART 3 : WHY POWER OF N = CONNECTED COMPONENTS
# ──────────────────────────────────────────────────────────────────────────────

def part3():
    print("=" * 70)
    print("PART 3 : Why power of N = number of free (independent) indices")
    print("=" * 70)
    print("""
  After performing the Wick contraction for a given sigma, we get a
  product of 2n Kronecker deltas.  For example for n=3, sigma=[1,2,0]:

    delta(a0, b2) delta(b1, a1) delta(a1, b0) delta(b2, a2) delta(a2, b1) delta(b0, a0)

  We must sum over ALL index variables: a0,a1,a2,b0,b1,b2.
  But the deltas force some indices to be equal:
    a0=b2, b1=a1, a1=b0, b2=a2, a2=b1, b0=a0

  This means: a0=b2=a2=b1=a1=b0=a0.  All six indices are equal!
  So the sum  Σ_{a0,a1,a2,b0,b1,b2} [product of deltas]  collapses to
  Σ_{a0} 1  =  N^1.

  For sigma=[1,0,2] (see Part 2):
    a0=b2, b1=a1, a1=b1, b0=a2, a2=b0, b2=a0
    => a0=b2 (one group), a1=b1 (second group), a2=b0 (third group).
  Three independent free variables: a0, a1, a2.
  Sum = Σ_{a0} Σ_{a1} Σ_{a2} 1  =  N^3.

  RULE: model each index as a node, each delta as an edge.
  Power of N = number of connected components of this graph.

  Union-Find is simply an efficient algorithm to count components.
  It maintains a "parent" pointer for each node and merges components
  when an equality is discovered.
""")


# ──────────────────────────────────────────────────────────────────────────────
# PART 4 : THE CYCLE FORMULA  f = tau o sigma^{-1} o tau o sigma
# ──────────────────────────────────────────────────────────────────────────────

def part4():
    print("=" * 70)
    print("PART 4 : The cycle formula for the power of N")
    print("=" * 70)
    print("""
  The 2n-node constraint graph is 2-REGULAR: every node appears in
  exactly one delta on its left AND one delta on its right.
  (Each a_k and each b_k is forced equal to exactly one other index.)

  A 2-regular graph is a disjoint union of simple cycles.
  => Power of N = number of such cycles.

  We can TRACE the cycles directly without building the graph.
  Start at node a_k:

    Step 1:  a_k = b_{(sigma(k)+1) mod n}    [from delta type 1]
             We have arrived at b-node  j = (sigma(k)+1) mod n.

    Step 2:  b_j = a_{(sigma^{-1}(j)+1) mod n}  [from delta type 2:
             b_{sigma(m)} = a_{(m+1) mod n}, read with m = sigma^{-1}(j)]
             We have arrived at a-node  f(k) = (sigma^{-1}(j)+1) mod n
                                              = (sigma^{-1}((sigma(k)+1) mod n)+1) mod n

  So each complete two-step journey around the cycle returns us from
  a_k to a_{f(k)}.  The a-nodes form orbits under the map f, and each
  orbit is one cycle in the full 2n-node graph.

  In permutation notation:  f = tau o sigma^{-1} o tau o sigma
  where  tau(k) = (k+1) mod n  (the cyclic shift / "trace permutation").

  Power of N  =  number of cycles of  f = tau sigma^{-1} tau sigma.

  Verification for n=3:
""")

    n = 3
    tau = [(k+1)%n for k in range(n)]

    def compose(p, q):
        return [p[q[k]] for k in range(len(q))]

    def inv(p):
        r = [0]*len(p)
        for k in range(len(p)): r[p[k]] = k
        return r

    def cycles(p):
        vis, cycs = [False]*len(p), []
        for s in range(len(p)):
            if not vis[s]:
                c, j = [], s
                while not vis[j]: vis[j]=True; c.append(j); j=p[j]
                cycs.append(c)
        return cycs

    for sigma in permutations(range(n)):
        sigma = list(sigma)
        si = inv(sigma)
        f = compose(tau, compose(si, compose(tau, sigma)))
        cs = cycles(f)
        power = len(cs)
        # also check via union-find
        parent = list(range(2*n))
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        def unite(x,y):
            px,py=find(x),find(y)
            if px!=py: parent[px]=py
        for k in range(n):
            unite(k, n+(sigma[k]+1)%n)
            unite(n+sigma[k], (k+1)%n)
        uf_power = len({find(i) for i in range(2*n)})
        assert power == uf_power

        f_str = str(f)
        cycles_str = str(cs)
        print(f"    sigma={sigma}: f={f_str}  cycles={cycles_str}  -> N^{power}")
    print()
    print("  These match the direct union-find results from Part 2 exactly.")
    print()

    print("  WHY n PLANAR DIAGRAMS?")
    print("  Power is maximized (= n) iff f = identity, i.e. sigma commutes with tau.")
    print("  The set of sigma commuting with the n-cycle tau is:")
    print("  {id, tau, tau^2, ..., tau^{n-1}} — exactly n elements.")
    print("  These are the PLANAR diagrams.")
    print()
    for n in [3, 4, 5]:
        tau_n = list(range(1, n)) + [0]
        def comm(s):
            s = list(s)
            si = inv(s)
            f = compose(tau_n, compose(si, compose(tau_n, s)))
            return f == list(range(n))
        planar_sigmas = [list(s) for s in permutations(range(n)) if comm(s)]
        print(f"    n={n}: planar sigma list = {planar_sigmas}  (count={len(planar_sigmas)})")
    print()


# ──────────────────────────────────────────────────────────────────────────────
# PART 5 : DERIVATION OF FORM I — SUM OF RISING FACTORIALS
# ──────────────────────────────────────────────────────────────────────────────

def part5():
    print("=" * 70)
    print("PART 5 : Derivation of Form I  (representation theory route)")
    print("=" * 70)
    print("""
  We use the fact that the Schur polynomials diagonalise the two-point
  function and that Tr(Z^n) can be expanded in them.

  ── Step 5.1: Schur polynomials and their two-point function ──

  For every Young diagram R with n boxes, define the Schur polynomial:
    chi_R(Z) = Tr(P_R Z^{tensor n})
  where P_R is the Young projector.

  The Schur polynomial two-point function is diagonal:
    <chi_R(Z) chi_S(Z†)>  =  delta_{RS}  f_R

  where f_R = product of the "box factors" of R.
  The box in row i, column j has factor  (N - i + j).
  So f_R = product over all boxes of (N - row + column).

  ── Step 5.2: Expand Tr(Z^n) in the Schur basis ──

  Fourier inversion on S_n gives:
    Tr(sigma Z^{tensor n})  =  sum_R  chi_R(sigma)  chi_R(Z)

  where chi_R(sigma) is the character of permutation sigma in irrep R.
  For sigma = tau (the n-cycle), we need chi_R(tau) for all R.

  ── Step 5.3: Which representations contribute? ──

  By the Murnaghan-Nakayama rule, chi_R(n-cycle) = 0 unless R is a
  HOOK Young diagram, i.e. R = (n-k, 1^k)  for k = 0, 1, ..., n-1.

  A hook (n-k, 1^k) looks like:
    [ ][ ][ ] ... [ ]       <- row 1 has n-k boxes
    [ ]
    [ ]
    ...                     <- k boxes in column 1 below row 1
    [ ]

  For hooks: chi_{(n-k,1^k)}(tau) = (-1)^k.

  (Proof sketch: the n-cycle removes all n boxes as one n-ribbon.
   From a hook, this ribbon has height k+1, giving sign (-1)^k.)

  So:
    Tr(Z^n) = sum_{k=0}^{n-1}  (-1)^k  chi_{(n-k,1^k)}(Z)

  ── Step 5.4: Compute the two-point function ──

  <O_n O_n†>  =  <Tr(Z^n) Tr((Z†)^n)>
              =  sum_{k=0}^{n-1}  ((-1)^k)^2  f_{(n-k,1^k)}
              =  sum_{k=0}^{n-1}  f_{(n-k,1^k)}

  ── Step 5.5: Compute f_{(n-k,1^k)} ──

  The hook (n-k, 1^k) has boxes:
    Row 1: (1,1),(1,2),...,(1,n-k)   with factors  N, N+1, ..., N+n-k-1
    Row 2: (2,1)                      with factor   N-1
    Row 3: (3,1)                      with factor   N-2
    ...
    Row k+1: (k+1,1)                  with factor   N-k

  f_{(n-k,1^k)}  =  N(N+1)...(N+n-k-1)  *  (N-1)(N-2)...(N-k)
                 =  (N-k)^{(n)}   [rising factorial, n terms starting at N-k]

  ── Step 5.6: FORM I ──

  <O_n O_n†>  =  sum_{k=0}^{n-1}  (N-k)(N-k+1)...(N+n-k-1)
""")

    # Numerical verification
    def rising_factorial(start, n):
        """(start)(start+1)...(start+n-1) as polynomial in N.
        Here start = N + offset, so we compute prod_{j=0}^{n-1}(N + (j-k))."""
        raise NotImplementedError  # will use symbolic below

    from fractions import Fraction

    def hook_factor_poly(k, n):
        """f_{(n-k,1^k)} as polynomial in N (list of coefficients [c0,c1,...])."""
        poly = [Fraction(1)]
        for j in range(n):
            shift = Fraction(j - k)
            new = [Fraction(0)] * (len(poly) + 1)
            for d, c in enumerate(poly):
                new[d+1] += c
                new[d]   += shift * c
            poly = new
        return poly

    print("  Numerical verification — hook factors f_{(n-k,1^k)}:")
    for n in [2, 3, 4]:
        total = [Fraction(0)] * (n + 1)
        print(f"\n  n={n}:")
        for k in range(n):
            p = hook_factor_poly(k, n)
            terms = []
            for d in range(len(p)-1, -1, -1):
                if p[d] != 0:
                    if d == 0:   terms.append(str(int(p[d])))
                    elif d == 1: terms.append(f"{int(p[d])}N")
                    else:        terms.append(f"{int(p[d])}N^{d}")
            pstr = " + ".join(terms)
            print(f"    k={k}:  f_{{({n-k},1^{k})}} = {pstr}")
            for d, c in enumerate(p):
                total[d] += c

        terms = []
        for d in range(len(total)-1, -1, -1):
            if total[d] != 0:
                if d == 0:   terms.append(str(int(total[d])))
                elif d == 1: terms.append(f"{int(total[d])}N")
                else:        terms.append(f"{int(total[d])}N^{d}")
        tstr = " + ".join(terms)
        print(f"    Sum  = {tstr}")
    print()


# ──────────────────────────────────────────────────────────────────────────────
# PART 6 : DERIVATION OF FORM II — COMPACT BINOMIAL FORM
# ──────────────────────────────────────────────────────────────────────────────

def part6():
    print("=" * 70)
    print("PART 6 : Derivation of Form II  (hockey-stick identity)")
    print("=" * 70)
    print("""
  Starting from Form I:

    <O_n O_n†>  =  sum_{k=0}^{n-1}  (N-k)(N-k+1)...(N+n-k-1)

  Note that (N-k)(N-k+1)...(N+n-k-1) is a product of n consecutive
  integers starting at N-k.  This equals  n! * C(N+n-k-1, n):

    n! * C(N+n-k-1, n) = n! * (N+n-k-1)! / (n! * (N-k-1)!)
                       = (N-k-1+1)(N-k-1+2)...(N-k-1+n)
                       = (N-k)(N-k+1)...(N+n-k-1)  ✓

  So:
    <O_n O_n†>  =  n!  *  sum_{k=0}^{n-1}  C(N+n-k-1, n)

  Substituting  j = n-k-1  (as k goes 0->n-1, j goes n-1->0):
    =  n!  *  sum_{j=0}^{n-1}  C(N+j, n)

  Now use the HOCKEY-STICK IDENTITY:
    sum_{j=a}^{b} C(j, r)  =  C(b+1, r+1) - C(a, r+1)

  With  r=n,  a=N,  b=N+n-1  (renaming: sum over C(N+j, n) for j=0..n-1
  is the same as sum over C(i, n) for i=N..N+n-1):

    sum_{j=0}^{n-1} C(N+j, n)  =  sum_{i=N}^{N+n-1} C(i, n)
                                 =  C(N+n, n+1) - C(N, n+1)

  Therefore:

    ┌──────────────────────────────────────────────────────────────┐
    │  <O_n O_n†>  =  n! * [ C(N+n, n+1)  -  C(N, n+1) ]         │
    └──────────────────────────────────────────────────────────────┘

  Note:
  - C(N+n, n+1) is a degree n+1 polynomial in N.
  - C(N,   n+1) is also degree n+1 in N.
  - Their leading terms (N^{n+1}) cancel, leaving a degree n polynomial. ✓
  - C(N, n+1) = 0 for integer N < n+1.  For such N only the first term
    contributes, which is correct (fewer trace relations to worry about).

  ── Verification for n=3 ──

  C(N+3, 4) = (N+3)(N+2)(N+1)N / 24
  C(N, 4)   = N(N-1)(N-2)(N-3) / 24
  Difference = N/24 * [(N+3)(N+2)(N+1) - (N-1)(N-2)(N-3)]

  (N+3)(N+2)(N+1) = N^3 + 6N^2 + 11N + 6
  (N-1)(N-2)(N-3) = N^3 - 6N^2 + 11N - 6
  Difference       =       12N^2       + 12   = 12(N^2+1)

  n! * N/24 * 12(N^2+1) = 6 * N * 12(N^2+1) / 24 = 3N(N^2+1) = 3N^3 + 3N ✓
""")

    # Numerical verification of Form II against Form I
    def form_ii(n):
        p1 = [Fraction(0)] * (n + 2)
        p2 = [Fraction(0)] * (n + 2)
        # C(N+n, n+1) = prod_{j=0}^{n} (N+n-j) / (n+1)!
        poly1 = [Fraction(1)]
        for j in range(n+1):
            shift = Fraction(n - j)
            new = [Fraction(0)] * (len(poly1) + 1)
            for d, c in enumerate(poly1):
                new[d+1] += c; new[d] += shift * c
            poly1 = new
        f1 = math.factorial(n+1)
        poly1 = [c/f1 for c in poly1]
        # C(N, n+1) = prod_{j=0}^{n} (N-j) / (n+1)!
        poly2 = [Fraction(1)]
        for j in range(n+1):
            shift = Fraction(-j)
            new = [Fraction(0)] * (len(poly2) + 1)
            for d, c in enumerate(poly2):
                new[d+1] += c; new[d] += shift * c
            poly2 = new
        poly2 = [c/f1 for c in poly2]
        fn = Fraction(math.factorial(n))
        length = max(len(poly1), len(poly2))
        result = {}
        for j in range(length):
            c1 = poly1[j] if j < len(poly1) else Fraction(0)
            c2 = poly2[j] if j < len(poly2) else Fraction(0)
            val = fn * (c1 - c2)
            if val != 0:
                result[j] = int(val)
        return result

    def form_i(n):
        total = defaultdict(Fraction)
        for k in range(n):
            poly = [Fraction(1)]
            for j in range(n):
                shift = Fraction(j - k)
                new = [Fraction(0)] * (len(poly) + 1)
                for d, c in enumerate(poly):
                    new[d+1] += c; new[d] += shift * c
                poly = new
            for d, c in enumerate(poly):
                total[d] += c
        return {j: int(v) for j, v in total.items() if v != 0}

    print("  Verification: Form I = Form II for n=1..10:")
    for n in range(1, 11):
        f1 = form_i(n)
        f2 = form_ii(n)
        match = (f1 == f2)
        powers = sorted(f1.keys(), reverse=True)
        poly = " + ".join(f"{f1[p]}*N^{p}" for p in powers)
        print(f"    n={n:>2}: {poly}   [match: {match}]")
    print()


# ──────────────────────────────────────────────────────────────────────────────
# PART 7 : DOES NON-PLANAR DOMINATE?  NORMALIZATION ANALYSIS.
# ──────────────────────────────────────────────────────────────────────────────

def part7():
    print("=" * 70)
    print("PART 7 : Does non-planar dominate?  Is the normalization wrong?")
    print("=" * 70)
    print("""
  ── The exact correlator ──

  <O_n O_n†>  =  n * N^n  +  n*C(n+1,4) * N^{n-2}  +  ...
              =  (planar)   +  (first non-planar)    +  ...

  There are:   n            planar diagrams, each giving  N^n
               n*C(n+1,4)  non-planar diagrams (first correction), each giving N^{n-2}

  ── QUESTION: does non-planar dominate because there are more of them? ──

  No — because each non-planar diagram gives a LOWER power of N.
  The key ratio is:

    (first non-planar contribution) / (planar contribution)
        =  n*C(n+1,4) * N^{n-2}  /  (n * N^n)
        =  C(n+1,4) / N^2
        =  (n+1)*n*(n-1)*(n-2) / (24 * N^2)

  For FIXED n, LARGE N:   this  -> 0   as  N -> infinity.
  The non-planar correction vanishes.  Planar DOMINATES.  ✓
""")

    # Numerical table: ratio for various n and N
    print("  Table: (first non-planar) / (planar)  =  C(n+1,4) / N^2")
    print()
    print(f"  {'n\\N':>6} | ", end="")
    N_vals = [5, 10, 20, 50, 100]
    for Nv in N_vals:
        print(f"  N={Nv:<4}", end="")
    print()
    print("  " + "-" * 65)
    for n in [2, 3, 4, 5, 6, 8, 10]:
        cn14 = math.comb(n+1, 4)
        print(f"  {n:>6} | ", end="")
        for Nv in N_vals:
            ratio = cn14 / Nv**2
            print(f"  {ratio:>7.4f}", end="")
        print(f"   [C(n+1,4)={cn14}]")
    print()

    print("""
  ── What changes for HEAVY operators (n ~ N)? ──

  For n ~ N, the ratio C(n+1,4)/N^2 ~ n^4/(24 N^2) ~ N^2/24 -> INFINITY.
  Non-planar diagrams are no longer suppressed — they overwhelm planar.
""")

    # Exact correlator values for n = N (heavy operators)
    def exact_correlator(n, N):
        """n! * [C(N+n,n+1) - C(N,n+1)] evaluated at integer N."""
        def binom(a, b):
            if b < 0 or b > a: return 0
            return math.comb(a, b)
        return math.factorial(n) * (binom(N+n, n+1) - binom(N, n+1))

    print("  Exact correlator values (integer N) for n=N (heavy operator):")
    print()
    print(f"  {'N=n':>5} | {'<O_n O_n†>':>30} | {'planar: n*N^n':>20} | {'ratio':>12}")
    print("  " + "-" * 80)
    for Nval in [2, 3, 4, 5, 6, 8, 10]:
        n = Nval
        corr  = exact_correlator(n, Nval)
        plan  = n * Nval**n
        ratio = corr / plan
        print(f"  {Nval:>5} | {corr:>30} | {plan:>20} | {ratio:>12.4f}")
    print()
    print("  ratio = <O_n O_n†> / (planar contribution)  >> 1  for large N=n.")
    print("  Non-planar diagrams DOMINATE when n ~ N.")
    print()

    print("""
  ── The normalization O_n / sqrt(n N^n) ──

  Paper eq. (8) normalises to unit two-point function at large N:
      tilde{O}_n  =  O_n / sqrt(n * N^n)
  so that <tilde{O}_n  tilde{O}_n†>  = 1  +  O(1/N^2).

  This works perfectly for LIGHT operators (n fixed, N -> infinity):
""")
    print("  <tilde{O}_n tilde{O}_n†> = [n*N^n + n*C(n+1,4)*N^{n-2} + ...] / (n*N^n)")
    print("                           = 1  +  C(n+1,4)/N^2  +  ...")
    print()
    print(f"  {'n':>4} | ", end="")
    N_vals2 = [10, 20, 50, 100, 1000]
    for Nv in N_vals2:
        print(f"  N={Nv:<5}", end="")
    print()
    print("  " + "-" * 72)
    for n in [2, 3, 4, 5, 8]:
        # Use exact closed form for the ratio
        print(f"  {n:>4} | ", end="")
        for Nv in N_vals2:
            corr  = exact_correlator(n, Nv)
            plan  = n * Nv**n
            ratio = corr / plan   # this is <tilde O tilde O†>
            print(f"  {ratio:>8.5f}", end="")
        print()
    print()
    print("  -> All approach 1 from above as N grows. Normalization is CORRECT")
    print("     for light operators.")
    print()

    print("""
  For HEAVY operators (n ~ N):  the normalization BREAKS DOWN.
""")
    print("  <tilde{O}_n tilde{O}_n†>  =  <O_n O_n†> / (n * N^n)")
    print()
    print(f"  {'N=n':>5} | {'<O O†>/(n*N^n)':>20} | {'interpretation'}")
    print("  " + "-" * 55)
    for Nval in [2, 3, 4, 5, 6, 8, 10, 15]:
        n = Nval
        corr  = exact_correlator(n, Nval)
        plan  = n * Nval**n
        ratio = corr / plan
        note  = "finite" if ratio < 2 else ("diverging" if ratio < 100 else "exponentially large")
        print(f"  {Nval:>5} | {ratio:>20.4f} | {note}")
    print()

    print("""
  SUMMARY:

  1. For a two-point function <O_n O_n†> with n FIXED and N -> infinity:
       - Non-planar diagrams are suppressed by powers of 1/N^2.
       - Total count of non-planar diagrams grows with n (as n^5, n^9, ...)
         but EACH diagram gives a lower power of N, and the N suppression wins.
       - Normalization  tilde{O} = O/sqrt(n N^n)  is correct.
       - <tilde{O}_n tilde{O}_n†> = 1 + O(1/N^2).

  2. For n ~ N (heavy operators):
       - The first non-planar correction C(n+1,4)/N^2 ~ N^2 -> infinity.
       - Non-planar diagrams dominate.  The full correlator grows much
         faster than the planar approximation.
       - The normalization  O/sqrt(n N^n)  is WRONG for heavy operators.
       - The correct framework (from the paper) is restricted Schur polynomials,
         which are NOT normalised by the naive planar formula.
""")


# ──────────────────────────────────────────────────────────────────────────────
# RUN ALL PARTS
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    part1()
    part2()
    part3()
    part4()
    part5()
    part6()
    part7()
