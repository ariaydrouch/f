# Formula sheet — PYL7167 quiz

Memorise boxed items. Stars mark high-frequency exam results.

---

## 1. Hydrogenic energies and spectra

**Bohr / Schrödinger (infinite nuclear mass)**

\[
\boxed{E_n = -\frac{\mu Z^2 e^4}{2(4\pi\epsilon_0)^2\hbar^2}\, \frac{1}{n^2}
= -\,13.6\,\mathrm{eV}\cdot\frac{\mu}{m_e}\cdot\frac{Z^2}{n^2}}
\]

\[
\boxed{\frac{1}{\lambda} = R_M Z^2\left(\frac{1}{n_f^2}-\frac{1}{n_i^2}\right),\qquad
R_M = R_\infty\frac{\mu}{m_e} = \frac{R_\infty}{1+m_e/M}}
\]

\[
R_\infty = \frac{m_e e^4}{8\varepsilon_0^2 h^3 c} = 109\,737.318~\mathrm{cm}^{-1}
\]

Series **limit** (\(n_i\to\infty\)): \(1/\lambda_\infty = R_M Z^2/n_f^2\).

| Series | \(n_f\) | \(\lambda\) range (H) | Region | Overlap? |
|---|---|---|---|---|
| Lyman | 1 | 91.2–121.6 nm | UV | no overlap with Balmer |
| Balmer | 2 | 364.6–656.3 nm | vis → near UV | no overlap with Paschen |
| Paschen | 3 | 820.4–1875 nm | IR | **overlaps Brackett** |
| Brackett | 4 | 1458–4051 nm | IR | **overlaps Paschen and Pfund** |
| Pfund | 5 | 2279–7460 nm | IR | **overlaps Brackett** |

Longest \(\lambda\) in a series: \(n_i = n_f+1\). Shortest = series limit.

**Correspondence principle** (\(n\gg 1\), \(\Delta n=p\) small):

\[
\frac{1}{\lambda}\approx (\text{const})\frac{p}{n^3},\qquad
\omega_\text{orb} = 2\pi\cdot 2Rc/n^3.
\]

Equating classical \(E(\omega)\) to \(E_n=-Rch/n^2\) recovers \(R_\infty\).

**Exotic atoms / excitons** — same formulae with the actual reduced mass and dielectric constant:

\[
\mu_{\pi p}=\frac{m_\pi m_p}{m_\pi+m_p},\qquad
R_\text{ex}=\frac{13.6\,\mathrm{eV}}{\varepsilon_r^2}\frac{\mu}{m_e}.
\]

Wannier exciton: \(E_n=E_g - R_\text{ex}/n^2\). Absorption: hydrogen-like discrete lines plus continuum for \(h\nu>E_g\).

---

## 2. Atomic units, sizes, virial

\[
a_0=0.529~\text{Å},\quad
1~\text{Hartree}=27.2~\mathrm{eV}=2\times 13.6~\mathrm{eV},\quad
v_1=\alpha c=c/137.
\]

\[
\boxed{\langle r\rangle_{nlm}=\frac{a_0 n^2}{Z}\left\{1+\frac12\left[1-\frac{l(l+1)}{n^2}\right]\right\}}
\qquad
\boxed{\left\langle\frac1r\right\rangle_{nlm}=\frac{Z}{a_\mu n^2}}
\]

Most probable radius \(\neq\langle r\rangle\) (the radial tail pulls \(\langle r\rangle\) out). For 1s: \(r_\text{mp}=a_0/Z\), \(\langle r\rangle=1.5\,a_0/Z\).

Rydberg atom: \(r_n=n^2 a_0\), \(E_b=13.6\,\mathrm{eV}/n^2\), weakly bound.

**Virial** for \(V=\alpha r^k\): \(2\langle T\rangle=k\langle V\rangle\).

- Coulomb \(k=-1\): \(\langle T\rangle=-\,E\), \(\langle V\rangle=2E\).
- HO \(k=2\): \(\langle T\rangle=\langle V\rangle\).

**Small-\(r\) radial behaviour:** \(R_{nl}(r)\propto r^{l}\) (the function \(u=rR\propto r^{l+1}\)).

**Unsold:** \(\sum_{m=-l}^{l}|Y_{lm}|^2=(2l+1)/4\pi\) (angle-independent). Closed shells are spherically symmetric.

---

## 3. Alkali atoms and quantum defect

Central field is still spherical (so \(m\) remains degenerate) but **not** pure Coulomb, so **\(l\)-degeneracy dies**.

\[
\boxed{E_{nl}=-R\,hc\left/\bigl(n-\delta_{nl}\bigr)^2\right.}
\]

Penetration: \(\delta_s\gg\delta_p\gg\delta_d\approx\delta_f\approx 0\). For Li (your notes): \(\delta_s\approx 0.4\), \(\delta_p\approx 0.04\), \(\delta_{d,f}\approx 0\).

Ground state of Li: \(1s^2 2s\; {}^2S_{1/2}\). Resonance line \(2p\to 2s\).

Why \(l<n\): radial quantum number \(n_r=n-l-1\ge 0\).

---

## 4. Angular momentum, terms, coupling

\[
\mathbf{J}=\mathbf{L}+\mathbf{S},\qquad
\mathbf{L}\cdot\mathbf{S}=\frac12\bigl(J^2-L^2-S^2\bigr)
\]

Term: \(\boxed{^{2S+1}L_J}\) with \(L=S,P,D,F,\ldots\) (\(L=0,1,2,3,\ldots\)).

**LS (light atoms):** \(\mathbf{L}=\sum\mathbf{l}_i\), \(\mathbf{S}=\sum\mathbf{s}_i\), then \(\mathbf{J}=\mathbf{L}+\mathbf{S}\).
**jj (heavy atoms):** \(\mathbf{j}_i=\mathbf{l}_i+\mathbf{s}_i\), then \(\mathbf{J}=\sum\mathbf{j}_i\).

Two nonequivalent electrons \(\ell_1=1,\ell_2=2\):

\[
L=1,2,3,\quad S=0,1
\quad\Rightarrow\quad
{}^1P,{}^1D,{}^1F,{}^3P,{}^3D,{}^3F
\]

with \(J=|L-S|\ldots L+S\).

**Hund (LS, equivalent electrons):** (1) max \(S\); (2) then max \(L\); (3) \(J_\min\) if shell \(<\) half full, \(J_\max\) if \(>\) half full.

**jj equivalent electrons** \(j=5/2\):

\[
(5/2)^1,^5:\;J=5/2;\quad
(5/2)^2,^4:\;J=0,2,4;\quad
(5/2)^3:\;J=3/2,5/2,9/2;\quad
(5/2)^6:\;J=0.
\]

Hole–particle: \((j)^{2j+1-N}\) has the same \(J\) list as \((j)^N\).

**Magnetic moment (weak \(B\))**

\[
\boxed{\boldsymbol{\mu}_J=-g_J\mu_B\mathbf{J}/\hbar,\qquad
g_J=1+\frac{J(J+1)+S(S+1)-L(L+1)}{2J(J+1)}}
\]

\[
\mu=g_J\sqrt{J(J+1)}\,\mu_B,\qquad
\Delta E=g_J\mu_B B m_J.
\]

\(g_L=1\), \(g_S=2.0023\approx 2\). Gyromagnetic: \(\omega_L=\gamma B\), \(\gamma_L=e/2m\), \(\gamma_S\approx e/m\).

Helium: para \(S=0\) (singlets, incl. GS \(1s^2\;{}^1S_0\)); ortho \(S=1\) (triplets). Intercombination lines are E1-forbidden \(\Rightarrow\) two superimposed spectra.

---

## 5. Fine structure (spin–orbit)

Internal \(\mathbf{B}\) of orbital motion + Thomas factor \(1/2\):

\[
V_{LS}=\frac{Ze^2\mu_0}{8\pi m_e^2 r^3}\,\mathbf{S}\cdot\mathbf{L}
=\frac{a}{2}\bigl[j(j+1)-l(l+1)-s(s+1)\bigr]
\]

\[
\left\langle\frac1{r^3}\right\rangle=\frac{Z^3}{a_H^3 n^3 l(l+\tfrac12)(l+1)}
\quad(l\ge 1)
\]

Interval between \(j=l+\tfrac12\) and \(j=l-\tfrac12\):

\[
\boxed{\Delta E_{fs}\propto\frac{Z^4}{n^3\,l(l+1)}}
\]

(the \(l+\tfrac12\) in the denominator cancels against the Landé interval). Hydrogen-like scaling is \(Z^4/n^3\).

Dirac / rel. QM: \(E=E(n,j)\) not \(E(n,l)\). Lamb shift (QED) splits \(2S_{1/2}\) **above** \(2P_{1/2}\) by \(1057.8~\mathrm{MHz}\approx 0.035~\mathrm{cm}^{-1}\) (lecture slip: this is **not** 0.031 eV). \(2S_{1/2}\) is **metastable** (E1 \(2S\to 1S\) forbidden, \(\Delta l=0\)).

---

## 6. External fields

**Stern–Gerlach**

\[
U=-\boldsymbol{\mu}\cdot\mathbf{B},\qquad
F_z\approx\mu_z\frac{\partial B_z}{\partial z}
\]

(\(F_x,F_y\) neglected if \(\partial B_z/\partial z\) dominates.) \(^2S_{1/2}\) alkali: 2 beams, \(\mu_z=\pm\mu_B\). Cannot be done with free electrons (Lorentz force \(q\mathbf{v}\times\mathbf{B}\) swamps the spin force).

Deflection of one component after magnet length \(L\) plus drift \(l\), speed \(v\):

\[
\boxed{s=\frac{\mu_z}{M}\frac{\partial B_z}{\partial z}\frac{L}{v^2}\left(l+\frac{L}{2}\right)}
\qquad\text{spot separation }=2s
\]

Use \(v=\sqrt{2kT/M}\) (most probable) unless told otherwise.

**Zeeman Hamiltonian**

\[
H'= \frac{\mu_B}{\hbar}(\mathbf{L}+2\mathbf{S})\cdot\mathbf{B}
=\mu_B B(L_z+2S_z)/\hbar
\]

| Regime | Criterion | Energies | Pattern |
|---|---|---|---|
| Weak / anomalous | \(\mu_B B\ll E_{fs}\) | \(g_J\mu_B B m_J\) | many uneven components |
| Normal | \(S=0\) so \(g=1\) | \(\mu_B B m_L\) | Lorentz triplet |
| Paschen–Back | \(\mu_B B\gg E_{fs}\) | \(\mu_B B(m_L+2m_S)\) | normal triplet restored |

E1 selection: \(\Delta m_J=0\) (**π**, linear \(\parallel\mathbf{B}\)), \(\Delta m_J=\pm 1\) (**σ**, circular about \(\mathbf{B}\); linear \(\perp\mathbf{B}\) when viewed from the side). Also \(\Delta J=0,\pm1\) (not \(0\to 0\)), \(\Delta L=\pm 1\), \(\Delta S=0\), \(\Delta m_S=0\) (Paschen–Back).

**Landé \(g\) values you will need**

| Term | \(g_J\) |
|---|---|
| \(^2S_{1/2}\) | \(2\) |
| \(^2P_{1/2}\) | \(2/3\) |
| \(^2P_{3/2}\) | \(4/3\) |
| \(^2D_{3/2}\) | \(4/5\) |
| \(^2D_{5/2}\) | \(6/5\) |
| \(^1P_1,{}^1D_2\) (singlets) | \(1\) |

**Linear Stark (hydrogen only, first order)** because of \(\ell\)-degeneracy.

\[
\Delta E=\frac32 n(n_1-n_2)\,e a_0\,\mathcal{E}
\]

\(n=n_1+n_2+|m|+1\).

- \(n=2\): three levels, \(\Delta E=0,\pm 3\,e a_0\mathcal{E}\).
- \(n=3\): five levels, \(\Delta E=0,\pm\tfrac92 e a_0\mathcal{E},\pm 9\,e a_0\mathcal{E}\).

Alkali / non-H: only **quadratic** Stark (no first-order shift of nondegenerate states with definite parity).

Polarisation: π if \(\Delta m=0\) (\(\mathbf{E}_\text{light}\parallel\boldsymbol{\mathcal{E}}\)), σ if \(\Delta m=\pm 1\).

---

## 7. Radiation, Einstein, selection rules

Semiclassical: field classical, atom quantum. Coulomb gauge \(\nabla\cdot\mathbf{A}=0\).

\[
H=\frac1{2m}(\mathbf{p}+e\mathbf{A})^2+V,\qquad
\text{drop }A^2\text{ at low intensity (keeping it }=\text{ multiphoton).}
\]

First-order TDPT, long-time limit \(F(t,\bar\omega)\to\pi t\,\delta(\bar\omega)\):

\[
|c_b|^2 \propto \underbrace{\bigl[e A(\omega_{ba})/m\bigr]^2}_{\text{intensity}}\underbrace{|M_{ba}|^2}_{\text{atom}}\, t
\]

**Dipole (E1):** \(e^{i\mathbf{k}\cdot\mathbf{r}}\approx 1\), rate \(\propto|\hat{\epsilon}\cdot\mathbf{r}_{ba}|^2\).

**E1 selection**

\[
\Delta \ell=\pm 1,\quad \Delta m=0,\pm 1,\quad \Delta S=0,\quad
\Delta J=0,\pm 1\ (J=0\not\to J=0),\quad \text{parity changes.}
\]

\(\Delta m=0\): linear (z, π). \(\Delta m=\pm 1\): circular (σ±, \(x\pm iy\)).

Dipole-forbidden \(\neq\) strictly forbidden (M1, E2, two-photon, collisions).

Einstein (energy density per Hz):

\[
\boxed{A_{21}=\frac{8\pi h\nu^3}{c^3}B_{21},\qquad
B_{12}=\frac{g_2}{g_1}B_{21}}
\]

(Notes’ angular-frequency form: \(A=\hbar\omega^3 B/\pi^2 c^3\).)

Stimulated rate \(\propto\) intensity / energy density. Spontaneous \(A\) is not.

Natural (Lorentzian) FWHM of a line to a stable lower level:

\[
\boxed{\Delta E=\hbar/\tau,\qquad \Delta\nu=\frac{1}{2\pi\tau},\qquad
\Delta\lambda=\frac{\lambda^2}{c}\Delta\nu}
\]

\(\tau=\) **mean** life. If half-life is given, \(\tau=t_{1/2}/\ln 2\).

---

## 8. Line shapes

**Doppler (Gaussian), FWHM**

\[
\boxed{\Delta\nu_D=\frac{2\nu_0}{c}\sqrt{\frac{2kT\ln 2}{M}}
\qquad
\Delta\lambda_D=\frac{2\lambda_0}{c}\sqrt{\frac{2kT\ln 2}{M}}}
\]

\[
I(\nu)=I(\nu_0)\exp\left[-\frac{Mc^2}{2kT}\left(\frac{\nu-\nu_0}{\nu_0}\right)^2\right]
\]

Doppler **shift** of one velocity class: \(\Delta\nu/\nu=v/c\). Doppler **width** is the FWHM of the thermal envelope.

Voigt = Lorentz (natural/pressure) ⊗ Gaussian (Doppler). Core often Doppler, far wings natural. Pressure broadening: collisions, can be **asymmetric**, and shortens lifetime.

---

## 9. Odds that lectures flagged

- Optical electron = valence electron that is excited. Equivalent electrons share \((n,\ell)\).
- Line spectra: atoms. Band: molecules/solids. Continuous: BBR / free–bound.
- Photocell: reverse-biased pn, \(h\nu>E_g\). Solar cell: same physics, **no** bias.
- Auger kinetic energy is a **difference of binding energies**; independent of the photon that dug the hole. (Coster–Kronig = intra-shell Auger.)
- King: \(|q_p+q_e|\lesssim 10^{-20}e\) (atoms are neutral; no long-range Coulomb leftover).
- Classical radiative collapse of H: Larmor, \(T\sim 10^{-11}\,\mathrm{s}\) (not ms).
- Relativistic mass correction to \(R\) is **not** enough for \(Z\gtrsim 20\).
