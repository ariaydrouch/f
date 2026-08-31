# BTP — Minimal Physical Model of a Crawling Cell

Phase-field / active-polar-fluid simulations of cell crawling, following
Tjhung, Tiribocchi, Marenduzzo & Cates, *A minimal physical model captures the
shapes of crawling cells*, Nat. Commun. **6**, 5420 (2015).

The project is built up in deliberately small, testable versions.

| notebook | what it adds | status |
|---|---|---|
| `BTP_version1.ipynb` | Cell field $\phi$ in free space, actin polarization $\mathbf P$, active treadmilling $w_0\mathbf P$ | cell translates rigidly; area drifts by ~4.5% |
| `BTP_version2.ipynb` | Wall geometry, treadmilling confined near the substrate, exactly conserved volume, viscous screening in place of a flow solver | **protrusion + steady crawling, volume conserved to $10^{-16}$** |

## Version 2 at a glance

A cell sits on a no-slip wall in a side-view $y$–$z$ slice. Treadmilling is
confined to a layer of thickness $\lambda$ near the substrate,

$$w(z) = w_0\cdot\tfrac12\big(1-\tanh\tfrac{z-\lambda}{w_\tau}\big),$$

so the near-wall material runs out ahead of the cell body while surface tension
pulls it back. The steady state of that competition is a thin leading
protrusion, and the cell crawls forward.

Two ingredients make this work without a Navier–Stokes solver:

- **Exact volume conservation.** Advection is written in conservative flux form
  and the Allen–Cahn relaxation carries a uniform Lagrange multiplier, so
  $\int\phi\,dA$ is constant by construction rather than by accuracy. The
  multiplier is conjugate to volume, i.e. it acts as an internal pressure, which
  is what lets a growing protrusion be paid for by a retracting rear.
- **Viscous screening.** The flow field is replaced by the thin-film (Brinkman)
  closure $(1-\ell_v^2\partial_z^2)\mathbf u = w(z)\mathbf P$, one tridiagonal
  solve per step. The screening length $\ell_v=\sqrt{\eta/\xi}$ plays the role of
  substrate adhesion: small $\ell_v$ is strong adhesion.

Results reproduced qualitatively: the two shape regimes of Fig. 1a, the
protrusion transition in $w_0$ of Fig. 1b, and the effect of adhesion of Fig. 1c.

## Running

```bash
pip install numpy matplotlib
jupyter notebook BTP_version2.ipynb
```

The notebook ships with outputs. A full re-run takes about 8 minutes on 1 core;
most of that is the two parameter sweeps, which can be shortened by lowering
`t_final`.

## Known limitation, and Version 3

The protruded cell is a wedge with a thin leading lamella, whereas the paper
shows a rounded body with a distinctly stepped tongue. The screening operator
conserves the depth-integrated drive, so a faster near-wall layer necessarily
comes at the expense of the body and the velocity profile stays monotonic in
$z$. A Stokes solve — linear and elliptic, no inertia — is the ingredient that
would transport the body coherently and convert the wedge into a step. That,
plus contractility $\zeta$ and interface anchoring $\beta$, is Version 3.
