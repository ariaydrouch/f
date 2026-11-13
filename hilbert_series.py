#!/usr/bin/env python3
"""
Hilbert series of d N x N matrices under simultaneous conjugation
(Molien-Weyl integral, evaluated by iterated residues).

Data model (see the accompanying document for the full explanation)
-------------------------------------------------------------------
Variables are indexed 0 .. L-1 with L = (N-1) + d:
    indices 0 .. N-2      -> torus variables t_1 .. t_{N-1}
    indices N-1 .. L-1    -> weights x_1 .. x_d
A monomial is an integer exponent tuple of length L.

A TERM is   coef * x^mono * prod_i (1 - x^key_i) ^ e_i
    coef : python int
    mono : exponent tuple (the "prefactor")
    facs : dict  canonical key -> signed exponent  (e_i < 0: denominator)

The integrand is a FLAT LIST of terms, stored as a dict
    (mono, sorted facs tuple) -> coef
so that equal terms merge automatically.

Versions (selected with hilbert_series(..., equal_x=..., workers=...))
-----------------------------------------------------------------------
* general   : d independent weights x_1..x_d (L = N-1+d variables).
* equal_x   : all x_i set equal to one variable x from the start.  There is a
              single weight variable (L = N), and every x-dependent factor of the
              integrand carries multiplicity d, so poles have higher order and the
              series method of `residues` is used.
* workers>1 : the terms of the list are independent, so each iterated residue
              (and the numerator sum of the final assembly) is farmed out to a
              process pool.  Processes, not threads: the work is pure Python,
              so threads would be serialized by the GIL.

Canonical key: the exponent tuple m of a binomial (1 - x^m) is normalised so
its first nonzero entry is positive, using  1 - x^(-m) = -x^(-m) (1 - x^m).
Because the t's come first and are integrated in order, every binomial that
contains the current variable t_j has exponent exactly +1 on t_j.
"""
import sys
import time

import sympy as sp
from sympy.polys.rings import ring
from sympy.polys.domains import ZZ


# ---------------------------------------------------------------------------
# Section 1: small vector helpers and the generalised binomial coefficient
# ---------------------------------------------------------------------------
def vadd(a, b):
    return tuple(u + v for u, v in zip(a, b))


def vscale(a, k):
    return tuple(k * u for u in a)


def vneg(a):
    return tuple(-u for u in a)


def vzero_at(a, j):
    """Copy of a with component j set to zero."""
    return a[:j] + (0,) + a[j + 1:]


def gen_binom(e, q):
    """binom(e, q) for any integer e (negative allowed) and q >= 0."""
    c = 1
    for i in range(1, q + 1):
        c = c * (e - i + 1) // i  # exact at every step
    return c


# ---------------------------------------------------------------------------
# Section 2: canonical binomials and term construction
# ---------------------------------------------------------------------------
def canon(m):
    """Return (flipped, key) for the binomial (1 - x^m).
    flipped is None if m == 0 (the binomial is 1 - 1 = 0)."""
    for c in m:
        if c != 0:
            if c > 0:
                return False, m
            return True, vneg(m)
    return None, None


def insert_factor(facs, mono, coef, m, e):
    """Multiply the term (coef, mono, facs) by (1 - x^m)^e.
    facs is modified in place; returns the new (mono, coef), or None if the
    term becomes zero.  Cancellation of equal numerator / denominator
    factors happens here, because exponents under one key simply add."""
    if e == 0:
        return mono, coef
    flipped, key = canon(m)
    if flipped is None:
        if e > 0:
            return None          # (1 - 1)^e = 0 kills the term
        raise ZeroDivisionError("denominator factor 1 - 1 encountered")
    if flipped:
        # (1 - x^m)^e = (-1)^e x^(e m) (1 - x^-m)^e
        if e & 1:
            coef = -coef
        mono = vadd(mono, vscale(m, e))
    new = facs.get(key, 0) + e
    if new:
        facs[key] = new
    else:
        facs.pop(key, None)
    return mono, coef


def freeze(mono, facs):
    return (mono, tuple(sorted(facs.items())))


def initial_state(N, nx, mult=1):
    """The full integrand as one term (without the Z1^N factor).
    nx   : number of weight variables (d, or 1 in the all-equal version)
    mult : multiplicity of every x-dependent denominator factor
           (1 in the general version, d in the all-equal version)."""
    nt = N - 1
    L = nt + nx
    mono = tuple([-1] * nt + [0] * nx)          # 1 / (t_1 ... t_{N-1})
    coef = 1
    facs = {}
    for k in range(nt):
        for r in range(k, nt):
            a = tuple(1 if k <= i <= r else 0 for i in range(nt)) + (0,) * nx
            mono, coef = insert_factor(facs, mono, coef, a, +1)          # (1 - a)
            for i in range(nx):
                ex = tuple(1 if nt + i == u else 0 for u in range(L))
                mono, coef = insert_factor(facs, mono, coef, vadd(ex, a), -mult)        # 1/(1 - x a)^mult
                mono, coef = insert_factor(facs, mono, coef, vadd(ex, vneg(a)), -mult)  # 1/(1 - x/a)^mult
    return {freeze(mono, facs): coef}


# ---------------------------------------------------------------------------
# Section 3: pole identification
# ---------------------------------------------------------------------------
def first_primes(d):
    ps, n = [], 2
    while len(ps) < d:
        if all(n % p for p in ps):
            ps.append(n)
        n += 1
    return ps


class PoleClassifier:
    """Exact inside/outside test.

    We evaluate at x_i = 1/q_i (distinct primes).  The pole of (1 - t*r) is
    t = r^-1.  Its modulus depends on the later t's, which sit on circles of
    radius exp(-eta_s) with eta_1 >> eta_2 >> ... > 0 (all infinitesimal), and on
    the x-part of r:
        * x-part of r nonzero: modulus is prod q_i^(r_i) (a finite number != 1);
          the pole is inside iff that product is < 1.
        * x-part of r zero ("neutral" pole, modulus 1 up to infinitesimals):
          the integration radius exp(-eta_j) is slightly below 1 and dominates
          the later eta's, so the pole is OUTSIDE.
    The integrand is analytic in the thin annulus around the unit torus, so
    shrinking the radii by an infinitesimal amount does not change the integral."""

    def __init__(self, nt, d):
        self.nt = nt
        self.q = first_primes(d)
        self.cache = {}

    def __call__(self, r):
        rx = r[self.nt:]
        side = self.cache.get(rx)
        if side is None:
            num = den = 1
            for qi, ri in zip(self.q, rx):
                if ri > 0:
                    num *= qi ** ri
                elif ri < 0:
                    den *= qi ** (-ri)
            side = 'inside' if num < den else 'outside'   # num == den: neutral -> outside
            self.cache[rx] = side
        return side


def check_leading(key, j):
    if key[j] != 1 or any(key[:j]):
        raise AssertionError(f"binomial {key} not linear in t_{j + 1}")


def find_poles(mono, facs, j, classify):
    """Poles of one term inside |t_j| < 1.
    Returns a list of (kind, key, order):
        ('zero', None, order)   pole at t_j = 0 from the prefactor
        ('factor', key, order)  pole of the denominator factor `key`"""
    poles = []
    if mono[j] < 0:
        poles.append(('zero', None, -mono[j]))
    for key, e in facs.items():
        if e < 0 and key[j] != 0:
            check_leading(key, j)
            if classify(vzero_at(key, j)) == 'inside':
                poles.append(('factor', key, -e))
    return poles


# ---------------------------------------------------------------------------
# Section 4: residue calculation
# ---------------------------------------------------------------------------
def prefactor_slot(k, p, n):
    """Series of t^k around t = p, in s = t - p:  sum_q binom(k,q) p^(k-q) s^q."""
    cap = n if k < 0 else min(n, k)
    return [(q, gen_binom(k, q), vscale(p, k - q), None) for q in range(cap + 1)]


def factor_slot(e, R, m, n):
    """Series of (1 - t R)^e around t = p, with m = p + R the exponent of p*R:
         (1 - (p+s)R)^e = A^e (1 - s R/A)^e,  A = 1 - p R
       = sum_q binom(e,q) (-1)^q R^q A^(e-q) s^q."""
    flipped, key = canon(m)
    if flipped is None:
        raise ArithmeticError("a numerator/denominator factor coincides with the pole")
    cap = n if e <= 0 else min(n, e)
    opts = []
    for q in range(cap + 1):
        E = e - q
        c = gen_binom(e, q) * (-1) ** q
        dm = vscale(R, q)
        if flipped:
            if E & 1:
                c = -c
            dm = vadd(dm, vscale(m, E))
        opts.append((q, c, dm, (key, E)))
    return opts


def factor_slot_at_zero(e, R, n):
    """Series of (1 - t R)^e around t = 0: sum_q binom(e,q) (-1)^q R^q t^q."""
    cap = n if e <= 0 else min(n, e)
    return [(q, gen_binom(e, q) * (-1) ** q, vscale(R, q), None) for q in range(cap + 1)]


def distribute(slots, n, L):
    """All ways to pick one option per slot with the q's summing to n.
    Yields (coefficient product, summed monomial shift, list of factor updates)."""
    caps = [max(o[0] for o in s) for s in slots]
    suffix = [0] * (len(slots) + 1)
    for i in range(len(slots) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + caps[i]
    out = []

    def rec(i, remaining, c, dm, upds):
        if i == len(slots):
            if remaining == 0:
                out.append((c, dm, upds))
            return
        if remaining > suffix[i]:
            return
        for q, cc, dd, upd in slots[i]:
            if q > remaining:
                break
            rec(i + 1, remaining - q, c * cc, vadd(dm, dd),
                upds + [upd] if upd is not None else upds)

    rec(0, n, 1, (0,) * L, [])
    return out


def residues(coef, mono, facs, j, kind, pole_key, mu, L):
    """Residue of one term at one pole, as a list of (coef, mono, facs) terms.

    Split the term as   coef * t^k * M' * [pole factor]^-mu * prod(other t-dependent) * prod(t-free).
    Pull out the pole factor:  (1 - t r)^-mu = (-1)^mu r^-mu (t - p)^-mu,  p = 1/r.
    The residue is  C * [s^(mu-1)] of the regular part expanded in s = t - p."""
    k = mono[j]
    mono_rest = vzero_at(mono, j)
    free, dep = {}, []
    for key, e in facs.items():
        if key[j] == 0:
            free[key] = e
        elif kind == 'factor' and key == pole_key:
            continue
        else:
            check_leading(key, j)
            dep.append((key, e))

    n = mu - 1
    slots = []
    if kind == 'factor':
        r = vzero_at(pole_key, j)
        p = vneg(r)
        if mu & 1:
            coef = -coef
        mono_rest = vadd(mono_rest, vscale(r, -mu))
        slots.append(prefactor_slot(k, p, n))
        for key, e in dep:
            R = vzero_at(key, j)
            slots.append(factor_slot(e, R, vadd(p, R), n))
    else:  # pole at t_j = 0, order mu = -k
        for key, e in dep:
            slots.append(factor_slot_at_zero(e, vzero_at(key, j), n))

    results = []
    for c, dm, upds in distribute(slots, n, L):
        if c == 0:
            continue
        f2 = dict(free)
        for key, E in upds:
            new = f2.get(key, 0) + E
            if new:
                f2[key] = new
            else:
                f2.pop(key, None)
        results.append((coef * c, vadd(mono_rest, dm), f2))
    return results


def _integrate_items(items, j, L, classify):
    """Serial kernel: eliminate t_{j+1} from a list of ((mono, facs), coef) items."""
    new_state = {}
    for (mono, facs_t), coef in items:
        facs = dict(facs_t)
        for kind, key, mu in find_poles(mono, facs, j, classify):
            for c2, mono2, f2 in residues(coef, mono, facs, j, kind, key, mu, L):
                sig = freeze(mono2, f2)
                new_state[sig] = new_state.get(sig, 0) + c2
    return new_state


def _integrate_task(args):
    """Process-pool entry point (must be a module-level function)."""
    items, j, L, nt, nx = args
    return _integrate_items(items, j, L, PoleClassifier(nt, nx))


MIN_PARALLEL_TERMS = 16      # below this the pool overhead is not worth paying


def integrate_variable(state, j, L, nt, nx, pool=None, workers=1):
    """One iterated residue: eliminate t_{j+1} from every term.
    Terms are independent, so with a pool they are split into chunks that are
    processed in separate processes and merged afterwards."""
    items = list(state.items())
    if pool is None or len(items) < MIN_PARALLEL_TERMS:
        new_state = _integrate_items(items, j, L, PoleClassifier(nt, nx))
    else:
        nchunks = min(len(items), workers * 4)           # several chunks per worker: load balance
        tasks = [(items[i::nchunks], j, L, nt, nx) for i in range(nchunks)]
        new_state = {}
        for part in pool.map(_integrate_task, tasks):
            for sig, c in part.items():
                new_state[sig] = new_state.get(sig, 0) + c
    return {sig: c for sig, c in new_state.items() if c}


# ---------------------------------------------------------------------------
# Section 5: final assembly (x-only terms -> one rational function)
# ---------------------------------------------------------------------------
def exact_div(f, g):
    """Exact division of polynomials given as {exponent tuple: int} dicts (lex order).
    Returns the quotient dict, or None if g does not divide f.
    Heap-based long division: O(|q| |g| log |f|), much faster than repeatedly
    searching for the leading term."""
    import heapq
    lt = max(g)
    lc = g[lt]
    rest = [(m, c) for m, c in g.items() if m != lt]
    f = dict(f)
    heap = [tuple(-u for u in m) for m in f]
    heapq.heapify(heap)
    q = {}
    while heap:
        m = tuple(-u for u in heapq.heappop(heap))
        c = f.pop(m, 0)
        if c == 0:
            continue
        qm = tuple(a - b for a, b in zip(m, lt))
        if min(qm) < 0 or c % lc:
            return None
        qc = c // lc
        q[qm] = qc
        for gm, gc in rest:
            t = tuple(a + b for a, b in zip(qm, gm))
            if t in f:
                f[t] -= qc * gc
            else:
                f[t] = -qc * gc
                heapq.heappush(heap, tuple(-u for u in t))
    return q


def _numerator_task(args):
    """Sum of coef * x^shift * prod g^exp over a chunk of rows, as {monomial: coef}.
    Rows sharing the same irreducible-factor multiplier are grouped first, so each
    distinct multiplier is multiplied in only once."""
    names, rows, gdicts, dmax, smin = args
    R, *_ = ring(names, ZZ)
    d = len(names)
    groups = {}
    for c, shift, net in rows:
        key = tuple(sorted((gi, net.get(gi, 0) + dmax.get(gi, 0))
                           for gi in set(net) | set(dmax)
                           if net.get(gi, 0) + dmax.get(gi, 0)))
        mon = tuple(shift[i] - smin[i] for i in range(d))
        bucket = groups.setdefault(key, {})
        bucket[mon] = bucket.get(mon, 0) + c
    gcache = {}
    total = R.zero
    for key, bucket in groups.items():
        W = R.from_dict({m: c for m, c in bucket.items() if c})
        for gi, ex in key:
            if gi not in gcache:
                gcache[gi] = R.from_dict(dict(gdicts[gi]))
            W = W * gcache[gi] ** ex
        total = total + W
    return {m: int(c) for m, c in total.items()}


def assemble(state, N, nx, mult, xs, nt, pool=None, workers=1):
    """Sum the remaining x-only terms (times Z1^N) into a single fraction.

    Every binomial (1 - x^v) is rewritten  x^(-v^-) * (x^(v^-) - x^(v^+)) and the
    polynomial is split into irreducible factors once.  Exponents of the same
    irreducible factor are added across numerator and denominator (this is the
    cyclotomic cancellation, e.g. (1-x^2) against (1-x)).  Terms are brought to
    the least common denominator, summed in a polynomial ring (in parallel chunks
    if a pool is given), and the common denominator factors are removed by exact
    division."""
    R, *gens = ring(xs, ZZ)
    d = nx
    cache = {}
    glist, gindex = [], {}

    def gid(fr):
        key = tuple(sorted(fr.items()))
        if key not in gindex:
            gindex[key] = len(glist)
            glist.append(tuple((m, int(c)) for m, c in key))
        return gindex[key]

    def split(v):
        if v not in cache:
            neg = {i: -c for i, c in enumerate(v) if c < 0}
            pos = {i: c for i, c in enumerate(v) if c > 0}
            P = sp.Mul(*[xs[i] ** c for i, c in neg.items()]) - sp.Mul(*[xs[i] ** c for i, c in pos.items()])
            content, flist = sp.factor_list(sp.expand(P))
            sign = 1 if content > 0 else -1
            if abs(content) != 1:
                raise AssertionError("unexpected content in binomial")
            parts = []
            for f, mult_f in flist:
                fr = R.from_expr(f)
                if fr.LC < 0:
                    fr = -fr
                    if mult_f & 1:
                        sign = -sign
                parts.append((gid(fr), mult_f))
            shift = vneg(tuple(max(-c, 0) for c in v))        # x^(-v^-)
            cache[v] = (sign, parts, shift)
        return cache[v]

    rows = []
    for (mono, facs_t), coef in state.items():
        if any(mono[:nt]):
            raise AssertionError("t-dependence left after integration")
        facs = dict(facs_t)
        for i in range(d):                       # Z1^N = prod (1 - x_i)^(-N*mult)
            key = (0,) * nt + tuple(1 if u == i else 0 for u in range(d))
            facs[key] = facs.get(key, 0) - N * mult
        shift = list(mono[nt:])
        sign = 1
        net = {}
        for key, e in facs.items():
            if e == 0:
                continue
            s_, parts, sh = split(key[nt:])
            if e & 1 and s_ < 0:
                sign = -sign
            for gi, mult_f in parts:
                net[gi] = net.get(gi, 0) + e * mult_f
            for i in range(d):                   # x^(-e v^-)
                shift[i] += e * sh[i]
        rows.append((coef * sign, shift, net))

    dmax = {}
    for _, _, net in rows:
        for gi, e in net.items():
            if -e > dmax.get(gi, 0):
                dmax[gi] = -e
    smin = [min(row[1][i] for row in rows) for i in range(d)]
    names = [str(x) for x in xs]

    if pool is None or len(rows) < MIN_PARALLEL_TERMS:
        parts = [_numerator_task((names, rows, glist, dmax, smin))]
    else:
        nchunks = min(len(rows), workers * 4)
        tasks = [(names, rows[i::nchunks], glist, dmax, smin) for i in range(nchunks)]
        parts = list(pool.map(_numerator_task, tasks))
    num = {}
    for part in parts:
        for m, c in part.items():
            num[m] = num.get(m, 0) + c
    num = {m: c for m, c in num.items() if c}

    # remove common denominator factors by exact division
    remaining = {}
    for gi, e in dmax.items():
        g = dict(glist[gi])
        left = e
        while left > 0:
            q = exact_div(num, g)
            if q is None:
                break
            num = q
            left -= 1
        if left:
            remaining[gi] = left

    # strip the monomial content of the numerator
    if num:
        mins = [min(m[i] for m in num) for i in range(d)]
        num = {tuple(m[i] - mins[i] for i in range(d)): c for m, c in num.items()}
        smin = [smin[i] + mins[i] for i in range(d)]

    numer = R.from_dict(num).as_expr()
    mono_expr = sp.Mul(*[xs[i] ** smin[i] for i in range(d)])
    denom = sp.Mul(*[R.from_dict(dict(glist[gi])).as_expr() ** e for gi, e in remaining.items()])
    return mono_expr, numer, denom


# ---------------------------------------------------------------------------
# Section 6: driver
# ---------------------------------------------------------------------------
def hilbert_series(N, d, equal_x=False, workers=1, verbose=False):
    """Hilbert series of d N x N matrices under simultaneous conjugation.

    equal_x=False: returns (Z, Z with all x_i = x) with Z in x1..xd
                   (the second entry is None for d == 1, where Z already is that).
    equal_x=True : all x_i = x from the start; returns (None, Z(x)).
    workers      : 1 = serial; k > 1 = pool of k processes; 0 = all cores."""
    import os
    if workers == 0:
        workers = os.cpu_count() or 1
    single = equal_x or d == 1
    nx = 1 if single else d
    mult = d if equal_x else 1
    xs = list(sp.symbols(f"x1:{nx + 1}")) if nx > 1 else [sp.Symbol("x")]
    if N == 1:
        Z = sp.Mul(*[1 / (1 - x) for x in xs]) ** mult
    else:
        nt = N - 1
        L = nt + nx
        t0 = time.time()
        pool = None
        if workers > 1:
            from concurrent.futures import ProcessPoolExecutor
            pool = ProcessPoolExecutor(max_workers=workers)
        try:
            state = initial_state(N, nx, mult)
            for j in range(nt):
                state = integrate_variable(state, j, L, nt, nx, pool, workers)
                if verbose:
                    print(f"  integrated t{j + 1}: {len(state)} terms "
                          f"({time.time() - t0:.2f}s)", file=sys.stderr)
            mono_expr, numer, denom = assemble(state, N, nx, mult, xs, nt, pool, workers)
        finally:
            if pool is not None:
                pool.shutdown()
        if verbose:
            print(f"  assembled ({time.time() - t0:.2f}s)", file=sys.stderr)
        Z = sp.factor(numer) * mono_expr / denom        # numerator and denominator are coprime
    if single:
        return (None, Z) if equal_x else (Z, None)
    x = sp.Symbol("x")
    return Z, sp.factor(sp.cancel(Z.subs({xi: x for xi in xs})))


def main():
    N = int(input("N (size of matrices): "))
    d = int(input("d (number of matrices): "))
    eq = d > 1 and input("Compute only the all-equal case x_i = x directly? (y/n): ").strip().lower().startswith("y")
    w = int(input("Worker processes (1 = serial, 0 = all cores): ") or "1")
    Z, Zx = hilbert_series(N, d, equal_x=eq, workers=w, verbose=True)
    print()
    if Z is not None:
        print("Z =", Z)
    if Zx is not None:
        print()
        print("Z with all x_i = x:" if not eq else "Z (all x_i = x):", Zx)


if __name__ == "__main__":
    main()
