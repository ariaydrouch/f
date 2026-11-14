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
from fractions import Fraction

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
CHUNKS_PER_WORKER = 16       # small chunks: load balance and bounded per-worker memory


def integrate_variable(state, j, L, nt, nx, pool=None, workers=1):
    """One iterated residue: eliminate t_{j+1} from every term.
    Terms are independent, so with a pool they are split into chunks that are
    processed in separate processes; each partial result is merged into the new
    state as soon as it arrives and then dropped, so that at most a few partial
    dictionaries are alive at any time."""
    from concurrent.futures import as_completed
    items = list(state.items())
    if pool is None or len(items) < MIN_PARALLEL_TERMS:
        new_state = _integrate_items(items, j, L, PoleClassifier(nt, nx))
    else:
        nchunks = min(len(items), workers * CHUNKS_PER_WORKER)
        futures = {pool.submit(_integrate_task, (items[i::nchunks], j, L, nt, nx))
                   for i in range(nchunks)}
        del items
        new_state = {}
        for fut in as_completed(futures):
            futures.discard(fut)
            part = fut.result()
            del fut
            for sig, c in part.items():
                new_state[sig] = new_state.get(sig, 0) + c
            del part
    for sig in [sig for sig, c in new_state.items() if not c]:
        del new_state[sig]
    return new_state


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


# ---------------------------------------------------------------------------
# Section 7: Hironaka form of the singly graded series
# ---------------------------------------------------------------------------
# Z(x) = P(x) / prod_i (1 - x^{d_i})^{m_i}, with sum m_i = Krull dimension.
# The ring of invariants is Cohen-Macaulay (Hochster-Roberts), so for the degrees
# of an actual system of primary invariants P has non-negative coefficients and
# P(1) is the number of secondary invariants (including the trivial one, 1).
#
# P(1) is NOT an invariant of the ring: with e = lim_{x->1} (1-x)^D Z(x),
#     P(1) = e * prod_i d_i^{m_i},
# so a different (equally valid) choice of primary degrees changes the count.
#
# Polynomials below are dense coefficient lists, lowest degree first.

def _poly_mul_binomial(p, k):
    """p(x) * (1 - x^k)."""
    out = p + [0] * k
    for i, c in enumerate(p):
        out[i + k] -= c
    return out


def _poly_exact_div(p, q):
    """p / q for integer polynomials, q with leading coefficient +-1; error if inexact."""
    p = list(p)
    dq = len(q) - 1
    lc = q[-1]
    if lc not in (1, -1):
        raise ValueError("divisor must have leading coefficient +-1")
    quo = [0] * max(len(p) - dq, 1)
    for i in range(len(p) - 1 - dq, -1, -1):
        c = p[i + dq] * lc
        if c:
            quo[i] = c
            for j, qc in enumerate(q):
                p[i + j] -= c * qc
    if any(p[:dq]):
        raise ArithmeticError("denominator does not divide numerator")
    while len(quo) > 1 and quo[-1] == 0:
        quo.pop()
    return quo


def _coeffs(expr, x):
    return [int(c) for c in reversed(sp.Poly(expr, x).all_coeffs())]


def cyclotomic_exponents(den, x):
    """{k: a_k} with den = +- prod_k Phi_k(x)^{a_k}."""
    _, flist = sp.factor_list(den, x)
    a = {}
    for f, m in flist:
        fp = sp.Poly(f, x)
        deg = fp.degree()
        for k in range(1, 2 * deg * deg + 3):            # phi(k) >= sqrt(k/2)
            if sp.totient(k) != deg:
                continue
            ck = sp.Poly(sp.cyclotomic_poly(k, x), x)
            if fp == ck or fp == -ck:
                a[k] = a.get(k, 0) + m
                break
        else:
            raise ValueError(f"denominator factor {f} is not cyclotomic")
    return a


def covers(degrees, a):
    """True if prod (1 - x^d)^m is divisible by prod Phi_k^{a_k}: for every k at
    least a_k of the degrees are multiples of k, and there are exactly a_1 of them."""
    if sum(degrees.values()) != a.get(1, 0):
        return False
    return all(sum(m for d, m in degrees.items() if d % k == 0) >= ak for k, ak in a.items())


# Primary degrees quoted in arXiv:2503.20097 for d = 2 (eqs. 3.40, 3.46, 3.48,
# 3.51, D.1).  The Hilbert series alone does not fix these; they are a choice.
PAPER_DEGREES_D2 = {
    1: {1: 2},
    2: {1: 2, 2: 3},
    3: {1: 2, 2: 3, 3: 4, 4: 1},
    4: {1: 2, 2: 3, 3: 4, 4: 6, 6: 2},
    5: {1: 2, 2: 3, 3: 4, 4: 6, 5: 6, 6: 5},
    6: {1: 2, 2: 3, 3: 4, 4: 6, 5: 7, 6: 9, 8: 6},
    7: {1: 2, 2: 3, 3: 4, 4: 6, 5: 8, 6: 11, 7: 8, 8: 5, 10: 2, 12: 1},
}


class HironakaForm:
    """Z(x) = numerator(x) / prod_{d, m in degrees} (1 - x^d)^m."""

    def __init__(self, degrees, numerator):
        self.degrees = degrees                  # {d: m}
        self.numerator = numerator              # coefficient list, lowest degree first

    @property
    def krull_dim(self):
        return sum(self.degrees.values())

    @property
    def secondaries(self):
        """P(1): number of secondary invariants, the trivial one (=1) included."""
        return sum(self.numerator)

    @property
    def nonnegative(self):
        return all(c >= 0 for c in self.numerator)

    @property
    def palindromic(self):
        return self.numerator == self.numerator[::-1]

    def degree_sum(self):
        return sum(d * m for d, m in self.degrees.items())

    def series(self, n):
        """First n+1 coefficients of Z(x)."""
        s = (self.numerator + [0] * (n + 1))[:n + 1]
        for d, m in self.degrees.items():
            for _ in range(m):
                for i in range(d, n + 1):
                    s[i] += s[i - d]
        return s

    def denominator_str(self):
        parts = []
        for d, m in self.degrees.items():
            b = "(1 - x)" if d == 1 else f"(1 - x^{d})"
            parts.append(b if m == 1 else f"{b}^{m}")
        return " ".join(parts)

    def numerator_str(self):
        terms = []
        for i, c in enumerate(self.numerator):
            if c:
                mon = "1" if i == 0 else ("x" if i == 1 else f"x^{i}")
                if i == 0:
                    terms.append(f"{c}")
                else:
                    terms.append(mon if c == 1 else f"-{mon}" if c == -1 else f"{c}*{mon}")
        return " + ".join(terms).replace("+ -", "- ")

    def __str__(self):
        return f"({self.numerator_str()}) / ({self.denominator_str()})"


class ReducedSeries:
    """Z(x) = num(x) / den(x) in lowest terms, den = +- prod_k Phi_k^{a_k}."""

    def __init__(self, Z, x=None):
        if x is None:
            (x,) = Z.free_symbols
        num, den = sp.fraction(sp.cancel(sp.together(Z)))
        self.a = cyclotomic_exponents(den, x)
        self.num = _coeffs(num, x)
        self.den = _coeffs(den, x)
        self.krull_dim = self.a.get(1, 0)
        # e = lim_{x->1} (1-x)^D Z(x); Phi_k(1) = p for k = p^j, else 1 (k > 1)
        phi1 = 1
        for k, ak in self.a.items():
            if k > 1:
                fac = sp.factorint(k)
                if len(fac) == 1:
                    phi1 *= next(iter(fac)) ** ak
        self.e = Fraction(abs(sum(self.num)), phi1)

    def numerator_for(self, degrees):
        p = list(self.num)
        for d, m in degrees.items():
            for _ in range(m):
                p = _poly_mul_binomial(p, d)
        return _poly_exact_div(p, self.den)

    def series(self, n):
        """First n+1 Taylor coefficients of num/den (den(0) = +-1)."""
        c0 = self.den[0]
        out = []
        for i in range(n + 1):
            v = self.num[i] if i < len(self.num) else 0
            for j in range(1, min(i, len(self.den) - 1) + 1):
                v -= self.den[j] * out[i - j]
            out.append(v * c0)
        return out


def admissible(hf, h):
    """Necessary conditions on a Hironaka form for primary invariants of its
    degrees to exist, given the Hilbert series coefficients h (len(h) > deg P):
      * P_k >= 0  (P_k counts the secondary invariants of degree k), and
      * P_k <= h_k (secondaries of degree k are linearly independent invariants)."""
    return all(0 <= c <= h[k] for k, c in enumerate(hf.numerator))


def hironaka_candidates(Z, x=None, max_secondaries=None):
    """All primary-degree choices {d: m} that pass `admissible` and have
    P(1) <= max_secondaries, sorted by (P(1), sum of degrees).  The search is
    exhaustive: no degree is excluded a priori, the bound on P(1) limits them.

    With max_secondaries=None the bound is raised (x4) until something is found;
    the first entry is then the admissible choice with the smallest P(1), which
    is a LOWER BOUND for the number of secondary invariants of any Hironaka
    decomposition.  Whether it is attained (whether algebraically independent
    invariants of those degrees exist) cannot be read off the Hilbert series.

    Search: degrees are fixed in increasing order.  Factors of degree > k do not
    change the coefficients of x^0..x^k, so with P the running product
    Z * prod (1 - x^d)^m over the degrees chosen so far, at most P[k] factors of
    degree k may be added.  P(1) = e * prod d^m >= e * prod * k^left prunes the
    rest, which also caps the largest degree that can occur."""
    rs = Z if isinstance(Z, ReducedSeries) else ReducedSeries(Z, x)
    a, D, e = rs.a, rs.krull_dim, rs.e
    if max_secondaries is None:
        max_secondaries = 4
        while True:
            found = hironaka_candidates(rs, None, max_secondaries)
            if found:
                return found
            max_secondaries *= 4
    found = []
    series_cache = {}

    def series(n):
        if n not in series_cache:
            series_cache[n] = rs.series(n)
        return series_cache[n]

    def times_binomial(P, k):
        P = list(P)
        for i in range(len(P) - 1, k - 1, -1):
            P[i] -= P[i - k]
        return P

    def rebuild(chosen, n):
        P = series(n)
        for d, m in chosen.items():
            for _ in range(m):
                P = times_binomial(P, d)
        return P

    def rec(k, P, chosen, left, prod):
        if left == 0:
            if covers(chosen, a):
                hf = HironakaForm(dict(chosen), rs.numerator_for(chosen))
                if admissible(hf, series(len(hf.numerator))):
                    found.append(hf)
            return
        if e * prod * k ** left > max_secondaries:
            return
        if k >= len(P):
            P = rebuild(chosen, 2 * k + 8)
        for m in range(min(P[k], left), -1, -1):
            if m < left and e * prod * k ** m * (k + 1) ** (left - m) > max_secondaries:
                continue
            P2 = P
            for _ in range(m):
                P2 = times_binomial(P2, k)
            if m:
                chosen[k] = m
            rec(k + 1, P2, chosen, left - m, prod * k ** m)
            chosen.pop(k, None)

    rec(1, series(2 * max(a) + 8), {}, D, 1)
    found.sort(key=lambda hf: (hf.secondaries, hf.degree_sum()))
    return found


def hironaka_form(Z, x=None, degrees=None):
    """Rewrite a univariate Hilbert series Z(x) as P(x) / prod (1 - x^d)^m.

    degrees : {d: m}, e.g. PAPER_DEGREES_D2[N].  Any choice that covers the
              reduced denominator gives a polynomial P (checked by exact division).
              If omitted, the admissible choice with the smallest P(1) is used
              (see `hironaka_candidates` for why this is only a lower bound)."""
    rs = Z if isinstance(Z, ReducedSeries) else ReducedSeries(Z, x)
    if degrees is None:
        return hironaka_candidates(rs)[0]
    degrees = dict(sorted(degrees.items()))
    if sum(degrees.values()) != rs.krull_dim:
        raise ValueError(f"{sum(degrees.values())} denominator factors given, "
                         f"Krull dimension is {rs.krull_dim}")
    return HironakaForm(degrees, rs.numerator_for(degrees))


def free_trace_series(d, n):
    """First n+1 coefficients of the N -> infinity series prod_k (1 - x^k)^(-c_k),
    c_k = number of necklaces of length k in d colours (single traces of length k)."""
    s = [1] + [0] * n
    for k in range(1, n + 1):
        ck = int(sum(sp.totient(m) * d ** (k // m) for m in sp.divisors(k)) // k)
        # (1 - x^k)^(-ck) = sum_j binom(ck + j - 1, j) x^(jk)
        b = [1]
        for j in range(1, n // k + 1):
            b.append(b[-1] * (ck + j - 1) // j)
        s = [sum(b[j] * s[i - j * k] for j in range(i // k + 1)) for i in range(n + 1)]
    return s


def first_difference(a, b):
    """Index of the first differing coefficient (None if equal over the common length)."""
    return next((i for i, (u, v) in enumerate(zip(a, b)) if u != v), None)


def _row(N, d, hf, rs, source):
    return {
        "N": N, "d": d, "source": source,
        "denominator": {str(k): m for k, m in hf.degrees.items()},
        "krull_dim": hf.krull_dim,
        "numerator": hf.numerator,
        "numerator_degree": len(hf.numerator) - 1,
        "secondaries_P1": hf.secondaries,
        "nontrivial_secondaries": hf.secondaries - 1,
        "nonnegative": hf.nonnegative,
        "palindromic": hf.palindromic,
        "e": str(rs.e),
    }


def tabulate(Ns, d=2, workers=1, verbose=False, series_terms=40):
    """Hironaka data for the singly graded series of d matrices.

    Per N: one row with the paper's primary degrees (d = 2, N <= 7) and one with
    the admissible choice of smallest P(1).  `e` = P(1) / prod d^m does not
    depend on the choice.  `agrees_with_free_below` is the first degree at which
    Z_N differs from the N -> infinity series (trace relations start at N + 1)."""
    rows = []
    free = free_trace_series(d, series_terms)
    for N in Ns:
        t0 = time.time()
        _, Zx = hilbert_series(N, d, equal_x=d > 1, workers=workers, verbose=verbose)
        rs = ReducedSeries(Zx, sp.Symbol("x"))
        forms = []
        if d == 2 and N in PAPER_DEGREES_D2:
            forms.append((hironaka_form(rs, degrees=PAPER_DEGREES_D2[N]), "paper"))
        best = hironaka_candidates(rs)[0]
        if not forms or best.degrees != forms[0][0].degrees:
            forms.append((best, "min P(1)"))
        diff = first_difference(rs.series(series_terms), free)
        for hf, source in forms:
            row = _row(N, d, hf, rs, source)
            row["agrees_with_free_below"] = diff
            row["seconds"] = round(time.time() - t0, 2)
            rows.append(row)
    return rows


def _print_hironaka(hf):
    print(f"Hironaka form: Z(x) = P(x) / [{hf.denominator_str()}]")
    print(f"  P(x) = {hf.numerator_str()}")
    print(f"  primary invariants (Krull dim) = {hf.krull_dim}")
    print(f"  P(1) = {hf.secondaries} secondary invariants "
          f"({hf.secondaries - 1} non-trivial, i.e. excluding 1)")
    print(f"  P >= 0: {hf.nonnegative}   palindromic: {hf.palindromic}   "
          f"deg P = {len(hf.numerator) - 1}, sum d_i m_i = {hf.degree_sum()}")


def _parse_degrees(s):
    """'1:2,2:3,3:4' -> {1: 2, 2: 3, 3: 4}"""
    return {int(k): int(m) for k, m in (item.split(":") for item in s.split(","))}


def main():
    import argparse
    import json
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--N", type=int, help="matrix size (omit for interactive mode)")
    ap.add_argument("--d", type=int, default=2, help="number of matrices")
    ap.add_argument("--graded", action="store_true",
                    help="also compute the multigraded series in x1..xd")
    ap.add_argument("--table", nargs=2, type=int, metavar=("NMIN", "NMAX"),
                    help="tabulate Hironaka numerators for N = NMIN..NMAX")
    ap.add_argument("--json", help="write the table to this file")
    ap.add_argument("--workers", type=int, default=1, help="1 = serial, 0 = all cores")
    ap.add_argument("--degrees", type=_parse_degrees,
                    help="explicit primary degrees for the Hironaka form, e.g. 1:2,2:3,3:4,4:6,6:2")
    ap.add_argument("--choice", choices=("min", "paper"), default="min",
                    help="if --degrees is not given: 'min' = admissible choice with the fewest "
                         "secondary invariants (default), 'paper' = arXiv:2503.20097 (d = 2, N <= 7)")
    ap.add_argument("--candidates", type=int, default=0, metavar="K",
                    help="also list the K admissible degree choices with smallest P(1)")
    args = ap.parse_args()

    if args.table:
        rows = tabulate(range(args.table[0], args.table[1] + 1), args.d, args.workers, verbose=True)
        print(f"{'N':>3} {'source':>9} {'primary':>7} {'P(1)':>20} {'non-trivial':>20} "
              f"{'deg P':>5}  denominator degrees d^m")
        for r in rows:
            den = " ".join(f"{k}^{m}" for k, m in r["denominator"].items())
            print(f"{r['N']:>3} {r['source']:>9} {r['krull_dim']:>7} {r['secondaries_P1']:>20,} "
                  f"{r['nontrivial_secondaries']:>20,} {r['numerator_degree']:>5}  {den}"
                  + ("" if r["nonnegative"] else "  (P has negative coefficients!)"))
        if args.json:
            with open(args.json, "w") as fh:
                json.dump(rows, fh, indent=1)
        return

    if args.N is None:
        N = int(input("N (size of matrices): "))
        d = int(input("d (number of matrices): "))
        eq = d > 1 and input("Compute only the all-equal case x_i = x directly? (y/n): ").strip().lower().startswith("y")
        w = int(input("Worker processes (1 = serial, 0 = all cores): ") or "1")
    else:
        N, d, eq, w = args.N, args.d, not args.graded, args.workers
    Z, Zx = hilbert_series(N, d, equal_x=eq and d > 1, workers=w, verbose=True)
    print()
    if Z is not None:
        print("Z =", Z)
    if Zx is not None:
        print()
        print("Z with all x_i = x:" if not eq else "Z (all x_i = x):", Zx)
    Zx = Zx if Zx is not None else Z
    rs = ReducedSeries(Zx, sp.Symbol("x"))
    degrees = args.degrees
    if degrees is None and args.choice == "paper":
        if d != 2 or N not in PAPER_DEGREES_D2:
            raise SystemExit("--choice paper is only available for d = 2, N <= 7")
        degrees = PAPER_DEGREES_D2[N]
    print()
    _print_hironaka(hironaka_form(rs, degrees=degrees))
    print(f"  e = P(1) / prod d^m = {rs.e}  (independent of the choice of degrees)")
    if args.candidates:
        print("\nAdmissible choices with smallest P(1) (0 <= P_k <= h_k: necessary, "
              "not sufficient, for primary invariants of these degrees):")
        for hf in hironaka_candidates(rs)[:args.candidates]:
            print(f"  P(1) = {hf.secondaries:>12,}   {hf.denominator_str()}")


if __name__ == "__main__":
    main()
