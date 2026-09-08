# BTP — Minimal Physical Model of a Crawling Cell

Phase-field / active-polar-fluid simulations of cell crawling.

Primary reference: Tjhung, Tiribocchi, Marenduzzo & Cates, *A minimal physical
model captures the shapes of crawling cells*, Nat. Commun. **6**, 5420 (2015).
Adhesion physics follows Leoni & Sens, *Model of cell crawling controlled by
mechanosensitive adhesion*, Phys. Rev. Lett. **118**, 228101 (2017).

The project is built up in deliberately small, testable versions.

| notebook | geometry | what it adds | headline result |
|---|---|---|---|
| `BTP_version1.ipynb` | free space, top view | $\phi$, $\mathbf P$, treadmilling $w_0\mathbf P$ | cell translates rigidly; area drifts 4.5% |
| `BTP_version2.ipynb` | side view, wall at $z=0$ | near-wall treadmilling $w(z)$, exact volume, viscous screening | **protrusion + steady crawling** |
| `BTP_version3.ipynb` | top view, substrate friction | **full model: Stokes flow, active stress, Frank/elastic stress, vorticity, flow alignment, anchoring, adhesion** | **cell morphologies: aster, lamellipodium, fan** |
| `BTP_version4.ipynb` | top view, substrate friction | **no Stokes solve** (friction-dominated limit), **area free** with soft volume restoring force | **crawls 240 units in 16 s; ~5× faster; ready for many cells** |

Versions 2 and 3 are complementary rather than sequential: the protrusion of
Fig. 1 of the paper is a *near-substrate* structure and needs the side view,
while the cell shapes of its Fig. 2 are *top-view* shapes and need the plane.

## Version 3 — the full 2D model

Solves, on a periodic $(x,y)$ grid:

$$\partial_t\phi+\nabla\cdot[\phi(\mathbf v+w_0\mathbf P)]=-M[\mu_\phi-\Lambda g(\phi)]$$

$$\partial_t\mathbf P+[(\mathbf v+w_0\mathbf P)\cdot\nabla]\mathbf P=-\mathbf\Omega\cdot\mathbf P+\chi\mathbf D\cdot\mathbf P-\mathbf h/\Gamma$$

$$0=-\nabla p+\eta\nabla^2\mathbf v-\xi\mathbf v+\nabla\cdot(\sigma^{act}+\sigma^{el})-\phi\nabla\mu_\phi,\qquad \nabla\cdot\mathbf v=0$$

with $\sigma^{act}_{\alpha\beta}=-\zeta\phi P_\alpha P_\beta$ and the full
elastic stress of the paper's Eq. (6).

Implementation notes:

- **Spectral Stokes solve.** Periodic in both directions, so a Leray projection
  in Fourier space eliminates the pressure exactly and the viscous term costs no
  time-step restriction. One FFT pair per step, no iteration.
- **Substrate friction $\xi$** replaces the paper's 3D no-slip wall. This is the
  effective friction that Leoni & Sens obtain by averaging over the binding and
  unbinding of a carpet of linkers.
- **Volume exact to $10^{-16}$** via conservative flux-form advection plus an
  interface-weighted Lagrange multiplier (conservative Allen–Cahn).
- **Validated in the passive limit**: an ellipse relaxes to a circle, the free
  energy decreases monotonically, the flow decays to $10^{-5}$.

### Results

Reproduced from the paper: the **non-motile aster** ("fried egg" — radial
$\mathbf P$ with a $+1$ defect, $|\langle\mathbf P\rangle|=0$ and zero speed to
machine precision), the **lamellipodium / keratocyte fan** (broad convex leading
edge with two trailing wings), crawl speed $\approx w_0$ in every motile state,
and the trend that fan shapes require larger anchoring.

The most useful result is a control experiment that is *not* in the paper: a
$2\times2$ switching anchoring against the flow, at otherwise identical
parameters. Steady aspect ratio (1 = circle):

| | flow off | flow on |
|---|---|---|
| $\beta=0$ | 1.07 | 1.61 |
| $\beta=0.25$ | 2.85 | 2.92 |

So the flow *does* deform the cell on its own (1.07 → 1.61) and is the only
deformation mechanism available when $\beta=0$ — but on top of anchoring it adds
about 2%. In this top-view geometry the fan shape is predominantly
**anchoring**-driven, not hydrodynamic. Independently, the adhesion sweep
confirms the limit: at strong adhesion the flow is screened away and the aspect
ratio saturates onto the flow-free value of 2.85.

Reported as *not* reproduced, with reasons:

- the **pseudopod** — a near-substrate structure set by the vertical confinement
  $w(z)=w_0e^{-z/\lambda}$, so it has no top-view counterpart; Version 2 captures
  it instead;
- the **phagocytic cup** — raising anchoring gives fan → strongly fanned →
  turning → aster, with no indented leading edge anywhere; in the paper this
  shape is explicitly 3D;
- the **lab-frame flow fields** of the paper's Fig. 4, because the $k=0$ mode of
  $\mathbf v$ is set to zero, so what is computed is the internal circulation
  relative to the cell's own drift;
- the **adhesion-dependent biphasic speed** of Leoni & Sens — their propulsion is
  mechanosensitive traction, ours is treadmilling, so a constant $\xi$ cannot see
  their mechanism. Here the speed is flat to 2% across a 32-fold change in
  adhesion.

## Version 4 — the fast model, and the one to build on

Version 3 answers "what does the full model do", but its elliptic Stokes solve is
too expensive to carry into simulations of many interacting cells. Version 4
removes it, for a stated physical reason rather than as a shortcut.

**No Stokes solve.** When substrate friction beats viscosity the force balance
stops being elliptic and becomes local algebra:

$$\frac{\eta k^2}{\xi}\sim\frac{\eta}{\xi R^2}\approx 0.006
\qquad\Longrightarrow\qquad \xi\mathbf v=\mathbf f,\quad \mathbf v=\mathbf f/\xi$$

This is the Darcy limit, the basis of the Ziebert–Aranson class of 2D
crawling-cell models. It is not a guess: the Version 3 adhesion sweep already
showed the flow falling off as $1/\xi$ and the cell shape saturating onto the
flow-free limit as adhesion strengthened.

**Volume, not area.** A crawling cell holds its volume $V_0\approx h A$ and spreads
by thinning, so pinning the projected area is an artificial constraint. The exact
Lagrange multiplier is replaced by a soft restoring force
$\Lambda=-k_A(A/A_0-1)$, and the implied thickness $h=V_0/A$ is tracked. The cell
spreads 15% and thins to 0.87 while crawling.

**Cost.** 1.1 ms/step versus 2.7 ms, and a 3× larger stable time step, so about
**5× faster** at the default $dt=0.02$ and 7× at $dt=0.03$. More importantly every
operation is now a local stencil, so cost scales linearly in grid points with no
global coupling — which is the property that makes many cells affordable.

**Validated** against Version 3 to 0.2% in the limit where the two models coincide
(flow off, rigid area: aspect 2.855 vs 2.850), despite sharing no solver code.
Note that $\zeta$ is *not* transferable — without the pressure to resist it, the
friction-dominated flow deforms the cell about ten times more per unit $\zeta$.

Two results worth knowing:

- The area constraint mostly controls **shape, not speed**. Going from rigid area
  to $k_A=2$ changes the crawl speed by under 1% but the aspect ratio by 35%.
- **Removing the constraint entirely does not work.** The $-\alpha|\mathbf P|^2$
  term makes the polarized interior cheaper than the exterior, so with nothing
  opposing it the cell inflates 14× until it fills the box and stops crawling. The
  constraint should be soft, not absent.

## Running

```bash
pip install numpy matplotlib
jupyter notebook BTP_version3.ipynb
```

All notebooks ship with outputs. Version 4 re-runs in about 4 minutes on one
core; Version 3 takes about 20 minutes, most of it in the two parameter sweeps
(set `QUICK = True` in its parameters cell while developing).

## Next steps

Multiple interacting cells, on top of Version 4: one phase field $\phi_i$ per cell
with its own $\mathbf P_i$, a repulsive overlap term
$\varepsilon_{rep}\sum_{i\neq j}\phi_i^2\phi_j^2$ in the free energy to give contact
forces, a per-cell target area (which the soft constraint already provides), and a
fixed laboratory frame instead of re-centring. None of this needs a solver.

Longer term: mechanosensitive adhesion $\xi(|\mathbf v|)$ with a cycle in the
activity, to test the Leoni & Sens biphasic prediction inside a continuum model;
spontaneous polarity so the cell chooses its own direction rather than being
handed a uniform or radial $\mathbf P$; and coupling the Version 2 slice to the
Version 3 solver to get the pseudopod and the cell shapes in one calculation.
