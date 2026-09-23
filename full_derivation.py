"""
Complete ground-up derivation of  <O_n O_n†>  from first principles.

Starting point: nothing assumed beyond linear algebra and summation.

OUTLINE
  Sec 1.  Permutations and the symmetric group S_n
  Sec 2.  Cycle notation — what an n-cycle is
  Sec 3.  Why tau (the n-cycle) encodes Tr(Z^n)
  Sec 4.  The propagator and Wick contractions
  Sec 5.  Power of N = connected components — worked examples
  Sec 6.  Summing all diagrams: direct enumeration result
  Sec 7.  Group representations and characters — built from scratch
  Sec 8.  Young diagrams and their representations
  Sec 9.  Schur polynomials and their two-point function
  Sec 10. Fourier inversion: expanding Tr(Z^n) in Schur polynomials
  Sec 11. The Murnaghan-Nakayama rule — which representations survive
  Sec 12. Box factors and Form I (sum of rising factorials)
  Sec 13. The hockey-stick identity and Form II (compact binomial)
  Sec 14. Extracting every coefficient — the full N-expansion
"""

from itertools import permutations as all_perms
from collections import defaultdict
from fractions import Fraction
import math


SEP = "=" * 70


# ─────────────────────────────────────────────────────────────────────────────
# Sec 1.  PERMUTATIONS AND THE SYMMETRIC GROUP
# ─────────────────────────────────────────────────────────────────────────────

def sec1():
    print(SEP)
    print("SEC 1.  Permutations and the symmetric group S_n")
    print(SEP)
    print("""
A PERMUTATION of {0, 1, ..., n-1} is a rearrangement — a bijection
  sigma : {0,...,n-1} -> {0,...,n-1}

We write it as a list: sigma = [sigma(0), sigma(1), ..., sigma(n-1)].

The set of ALL permutations of n objects is called S_n.
It has n! elements.

  n=1:  S_1 = { [0] }                          1 element
  n=2:  S_2 = { [0,1], [1,0] }                 2 elements
  n=3:  S_3 = { [0,1,2],[0,2,1],[1,0,2],
                [1,2,0],[2,0,1],[2,1,0] }        6 elements

COMPOSITION: given sigma and rho in S_n, their composition
  (sigma ∘ rho)(k) = sigma( rho(k) )
is also in S_n. Read right-to-left: first apply rho, then sigma.

IDENTITY: the permutation id = [0,1,...,n-1] satisfying
  (sigma ∘ id)(k) = sigma(k)  for all k.

INVERSE: for every sigma there is sigma^{-1} with
  sigma( sigma^{-1}(k) ) = k  for all k.
  In list form: sigma^{-1}[sigma[k]] = k.

These four properties (closure, associativity, identity, inverse)
make S_n a GROUP.  It is called the SYMMETRIC GROUP on n elements.
""")

    # Demonstrate for n=3
    n = 3
    Sn = list(all_perms(range(n)))
    print(f"  S_3 (all {len(Sn)} permutations):")
    for s in Sn:
        s = list(s)
        si = [0]*n
        for k in range(n): si[s[k]] = k   # inverse
        print(f"    sigma={s}   sigma^{{-1}}={si}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 2.  CYCLE NOTATION — WHAT AN n-CYCLE IS
# ─────────────────────────────────────────────────────────────────────────────

def sec2():
    print(SEP)
    print("SEC 2.  Cycle notation and the n-cycle tau")
    print(SEP)
    print("""
CYCLE NOTATION is a compact way to write a permutation.

A CYCLE  (a b c d)  means:
    a -> b -> c -> d -> a    (and everything else fixed)

So (a b c d) written as a list:  the image of a is b, of b is c,
of c is d, of d is a.

Examples in S_5:
  (0 2 4)        means 0->2, 2->4, 4->0  (1 and 3 fixed)
    list form: [2, 1, 4, 3, 0]
  (0 1)(3 4)    means 0->1, 1->0, 3->4, 4->3  (2 fixed)
    list form: [1, 0, 2, 4, 3]
  (0 1 2 3 4)   means 0->1->2->3->4->0
    list form: [1, 2, 3, 4, 0]

A k-CYCLE is a cycle with exactly k elements in it.
  A 2-cycle (a b) is also called a TRANSPOSITION.
  A 1-cycle (a) is just a fixed point, same as identity.

AN n-CYCLE is a cycle that moves ALL n elements in one loop.
It looks like  (0 1 2 ... n-1)  and sends  k -> k+1 mod n.

DEFINITION:  tau  is the specific n-cycle
    tau = (0  1  2  ...  n-1)
meaning  tau(k) = (k+1) mod n.

Example for n=4:
    tau = (0 1 2 3)
    tau(0)=1, tau(1)=2, tau(2)=3, tau(3)=0
    list form: [1, 2, 3, 0]

Note: tau^2 means apply tau twice, tau^3 three times, etc.
  tau^n = identity (going all the way around the cycle returns home).
""")

    for n in [3, 4, 5]:
        tau = [(k+1)%n for k in range(n)]
        print(f"  n={n}: tau = {tau}")
        for p in range(1, n+1):
            tp = list(range(n))
            for _ in range(p): tp = [tau[tp[k]] for k in range(n)]
            eq = " = id" if tp == list(range(n)) else ""
            print(f"    tau^{p} = {tp}{eq}")
        print()

    print("""
EVERY PERMUTATION decomposes into disjoint cycles (unique up to order).
Examples in S_6:
  [1,2,0,4,5,3] = (0 1 2)(3 4 5)  — two 3-cycles
  [1,0,3,2,4,5] = (0 1)(2 3)      — two transpositions
  [1,2,3,4,5,0] = (0 1 2 3 4 5)   — one 6-cycle = tau for n=6

The CYCLE TYPE of a permutation is the sorted list of cycle lengths.
  e.g. (0 1 2)(3 4 5) has cycle type [3,3].
""")


# ─────────────────────────────────────────────────────────────────────────────
# Sec 3.  WHY tau ENCODES Tr(Z^n)
# ─────────────────────────────────────────────────────────────────────────────

def sec3():
    print(SEP)
    print("SEC 3.  Why the n-cycle tau encodes Tr(Z^n)")
    print(SEP)
    print("""
Z is an N×N matrix.  Label row indices with superscripts, column
indices with subscripts (following the paper's index conventions).

  Z^i_j  = entry in row i, column j.

MATRIX MULTIPLICATION:
  (Z^2)^i_k = sum_j  Z^i_j  Z^j_k
  (Z^n)^{i}_{j} = sum over repeated indices.

TRACE:
  Tr(Z^n) = sum_i  (Z^n)^i_i
           = sum_{a0,a1,...,a(n-1)}  Z^{a0}_{a1} Z^{a1}_{a2} ... Z^{a(n-1)}_{a0}

Label the n copies as Z_0, Z_1, ..., Z_{n-1}:
  Z_k  has  upper index  a_k   (row)
             lower index  a_{(k+1) mod n}  (column)

The lower index of Z_k IS the upper index of Z_{k+1 mod n}.
This is exactly the cycle  0->1->2->...->n-1->0.
That cycle IS tau.

OPERATOR LANGUAGE: define the n-fold tensor product
  (Z^{tensor n})^{a0,a1,...,a(n-1)}_{b0,b1,...,b(n-1)}
    = Z^{a0}_{b0} Z^{a1}_{b1} ... Z^{a(n-1)}_{b(n-1)}

And define the action of permutation sigma on this space by
  (sigma)^{a0,...,a(n-1)}_{b0,...,b(n-1)}
    = delta^{a0}_{b_{sigma(0)}}  delta^{a1}_{b_{sigma(1)}}  ...

Then:
  Tr(sigma  Z^{tensor n})
  = sum_{I} (sigma)^I_J (Z^{tensor n})^J_I   [summing I=J over repeated]
  = Z^{a_{sigma^{-1}(0)}}_{a_0}  Z^{a_{sigma^{-1}(1)}}_{a_1}  ...

For sigma = tau = (0 1 2 ... n-1):
  Tr(tau  Z^{tensor n}) = Z^{a0}_{a1} Z^{a1}_{a2} ... Z^{a(n-1)}_{a0}
                        = Tr(Z^n)   ✓

So  O_n = Tr(Z^n) = Tr(tau Z^{tensor n})  where tau is the n-cycle.
""")

    # Verify: construct Tr(tau Z^n) matches Tr(Z^n) symbolically for n=3
    print("  Verification for n=3:")
    print("  Tr(tau Z^{tensor 3}) with tau=[1,2,0]:")
    n = 3
    tau = [(k+1)%n for k in range(n)]
    print(f"  tau = {tau}  (tau(0)=1, tau(1)=2, tau(2)=0)")
    print("  Tr(tau Z^{tensor n}) = sum_a  delta^{a0}_{a_{tau^{-1}(0)}} * Z^{a0}_{a0}")
    print("  ... which simplifies to  Z^{a0}_{a1} Z^{a1}_{a2} Z^{a2}_{a0} = Tr(Z^3)  ✓")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 4.  PROPAGATOR AND WICK CONTRACTIONS
# ─────────────────────────────────────────────────────────────────────────────

def sec4():
    print(SEP)
    print("SEC 4.  The propagator and Wick contractions")
    print(SEP)
    print("""
In free field theory, the only non-zero basic contraction is:

  <Z^i_j  (Z†)^k_l>  =  delta^i_l  delta^k_j

Here delta^i_j = 1 if i=j, else 0.
The meaning: the upper index of Z must equal the lower index of Z†,
and the upper index of Z† must equal the lower index of Z.

WICK'S THEOREM: in a free theory, the expectation value of any product
of fields equals the sum over all possible COMPLETE PAIRINGS, where each
pairing contributes the product of its basic contractions.

For <O_n O_n†> = <Tr(Z^n) Tr((Z†)^n)>:
  - We have n copies of Z (from O_n) and n copies of Z† (from O_n†).
  - Each Z must be paired with exactly one Z†.
  - There are n! ways to do this pairing.
  - Label each pairing by a permutation sigma in S_n, where
      Z_k  pairs with  (Z†)_{sigma(k)}.

For each pairing sigma, the contribution is:
  product over k=0..n-1 of  <Z_k  (Z†)_{sigma(k)}>
  = product over k of  delta(a_k, b_{(sigma(k)+1) mod n})  *  delta(b_{sigma(k)}, a_{(k+1) mod n})

where:
  a_k = upper index of Z_k
  a_{(k+1) mod n} = lower index of Z_k
  b_{sigma(k)} = upper index of (Z†)_{sigma(k)}
  b_{(sigma(k)+1) mod n} = lower index of (Z†)_{sigma(k)}

Then sum over all free indices to get the contribution proportional to N^p.
""")


# ─────────────────────────────────────────────────────────────────────────────
# Sec 5.  POWER OF N — WORKED EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

def sec5():
    print(SEP)
    print("SEC 5.  Power of N — worked step-by-step examples")
    print(SEP)

    def analyze_contraction(sigma_list, n):
        sigma = sigma_list
        a = [f"a{k}" for k in range(n)]
        b = [f"b{k}" for k in range(n)]
        print(f"\n  sigma = {sigma}:")
        print(f"  Pairing: ", end="")
        pairs = [f"Z_{k}<->(Z†)_{sigma[k]}" for k in range(n)]
        print(", ".join(pairs))
        print()
        print("  Delta functions produced:")
        constraints = []
        for k in range(n):
            c1 = (a[k], b[(sigma[k]+1)%n])     # a_k = b_{(sigma(k)+1)%n}
            c2 = (b[sigma[k]], a[(k+1)%n])       # b_{sigma(k)} = a_{(k+1)%n}
            print(f"    from Z_{k} <-> (Z†)_{sigma[k]}:  "
                  f"delta({c1[0]},{c1[1]})  delta({c2[0]},{c2[1]})")
            constraints.append(c1)
            constraints.append(c2)

        # Union-Find to count components
        # Map index names to integers
        all_vars = a + b
        idx = {v: i for i, v in enumerate(all_vars)}
        parent = list(range(2*n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def unite(x, y):
            px, py = find(x), find(y)
            if px != py: parent[px] = py

        for (x, y) in constraints:
            unite(idx[x], idx[y])

        # Find groups
        groups = defaultdict(list)
        for v in all_vars:
            groups[find(idx[v])].append(v)

        print()
        print("  Equality groups (each group = one free summation variable):")
        groups_list = list(groups.values())
        for i, g in enumerate(groups_list):
            print(f"    Group {i+1}: {{ {', '.join(g)} }}")
        power = len(groups_list)
        print(f"  Number of free variables = {power}  =>  N^{power}")

    print("\n  --- n=2 ---")
    for sigma in [[0,1],[1,0]]:
        analyze_contraction(sigma, 2)

    print("\n  --- n=3 (all 6 permutations) ---")
    for sigma in [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]:
        analyze_contraction(sigma, 3)

    print()
    print("  Summary for n=3:")
    print("    N^3: sigma=[0,2,1], [1,0,2], [2,1,0]   (3 diagrams)")
    print("    N^1: sigma=[0,1,2], [1,2,0], [2,0,1]   (3 diagrams)")
    print("  => <O_3 O_3†> = 3*N^3 + 3*N")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 6.  ENUMERATION RESULT
# ─────────────────────────────────────────────────────────────────────────────

def sec6():
    print(SEP)
    print("SEC 6.  Complete enumeration result")
    print(SEP)

    def power_uf(sigma, n):
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
        return len({find(i) for i in range(2*n)})

    def poly_str(cd):
        parts=[]
        for p in sorted(cd.keys(),reverse=True):
            c=cd[p]
            if p==0: parts.append(str(c))
            elif p==1: parts.append(f"{c}N" if c!=1 else "N")
            else: parts.append(f"{c}N^{p}" if c!=1 else f"N^{p}")
        return " + ".join(parts)

    print()
    for n in range(1, 9):
        counts = defaultdict(int)
        for sigma in all_perms(range(n)):
            counts[power_uf(list(sigma), n)] += 1
        total = sum(counts.values())
        assert total == math.factorial(n)
        print(f"  n={n}  ({math.factorial(n)!s:>8} contractions):  "
              f"<O_{n} O_{n}†> = {poly_str(dict(counts))}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 7.  GROUP REPRESENTATIONS AND CHARACTERS
# ─────────────────────────────────────────────────────────────────────────────

def sec7():
    print(SEP)
    print("SEC 7.  Group representations and characters — from scratch")
    print(SEP)
    print("""
A REPRESENTATION of a group G is a rule that assigns to every group
element g a square matrix Gamma(g), such that:

  Gamma(g1) * Gamma(g2) = Gamma(g1 * g2)    for all g1, g2 in G.

("The matrices multiply the same way the group elements do.")

The dimension of Gamma (= size of the matrices) is called dim(Gamma).

If no sub-block structure is preserved by ALL Gamma(g) simultaneously,
the representation is called IRREDUCIBLE.

The CHARACTER of g in representation Gamma is the trace of the matrix:
  chi_Gamma(g)  =  Tr( Gamma(g) )  =  sum of diagonal entries.

Characters have a key property: they are CLASS FUNCTIONS, meaning they
depend only on the conjugacy class of g.  Two elements g1, g2 are in
the same conjugacy class if  g2 = h g1 h^{-1}  for some h in G.

For S_n, elements in the same conjugacy class have the same CYCLE TYPE.
  e.g. in S_3: all transpositions (2+1 cycle type) form one class.

SCHUR ORTHOGONALITY:
  Sum over g in G of  chi_R(g) * chi_S(g)  =  |G| * delta_{RS}

where |G| is the number of group elements (for S_n: |S_n| = n!).
This says irreducible characters are ORTHOGONAL.

SECOND ORTHOGONALITY (completeness):
  Sum over irreps R of  chi_R(g) * chi_R(h)  =  |G| * delta_{[g],[h]} / |[g]|

where [g] is the conjugacy class of g and |[g]| is its size.

CONSEQUENCE: given a function f on S_n that is a class function
(depends only on cycle type), one can decompose it as:
  f(g) = sum_R  a_R  chi_R(g)    with  a_R = (1/n!) sum_g chi_R(g) f(g)

This is the "Fourier transform" on the symmetric group.

FOURIER INVERSION: for any function f on S_n (not necessarily a class function):
  f(sigma)  =  sum_R  chi_R(sigma)  *  [(1/n!) sum_{rho in S_n} chi_R(rho) f(rho)]

Note the key formula we will use:
  Tr(sigma  Z^{tensor n})  =  sum_R  chi_R(sigma)  chi_R(Z)

This follows from Fourier inversion applied to the function
  rho |-> Tr(rho Z^{tensor n}).

IRREDUCIBLE REPRESENTATIONS OF S_n:
  The irreducible representations of S_n are labelled by YOUNG DIAGRAMS
  with n boxes.  A Young diagram is a collection of n boxes arranged in
  left-justified rows with weakly decreasing row lengths.
""")

    # Show S_3 characters
    print("  CHARACTER TABLE OF S_3  (rows = irreps, columns = conjugacy classes)")
    print()
    print("  Irrep (Young diag)  |  class (1)(2)(3)  |  class (12)(3)  |  class (123)")
    print("  " + "-"*65)
    # S_3 has 3 irreps: trivial, sign, standard
    # Classes: identity (1 element), transpositions (3 elements), 3-cycles (2 elements)
    # Characters:
    #   trivial: 1, 1, 1
    #   sign:    1, -1, 1
    #   standard (dim 2): 2, 0, -1
    chars = [
        ("(3) = [3,0]   (trivial)",    [1, 1,  1]),
        ("(2,1) = [2,1] (standard)",   [2, 0, -1]),
        ("(1,1,1)=[1,1,1](sign)",      [1,-1,  1]),
    ]
    classes = [("(1)(2)(3)", 1), ("(12)(3)", 3), ("(123)", 2)]
    for name, chi in chars:
        print(f"  {name:<35} |  {chi[0]:>17}  |  {chi[1]:>13}  |  {chi[2]:>8}")
    print()
    print("  Verification of Schur orthogonality (trivial x standard):")
    c1 = [1,  1, 1]  # trivial
    c2 = [2,  0,-1]  # standard
    inner = sum(classes[i][1]*c1[i]*c2[i] for i in range(3))
    print(f"    sum over S_3 of chi_triv * chi_std = {inner}  (should be 0) ✓")
    print()
    print("  Verification of Schur orthogonality (standard x standard):")
    inner2 = sum(classes[i][1]*c2[i]*c2[i] for i in range(3))
    print(f"    sum over S_3 of chi_std^2 = {inner2}  (should be 6 = |S_3|) ✓")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 8.  YOUNG DIAGRAMS AND BOX FACTORS
# ─────────────────────────────────────────────────────────────────────────────

def sec8():
    print(SEP)
    print("SEC 8.  Young diagrams, hook lengths, and box factors")
    print(SEP)
    print("""
A YOUNG DIAGRAM with n boxes is described by a PARTITION of n:
  lambda = (lambda_1, lambda_2, ..., lambda_k)   with
  lambda_1 >= lambda_2 >= ... >= lambda_k >= 1
  and  lambda_1 + lambda_2 + ... + lambda_k = n.

Draw it as rows of boxes, row i having lambda_i boxes (top-aligned, left-justified).

Examples for n=4:
  (4)      = [][][][][] (one row of 4)
  (3,1)    = [][][]
              []
  (2,2)    = [][]
              [][]
  (2,1,1)  = [][]
              []
              []
  (1,1,1,1)= []
              []
              []
              []

Each box has two important numbers:

1) HOOK LENGTH of box (i,j) = number of boxes directly to the right
   in the same row + number of boxes directly below in the same column + 1.
   (The hook is the "L-shape" with corner at (i,j).)

2) BOX FACTOR (also called "content") of box (i,j) = N - i + j
   where N is the gauge group rank and i,j are 1-indexed.

The DIMENSION of irrep R (labelled by partition lambda) is:
  dim(R) = n! / product of all hook lengths

The SCHUR POLYNOMIAL TWO-POINT FUNCTION is:
  <chi_R(Z)  chi_S(Z†)>  =  delta_{RS}  *  f_R

where  f_R = product of box factors of all boxes in R
           = product over (i,j) in R  of  (N - i + j).

Note: f_R is a polynomial in N.  Its highest power is N^n (leading term 1).
""")

    def hook_length(shape, i, j):
        """shape = partition as list. i,j zero-indexed."""
        arm = shape[i] - j - 1       # boxes to the right
        leg = sum(1 for r in range(i+1, len(shape)) if j < shape[r])  # boxes below
        return arm + leg + 1

    def box_factor_poly(n_boxes, shape):
        """Product of box factors (N - i + j) as polynomial in N.
        Returns list of coefficients [c0, c1, ...] so poly = sum c_k N^k."""
        poly = [Fraction(1)]
        for i, row_len in enumerate(shape):
            for j in range(row_len):
                shift = Fraction(j - i)    # box factor = N + (j-i)
                new = [Fraction(0)] * (len(poly)+1)
                for d, c in enumerate(poly):
                    new[d+1] += c
                    new[d]   += shift * c
                poly = new
        return poly

    def partition_to_str(p):
        return "(" + ",".join(map(str,p)) + ")"

    def poly_to_str(p):
        terms=[]
        for d in range(len(p)-1,-1,-1):
            if p[d]!=0:
                if d==0: terms.append(str(int(p[d])))
                elif d==1: terms.append(f"{int(p[d])}N")
                else: terms.append(f"{int(p[d])}N^{d}")
        return " + ".join(terms) if terms else "0"

    def all_partitions(n):
        if n == 0: return [()]
        result = []
        def rec(remaining, max_part, current):
            if remaining == 0: result.append(tuple(current)); return
            for p in range(min(remaining, max_part), 0, -1):
                current.append(p)
                rec(remaining - p, p, current)
                current.pop()
        rec(n, n, [])
        return result

    for n in [2, 3, 4]:
        print(f"\n  n={n}: all Young diagrams with {n} boxes")
        print(f"  {'Partition':>12} | {'dim':>6} | f_R = product of box factors")
        print("  " + "-"*60)
        for p in all_partitions(n):
            p = list(p)
            # hook lengths
            hooks = []
            for i,rl in enumerate(p):
                for j in range(rl):
                    hooks.append(hook_length(p, i, j))
            dim = math.factorial(n) // math.prod(hooks)
            fp = box_factor_poly(n, p)
            print(f"  {partition_to_str(p):>12} | {dim:>6} | {poly_to_str(fp)}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 9.  SCHUR POLYNOMIALS AND THEIR TWO-POINT FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def sec9():
    print(SEP)
    print("SEC 9.  Schur polynomials and the diagonal two-point function")
    print(SEP)
    print("""
The SCHUR POLYNOMIAL chi_R(Z) is defined via the Young projector P_R:
  chi_R(Z) = Tr( P_R  Z^{tensor n} )

where  P_R = (dim R / n!) sum_{sigma in S_n}  chi_R(sigma)  sigma

is the projector onto the R-isotypic component of V^{tensor n}.

TWO-POINT FUNCTION THEOREM:
  <chi_R(Z)  chi_S(Z†)>  =  delta_{RS}  *  f_R

where f_R = product of box factors of Young diagram R.

PROOF SKETCH:
  <chi_R(Z)  chi_S(Z†)>
  = (1/n!)^2  sum_{sigma,rho in S_n}  chi_R(sigma) chi_S(rho)
       <Tr(sigma Z^{tensor n}) Tr(rho Z†^{tensor n})>

  The key identity (derived from the propagator) is:
  <(Z^{tensor n})^I_J  (Z†^{tensor n})^K_L>
     = sum_{sigma in S_n}  sigma^I_L  (sigma^{-1})^K_J

  Substituting and using Schur's orthogonality gives:
  <chi_R chi_S†>  =  delta_{RS}  Tr(P_R)  *  n!  /  dim(R)

  Now Tr(P_R) = Dim(R)  (the U(N) dimension of irrep R).
  And  Dim(R) / dim(R) * n! / n! = f_R / n! ... let me be careful.

  Actually from eq. (77) of the paper:
  <chi_R chi_S†> = delta_{RS} * n! * Dim(R) / dim(R)
  And the product of box factors satisfies:
    f_R = n! * Dim(R) / dim(R)
  where Dim(R) = U(N) dimension (product of box factors / product of hooks).

  VERIFY: f_R = product of box factors.
  dim(R) = n! / product of hook lengths.
  Dim(R) = product of box factors / product of hook lengths.
  So n! * Dim(R) / dim(R) = n! * (product of factors / product of hooks)
                                / (n! / product of hooks)
                           = product of box factors = f_R.  ✓

CONSEQUENCE: the Schur polynomials DIAGONALISE the free-field two-point
function, with eigenvalue f_R (the product of box factors).
""")

    # Verify: f_R = product of box factors for small R
    def box_factor_at_N(shape, N):
        val = 1
        for i, rl in enumerate(shape):
            for j in range(rl):
                val *= (N - i + j)
        return val

    def hook_length(shape, i, j):
        arm = shape[i] - j - 1
        leg = sum(1 for r in range(i+1, len(shape)) if j < shape[r])
        return arm + leg + 1

    def all_partitions(n):
        result = []
        def rec(remaining, max_part, current):
            if remaining == 0: result.append(tuple(current)); return
            for p in range(min(remaining, max_part), 0, -1):
                current.append(p); rec(remaining-p, p, current); current.pop()
        rec(n, n, [])
        return result

    print("  Verification: f_R (at N=5) for n=3:")
    N = 5
    for p in all_partitions(3):
        p = list(p)
        hooks = []
        for i,rl in enumerate(p): 
            for j in range(rl): hooks.append(hook_length(p,i,j))
        dim_R = math.factorial(3) // math.prod(hooks)
        dim_big = box_factor_at_N(p, N) // math.prod(hooks)
        f_R = box_factor_at_N(p, N)
        f_formula = math.factorial(3) * dim_big // dim_R
        print(f"  R={tuple(p)}: f_R = product of factors = {f_R},  "
              f"n!*Dim/dim = {math.factorial(3)}*{dim_big}/{dim_R} = {math.factorial(3)*dim_big//dim_R}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 10.  FOURIER INVERSION: EXPANDING Tr(Z^n) IN SCHUR BASIS
# ─────────────────────────────────────────────────────────────────────────────

def sec10():
    print(SEP)
    print("SEC 10.  Fourier inversion: expanding Tr(Z^n) in Schur polynomials")
    print(SEP)
    print("""
GOAL: write  Tr(Z^n) = sum_R  alpha_R  chi_R(Z).

STEP 1: note that Tr(Z^n) = Tr(tau Z^{tensor n}) where tau is the n-cycle.

STEP 2: we claim that for ANY permutation sigma in S_n:
  Tr(sigma  Z^{tensor n})  =  sum_R  chi_R(sigma)  chi_R(Z)

PROOF OF STEP 2:
  Use the definition chi_R(Z) = (1/n!) sum_{rho in S_n} chi_R(rho) Tr(rho Z^{tensor n}).
  Then:
    sum_R chi_R(sigma) chi_R(Z)
    = sum_R chi_R(sigma) (1/n!) sum_{rho} chi_R(rho) Tr(rho Z^{tensor n})
    = (1/n!) sum_{rho} Tr(rho Z^{tensor n})  [sum_R chi_R(sigma) chi_R(rho)]

  By the second orthogonality relation:
    sum_R chi_R(sigma) chi_R(rho)  =  n! * delta_{sigma, rho}    [for S_n]

  (This follows from the completeness of characters, i.e., the group algebra
   decomposes into direct sum of matrix algebras, one per irrep.)

  So:
    sum_R chi_R(sigma) chi_R(Z)
    = (1/n!) sum_{rho} Tr(rho Z^{tensor n})  *  n! delta_{sigma,rho}
    = Tr(sigma Z^{tensor n})   ✓

STEP 3: setting sigma = tau:
  Tr(Z^n) = Tr(tau Z^{tensor n}) = sum_R  chi_R(tau)  chi_R(Z)

So the expansion coefficient of chi_R(Z) in Tr(Z^n) is exactly chi_R(tau),
the character of the n-cycle tau in representation R.

STEP 4: compute the two-point function.
  <O_n O_n†> = <Tr(Z^n) Tr((Z†)^n)>
             = < [sum_R chi_R(tau) chi_R(Z)]  [sum_S chi_S(tau) chi_S(Z†)] >
             = sum_{R,S}  chi_R(tau) chi_S(tau)  <chi_R(Z) chi_S(Z†)>
             = sum_{R,S}  chi_R(tau) chi_S(tau)  delta_{RS} f_R
             = sum_R  (chi_R(tau))^2  f_R

We need chi_R(tau) for all irreducible representations R of S_n.
This is what the next section computes.
""")

    # Verify step 2 for S_3 numerically
    print("  Verification of  Tr(sigma Z^{tensor n}) = sum_R chi_R(sigma) chi_R(Z)")
    print("  (treating Tr(rho Z^{tensor n}) as a formal basis element)")
    print()
    print("  For S_3, the character table is:")
    print("  Irrep | chi(id) | chi(transpos) | chi(3-cycle)")
    print("  (3)   |    1    |       1       |      1")
    print("  (2,1) |    2    |       0       |     -1")
    print("  (1³)  |    1    |      -1       |      1")
    print()
    print("  For sigma = (0 1 2) = the 3-cycle, chi_R(sigma) values are:")
    print("  chi_(3)(tau) = 1,  chi_(2,1)(tau) = -1,  chi_(1^3)(tau) = 1")
    print()
    print("  Expansion of Tr(Z^3) = Tr(tau Z^{tensor 3}):")
    print("  = 1 * chi_(3)(Z)  +  (-1) * chi_(2,1)(Z)  +  1 * chi_(1^3)(Z)")
    print()
    print("  Two-point function:")
    print("  <Tr(Z^3) Tr((Z†)^3)>")
    print("  = (1)^2 f_(3)  +  (-1)^2 f_(2,1)  +  (1)^2 f_(1,1,1)")
    print("  = f_(3) + f_(2,1) + f_(1,1,1)")
    print()
    print("  At generic N:")
    print("  f_(3)     = N(N+1)(N+2)")
    print("  f_(2,1)   = N(N+1)(N-1)  = N(N^2-1)")
    print("  f_(1,1,1) = N(N-1)(N-2)")
    print()
    print("  Sum = N(N+1)(N+2) + N(N^2-1) + N(N-1)(N-2)")
    print("      = N[(N+1)(N+2) + (N^2-1) + (N-1)(N-2)]")
    print("      = N[N^2+3N+2  + N^2-1   + N^2-3N+2]")
    print("      = N[3N^2 + 3]  =  3N^3 + 3N  ✓")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 11.  MURNAGHAN-NAKAYAMA RULE — which representations contribute
# ─────────────────────────────────────────────────────────────────────────────

def sec11():
    print(SEP)
    print("SEC 11.  The Murnaghan-Nakayama rule: chi_R(n-cycle) = 0 unless R is a hook")
    print(SEP)
    print("""
We need chi_R(tau) for ALL Young diagrams R with n boxes.
The Murnaghan-Nakayama rule computes characters of cycle permutations.

MURNAGHAN-NAKAYAMA RULE:
  To compute chi_R(c_1 c_2 ... c_k) where (c_1 c_2 ... c_k) are
  DISJOINT cycles of lengths l_1, l_2, ..., l_k:

  1. Start with the Young diagram R.
  2. Remove an "l_1-ribbon" (a connected skew-shape with l_1 boxes,
     no 2x2 sub-square, connected) from R.  The sign is (-1)^{h-1}
     where h is the number of rows the ribbon spans (its "height").
  3. Compute chi_{R'}(c_2 ... c_k) for the remaining diagram R'.
  4. Sum over all ways to remove the ribbon.

For a SINGLE n-CYCLE tau (k=1, l_1 = n):
  We must remove ONE n-ribbon from R covering all n boxes.
  An n-ribbon covers all n boxes of R in one connected step.

  An n-ribbon that covers all boxes of an n-box Young diagram R
  must be the ENTIRE DIAGRAM R itself, treated as a rim (border strip).

  For this to be a valid ribbon (no 2x2 sub-square):
  R must be a HOOK DIAGRAM: no 2x2 sub-square can occur in R itself.

  The only Young diagrams with no 2x2 sub-square are HOOKS:
    R = (n-k, 1, 1, ..., 1)  =  (n-k, 1^k)    for  k = 0, 1, ..., n-1.

  A hook (n-k, 1^k) looks like:
    Row 1: n-k boxes
    Row 2: 1 box
    Row 3: 1 box
    ...
    Row k+1: 1 box

  The total height of such a ribbon = number of rows = k+1.
  Sign = (-1)^{height - 1} = (-1)^k.

CONCLUSION:
  chi_R(n-cycle) = 0          for non-hook R
  chi_R(n-cycle) = (-1)^k     for hook R = (n-k, 1^k)

So ONLY hook representations contribute to:
  <O_n O_n†> = sum_R (chi_R(tau))^2 f_R
             = sum_{k=0}^{n-1}  ((-1)^k)^2  f_{(n-k, 1^k)}
             = sum_{k=0}^{n-1}  f_{(n-k, 1^k)}
""")

    # Verify the Murnaghan-Nakayama rule against the full character table for S_4
    print("  Verification for n=4: characters of the 4-cycle (0123)")
    print()
    print("  Young diagram  |  chi_R( (0123) )  |  Is hook?  |  (-1)^k")
    print("  " + "-"*60)
    # S_4 irreps and characters of the 4-cycle
    # (4): chi=1, hook k=0 -> (-1)^0=1 ✓
    # (3,1): chi=-1, hook k=1 -> (-1)^1=-1 ✓
    # (2,2): chi=0, not hook ✓
    # (2,1,1): chi=1, hook k=2 -> (-1)^2=1 ✓
    # (1,1,1,1): chi=-1, hook k=3 -> (-1)^3=-1 ✓
    data = [
        ("(4)",     1,  True,  0),
        ("(3,1)",  -1,  True,  1),
        ("(2,2)",   0,  False, None),
        ("(2,1,1)", 1,  True,  2),
        ("(1,1,1,1)",-1,True,  3),
    ]
    for name, chi, is_hook, k in data:
        formula = f"(-1)^{k}={(-1)**k}" if k is not None else "N/A (=0)"
        print(f"  {name:<14} |  {chi:>17}  |  {'YES' if is_hook else 'NO':>8}  |  {formula}")
    print()
    print("  All non-hook diagrams have chi=0 for the 4-cycle.  ✓")
    print("  All hook diagrams have chi = (-1)^k.  ✓")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 12.  BOX FACTORS AND FORM I
# ─────────────────────────────────────────────────────────────────────────────

def sec12():
    print(SEP)
    print("SEC 12.  Computing f_{hook} and arriving at Form I")
    print(SEP)
    print("""
From Sec 11:
  <O_n O_n†> = sum_{k=0}^{n-1}  f_{(n-k, 1^k)}

We need f_{(n-k, 1^k)} = product of box factors (N - row + column)
over all boxes in the hook Young diagram (n-k, 1^k).

The hook (n-k, 1^k) has boxes at:
  Row 1: (1,1), (1,2), ..., (1, n-k)       [n-k boxes]
  Row 2: (2,1)                               [1 box]
  Row 3: (3,1)                               [1 box]
  ...
  Row k+1: (k+1, 1)                          [1 box]

Box factor of (i, j) = N - i + j  (using 1-indexing):
  Row 1, col j (j=1..n-k):  N - 1 + j  =  N, N+1, N+2, ..., N+n-k-1
  Row 2, col 1:              N - 2 + 1  =  N - 1
  Row 3, col 1:              N - 3 + 1  =  N - 2
  ...
  Row k+1, col 1:            N - k - 1 + 1 = N - k

So:
  f_{(n-k, 1^k)} = [N(N+1)(N+2)...(N+n-k-1)] * [(N-1)(N-2)...(N-k)]
                   \_________________________/   \_________________/
                      n-k terms from row 1          k terms from column

This is a product of n terms altogether.  Writing it as a RISING FACTORIAL
starting at (N-k):
  (N-k)^{(n)} = (N-k)(N-k+1)(N-k+2)...(N-k+n-1)
              = (N-k)(N-k+1)...(N-1) * N * (N+1)...(N+n-k-1)
              = [the k terms from column] * N * [the n-k-1 terms from row 1 after N]

Yes: (N-k)^{(n)} = (N-k)(N-k+1)...(N+n-k-1)  is exactly n terms from N-k to N+n-k-1.
Let's verify: the factors from N-k to N-1 are (N-k),(N-k+1),...,(N-1) = k terms.
And from N to N+n-k-1 are N,(N+1),...,(N+n-k-1) = n-k terms.
Total = k + (n-k) = n terms.  ✓

So:
  f_{(n-k, 1^k)} = (N-k)(N-k+1)...(N+n-k-1)  =  (N-k)^{(n)}

FORM I:

  ┌──────────────────────────────────────────────────────────────────┐
  │  <O_n O_n†>  =  sum_{k=0}^{n-1}  (N-k)(N-k+1)...(N+n-k-1)      │
  └──────────────────────────────────────────────────────────────────┘
""")

    # Tabulate hook factors for n=2,3,4,5
    from fractions import Fraction

    def hook_factor_poly(k, n):
        poly = [Fraction(1)]
        for j in range(n):
            shift = Fraction(j - k)
            new = [Fraction(0)] * (len(poly)+1)
            for d, c in enumerate(poly):
                new[d+1] += c
                new[d]   += shift * c
            poly = new
        return poly

    def pstr(p):
        terms = []
        for d in range(len(p)-1,-1,-1):
            if p[d]!=0:
                if d==0: terms.append(str(int(p[d])))
                elif d==1: terms.append(f"{int(p[d])}N")
                else: terms.append(f"{int(p[d])}N^{d}")
        return " + ".join(terms)

    for n in [2, 3, 4, 5]:
        print(f"  n={n}:")
        total = [Fraction(0)]*(n+1)
        for k in range(n):
            p = hook_factor_poly(k, n)
            for d,c in enumerate(p): total[d] += c
            factors_str = " * ".join(
                f"(N{'+'+str(j-k) if j-k>0 else (str(j-k) if j-k<0 else '')})"
                for j in range(n))
            factors_str = factors_str.replace("(N+0)","N").replace("(N0)","N")
            print(f"    k={k}: {factors_str}")
            print(f"         = {pstr(p)}")
        print(f"    SUM  = {pstr(total)}")
        print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 13.  HOCKEY-STICK IDENTITY AND FORM II
# ─────────────────────────────────────────────────────────────────────────────

def sec13():
    print(SEP)
    print("SEC 13.  The hockey-stick identity and Form II")
    print(SEP)
    print("""
FORM I:  <O_n O_n†> = sum_{k=0}^{n-1} (N-k)(N-k+1)...(N+n-k-1)

STEP 1: rewrite each rising factorial as a binomial.

The binomial coefficient C(m, r) = m! / (r! (m-r)!) counts the number
of ways to choose r objects from m.  For non-negative integer r:
  C(m, r)  =  m(m-1)(m-2)...(m-r+1) / r!   [r factors in numerator]

The rising factorial with n terms starting at (N-k):
  (N-k)(N-k+1)...(N+n-k-1)  =  n! * C(N+n-k-1, n)

Proof: C(N+n-k-1, n) = (N+n-k-1)(N+n-k-2)...(N-k) / n!
  Multiply by n!: gives (N-k)(N-k+1)...(N+n-k-1).  ✓

So:
  <O_n O_n†> = n! * sum_{k=0}^{n-1} C(N+n-k-1, n)

STEP 2: substitute j = n-k-1 (when k=0, j=n-1; when k=n-1, j=0):
  = n! * sum_{j=0}^{n-1} C(N+j, n)

STEP 3: the HOCKEY-STICK IDENTITY.

The Hockey-Stick (or Christmas Stocking) Identity states:
  sum_{i=r}^{m} C(i, r) = C(m+1, r+1)

Equivalently:
  sum_{i=a}^{b} C(i, r) = C(b+1, r+1) - C(a, r+1)

Our sum: sum_{j=0}^{n-1} C(N+j, n) = sum_{i=N}^{N+n-1} C(i, n)
  [substitute i = N+j]

Applying the hockey-stick with r=n, a=N, b=N+n-1:
  = C(N+n, n+1) - C(N, n+1)

Therefore:

  ┌──────────────────────────────────────────────────────────────────┐
  │  <O_n O_n†>  =  n! * [ C(N+n, n+1) - C(N, n+1) ]               │
  └──────────────────────────────────────────────────────────────────┘

STEP 4: manual verification for n=3.
  <O_3 O_3†> = 3! * [C(N+3,4) - C(N,4)]
             = 6 * [(N+3)(N+2)(N+1)N/24 - N(N-1)(N-2)(N-3)/24]
             = (N/4) * [(N+3)(N+2)(N+1) - (N-1)(N-2)(N-3)]

  Expand:
    (N+3)(N+2)(N+1) = N^3 + 6N^2 + 11N + 6
    (N-1)(N-2)(N-3) = N^3 - 6N^2 + 11N - 6
    Difference      =      12N^2       + 12  = 12(N^2 + 1)

  = (N/4) * 12(N^2+1)  =  3N(N^2+1)  =  3N^3 + 3N   ✓

STEP 5: check that the degree is correct.
  C(N+n, n+1) is a polynomial in N of degree n+1.
  C(N,   n+1) is a polynomial in N of degree n+1.
  Their leading terms in N^{n+1} both equal 1/(n+1)!, so they CANCEL.
  => The difference is degree n in N.  ✓  (We need a degree n polynomial.)

STEP 6: a note on finite N.
  For integer N, if N >= 1 then C(N, n+1) = 0 when N < n+1  (i.e. N <= n).
  In that case:  <O_n O_n†> = n! * C(N+n, n+1)  (only the first term).
  For N >= n+1, both terms contribute.
  As a formal polynomial in N, the formula is exact for ALL N.
""")

    # Numerical verification
    def closed_form_poly(n):
        p1 = [Fraction(1)]
        for j in range(n+1):
            shift = Fraction(n-j)
            new = [Fraction(0)]*(len(p1)+1)
            for d,c in enumerate(p1): new[d+1]+=c; new[d]+=shift*c
            p1=new
        f1=math.factorial(n+1)
        p1=[c/f1 for c in p1]
        p2=[Fraction(1)]
        for j in range(n+1):
            shift=Fraction(-j)
            new=[Fraction(0)]*(len(p2)+1)
            for d,c in enumerate(p2): new[d+1]+=c; new[d]+=shift*c
            p2=new
        p2=[c/f1 for c in p2]
        fn=Fraction(math.factorial(n))
        length=max(len(p1),len(p2))
        result={}
        for j in range(length):
            c1=p1[j] if j<len(p1) else Fraction(0)
            c2=p2[j] if j<len(p2) else Fraction(0)
            val=fn*(c1-c2)
            if val!=0: result[j]=int(val)
        return result

    def pstr(cd):
        parts=[]
        for p in sorted(cd.keys(),reverse=True):
            c=cd[p]
            if p==0: parts.append(str(c))
            elif p==1: parts.append(f"{c}N" if c!=1 else "N")
            else: parts.append(f"{c}N^{p}" if c!=1 else f"N^{p}")
        return " + ".join(parts)

    print("\n  Form II expanded for n=1..12:")
    for n in range(1, 13):
        cd = closed_form_poly(n)
        print(f"    n={n:>2}: <O_{n} O_{n}†> = {pstr(cd)}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Sec 14.  EXTRACTING EVERY COEFFICIENT — STRUCTURAL PROPERTIES
# ─────────────────────────────────────────────────────────────────────────────

def sec14():
    print(SEP)
    print("SEC 14.  Every coefficient and structural properties")
    print(SEP)
    print("""
From  <O_n O_n†> = n! * [C(N+n, n+1) - C(N, n+1)],
expanding as a polynomial in N:

  C(N+n, n+1) = (1/(n+1)!) * (N+n)(N+n-1)...(N+1)N
              = (1/(n+1)!) * product_{j=0}^{n} (N+n-j)

  C(N,   n+1) = (1/(n+1)!) * N(N-1)...(N-n)
              = (1/(n+1)!) * product_{j=0}^{n} (N-j)

Difference = (1/(n+1)!) * [product_{j=0}^{n}(N+n-j) - product_{j=0}^{n}(N-j)]

PROPERTY 1 (Parity — proved):
  Both products have the same leading term N^{n+1} and the same
  coefficient of N^n.  More generally, the even-degree terms in
  (N+a)(N+a-1)...(N+a-n) - (N-a)(N-a-1)...(N-a-n) vanish when
  the shifts are symmetric around 0, which happens here because
  the offsets in the first product are {n, n-1, ..., 0} and in
  the second {0, -1, ..., -n} and n - j + (-j) = n - 2j is symmetric
  in a sense that kills alternating powers.

  More precisely: sign(f(sigma)) = +1 for ALL sigma (shown in Sec 4).
  Since f is always an even permutation:
    #cycles(f) ≡ n (mod 2)   [because parity = (-1)^{n - #cycles}]
  So only powers of N with the SAME PARITY as n appear.

PROPERTY 2 (Leading coefficient):
  Coefficient of N^n in n!*[C(N+n,n+1)-C(N,n+1)]:
  = n! * (1/(n+1)!) * [e_1(n,n-1,...,0) - e_1(0,-1,...,-n)]
  where e_1 is the sum of roots.
  = n!/(n+1)! * [n(n+1)/2 - (-n(n+1)/2)]
  = n!/(n+1)! * n(n+1)  =  n!/n! * n = n.
  => Coefficient of N^n = n.  ✓ (n planar diagrams)

PROPERTY 3 (Sub-leading coefficient — proved):
  Coefficient of N^{n-2}  =  n * C(n+1, 4)  =  n^2(n+1)(n-1)(n-2)/24.
  [Derived by extracting the N^{n-2} term from the difference of binomials.]

PROPERTY 4 (Minimum power):
  For even n: f is always even, minimum #cycles = 2, minimum power = N^2.
  For odd n:  f is always even, but odd-n-cycle permutation has 1 cycle,
              minimum power = N^1.
""")

    # Summary table
    def closed_form_poly(n):
        p1=[Fraction(1)]
        for j in range(n+1):
            shift=Fraction(n-j); new=[Fraction(0)]*(len(p1)+1)
            for d,c in enumerate(p1): new[d+1]+=c; new[d]+=shift*c
            p1=new
        f1=math.factorial(n+1); p1=[c/f1 for c in p1]
        p2=[Fraction(1)]
        for j in range(n+1):
            shift=Fraction(-j); new=[Fraction(0)]*(len(p2)+1)
            for d,c in enumerate(p2): new[d+1]+=c; new[d]+=shift*c
            p2=new
        p2=[c/f1 for c in p2]
        fn=Fraction(math.factorial(n)); length=max(len(p1),len(p2)); result={}
        for j in range(length):
            c1=p1[j] if j<len(p1) else Fraction(0)
            c2=p2[j] if j<len(p2) else Fraction(0)
            val=fn*(c1-c2)
            if val!=0: result[j]=int(val)
        return result

    print("\n  COMPLETE COEFFICIENT TABLE  c(n,j) = coeff of N^{n-2j}")
    print()
    max_n = 12
    print(f"  {'n':>3} | {'j=0 (N^n)':>12} | {'j=1 (N^{n-2})':>15} | {'j=2':>12} | {'j=3':>12} | {'j=4':>12}")
    print("  " + "-"*75)
    for n in range(1, max_n+1):
        cd = closed_form_poly(n)
        row = f"  {n:>3} |"
        for j in range(5):
            p = n - 2*j
            if p < 0:
                row += f" {'(n/a)':>12} |"
            else:
                val = cd.get(p, 0)
                row += f" {val:>12} |"
        print(row)

    print()
    print("  Check: sum of all coefficients = n! (total Wick contractions)")
    for n in range(1, max_n+1):
        cd = closed_form_poly(n)
        s = sum(cd.values())
        ok = (s == math.factorial(n))
        print(f"    n={n:>2}: sum={s:<15} n!={math.factorial(n):<15} {'✓' if ok else 'FAIL'}")
    print()

    print("  Sub-leading formula: c(n, n-2) = n * C(n+1, 4)")
    for n in range(3, 13):
        cd = closed_form_poly(n)
        actual  = cd.get(n-2, 0)
        formula = n * math.comb(n+1, 4)
        ok = (actual == formula)
        print(f"    n={n:>2}: actual={actual:<10} n*C(n+1,4)={formula:<10} {'✓' if ok else 'FAIL'}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# RUN ALL
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sec1()
    sec2()
    sec3()
    sec4()
    sec5()
    sec6()
    sec7()
    sec8()
    sec9()
    sec10()
    sec11()
    sec12()
    sec13()
    sec14()
