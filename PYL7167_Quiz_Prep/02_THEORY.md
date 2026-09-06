# Theory notes — PYL7167 (atomic physics, quiz 1)

These notes follow your 24-page lecture script, filled out to the depth the practice problems demand. Textbook anchors: **Bransden & Joachain** (*Physics of Atoms and Molecules*), **Haken & Wolf** (*The Physics of Atoms and Quanta*), **H. E. White** (*Introduction to Atomic Spectra*), **C. J. Foot** (*Atomic Physics*), **Kittel** (excitons), **Jackson** (classical radiation).

---

## A. What an “atom” means in this course

**One-electron (hydrogenic) atoms:** a nucleus of charge \(+Ze\) plus exactly one electron. Examples: \(\mathrm{H}\), \(\mathrm{He}^+\), \(\mathrm{Li}^{2+}\), \(\mathrm{C}^{5+}\). Energies scale as \(Z^2\), lengths as \(1/Z\).

**Optical (valence) electrons:** the electrons that actually change state in optical spectra. Na has one; Ca has two. Inner closed shells are spectators at optical frequencies (they do appear in X-ray spectra).

**Equivalent electrons:** same \(n\) and \(\ell\). Helium \(1s^2\) is two equivalent \(s\) electrons. Pauli then forbids many LS or jj terms that nonequivalent electrons would be allowed to form.

**Three kinds of spectra**

| Kind | Source |
|---|---|
| Line | bound–bound in **atoms** (discrete \(E_n\)) |
| Band | **molecules** (electronic + vibrational + rotational) or solids (bands) |
| Continuous | free–bound, free–free, or black-body |

Helium looks like **two superimposed spectra**: *parahelium* (singlets, \(S=0\), includes the ground state \(1s^2\;{}^1S_0\)) and *orthohelium* (triplets, \(S=1\), lowest term \(1s2s\;{}^3S_1\), metastable). E1 cannot change \(S\), so the two systems barely talk to each other.

---

## B. Bohr model, Rydberg constant, correspondence principle

Classical circular orbit: Coulomb = centripetal

\[
\frac{1}{4\pi\epsilon_0}\frac{e^2}{r^2}=m r\omega^2
\quad\Rightarrow\quad
E=T+V=-\frac12\cdot\frac{e^2}{4\pi\epsilon_0 r}.
\]

Eliminating \(r\) in favour of \(\omega\) gives the classical \(E(\omega)\) written in lecture 2:

\[
E=-\frac12(4\pi\epsilon_0)^{-2/3}(e^4 m\omega^2)^{1/3}.
\]

Quantum frequencies of neighbouring levels at large \(n\) (correspondence: the atom must radiate at the orbital frequency):

\[
\nu=Rc\left(\frac{1}{n^2}-\frac{1}{(n+1)^2}\right)\approx 2Rc/n^3,
\qquad\omega=2\pi\nu.
\]

Match \(E_n=-Rch/n^2\) to the classical \(E(\omega)\) and you recover

\[
R_\infty=\frac{m_e e^4}{8\varepsilon_0^2 h^3 c}.
\]

Experiment: \(R_H=109\,677.58~\mathrm{cm}^{-1}\). Theory with infinite mass: \(R_\infty=109\,737.32~\mathrm{cm}^{-1}\). The gap \(\approx 60~\mathrm{cm}^{-1}\) is **reduced mass**, not a failure of QM:

\[
R_H=\frac{R_\infty}{1+m_e/M_p}.
\]

This fix is **not** enough for \(Z\gtrsim 20\): fine structure, Lamb shift and other relativistic / QED pieces grow as \(Z^4\) and higher.

**Resonance line** of H: Lyman-\(\alpha\), \(n=2\to 1\), \(121.6~\mathrm{nm}\).

**Classical collapse (Jackson / Larmor).** An accelerating charge radiates

\[
P=\frac{\mu_0 e^2 a^2}{6\pi c}.
\]

The time to spiral from \(a_0\) into the nucleus is \(\sim 10^{-11}\,\mathrm{s}\) — not milliseconds. Bohr’s postulates stop this by forbidding continuous radiation in a stationary state.

---

## C. Schrödinger hydrogen: degeneracy, radial functions, virial

Central potential \(\Rightarrow\) \([H,\mathbf{L}]=[H,L^2]=0\), so \(\{H,L^2,L_z\}\) share eigenfunctions

\[
\psi_{nlm}(\mathbf{r})=R_{nl}(r)\,Y_{lm}(\theta,\phi).
\]

- **Energy** of a pure Coulomb problem depends only on \(n\) (**accidental / \(\ell\)-degeneracy**), degeneracy \(n^2\) without spin, \(2n^2\) with spin.
- **\(m\)-degeneracy** is from **spherical symmetry** (any central \(V(r)\)). It survives in alkalis; \(\ell\)-degeneracy does not.

**Why \(\ell<n\):** the radial equation with \(u=rR\) has an effective potential \(\ell(\ell+1)\hbar^2/2\mu r^2+V(r)\). Bound Coulomb solutions exist only for \(n_r=0,1,2,\ldots\) with \(n=n_r+\ell+1\), so \(\ell=0,1,\ldots,n-1\).

Near the origin the centrifugal barrier wins:

\[
R_{nl}(r)\;\xrightarrow{r\to 0}\; r^{\ell}.
\]

(\(u=rR\propto r^{\ell+1}\). If a T/F says “\(R_{nl}\propto r^{\ell+1}\)”, it is **false**.)

Useful explicit functions (hydrogenic):

\[
R_{10}(r)=2\left(\frac{Z}{a_0}\right)^{3/2}e^{-Zr/a_0},
\qquad
R_{21}(r)=\frac{1}{\sqrt{3}}\left(\frac{Z}{2a_0}\right)^{3/2}\left(\frac{Zr}{a_0}\right)e^{-Zr/2a_0}.
\]

Larger \(Z\) pulls \(|R|^2\) inward (finite nucleus penetration \(\Rightarrow\) electron capture is possible for \(s\) waves; \(s\) waves have \(R(0)\neq 0\)).

Radial probability \(P(r)=r^2 |R_{nl}|^2=4\pi r^2|\psi|^2\) for \(s\) states. Maxima from \(dP/dr=0\), **not** from \(\langle r\rangle\).

\[
\langle r\rangle_{nlm}=\frac{a_0 n^2}{Z}\left\{1+\tfrac12\bigl[1-\ell(\ell+1)/n^2\bigr]\right\},
\qquad
\langle 1/r\rangle_{nlm}=Z/(a_\mu n^2).
\]

\(\langle r\rangle>r_\text{mp}\) because \(P(r)\) has a long outer tail.

**Virial theorem.** For a homogeneous potential of degree \(k\), \(2\langle T\rangle=k\langle V\rangle\).

| Potential | \(k\) | Relation | Hydrogen ground state |
|---|---|---|---|
| Coulomb | \(-1\) | \(2\langle T\rangle=-\langle V\rangle\) | \(\langle T\rangle=+13.6\,\mathrm{eV}\), \(\langle V\rangle=-27.2\,\mathrm{eV}\), \(E=-13.6\,\mathrm{eV}\) |
| HO | \(+2\) | \(\langle T\rangle=\langle V\rangle\) | — |

Kinetic energy as a local function \(E-V(r)\) vanishes at the classical turning points; it is **not** identically zero anywhere as an expectation.

**Unsold’s theorem.** For any \(\ell\),

\[
\sum_{m=-\ell}^{\ell}|Y_{\ell m}(\theta,\phi)|^2=\frac{2\ell+1}{4\pi}.
\]

A closed subshell is spherically symmetric. Proof for \(\ell=1\) is practice problem 17.

---

## D. Alkali atoms, quantum defect, ionisation

An alkali is hydrogen-like **outside** a closed noble-gas core. The valence electron sees:

- \(V\sim -e^2/4\pi\epsilon_0 r\) far away (core charge \(+1\)),
- \(V\sim -Ze^2/4\pi\epsilon_0 r\) if it penetrates the core.

The potential is still central \(\Rightarrow\) good \(\ell,m\), but it is **not** \(1/r\) \(\Rightarrow\) \(E=E_{n\ell}\). **Do not write** “the potential is not spherically symmetric” — that would split \(m\), which it does not. Spherical symmetry is intact; Coulomb degeneracy is not.

Quantum defect \(\delta_{n\ell}\) absorbs core penetration and polarisation:

\[
E_{n\ell}=-R_{\text{atom}}hc\big/(n-\delta_{n\ell})^2,\qquad n^*=n-\delta.
\]

\(\delta\) is nearly independent of \(n\) for a given \(\ell\), and falls rapidly with \(\ell\) (centrifugal barrier keeps high-\(\ell\) orbits out of the core). Your Li numbers: \(\delta_s\approx 0.4\), \(\delta_p\approx 0.04\), \(\delta_d\approx\delta_f\approx 0\).

**Term diagram vs hydrogen (qualitative, required).** Draw H levels at \(-13.6/n^2\). For Li, every \(ns\) level sits **below** the H level of the same \(n\) (more tightly bound); \(np\) slightly below; \(nd,nf\) almost on top of H. Ground state is \(2s\), not \(1s\) (the \(1s\) shell is filled). Allowed arrows: \(\Delta\ell=\pm 1\), e.g. \(2p\to 2s\) (principal series / resonance) and \(3d\to 2p\).

Ionisation energies jump when you start breaking a closed shell (Li: \(5.4\,\mathrm{eV}\) then \(\sim 75\,\mathrm{eV}\)). Franck–Hertz measures the first excitation / effective I.E. of the valence electron.

---

## E. Fine structure, relativistic QM, Lamb shift

### Spin–orbit

In the electron’s rest frame the nucleus orbits, producing

\[
\mathbf{B}_L=\frac{Z e\mu_0}{4\pi m_e r^3}\mathbf{L}.
\]

\(V=-\boldsymbol{\mu}_s\cdot\mathbf{B}_L\) with \(\boldsymbol{\mu}_s=-(e/m_e)\mathbf{S}\) and a Thomas factor \(1/2\):

\[
V_{LS}=\frac{Z e^2\mu_0}{8\pi m_e^2 r^3}\,\mathbf{S}\cdot\mathbf{L}.
\]

On \(\lvert n\ell j m_j\rangle\),

\[
\mathbf{L}\cdot\mathbf{S}=\frac{\hbar^2}{2}\bigl[j(j+1)-\ell(\ell+1)-s(s+1)\bigr],
\]

so each Bohr level with \(\ell\ge 1\) splits into \(j=\ell\pm\tfrac12\). The doublet interval

\[
\Delta E_{fs}=E_{\ell+1/2}-E_{\ell-1/2}=a\bigl(\ell+\tfrac12\bigr)
\propto \frac{Z^4}{n^3\,\ell(\ell+1)}.
\]

Hydrogen \(2p\) interval is \(0.365~\mathrm{cm}^{-1}\) (\(\sim 4.5\times 10^{-5}\,\mathrm{eV}\)). A problem that quotes “\(0.3\,\mathrm{eV}\)” is a **scaling exercise**, not a measured number.

### Dirac vs Lamb

Dirac hydrogen: \(E=E(n,j)\). Thus \(2S_{1/2}\) and \(2P_{1/2}\) are still degenerate. Experiment (Lamb–Retherford, 1947):

- microwave resonance on a \(2500^\circ\mathrm{C}\) H beam,
- \(2S_{1/2}\) is metastable and survives a \(10~\mathrm{cm}\) flight,
- a small \(\mathbf{B}\) is tuned through the crossing; absorption of a **fixed** microwave frequency dumps \(2S\) into \(2P\), which then decays,
- extrapolate to \(B=0\) with the Breit–Rabi formula.

Result: \(2S_{1/2}\) lies **\(1057.8~\mathrm{MHz}\) above** \(2P_{1/2}\). This is a **QED radiative correction** (electron self-energy + vacuum polarisation). It is **not** predicted by the Dirac equation. Frequency \(1057~\mathrm{MHz}\approx 4.4~\mu\mathrm{eV}\approx 0.035~\mathrm{cm}^{-1}\). If lecture notes say “\(0.031\,\mathrm{eV}\)”, that is a unit slip.

**Metastable states of H:** \(2S_{1/2}\) is the textbook one. E1 needs \(\Delta\ell=\pm 1\); there is no lower state with \(\ell=1\) below \(2S\). Decay is two-photon, lifetime \(\sim 0.12\,\mathrm{s}\). (\(2P\) lives \(1.6~\mathrm{ns}\).)

Single-photon E1-forbidden \(\neq\) probability zero (M1/E2/two-photon). “Strictly forbidden” would mean a selection rule of an exact symmetry (e.g. \(\Delta S\neq 0\) in pure LS, or \(J=0\to 0\)).

---

## F. Magnetic moments, Larmor precession, Stern–Gerlach

Orbital: \(\boldsymbol{\mu}_L=-(e/2m_e)\mathbf{L}=-g_L\mu_B\mathbf{L}/\hbar\) with \(g_L=1\).
Spin: \(\boldsymbol{\mu}_S=-g_S\mu_B\mathbf{S}/\hbar\) with \(g_S=2.0023\approx 2\).

Because \(g_S\neq g_L\), \(\boldsymbol{\mu}_J\) is **not** antiparallel to \(\mathbf{J}\) in the naive classical picture; the projection that survives is the Landé one,

\[
g_J=1+\frac{J(J+1)+S(S+1)-L(L+1)}{2J(J+1)}.
\]

Torque \(\boldsymbol{\tau}=\boldsymbol{\mu}\times\mathbf{B}\) \(\Rightarrow\) Larmor precession \(\omega_L=\gamma B\), **independent of the angle** \(\alpha\) between \(\boldsymbol{\mu}\) and \(\mathbf{B}\). That is why we can replace the fast precession by the time-averaged \(\mu_z\).

**SG force.** In an inhomogeneous field

\[
\mathbf{F}=\nabla(\boldsymbol{\mu}\cdot\mathbf{B}).
\]

With the standard pole-piece geometry \(\partial B_z/\partial z\) dominates, so \(F_z=\mu_z\partial B_z/\partial z\). Transverse components are designed to be small (and \(\nabla\cdot\mathbf{B}=0\) actually forces some \(\partial B_x/\partial x\), which is why the beam must be a thin ribbon).

Alkali GS \(^2S_{1/2}\): \(J=1/2\), \(g=2\), \(\mu_z=\pm\mu_B\), **two** spots. A \(J=3/2\) beam would give **four** spots.

Free electrons: the Lorentz force \(e\mathbf{v}\times\mathbf{B}\) is enormous compared with the spin force, so a direct SG on \(e^-\) fails. Use **neutral** atoms (Ag, Cu, H, Na, K, Cs — all \(^2S_{1/2}\)).

Static \(\mathbf{B}\) does no work (\(\mathbf{F}\perp\mathbf{v}\) is not the point — \(\mathbf{F}\) is along \(z\), but the potential is magnetic and conservative in the adiabatic \(\mu_z\)-fixed picture; a **time-dependent** \(\mathbf{B}\) induces \(\mathbf{E}\) and can do work).

---

## G. Zeeman, Paschen–Back, and Stark

Full magnetic Hamiltonian (one electron, ignoring diamagnetism):

\[
H=H_0+\zeta\,\mathbf{L}\cdot\mathbf{S}+\frac{\mu_B}{\hbar}(\mathbf{L}+2\mathbf{S})\cdot\mathbf{B}.
\]

“Weak” vs “strong” is **relative to the internal FS interval of that atom**, not an absolute tesla number. Earth’s field \(\sim 0.5~\mathrm{G}\) already produces a (tiny) Zeeman splitting.

### Normal Zeeman (\(S=0\), e.g. Cd \(^1D_2\to{}^1P_1\))

\(g=1\) on both levels. Splittings are \(\mu_B B m\). Selection \(\Delta m=0,\pm 1\) yields the **Lorentz triplet**, independent of \(L\):

- π: unshifted, polarised \(\parallel\mathbf{B}\),
- σ±: shifted by \(\pm\mu_B B/h\), circular about \(\mathbf{B}\).

### Anomalous Zeeman (\(S\neq 0\))

Each FS level fans into \(2J+1\) sublevels with spacing \(g_J\mu_B B\). Because \(g_\text{upper}\neq g_\text{lower}\), you get many components with **unequal** spacing. Sodium D lines:

```
          B=0 FS              weak B
  3p  ²P_{3/2} ────────    4 levels (m= ±3/2, ±1/2), g=4/3
      ²P_{1/2} ────────    2 levels, g=2/3
  3s  ²S_{1/2} ────────    2 levels, g=2
```

\(D_2={}^2P_{3/2}\to{}^2S_{1/2}\) (stronger); \(D_1={}^2P_{1/2}\to{}^2S_{1/2}\).

For \(3d\to 3p\) of Na see practice problem 9. Three FS lines (not four): \(\Delta J=2\) is E1-forbidden.

### Paschen–Back

\(\mathbf{L}\) and \(\mathbf{S}\) decouple and precess independently about \(\mathbf{B}\). Good quantum numbers: \(m_L,m_S\). Energies

\[
E=\mu_B B(m_L+2m_S)
\]

plus a residual first-order \(\langle\mathbf{L}\cdot\mathbf{S}\rangle= \zeta\hbar^2 m_L m_S\). Optical selection \(\Delta m_L=0,\pm 1\), \(\Delta m_S=0\) collapses the forest back to a **normal triplet** (with small residual structure). Polarisation: π for \(\Delta m_L=0\), σ for \(\Delta m_L=\pm 1\).

### Stark

Perturbation \(H' = e\mathcal{E} z\) (electron charge \(-e\) in field \(\boldsymbol{\mathcal{E}}\parallel z\); sign conventions differ, the *pattern* does not).

- **Hydrogen, linear (first-order) Stark:** \(\ell\)-degeneracy lets opposite-parity states mix. Use parabolic quantum numbers \((n_1,n_2,m)\) with \(n=n_1+n_2+|m|+1\) and

  \[
  \Delta E=\tfrac32 n(n_1-n_2)\,e a_0\,\mathcal{E}.
  \]

  \(n=3\) \(\to\) five components at \(0,\pm 9/2,\pm 9\) (units \(e a_0\mathcal{E}\)).
  \(n=2\) \(\to\) three components at \(0,\pm 3\).

- **Non-hydrogenic:** states have definite parity, \(\langle z\rangle=0\), first-order shift vanishes, **quadratic** Stark \(\propto\mathcal{E}^2\).

Selection / polarisation: π (\(\Delta m=0\)) and σ (\(\Delta m=\pm 1\)). There is no \(\Delta m=\pm 2\) in E1.

---

## H. Interaction with light (semiclassical)

Treat \(\mathbf{E},\mathbf{B}\) classically (Maxwell, Coulomb gauge \(\nabla\cdot\mathbf{A}=0\), often \(\Phi=0\) in free space) and the atom quantum-mechanically.

\[
i\hbar\partial_t\Psi=\left[\frac{1}{2m}(-i\hbar\nabla+e\mathbf{A})^2+V(r)\right]\Psi.
\]

- Identify \(H_0=p^2/2m+V\) and \(H'\approx (e/m)\mathbf{A}\cdot\mathbf{p}\) (drop \(A^2\) unless you want two-photon / AC Stark at high intensity).
- Expand \(\Psi=\sum c_k(t)\,e^{-iE_k t/\hbar}\psi_k\). First-order

  \[
  \dot c_b=(i\hbar)^{-1}\sum_k H'_{bk}(t)\,c_k\, e^{i\omega_{bk}t}.
  \]

- A wave-packet \(\mathbf{A}\) with polarisation \(\hat\epsilon\) produces

  \[
  |c_b^{(1)}(t)|^2=2\int d\omega\left[\frac{eA(\omega)}{m}\right]^2 |M_{ba}|^2 F(t,\omega-\omega_{ba}),
  \]

  with the diffraction-in-time function \(F(t,\bar\omega)=(1-\cos\bar\omega t)/\bar\omega^2\), which \(\to\pi t\,\delta(\bar\omega)\) as \(t\to\infty\). The central lobe has width \(\sim 2\pi/t\).

**Dipole approximation:** \(e^{i\mathbf{k}\cdot\mathbf{r}}\approx 1\) because \(\lambda\gg a_0\). Then \(M\propto\hat\epsilon\cdot\mathbf{r}_{ba}\).

Angular integrals of \(z=r\cos\theta\) (no \(\phi\)) force \(\Delta m=0\); \(x\pm iy\) force \(\Delta m=\pm 1\). Parity of \(Y_{\ell m}\) is \((-1)^\ell\), so E1 changes parity.

Einstein \(A\) (spontaneous) is **not** in semiclassical Maxwell theory; Einstein got it from thermal equilibrium with Planck’s law. QM derives \(B\) from the above, then

\[
A_{21}=\frac{8\pi h\nu^3}{c^3}B_{21}.
\]

Absorption and stimulated emission share the same \(|M|^2\) (they are complementary); spontaneous emission is the extra \(A\).

**Scattering \(\neq\) absorption/emission.** Scattering is a second-order two-photon process (in, then out, possibly via a virtual state). Absorption is first-order, real state, energy conserved on-shell.

---

## I. Widths and shapes

An excited state with mean life \(\tau\) is not monochromatic: \(\Delta E\,\Delta t\sim\hbar\) with \(\Delta t\sim\tau\).

| Mechanism | Shape | Scales as | Notes |
|---|---|---|---|
| Natural | Lorentzian | \(1/\tau\) | homogeneous; independent of \(T\) |
| Doppler | Gaussian | \(\sqrt{T/M}\,\nu_0\) | inhomogeneous; thermal \(v_x\) |
| Pressure / collision | often Lorentzian, can be **asymmetric** | density × σ × \(v\) | shortens effective \(\tau\) |

Natural line (lower level stable):

\[
f(\omega)\propto\frac{(\Gamma/2)^2}{(\omega-\omega_{ba})^2+(\Gamma/2)^2},\qquad\Gamma=1/\tau.
\]

FWHM \(\Delta\omega=\Gamma\), \(\Delta\nu=1/(2\pi\tau)\).

Doppler: map Maxwell \(dN(v_x)\propto e^{-Mv_x^2/2kT}dv_x\) through \(v_x/c=(\nu-\nu_0)/\nu_0\). FWHM is the formula on the sheet. Width \(\neq\) shift: a beam with mean velocity \(v\) is **shifted** by \(v/c\); an oven gas is **broadened** symmetrically (to first order).

Rule of thumb: optical Doppler at 300 K is GHz; natural is MHz (Na D2: \(\tau=16~\mathrm{ns}\Rightarrow\Delta\nu\approx 10~\mathrm{MHz}\)).

---

## J. Multi-electron bookkeeping

**LS coupling** (light atoms, residual Coulomb \(\gg\) spin–orbit):

1. Pauli-allowed \((S,L)\) terms of the configuration.
2. Fine-structure \(J=|L-S|\ldots L+S\).
3. Hund: max \(S\), then max \(L\), then \(J_\min\) (\(<\) half) or \(J_\max\) (\(>\) half).

**jj coupling** (heavy atoms, SO \(\gg\) residual Coulomb): each electron has a good \(j=\ell\pm 1/2\); equivalent-\(j\) occupations are restricted by Pauli on \(m_j\). Use the NIST table, or enumerate \(m_j\) slots, or use hole–particle symmetry.

Platinum ground configuration \([\mathrm{Xe}]4f^{14}5d^9 6s^1\) is a \(d\)-hole plus an \(s\) electron \(\Rightarrow\) terms \({}^3D\) and \({}^1D\). More-than-half \(d^9\) \(\Rightarrow\) inverted FS, GS \({}^3D_3\). Then \(g=4/3\), \(\mu=g\sqrt{J(J+1)}\,\mu_B=(8\sqrt{3}/3)\mu_B\), weak-field span \(=2J g_J\mu_B B=8\mu_B B\).

Helium spin functions: the triplet \(S=1\) subspace is \(\{\lvert\uparrow\uparrow\rangle,\;(\lvert\uparrow\downarrow\rangle+\lvert\downarrow\uparrow\rangle)/\sqrt{2},\;\lvert\downarrow\downarrow\rangle\}\). Each is a simultaneous eigenstate of \(S^2\) and \(S_z\). The singlet is the antisymmetric combination. Problem 15 is the \(\lvert\downarrow\downarrow\rangle\) case done with Pauli matrices.

---

## K. Side topics that showed up in lecture (short questions)

**Photocell vs solar cell.** Both: \(h\nu>E_g\) creates \(e\)–\(h\) pairs at a pn junction. Photocell is **reverse biased** (photocurrent on top of minority saturation current). Solar cell is photovoltaic, **no bias**; charge is separated by the built-in field.

**Faraday cup.** Measures beam current. A suppressor electrode (negative) throws secondary electrons back into the cup so they are not lost.

**King’s experiment.** Tests \(|q_e+q_p|\) to \(\sim 10^{-20}e\). If they differed, an atom would have a residual charge and feel a net Coulomb field; macroscopic matter would not be as electrically neutral as it is. Shielding is irrelevant for a *net* leftover charge.

**Auger / Coster–Kronig.** A core hole is filled by an electron from a higher shell; the energy released ejects another electron. \(K\) of the Auger electron \(= E_\text{hole}-E_1-E_2\), **independent of the photon (or electron) that made the hole**. Coster–Kronig: the filling electron comes from the **same shell** (different subshell). Hydrogen has only one electron, so no Auger.

**Polarisation of Zeeman components.** Viewed along \(\mathbf{B}\): only σ±, circular. Viewed perpendicular: π linear \(\parallel\mathbf{B}\), σ linear \(\perp\mathbf{B}\). Elliptical light: unequal amplitudes and/or phase \(\neq\pi/2\).

**Photoelectric effect (exam trap).** Threshold is a **frequency** condition \(h\nu>W_0\), not an energy-density condition. A very intense red beam still emits nothing if \(\nu<\nu_0\).

**Coherence** of a source grows when many radiators emit with a locked phase (a laser); merely increasing density without phase-locking does not make a thermal lamp coherent.

---

## L. Exotic hydrogenic systems (practice 2, 5, 6)

Anything bound by Coulomb physics is hydrogen with a new \(\mu\) and perhaps a dielectric \(\varepsilon_r\):

\[
E_n=-13.6\,\mathrm{eV}\cdot\frac{\mu}{m_e}\cdot\frac{Z^2}{n^2\varepsilon_r^2},\qquad
a=\frac{\varepsilon_r m_e}{\mu Z}a_0.
\]

- **Pionic atom** \(p^+\pi^-\): \(\mu=m_\pi m_p/(m_\pi+m_p)\). With \(m_\pi=250\,m_e\) you **must** reduce against the proton (\(m_p\approx 1836\,m_e\)); \(\mu\approx 220\,m_e\), not \(250\,m_e\).
- **Muonic atom:** \(\mu\approx 207\,m_e\), orbits \(\sim 200\times\) smaller, huge finite-size effects.
- **Rydberg atom:** \(n\gg 1\), radius \(n^2 a_0\) (microns at \(n\sim 100\)), binding \(13.6/n^2\,\mathrm{eV}\), neighbouring spacing \(\approx 27.2/n^3\,\mathrm{eV}\). Weakly bound, not strongly.
- **Wannier exciton:** \(e\)–\(h\) pair in a semiconductor, \(\varepsilon_r\sim 10\), \(\mu\sim 0.1\)–\(0.7\,m_e\). Rydberg collapses from eV to meV. Absorption: hydrogenic series converging to the band gap, then a continuum.

---

## M. Selection-rule and degeneracy cheat card

| What is conserved / good | Why | What it implies |
|---|---|---|
| \(n\) only (H, no FS) | \(1/r\) Coulomb + SO(4) | \(\ell\)-degeneracy |
| \(\ell\) | any central \(V(r)\) | alkali \(E_{n\ell}\) |
| \(m\) | spherical symmetry | not split until a vector field picks an axis |
| parity \((-1)^\ell\) | inversion | E1 changes it |
| \(S\) | LS, no spin–orbit in \(H'\) | no intercombination (approx.) |
| \(J,m_J\) | isolated atom, no external field | FS labels |
| \(m_L,m_S\) | Paschen–Back | \(L,S\) decoupled |

If you can name **which symmetry is broken** (Coulomb \(\to\) core, spherical \(\to\) \(\mathbf{B}\) or \(\boldsymbol{\mathcal{E}}\), inversion \(\to\) Stark mixing), you can write the splitting without memorising a picture.
