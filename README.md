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
| `BTP_version3.ipynb` | top view, substrate friction | **full model: Stokes flow, active stress, Frank/elastic stress, vorticity, flow alignment, anchoring, adhesion** | **cell morphologies: aster, lamellipodium, cup** |
| `BTP_version3_run_and_tumble.ipynb` | same physics as Version 3 | a decision layer: pick a random direction, deform and crawl that way for a (random) distance, switch activity off and relax back to a circle, repeat | **stop-and-go migration with repeated repolarisation** |
| `BTP_version3_two_cell_walk.ipynb` | same physics, closed box (soft walls) | two cells, each running its own decide/move/relax walk, sharing one Stokes solve; a steric term keeps them from merging | **collision → deformation and mutual rotation → redirect, executed and verified** |

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

## Running

```bash
pip install numpy matplotlib
jupyter notebook BTP_version3.ipynb
```

All notebooks ship with outputs. Version 3 takes about 20 minutes to re-run on
one core, most of it in the two parameter sweeps; set `QUICK = True` in the
parameters cell to shrink every run while developing.

### Section 19 — single-cell video, and why Version 3 (not 4) for many cells

A separate Version 4 (local, friction-dominated Darcy law in place of the
Stokes solve) was built to make many-cell runs cheap, and a first two-cell
experiment was done on top of it. The adviser's guidance was to extend
**Version 3** instead for multi-cell work: viscosity is exactly how one
cell's motion is felt by a colliding neighbour through the shared flow
field, and the local Darcy law throws that coupling away by construction.

Section 19, appended at the end of `BTP_version3.ipynb`, runs the
"lamellipodium" morphology for $t=150$ with a snapshot every time unit and
renders them into a short video (`version3_single_cell.mp4`, 150 frames at
30 fps = 5 s) — the single-cell baseline the upcoming two-cell *Version 3*
run will be compared against. **It is appended but not executed**: run it
yourself (needs `ffmpeg` on the `PATH`; full Stokes at $N=128$ costs about
$2.7\,\mathrm{ms}$/step, so the ~15 000-step run plus encoding should take
well under a minute).

## A cell that decides, moves, and resets: `BTP_version3_run_and_tumble.ipynb`

Every result above hands the cell one polarization at $t=0$ and lets it
crawl in whatever direction that implies for the whole run. This notebook
adds a decision layer on top of the *exact same* Version 3 mechanics
(copied over unchanged — grid, thermodynamics, body force, Stokes solve,
diagnostics):

1. **Decide.** Draw a random direction $\theta\sim U(0,2\pi)$ and a random
   travel distance (a fixed distance also works — pass `distance_range=(d,d)`).
2. **Deform and move.** Point $\mathbf P$ along $\theta$ with the usual
   lamellipodium activity ($w_0=1,\ \zeta=-1,\ \beta=0.25$) switched on;
   the cell polarises into its motile fan shape and crawls that way.
3. **Relax.** Once it has travelled the chosen distance, switch
   $\zeta,\beta,w_0$ off. With no energy sustaining the fan, the same
   interfacial relaxation validated in Version 3's passive-limit test
   (Section 13) pulls the cell back towards a circle; the phase ends once
   circularity clears a target (capped so it can't stall forever).
4. **Repeat** for `n_cycles`, each leg starting fresh from the relaxed
   shape with a new, independent direction.

Produces a path plot (coloured by phase), the usual aspect-ratio /
circularity diagnostics, and `run_and_tumble.mp4` — a video of the whole
decide → fan out → crawl → round off → decide-again cycle.

**Not executed in this repository** — run it yourself (four cycles at the
default settings is on the order of $35$–$45$ thousand steps, roughly
$1.5$–$2$ minutes at Version 3's $\approx2.7\,\mathrm{ms}$/step).

## Two cells, a closed box, a collision that redirects: `BTP_version3_two_cell_walk.ipynb`

Two independent walkers from the run-and-tumble notebook, sharing one
closed box, that **do not merge** when their paths cross — they
deform against each other, exchange rotation through the fluid, and
redirect. Figures and video are in `two_cell_walk_media/`. Two new
ingredients, both reused/adapted from earlier work, plus one
genuinely new piece of mechanics:

- **Non-merging: the same steric term as the Version 4 two-cell
  experiment**, $F_{\rm rep}=k_{\rm rep}\int\phi_1^2\phi_2^2$, carried
  over unchanged (it only ever adds $2k_{\rm rep}\phi_i\phi_j^2$ to
  each cell's own $\mu_i$).
- **A closed box, as a soft wall rather than a new solver.** The
  spectral Stokes solve only works on a periodic domain; a literal
  no-slip wall would need a real rewrite (finite differences/volumes,
  a sparse linear solve instead of two FFTs). Instead, one potential
  term is added to $\mu_\phi$ that ramps up near the domain edges —
  **but only through the force**, not the bare relaxation. The first
  attempt at this added it directly to the $\mu$ used by
  $-M(\mu-\Lambda g)$, and it diverged: with no $\phi$ factor, that
  term drains $\phi$ to $-\infty$ in empty space with nothing to stop
  it. Keeping it out of the relaxation term and adding it only where
  the capillary force $-\phi\,\partial_\alpha\mu$ already has a $\phi$
  prefactor fixes this: the wall potential now does nothing away from
  an actual cell.
- **The genuinely new piece — one shared Stokes solve for both
  cells.** This is the direct answer to "take momentum and rotation
  into account": `stokes_solve` is called once on
  $\mathbf f_1+\mathbf f_2$, returning one $\mathbf v$ felt by both
  cells, rather than two independent flow fields that never interact.
  Version 3's existing vorticity-driven corotation term in the
  $\mathbf P$ equation then does the rest: if contact generates local
  vorticity in that shared field, it torques **both** cells'
  polarizations. A controlled check in the notebook (fixed, opposing
  headings, no decision layer) confirms this directly: both mean
  polarization angles sit flat until contact, then rotate
  symmetrically, in opposite senses, the moment the overlap integral
  turns on (measured: $-8.8°$ and $+8.8°$ over the contact window). No
  rigid-body elastic-collision formula was added — that would need an
  independent notion of mass and velocity this over-damped,
  inertia-free model ($Re\sim10^{-5}$) does not actually have.

Each cell also redirects (ends its current "move" phase early, enters
"relax", then picks a fresh random heading) if it drifts into the
wall margin, or if a collision is detected (the overlap integral
crossing a threshold) — on top of the usual distance-reached and
relaxed-long-enough triggers from the single-cell run-and-tumble
notebook.

**Executed**, unlike the two single-cell additions — the physics here
(the shared Stokes solve, and especially the wall potential, which
diverged on the first attempt) was new enough that shipping it
unverified would not have been trustworthy. A $140$-time-unit run at
$N=192$ ($\approx9$–$11\,\mathrm{ms}$/step measured, not estimated)
produced $3$ collision events, a maximum contact overlap of $2.07$
(well under the $\approx8.7$ a non-interacting pair shows at nominal
touching — confirmed, not assumed), and a clean path plot showing
both cells visibly deflect at contact rather than cross straight
through each other. `two_cell_walk.mp4` is a 46-frame, 8 fps video of
the whole run.

## Next steps

More than two cells (the shared-Stokes idea generalises directly:
sum every cell's body force before the one solve, and add a steric
term for every pair); mechanosensitive adhesion $\xi(|\mathbf v|)$ with
a cycle in the activity, to test the Leoni & Sens biphasic prediction;
and coupling the Version 2 slice to the Version 3 solver to get the
pseudopod and the top-view cell shapes in one calculation.
