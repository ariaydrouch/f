# `hilbert_series.py` — Molien–Weyl Hilbert series and Hironaka forms

This document explains the mathematics behind `hilbert_series.py` and walks
through the code section by section. It covers:

1. what is computed, as the Molien–Weyl integral;
2. how the integral is evaluated, as iterated residues on a list of terms;
3. how the terms are summed into one rational function;
4. how that rational function is rewritten in Hironaka form, what $P(1)$, $D$,
   $d_i$ and $m_i$ mean, and how the choice with the fewest secondary
   invariants is found;
5. the command line, the results for $d = 2$, verification, and limits.

---

## 1. The problem

Let $X_1,\dots,X_d$ be $N\times N$ matrices and let $U(N)$ act by simultaneous
conjugation, $X_a \mapsto U^\dagger X_a U$. The gauge-invariant polynomials form a
graded ring $R = \mathbb C[X_1,\dots,X_d]^{U(N)}$, spanned by products of traces of
words $\operatorname{Tr}(X_{a_1}X_{a_2}\cdots)$. Its **Hilbert series**
(partition function) is

$$
Z(x_1,\dots,x_d) = \sum_{n_1,\dots,n_d\ge 0} \dim R_{n_1,\dots,n_d}\; x_1^{n_1}\cdots x_d^{n_d},
$$

where $R_{n_1,\dots,n_d}$ is the space of invariants of degree $n_a$ in $X_a$.
Setting all $x_a = x$ gives the singly graded series
$Z(x) = \sum_n \dim R_n\, x^n$, graded by total degree.

### Molien–Weyl formula

Averaging over the group with the Weyl integration formula reduces the integral
to the maximal torus. In the simple-root coordinates $t_1,\dots,t_{N-1}$ of
$SU(N)$, the positive roots of $A_{N-1}$ are the consecutive products
$t^{\alpha_{k,r}} = t_k t_{k+1}\cdots t_r$ for $1 \le k \le r \le N-1$. The adjoint
representation has $N$ zero weights (the Cartan of $\mathfrak u(N)$) and the roots
$\pm\alpha$. Using the form that keeps only the positive roots, which absorbs
the $1/|W|$ factor:

$$
Z = \underbrace{\prod_{a=1}^d (1-x_a)^{-N}}_{Z_1^N}\;
\oint_{|t_j|=1} \prod_{j=1}^{N-1}\frac{dt_j}{2\pi i\, t_j}\;
\prod_{\alpha>0}\frac{1-t^{\alpha}}{\prod_{a=1}^d (1-x_a t^{\alpha})(1-x_a t^{-\alpha})}.
$$

In the all-equal version every $x_a$ is replaced by $x$, so each $x$-dependent
factor appears with multiplicity $d$.

---

## 2. Data model (Sections 1–2 of the code)

**Variables.** These are indexed $0,\dots,L-1$ with $L=(N-1)+n_x$. Indices
$0..N-2$ are $t_1..t_{N-1}$; indices $N-1..L-1$ are the weights. Here $n_x = d$ in
the general version and $n_x = 1$ in the all-equal version. A monomial is an
integer exponent tuple of length $L$.

**Term.** A term is

$$
c \cdot x^{\text{mono}} \cdot \prod_i (1 - x^{\text{key}_i})^{e_i},
$$

stored as `coef` (Python int), `mono` (tuple) and `facs`, a dict mapping key to
a signed exponent ($e_i<0$ means a denominator factor). The whole integrand is
a dict `(mono, sorted facs) -> coef`, so identical terms merge automatically and
cancellations happen as soon as they occur.

**Canonical keys** (`canon`). We have $1-x^{-m} = -x^{-m}(1-x^{m})$. Each binomial is
therefore stored with its exponent normalised so that the first nonzero entry
is positive; the sign and the monomial $x^{-m}$ move into `coef` and `mono`.
Because the $t$'s come first, a binomial that involves the current integration
variable $t_j$ always has exponent exactly $+1$ on $t_j$ and none on the earlier
$t$'s. `check_leading` asserts this.

| function | role |
|---|---|
| `vadd`, `vscale`, `vneg`, `vzero_at` | exponent-vector arithmetic |
| `gen_binom(e, q)` | $\binom{e}{q}$ for any integer $e$, including negative $e$ (needed for denominator expansions) |
| `insert_factor` | multiplies a term by $(1-x^m)^e$, canonicalising and merging exponents under one key; returns `None` if a numerator $(1-1)$ kills the term |
| `freeze` | hashable form `(mono, sorted facs)` |
| `initial_state(N, nx, mult)` | the integrand as a single term: prefactor $1/(t_1\cdots t_{N-1})$, numerator $\prod(1-t^\alpha)$, denominators $(1-x t^{\pm\alpha})^{-\text{mult}}$ |

---

## 3. Iterated residues (Sections 3–4)

The $t_j$ are integrated one at a time ($j = 1,\dots,N-1$). For each term, the
integral over $|t_j|=1$ is the sum of residues at the poles inside the circle.

### 3.1 Which poles are inside? (`PoleClassifier`, `find_poles`)

A denominator $(1-t_j r)$, where $r$ is a monomial in the later variables, has
its pole at $t_j = r^{-1}$. The classifier evaluates at $x_i = 1/q_i$ with
$q_i$ distinct primes (`first_primes`):

* **The $x$-part of $r$ is nonzero.** Then $|r^{-1}| = \prod q_i^{\pm r_i}$. Unique
  factorisation guarantees this is never exactly $1$. The pole is inside iff the
  modulus is $< 1$.
* **The $x$-part is zero (a "neutral" pole).** Its modulus is $1$ up to the later
  $t$'s. The later radii are $e^{-\eta_s}$ with $\eta_1 \gg \eta_2 \gg \dots > 0$
  infinitesimal, and the current radius $e^{-\eta_j}$ dominates the later ones,
  so the pole is **outside**. Shrinking the contours by an infinitesimal amount
  is allowed because the integrand is analytic in a thin annulus around the
  unit torus.

A negative power of $t_j$ in the prefactor gives a pole at $t_j = 0$.

### 3.2 Residue of one term at one pole (`residues`)

At a pole of order $\mu$ from $(1-t r)^{-\mu}$, write
$(1-tr)^{-\mu} = (-1)^\mu r^{-\mu}(t-p)^{-\mu}$ with $p = r^{-1}$. The residue is
$(-1)^\mu r^{-\mu}$ times the coefficient of $s^{\mu-1}$, with $s = t-p$, in the
product of all the other $t$-dependent factors. Each such factor is expanded
around $t = p$ as a **slot**: a list of options `(q, coefficient, monomial shift, factor update)`.

* `prefactor_slot`: $t^k = \sum_q \binom{k}{q} p^{k-q} s^q$.
* `factor_slot`: $(1-(p+s)R)^e = A^e (1 - sR/A)^e$ with $A = 1-pR$, so
  $= \sum_q \binom{e}{q}(-1)^q R^q A^{e-q} s^q$. The new binomial $A$ (exponent
  $p+R$) stays as a factor with exponent $e-q$; canonicalising it may flip a sign.
  If $A$ would be $1-1$, a factor coincides with the pole and an
  `ArithmeticError` is raised (this does not happen for these integrands).
* `factor_slot_at_zero`: the same expansion at $t=0$, used for the $t^{-\mu}$ pole.

`distribute(slots, n, L)` enumerates every choice of one option per slot with
$\sum q = n = \mu-1$. It prunes with suffix sums of the maximal $q$ per slot.
Each choice yields one new term. $t_j$-free factors are copied unchanged.

### 3.3 One integration step (`integrate_variable`)

For every term, every pole inside is found, its residue terms are generated, and
they are merged into a new dict (zero coefficients are dropped). Terms are
independent, so with `workers > 1` the term list is split into
`workers * CHUNKS_PER_WORKER` chunks. The chunks are processed in a
`ProcessPoolExecutor`, and each partial result is merged as soon as it
completes (`as_completed`) and then released. Processes are used because the
work is pure Python, which threads would serialise under the GIL. Lists shorter
than `MIN_PARALLEL_TERMS` stay serial.

---

## 4. Final assembly (Section 5, `assemble`)

After $N-1$ steps no $t$ remains. Each term is now $c\,x^{s}\prod(1-x^{v})^{e}$ in the
weights only, and is multiplied by $Z_1^N$. To add the terms exactly:

1. **Factor every binomial once.** $1-x^{v} = x^{-v^-}(x^{v^-}-x^{v^+})$, and the
   polynomial in brackets is split into irreducible factors with
   `sympy.factor_list` and cached. In one variable these are cyclotomic
   polynomials. Exponents of the same irreducible factor are added across the
   numerator and denominator of each term, so for example $(1-x^2)/(1-x)$ cancels to $1+x$.
2. **Least common denominator.** For each irreducible $g$, `dmax[g]` is the
   largest power with which it appears in any denominator.
3. **Sum the numerators** (`_numerator_task`). Each term becomes
   $c\,x^{s-s_{\min}}\prod_g g^{\,\text{net}_g+\text{dmax}_g}$. Terms sharing the
   same multiplier are grouped so that each distinct product of $g$'s is formed
   once. The sum is computed in SymPy's sparse integer polynomial ring, in
   parallel chunks if a pool is available.
4. **Cancel.** Common factors of numerator and denominator are removed by
   exact division (`exact_div`, a heap-based multivariate long division), and
   the monomial content is stripped.

The result is returned as `(monomial, numerator, denominator)`, a fraction in
lowest terms.

### Driver (Section 6, `hilbert_series`)

```python
hilbert_series(N, d, equal_x=False, workers=1, verbose=False)
```

* `equal_x=False`: returns `(Z(x1..xd), Z(x))`. The second entry is obtained
  by substituting $x_a = x$ (it is `None` for $d = 1$).
* `equal_x=True`: integrates directly with all weights equal and returns
  `(None, Z(x))`. This is much faster and is all the Hironaka analysis needs.
* `workers`: `1` = serial, `k` = pool of `k` processes, `0` = all cores.

---

## 5. Hironaka form (Section 7)

### 5.1 Definitions: $D$, $d_i$, $m_i$, $P(1)$

$R$ is the ring of invariants of a reductive group acting on a vector space.
By the Hochster–Roberts theorem it is **Cohen–Macaulay**. This means that there
exist:

* **primary invariants** $\theta_1,\dots,\theta_D$: homogeneous and algebraically
  independent, a *homogeneous system of parameters* (hsop), and
* **secondary invariants** $\eta_1 = 1, \eta_2, \dots, \eta_S$,

such that every invariant can be written *uniquely* as
$\sum_k \eta_k\, f_k(\theta_1,\dots,\theta_D)$ with polynomials $f_k$. In other
words, $R$ is a free module over $\mathbb C[\theta_1,\dots,\theta_D]$ with basis
$\eta_1,\dots,\eta_S$. Counting dimensions degree by degree gives the
**Hironaka form**

$$
Z(x) = \frac{P(x)}{\prod_i (1-x^{d_i})^{m_i}}, \qquad P(x) = \sum_{k=1}^S x^{\deg \eta_k}.
$$

* **$d_i$ and $m_i$.** The primary invariants are grouped by degree: $m_i$ of
  them have degree $d_i$. The factor $1/(1-x^{d_i})^{m_i}$ counts the polynomials
  in those $m_i$ primaries. In the CLI output `1^2 2^3 3^4` means
  $(1-x)^2(1-x^2)^3(1-x^3)^4$, i.e. two primaries of degree 1, three of degree 2,
  four of degree 3. The quantity $\prod_i d_i^{m_i}$ is the product of the
  degrees of all primary invariants. For $1^2\,2^3\,3^4$ it is
  $1^2\cdot 2^3\cdot 3^4 = 648$.
* **$D = \sum_i m_i$** is the number of primary invariants. Every hsop has the
  same length, the **Krull dimension** of $R$, which is the dimension of the
  space of orbits:
  $D = dN^2 - (N^2-1) = (d-1)N^2+1$. Analytically, $D$ is the order of the
  pole of $Z(x)$ at $x = 1$, and the code reads it off as the exponent of
  $\Phi_1 = x-1$ in the reduced denominator.
* **$P(x)$** is the numerator. The coefficient of $x^k$ is the number of
  secondary invariants of degree $k$, so all coefficients are non-negative.
* **$P(1)$** is the sum of the coefficients, i.e. the **total number of
  secondary invariants $S$, including the trivial one $\eta_1 = 1$**. The
  "non-trivial" count is $P(1)-1$.

### 5.2 Why $P(1)$ depends on the choice: $P(1) = e\prod_i d_i^{m_i}$

Write $1-x^{d} = (1-x)(1+x+\dots+x^{d-1})$. Then
$\prod_i (1-x^{d_i})^{m_i} = (1-x)^D \prod_i (1+\dots+x^{d_i-1})^{m_i}$, so

$$
(1-x)^D Z(x) = \frac{P(x)}{\prod_i (1+x+\dots+x^{d_i-1})^{m_i}}
\;\xrightarrow{x\to1}\; e = \frac{P(1)}{\prod_i d_i^{m_i}}.
$$

The number $e = \lim_{x\to1}(1-x)^D Z(x)$ (the *degree* or multiplicity of $R$)
depends only on $Z$, not on the primaries. Hence

$$
\boxed{\;P(1) = e \cdot \prod_i d_i^{m_i}\;}
$$

The number of secondaries is proportional to the product of the primary
degrees. Picking primaries of higher degree inflates the secondary count by
exactly the ratio of the products. This is what happened between versions 1 and 2 of
arXiv:2503.20097: one $(1-x^6)$ replaced by $(1-x^8)$ multiplies $P(1)$ by $8/6$,
turning 48 into 64 for $N=4$ and 11,568 into 15,424 for $N=5$.

### 5.3 Fewest primary and fewest secondary invariants

* **Primary invariants.** The number is always $D = (d-1)N^2+1$. Every hsop
  has exactly $D$ elements, so there is nothing to minimise.
  (This is different from a *minimal generating set* of the algebra, which is
  usually much larger and is also not determined by $Z$.)
* **Secondary invariants.** $S = P(1) = e\prod d_i^{m_i}$, so minimising $S$
  means minimising the product of the primary degrees over all hsops that
  actually exist.

### 5.4 Does the Molien–Weyl integral give that directly? No.

The integral produces the *function* $Z(x)$, a unique rational function. It
says nothing about which sets of invariants are algebraically independent.
Every expression $P(x)/\prod(1-x^{d_i})^{m_i}$ equal to $Z(x)$ is equally
"produced" by the integral, and there are infinitely many of them:

* The lowest-terms fraction that the integral naturally gives is generally
  **not** of Hironaka form. For $N=3$, $d=2$ it is
  $\dfrac{1-x^2+x^4}{(1-x)^2(1-x^2)^4(1-x^3)^4}$, with a negative coefficient.
  The Hironaka form $\dfrac{1+x^6}{(1-x)^2(1-x^2)^3(1-x^3)^4(1-x^4)}$ is obtained by
  multiplying the numerator and denominator by $1+x^2$.
* For a given $Z$ there are usually several degree choices with non-negative
  numerators. For $N=4$, $d=2$ they include $P(1) = 40, 48, 50, 56, 60, 60, 64,\dots$.

What the Hilbert series *can* give is a **lower bound**. If an hsop with
degrees $\{d_i^{m_i}\}$ exists, the resulting numerator must satisfy

$$
0 \le P_k \le h_k \quad\text{for all }k, \qquad h_k = \dim R_k,
$$

because $P_k$ counts secondaries of degree $k$, and these are linearly
independent elements of $R_k$. The code calls a degree choice **admissible** if
it satisfies this. The smallest $P(1)$ over admissible choices is therefore
$\le$ the true minimum number of secondaries. It *equals* the true minimum
precisely when invariants of those degrees forming an hsop exist.

To certify a choice you would need actual invariants. By Hilbert's criterion,
homogeneous invariants $\theta_1..\theta_D$ form an hsop iff their common zero
set in $(\mathrm{Mat}_N)^d$ is the **nullcone**. Here the nullcone is the set of
tuples with all $\operatorname{Tr}(\text{word}) = 0$, equivalently tuples that
are simultaneously strictly upper triangular after a change of basis. Checking
this needs a Gröbner-basis or dimension computation, e.g. in Macaulay2 or
Singular, which is outside this code.

### 5.5 The code

All polynomials in this section are dense integer coefficient lists, lowest
degree first, so everything is exact.

| function / class | what it does |
|---|---|
| `cyclotomic_exponents(den, x)` | factors the reduced denominator as $\pm\prod_k \Phi_k(x)^{a_k}$ and returns `{k: a_k}`; $a_1 = D$ |
| `ReducedSeries(Z)` | lowest-terms numerator and denominator coefficients, `a`, `krull_dim` $=D$, and `e`. Since $\Phi_k(1) = p$ for $k=p^j$ and $1$ otherwise ($k>1$), $e = \lvert\text{num}(1)\rvert / \prod_{k>1}\Phi_k(1)^{a_k}$. `series(n)` gives $h_0..h_n$ by power-series division; `numerator_for(degrees)` gives $P = \text{num}\cdot\prod(1-x^{d})^m / \text{den}$ by exact division |
| `covers(degrees, a)` | $\prod(1-x^{d_i})^{m_i}$ is divisible by the reduced denominator iff for every $k$ at least $a_k$ of the degrees are multiples of $k$ (as $1-x^d = \prod_{k\mid d}\Phi_k$), and there are exactly $D$ degrees |
| `HironakaForm` | `degrees` $\{d_i: m_i\}$, `numerator` $P$; properties `krull_dim` ($D$), `secondaries` ($P(1)$), `nonnegative`, `palindromic`, `degree_sum` ($\sum d_i m_i$), `series(n)`, pretty printers |
| `admissible(hf, h)` | $0 \le P_k \le h_k$ for all $k$ |
| `hironaka_form(Z, degrees=None)` | Hironaka form for given degrees (validated by exact division), or by default the admissible choice with the smallest $P(1)$ |
| `hironaka_candidates(Z, max_secondaries=None)` | all admissible choices with $P(1) \le$ bound, sorted by $(P(1), \sum d_i m_i)$; with no bound, the bound starts at 4 and is multiplied by 4 until something is found |
| `PAPER_DEGREES_D2` | the denominators used in arXiv:2503.20097 for $d = 2$, $N \le 7$ |
| `free_trace_series(d, n)` | the $N\to\infty$ series $\prod_k (1-x^k)^{-c_k}$, with $c_k = \frac1k\sum_{m\mid k}\varphi(m)d^{k/m}$ the number of single traces of length $k$ (necklaces) |
| `tabulate(Ns, d)` | per $N$: a "paper" row (if available) and a "min P(1)" row with numerator, $P(1)$, $e$, and the first degree where $Z_N$ differs from $Z_\infty$ |

### 5.6 The search in `hironaka_candidates`, and why it is exhaustive

Choose the degrees in increasing order $k = 1, 2, \dots$ and let $P^{(k)}$ be the
running product $Z(x)\prod_{d<k}(1-x^d)^{m_d}$.

1. Factors $(1-x^{d})$ with $d \ge k$ do not change the coefficients of
   $x^0..x^{k-1}$. Those coefficients of the final $P$ are therefore already fixed;
   they were checked non-negative at earlier steps.
2. Adding $m$ factors of degree $k$ changes the coefficient of $x^k$ to
   $P^{(k)}_k - m$ (because $P_0 = 1$). Non-negativity forces $m \le P^{(k)}_k$.
3. With $\ell$ slots left, every remaining degree is $\ge k$, so
   $P(1) = e\prod d_i^{m_i} \ge e\cdot(\text{product so far})\cdot k^{\ell}$. Branches
   exceeding the bound are cut. This also caps the largest degree that can
   occur, so no degree limit is imposed by hand. The coefficient arrays are
   extended on demand (`rebuild`).
4. At the leaves, `covers` (is $P$ a polynomial?) and `admissible` are checked
   on the exact numerator.

Every admissible choice with $P(1) \le$ bound survives all the cuts, so the
first entry returned is the admissible minimum.

---

## 6. Command line

```bash
# interactive prompts (as in the original script)
python3 hilbert_series.py

# one N; Hironaka form with the fewest (admissible) secondaries
python3 hilbert_series.py --N 4 --d 2
python3 hilbert_series.py --N 4 --choice paper            # the paper's denominator
python3 hilbert_series.py --N 4 --degrees 1:2,2:3,3:4,4:6,6:1,8:1
python3 hilbert_series.py --N 4 --candidates 8             # list alternatives
python3 hilbert_series.py --N 3 --d 2 --graded             # also the x1, x2 series

# table over N, optionally saved as JSON with the full numerators
python3 hilbert_series.py --table 1 6 --workers 0 --json d2.json
```

Each JSON row contains `N, d, source, denominator, krull_dim, numerator`
(coefficient list), `numerator_degree, secondaries_P1, nontrivial_secondaries,
nonnegative, palindromic, e, agrees_with_free_below, seconds`.

---

## 7. Results for $d = 2$

| $N$ | $D$ | $e$ | paper denominator | paper $P(1)$ | fewest admissible $P(1)$ | its denominator |
|---|---|---|---|---|---|---|
| 1 | 2 | 1 | $1^2$ | 1 | 1 | same |
| 2 | 5 | 1/8 | $1^2 2^3$ | 1 | 1 | same |
| 3 | 10 | 1/1296 | $1^2 2^3 3^4 4$ | 2 | 2 | same |
| 4 | 17 | 1/1990656 | $1^2 2^3 3^4 4^6 6^2$ | 48 | **40** | $1^2 2^3 3^4 4^6 5\,6$ |
| 5 | 26 | 241/6718464000000 | $1^2 2^3 3^4 4^6 5^6 6^5$ | 11,568 | **9,640** | $1^2 2^3 3^4 4^6 5^7 6^4$ |
| 6 | 37 | 53/185752092672000000 | $1^2 2^3 3^4 4^6 5^7 6^9 8^6$ | 156,303,360 | **54,950,400** | $1^2 2^3 3^4 4^6 5^8 6^{11} 8^3$ |

($P(1)$ includes the trivial secondary; subtract 1 for the non-trivial count.)
For $N \le 3$ the paper's choice is already the minimum. The same holds for
$d = 3$, $N = 3$: the default output is the paper's eq. (3.44),
$(1-x)^3(1-x^2)^6(1-x^3)^8(1-x^4)^2$ with $P(1) = 252$ (251 non-trivial). For $N = 4, 5, 6$ the
admissible minimum is smaller. As explained in §5.4, it is a lower bound that
is attained only if primary invariants of those degrees exist.

For every $N$, $Z_N$ agrees with $Z_\infty$ (free traces) exactly through degree
$N$ and first differs at degree $N+1$, where the trace relations start.

### The discrepancies in arXiv:2503.20097

* Version 1 (Mar 2025): text and Table 3 both say 63, 15,423, 312,606,719.
* Version 2 (Aug 2025): Table 3 was changed to 48, 11,567, 156,303,360. The body
  text of §3.4 was left unchanged, including "2016 relations", which equals
  $63\cdot64/2$, the number of products of pairs of 63 secondaries.
* The v2 table mixes conventions: 48 and 156,303,360 are $P(1)$, while 11,567 and
  21,739,438,196,735 are $P(1)-1$.
* The v1 values are $P(1)-1$ for *other* denominators: $64 = 48\cdot\tfrac86$ and
  $15{,}424 = 11{,}568\cdot\tfrac86$ (one degree 6 replaced by 8), and
  $312{,}606{,}720 = 2\cdot 156{,}303{,}360$ (any one degree $d$ replaced by $2d$).
  This is an instance of $P(1) = e\prod d_i^{m_i}$.

---

## 8. Verification

* $N=4$: the series matches an independent brute-force constant-term
  evaluation of the Weyl integral through degree 10.
* With the paper's denominators, the numerators for $N = 3, 4, 5, 6$ agree
  coefficient by coefficient with eqs. (3.40), (3.47), (3.49), (3.52).
* The multigraded and all-equal versions agree, e.g. for $(N, d) = (3, 3)$, and
  serial and parallel runs agree.

## 9. Performance and limits

| $d=2$ | time (all-equal version) |
|---|---|
| $N \le 4$ | < 1 s |
| $N = 5$ | ~5 s |
| $N = 6$ | ~6 min on 4 cores |
| $N = 7$ | does not fit in 16 GB of RAM |

For $N = 7$ the fourth residue step blows up: a single chunk of about 4,000
terms produced more than 10 GB of residue terms in one worker. Reaching
$N \ge 7$ needs either much more memory or a different algorithm.

Small notes on the original code:

* `insert_factor` can return `None`, which `initial_state` would try to
  unpack. This cannot happen for these integrands because no zero exponent
  vector occurs.
* The original driver applied `sympy.factor` to the numerator. This is
  harmless but slow for large numerators, and it hides the Hironaka structure,
  which Section 7 reconstructs.
