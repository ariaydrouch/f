# Practice problems — fully worked solutions

**Use these as the quiz.** Cover the answer, solve on paper, then check. Numerical values use \(R_\infty=109\,737.318~\mathrm{cm}^{-1}\), \(13.6\,\mathrm{eV}\), \(a_0=0.529~\text{Å}\), \(m_p/m_e=1836\), \(M_D/m_e=3670.5\), \(k_B=1.381\times 10^{-23}\,\mathrm{J\,K}^{-1}\).

A one-line key is at the very bottom if you need a last-minute dump.

---

## Problem 1 — Series limit of deuterium, \(n=4\)

**Ask.** Series containing all transitions \(m(>n)\to n=4\) in **deuterium**. Quote \(R_\infty=(109\,737.318\pm 0.012)~\mathrm{cm}^{-1}\).

**Physics.** This is the Brackett series. The series limit is the ionisation threshold from \(n=4\):

\[
\bar\nu_\infty = \frac{1}{\lambda_\infty}=R_D\cdot\frac{1}{4^2}=\frac{R_D}{16}.
\]

You **must** convert \(R_\infty\to R_D\). The notes spent a page on this, and the uncertainty on \(R_\infty\) is given so that a 60 cm⁻¹ reduced-mass shift is obviously required.

\[
R_D=\frac{R_\infty}{1+m_e/M_D},\qquad \frac{M_D}{m_e}\approx 3670.48
\quad(\text{deuteron, not }2m_p).
\]

\[
R_D=109\,737.318\times\frac{3670.48}{3671.48}=109\,707.43~\mathrm{cm}^{-1}.
\]

(Using \(M_D=2m_p=3672\,m_e\) changes the result by \(<0.03~\mathrm{cm}^{-1}\).)

\[
\bar\nu_\infty=\frac{109\,707.43}{16}=6856.71~\mathrm{cm}^{-1}.
\]

Propagating the given uncertainty: \(\delta\bar\nu=\delta R_\infty/16=0.00075~\mathrm{cm}^{-1}\), negligible next to the reduced-mass modelling.

\[
\lambda_\infty=\frac{1}{6856.71~\mathrm{cm}^{-1}}=1.4584\times 10^{-4}~\mathrm{cm}
=\boxed{1458.4~\mathrm{nm}=14\,584~\text{Å}}.
\]

**Write on the paper:** \(\bar\nu_\infty=6856.71~\mathrm{cm}^{-1}\) **and** \(\lambda_\infty=1458.4~\mathrm{nm}\). Either is the “series limit”; wavenumber is the more natural spectroscopic quantity.

**Trap.** Using \(R_\infty\) raw gives \(6858.58~\mathrm{cm}^{-1}\) — wrong at the level they can see. Using \(R_H\) (protium) is also wrong; they asked for deuterium.

---

## Problem 2 — Pionic atom, \(n=4\) vs \(n=6\)

**Ask.** Energy difference in eV between \(n=4\) and \(n=6\) of \(p^+\pi^-\). Use \(m_\pi=250\,m_e\).

This is hydrogenic with reduced mass

\[
\mu=\frac{m_\pi m_p}{m_\pi+m_p}
=\frac{250\times 1836}{250+1836}\,m_e
=220.0\,m_e.
\]

(The proton is *not* infinitely heavy compared with the pion. The parenthetical “use \(m_\pi=250\,m_e\)” gives you the pion mass, not permission to skip \(\mu\).)

\[
E_n=-13.6\,\mathrm{eV}\cdot\frac{\mu}{m_e}\cdot\frac{1}{n^2}.
\]

The 6-level is **higher** (less negative) than the 4-level:

\[
\Delta E=E_6-E_4
=13.6\times 220.0\times\left(\frac{1}{16}-\frac{1}{36}\right)
=13.6\times 220.0\times\frac{5}{144}
=\boxed{103.9~\mathrm{eV}\approx 104~\mathrm{eV}}.
\]

Naive replacement \(m_e\to 250\,m_e\) (no reduced mass) gives \(118~\mathrm{eV}\). If the answer key was written that way you will be close, but the lecture on \(R_H\neq R_\infty\) tells you to reduce.

---

## Problem 3 — Natural width of the sodium \(D_2\) line

**Ask.** Lifetime (half-life) of \(3\,{}^2P_{3/2}\) is \(1.6\times 10^{-8}\,\mathrm{s}\). Natural width of \(3\,{}^2P_{3/2}\to 3\,{}^2S_{1/2}\).

**Mean life vs half-life.** In atomic physics “lifetime of a level” **is the mean life** \(\tau\). The parenthetical “(half-life)” is sloppy; the number \(16~\mathrm{ns}\) is the standard mean life of Na \(3p\) (natural width of \(D_2\) is the famous \(\approx 10~\mathrm{MHz}\)). Use \(\tau=1.6\times 10^{-8}\,\mathrm{s}\). If they truly meant \(t_{1/2}\), \(\tau=t_{1/2}/\ln 2\).

Lower level is the ground state (\(\tau=\infty\)), so \(\Gamma=1/\tau\).

\[
\Delta E=\frac{\hbar}{\tau}
=\frac{1.055\times 10^{-34}}{1.6\times 10^{-8}}
=6.59\times 10^{-27}~\mathrm{J}
=\boxed{4.11\times 10^{-8}~\mathrm{eV}}.
\]

\[
\Delta\nu=\frac{\Delta E}{h}=\frac{1}{2\pi\tau}
=\boxed{9.95~\mathrm{MHz}}.
\]

\(D_2\) wavelength \(\lambda=589.0~\mathrm{nm}=5890~\text{Å}\):

\[
\Delta\lambda=\frac{\lambda^2}{c}\Delta\nu
=1.15\times 10^{-14}~\mathrm{m}
=\boxed{1.15\times 10^{-4}~\text{Å}}.
\]

Wavenumber: \(\Delta\bar\nu=\Delta\nu/c=3.32\times 10^{-4}~\mathrm{cm}^{-1}\).

**Any of \(\Delta E\), \(\Delta\nu\), \(\Delta\lambda\), \(\Delta\bar\nu\) is a valid “width”.** The spectroscopic default is \(\Delta\nu\) in MHz or \(\Delta\bar\nu\) in cm⁻¹. \(\Delta\lambda\) in Å is tiny because \(\lambda\) is optical and the line is so sharp.

**Trap.** Using \(\Delta\nu=1/\tau=62.5~\mathrm{MHz}\) (forgetting \(2\pi\)). Using \(D_1\) (589.6 nm) instead of \(D_2\) (589.0 nm) — they named \(D_2\).

---

## Problem 4 — Do the hydrogen series overlap?

**Yes, but only in the infrared.** Compare longest \(\lambda\) of series \(n\) with shortest \(\lambda\) (limit) of series \(n+1\).

From the table in lecture 3 (H atom, nm):

| Series | \(n_f\) | Longest \(\lambda\) | Limit \(\lambda_\infty\) | Region |
|---|---|---|---|---|
| Lyman | 1 | 121.6 | 91.2 | UV |
| Balmer | 2 | 656.3 | 364.6 | vis / near UV |
| Paschen | 3 | 1875 | 820.4 | IR |
| Brackett | 4 | 4051 | 1458 | IR |
| Pfund | 5 | 7460 | 2279 | IR |

Check adjacent pairs:

- Lyman longest 121.6 **<** Balmer shortest 364.6 → **no overlap**.
- Balmer longest 656.3 **<** Paschen shortest 820.4 → **no overlap**.
- Paschen longest 1875 **>** Brackett shortest 1458 → **overlap**.
- Brackett longest 4051 **>** Pfund shortest 2279 → **overlap**.

Analytic test: series \(n\) and \(n+1\) overlap iff the \(n\to n\) ionisation limit of the higher series sits redward of the first line of the lower one, i.e. iff

\[
\frac{1}{n^2} < \frac{1}{(n+1)^2}-\frac{1}{(n+2)^2}
\quad\text{fails for }n=1,2\text{ and holds for }n\ge 3.
\]

**Answer to write:** Lyman and Balmer do **not** overlap anything neighbouring. Paschen–Brackett–Pfund **do** overlap in the IR. (Paschen also just reaches Brackett; Pfund overlaps Brackett and the next series.)

---

## Problem 5 — Two-laser pumping of H Rydberg states

**Setup.** Ground-state H. Laser 1 fixed at \(11.5~\mathrm{eV}\). Laser 2 tunable. Populate a **single** \(n\in\{20,30,40,50\}\).

Energy to climb from \(n=1\) to \(n\):

\[
\Delta E_{1\to n}=13.6\left(1-\frac{1}{n^2}\right)~\mathrm{eV}.
\]

Laser 1 already supplies 11.5 eV, so laser 2 must supply the rest (additive two-photon / two-colour absorption from the ground state; 11.5 eV itself is **not** resonant with a low-\(n\) Bohr level — \(13.6(1-1/n^2)=11.5\Rightarrow n\approx 2.55\)).

\[
E_2=13.6\left(1-\frac{1}{n^2}\right)-11.5
=2.1-\frac{13.6}{n^2}~\mathrm{eV},
\qquad
\lambda_2=\frac{hc}{E_2}=\frac{1240~\mathrm{eV\,nm}}{E_2}.
\]

Bohr radius of the state: \(r_n=n^2 a_0=n^2\times 0.529~\text{Å}\).
Binding: \(E_b=13.6/n^2~\mathrm{eV}\).

| \(n\) | \(E_2\) (eV) | \(\lambda_2\) (nm) | \(r_n\) | \(E_b\) (eV) | \(\lvert E_n-E_{n+1}\rvert\) (eV) |
|---|---|---|---|---|---|
| 20 | 2.066 | **600.1** | \(212~\text{Å}=21.2~\mathrm{nm}\) | 0.03400 | \(3.16\times 10^{-3}\) |
| 30 | 2.085 | **594.7** | \(476~\text{Å}\) | 0.01511 | \(9.59\times 10^{-4}\) |
| 40 | 2.092 | **592.8** | \(846~\text{Å}\) | 0.00850 | \(4.10\times 10^{-4}\) |
| 50 | 2.095 | **591.9** | \(1323~\text{Å}=0.132~\mu\mathrm{m}\) | 0.00544 | \(2.11\times 10^{-4}\) |

(Lecture flagged “Rydberg atom in micron”: that is \(n\sim 10^2\). At \(n=50\) you are at \(0.13~\mu\mathrm{m}\).)

**Maximum laser linewidth so that only one \(n\) is populated.**

The tightest neighbouring gap among the targets is \(n=50\leftrightarrow 51\):

\[
\Delta E_{50,51}=13.6\left(\frac{1}{50^2}-\frac{1}{51^2}\right)=2.11\times 10^{-4}~\mathrm{eV}.
\]

The two photons add, so the **sum** of the two lasers’ energy uncertainties must stay below half that gap (to miss the neighbour on both sides):

\[
\delta E_1+\delta E_2 \;<\; \tfrac12\Delta E_{50,51}
=1.06\times 10^{-4}~\mathrm{eV}.
\]

In frequency: \(1.06\times 10^{-4}\,\mathrm{eV}/h=25.5~\mathrm{GHz}\).

If the budget is split equally, each laser \(\delta E\lesssim 5\times 10^{-5}\,\mathrm{eV}\) (\(\approx 13~\mathrm{GHz}\)).

For laser 2 near \(592~\mathrm{nm}\),

\[
\delta\lambda_2=\lambda_2\frac{\delta E_2}{E_2}
\approx 592~\mathrm{nm}\times\frac{5\times 10^{-5}}{2.095}
\approx 0.014~\mathrm{nm}=0.14~\text{Å}.
\]

Laser 1 (\(E_1=11.5~\mathrm{eV}\), \(\lambda_1=hc/11.5\approx 108~\mathrm{nm}\)):

\[
\delta\lambda_1\approx 108~\mathrm{nm}\times\frac{5\times 10^{-5}}{11.5}\approx 4.7\times 10^{-4}~\mathrm{nm}.
\]

**Write:** \(\delta\nu_1+\delta\nu_2\lesssim 25~\mathrm{GHz}\) (or \(\delta E_\text{tot}<1.1\times 10^{-4}\,\mathrm{eV}\)). Mention that \(n=50\) sets the bound.

---

## Problem 6 — Wannier exciton in \(\mathrm{Cu_2O}\)

Electron + hole in a medium with \(\varepsilon_r\approx 10\), \(\mu\approx 0.7\,m_0\). Bohr model with scaled Coulomb \(e^2/4\pi\epsilon_0\varepsilon_r r\) and mass \(\mu\):

\[
R_\text{ex}=13.6~\mathrm{eV}\cdot\frac{\mu}{m_e}\cdot\frac{1}{\varepsilon_r^2}
=13.6\times 0.7\times\frac{1}{100}
=\boxed{95.2~\mathrm{meV}}.
\]

Levels measured from the band gap \(E_g\):

\[
E_n=E_g-\frac{R_\text{ex}}{n^2}.
\]

**(a)** Binding energies of the excited excitons (i.e. \(E_g-E_n=R_\text{ex}/n^2\)):

| \(n\) | \(R_\text{ex}/n^2\) |
|---|---|
| 2 | **23.8 meV** |
| 3 | **10.6 meV** |
| 4 | **5.95 meV** |
| 5 | **3.81 meV** |

(If they want the signed energies of the states, write \(E_n-E_g=-R_\text{ex}/n^2\).)

**(b) Absorption spectrum.** Exactly hydrogenic:

- a discrete series of lines at \(h\nu=E_g-R_\text{ex}/n^2\), \(n=1,2,3,\ldots\), crowding toward \(E_g\);
- oscillator strength falling \(\sim 1/n^3\);
- a **continuum** for \(h\nu>E_g\) (unbound \(e\)–\(h\) pair, Sommerfeld-enhanced at threshold);
- the \(n=1\) line is strongest and sits \(95~\mathrm{meV}\) below the gap.

This is the yellow series of \(\mathrm{Cu_2O}\), the textbook Wannier exciton (Kittel).

---

## Problem 7 — Scale spin–orbit from H \(2p\) to \(\mathrm{Li}^{2+}\) \(5p\)

Given \(\Delta E_{2p}(\mathrm{H})=0.3~\mathrm{eV}\) (a fake, scaled number). Find \(\Delta E_{5p}(\mathrm{Li}^{2+})\).

Hydrogenic FS interval

\[
\Delta E_{fs}(n,\ell,Z)\propto\frac{Z^4}{n^3\,\ell(\ell+1)}.
\]

Both are \(p\) (\(\ell=1\)), so \(\ell\) cancels.

\[
\frac{\Delta E(\mathrm{Li}^{2+},5p)}{\Delta E(\mathrm{H},2p)}
=\left(\frac{3}{1}\right)^4\left(\frac{2}{5}\right)^3
=81\times\frac{8}{125}
=5.184.
\]

\[
\Delta E=\;0.3\times 5.184=\boxed{1.555~\mathrm{eV}}.
\]

**Trap.** Using \(Z^3\) (the energy itself is \(Z^2\); SO is \(Z^4\)). Using \(n^4\). Forgetting that \(\mathrm{Li}^{2+}\) is hydrogenic with \(Z=3\), not neutral Li.

---

## Problem 8 — Doppler FWHM of H and D, \(m=5\to n=4\), \(T=5000~\mathrm{K}\)

Transition: Brackett-\(\alpha\),

\[
\frac{1}{\lambda}=R\left(\frac{1}{16}-\frac{1}{25}\right)=R\cdot\frac{9}{400}.
\]

\[
\lambda_H=\frac{400}{9 R_H},\qquad R_H=109\,677.6~\mathrm{cm}^{-1}
\;\Rightarrow\;\lambda_H=4.0523\times 10^{-4}~\mathrm{cm}=\boxed{40\,523~\text{Å}}.
\]

\[
\lambda_D=\frac{400}{9 R_D}=40\,512~\text{Å}.
\]

FWHM (Gaussian Doppler):

\[
\Delta\lambda_D=\frac{2\lambda_0}{c}\sqrt{\frac{2kT\ln 2}{M}}.
\]

\(T=5000~\mathrm{K}\), \(M_H=1.67\times 10^{-27}~\mathrm{kg}\), \(M_D=2M_H\), \(c=3.00\times 10^8~\mathrm{m\,s}^{-1}\).

\[
\sqrt{\frac{2kT\ln 2}{M_H}}
=\sqrt{\frac{2(1.381\times 10^{-23})(5000)(0.693)}{1.67\times 10^{-27}}}
=7.57\times 10^3~\mathrm{m\,s}^{-1}.
\]

\[
\Delta\lambda_H=\frac{2\times 4.052\times 10^{-6}~\mathrm{m}}{3.00\times 10^8}\times 7.57\times 10^3
=2.04\times 10^{-10}~\mathrm{m}
=\boxed{2.04~\text{Å}}.
\]

\[
\Delta\lambda_D=\Delta\lambda_H/\sqrt{2}\times(\lambda_D/\lambda_H)
\approx\boxed{1.45~\text{Å}}.
\]

(The \(\lambda_D/\lambda_H\approx 1\) factor is a 0.03 % correction; \(\sqrt{M_H/M_D}=1/\sqrt{2}\) dominates.)

**Traps.** Using rms vs most-probable speed in place of the FWHM factor \(\sqrt{2\ln 2}\) (that would be a different width definition). Reporting Hz instead of Å. Using \(R_\infty\) for both (tiny error on \(\lambda\), none on the \(\sqrt{1/M}\) ratio).

---

## Problem 9 — Na \(3d\to 3p\): FS, anomalous Zeeman, Paschen–Back, polarisation

### 9.1 Fine structure (zero field)

Configuration: valence \(3d\) (\(^2D\)) \(\to\) \(3p\) (\(^2P\)).

\[
\begin{align*}
3d&: {}^2D_{5/2},\; {}^2D_{3/2},\\
3p&: {}^2P_{3/2},\; {}^2P_{1/2}.
\end{align*}
\]

E1: \(\Delta\ell=\pm 1\) (ok), \(\Delta S=0\) (ok), \(\Delta J=0,\pm 1\) **not** \(0\to 0\).

| Upper \(\to\) lower | \(\Delta J\) | Allowed? |
|---|---|---|
| \(^2D_{5/2}\to{}^2P_{3/2}\) | \(-1\) | yes (strongest) |
| \(^2D_{5/2}\to{}^2P_{1/2}\) | \(-2\) | **no** |
| \(^2D_{3/2}\to{}^2P_{3/2}\) | \(0\) | yes |
| \(^2D_{3/2}\to{}^2P_{1/2}\) | \(+1\) | yes |

**Three lines**, not four. Inverted or regular: \(3p\) and \(3d\) of Na are both less than half-filled valence, so regular (higher \(J\) higher in energy). Sketch:

```
            ²D_{5/2}  ────────────────
    3d      ²D_{3/2}  ────────────
                 \        |    \
                  \       |     \
                   \      |      \
            ²P_{3/2} ─────────────
    3p      ²P_{1/2}  ────────
```

(The missing line is \(^2D_{5/2}\to{}^2P_{1/2}\).)

### 9.2 Landé \(g\)-factors (need these for relative Zeeman spacings)

\[
g_J=1+\frac{J(J+1)+S(S+1)-L(L+1)}{2J(J+1)}
\]

| Level | \(L\) | \(S\) | \(J\) | \(g_J\) |
|---|---|---|---|---|
| \(^2D_{5/2}\) | 2 | 1/2 | 5/2 | **6/5 = 1.2** |
| \(^2D_{3/2}\) | 2 | 1/2 | 3/2 | **4/5 = 0.8** |
| \(^2P_{3/2}\) | 1 | 1/2 | 3/2 | **4/3 ≈ 1.333** |
| \(^2P_{1/2}\) | 1 | 1/2 | 1/2 | **2/3 ≈ 0.667** |

Weak-field energies: \(E=E_{FS}+g_J\mu_B B\, m_J\), \(m_J=-J,\ldots,+J\).

### 9.3 Anomalous Zeeman, one FS line as a template

Take the strongest line \(^2D_{5/2}\to{}^2P_{3/2}\).

Upper: 6 sublevels, spacing \(1.2\,\mu_B B\).
Lower: 4 sublevels, spacing \(1.333\,\mu_B B\).

Selection \(\Delta m_J=0,\pm 1\):

- **π** (\(\Delta m_J=0\)): four lines, relative shifts
  \(\mu_B B\,(g_u-g_l)m\) with \(m=\pm 3/2,\pm 1/2\),
  i.e. \(\pm 1.5(1.2-4/3)\), \(\pm 0.5(1.2-4/3)\)
  \(= \mp 0.200,\;\mp 0.0667\) in units \(\mu_B B\).
- **σ±** (\(\Delta m_J=\pm 1\)): six lines each side, shifts
  \(g_u m_u-g_l m_l\) with \(m_u=m_l\pm 1\).

You do **not** need every number if the paper says “show”. Draw:

```
  ²D_{5/2}   m =  -5/2  -3/2  -1/2  +1/2  +3/2  +5/2
              even spacing  (6/5) μB B

  ²P_{3/2}   m =       -3/2  -1/2  +1/2  +3/2
              even spacing  (4/3) μB B

  π: vertical arrows (Δm=0)
  σ⁺: arrows one step right (Δm=+1)
  σ⁻: arrows one step left  (Δm=−1)
```

Repeat the same picture for the other two FS lines (\(^2D_{3/2}\to{}^2P_{3/2}\) and \(^2D_{3/2}\to{}^2P_{1/2}\)). Polarisation:

- viewed **\(\perp\mathbf{B}\)**: π linear \(\parallel\mathbf{B}\), σ linear \(\perp\mathbf{B}\);
- viewed **along \(\mathbf{B}\)**: only σ, right/left circular; π is absent (no longitudinal \(E_z\)).

### 9.4 Paschen–Back (\(\mu_B B\gg E_{FS}\))

Decouple: good quantum numbers \(m_\ell,m_s\) with

\[
E=\mu_B B(m_\ell+2m_s).
\]

\(3d\): \(m_\ell=-2,-1,0,1,2\), \(m_s=\pm 1/2\) → 10 states at
\(\mu_B B\times\{-3,-2,-1,0,+1,+2,+3\}\)
(the extremes \(\pm 3\) are unique: \(m_\ell=\pm 2,m_s=\pm 1/2\); the inner values are degenerate before residual SO).

\(3p\): \(m_\ell=-1,0,1\), \(m_s=\pm 1/2\) → 6 states at
\(\mu_B B\times\{-2,-1,0,+1,+2\}\).

Optical: \(\Delta m_\ell=0,\pm 1\), \(\mathbf{\Delta m_s=0}\) (the light does not flip spin). Then

\[
\Delta E=\mu_B B\,\Delta m_\ell \in \{-\mu_B B,\;0,\;+\mu_B B\}.
\]

**Normal Lorentz triplet**, independent of the residual \(\mathbf{L}\cdot\mathbf{S}\). Polarisation: π (\(\Delta m_\ell=0\)), σ± (\(\Delta m_\ell=\pm 1\)). Residual SO merely broadens / weakly splits each of the three.

---

## Problem 10 — LS terms for \(\ell_1=1\), \(\ell_2=2\) (nonequivalent)

Nonequivalent, so Pauli does not kill terms.

\[
L=|\ell_1-\ell_2|\ldots \ell_1+\ell_2=1,2,3 \quad\Rightarrow\quad P,D,F.
\]
\[
S=0,1 \quad\Rightarrow\quad \text{singlets and triplets}.
\]

| Term | \(L\) | \(S\) | \(J=\lvert L-S\rvert\ldots L+S\) | Symbols |
|---|---|---|---|---|
| singlet P | 1 | 0 | 1 | \(^1P_1\) |
| singlet D | 2 | 0 | 2 | \(^1D_2\) |
| singlet F | 3 | 0 | 3 | \(^1F_3\) |
| triplet P | 1 | 1 | 0,1,2 | \(^3P_0,{}^3P_1,{}^3P_2\) |
| triplet D | 2 | 1 | 1,2,3 | \(^3D_1,{}^3D_2,{}^3D_3\) |
| triplet F | 3 | 1 | 2,3,4 | \(^3F_2,{}^3F_3,{}^3F_4\) |

**Answer:** \(L=1,2,3\), \(S=0,1\), terms \(^{1,3}P,D,F\) with the ten levels listed.

---

## Problem 11 — Stern–Gerlach, potassium, \(P_2P_3\)

K ground state \(4s\;{}^2S_{1/2}\): two beams, \(\mu_z=\pm\mu_B\). \(T=700~\mathrm{K}\), \(\partial B_z/\partial z=10^3~\mathrm{T\,m}^{-1}\), \(L=0.1~\mathrm{m}\), \(\ell=1~\mathrm{m}\).

**Geometry (standard lecture figure).** Magnet of length \(L\) along the beam, then a field-free flight of length \(\ell\) to the plate. Spots \(P_2,P_3\) are the two components. (If *your* figure swaps the labels, swap \(L\leftrightarrow\ell\) in the last line; the derivation does not change.)

Force \(F_z=\mu_B\partial B_z/\partial z\) (constant), acceleration \(a=F_z/M\). Time in the magnet \(t_1=L/v\). Deflection at magnet exit \(\tfrac12 a t_1^2\), plus extra \(\,a t_1\cdot(\ell/v)\) during the drift:

\[
s=\frac{\mu_B}{M}\frac{\partial B_z}{\partial z}\,\frac{L}{v^2}\left(\ell+\frac{L}{2}\right).
\]

Most probable thermal speed \(v=\sqrt{2kT/M}\) (Maxwell peak; lecture used this for order-of-magnitude SG).

Potassium: \(M=39.1\,\mathrm{u}=6.49\times 10^{-26}~\mathrm{kg}\).

\[
v=\sqrt{\frac{2(1.381\times 10^{-23})(700)}{6.49\times 10^{-26}}}=546~\mathrm{m\,s}^{-1}.
\]

\[
a=\frac{(9.27\times 10^{-24})(10^3)}{6.49\times 10^{-26}}=1.43\times 10^5~\mathrm{m\,s}^{-2}.
\]

\[
s=a\cdot\frac{L}{v^2}\left(\ell+\frac{L}{2}\right)
=1.43\times 10^5\cdot\frac{0.1}{546^2}(1+0.05)
=0.0504~\mathrm{m}.
\]

Distance \(P_2P_3=2s=\boxed{10.1~\mathrm{cm}}\).

**If the figure takes \(\ell=1~\mathrm{m}\) as the magnet and \(L=0.1~\mathrm{m}\) as the drift** (German \(l\) for magnet length): \(2s\approx 58~\mathrm{cm}\). Quote the geometry you drew. The physically typical SG deflection with a 10 cm magnet is the **10 cm** answer, not 58 cm.

**Traps.** Using \(J=3/2\) (excited K) → 4 spots. Using \(g=1\) instead of \(g=2\) for \(^2S_{1/2}\) (that would halve \(\mu_z\)). Trying to do SG on electrons (Lorentz force).

---

## Problem 12 — Linear Stark of H, \(n=3\), and \(n=3\to 2\)

Parabolic formula

\[
\Delta E=\frac32 n(n_1-n_2)\,e a_0\,\mathcal{E},\qquad
n=n_1+n_2+|m|+1.
\]

### \(n=3\) (9 orbital states → 5 energies)

| \(n_1\) | \(n_2\) | \(m\) | \(n_1-n_2\) | \(\Delta E/(e a_0\mathcal{E})\) | degeneracy |
|---|---|---|---|---|---|
| 2 | 0 | 0 | +2 | **+9** | 1 |
| 1 | 0 | \(\pm 1\) | +1 | **+9/2** | 2 |
| 1 | 1 | 0 | 0 | **0** | 1 |
| 0 | 0 | \(\pm 2\) | 0 | **0** | 2 |
| 0 | 1 | \(\pm 1\) | −1 | **−9/2** | 2 |
| 0 | 2 | 0 | −2 | **−9** | 1 |

Five levels: \(\pm 9,\;\pm 9/2,\;0\) (units \(e a_0\mathcal{E}\)). Degeneracies 1, 2, 3, 2, 1.

In the \(\lvert n\ell m\rangle\) picture the same mixing is: \(\{3s,3p_0,3d_0\}\) couple (\(\Delta m=0\)); \(\{3p_{\pm 1},3d_{\pm 1}\}\) couple; \(3d_{\pm 2}\) are unshifted.

### \(n=2\) (for the transitions)

Three levels: \(\Delta E=0,\pm 3\,e a_0\mathcal{E}\).

```
 n=3    +9  ──
       +9/2 ────
         0  ──────
       −9/2 ────
        −9  ──

 n=2    +3  ────
         0  ──────
        −3  ────
```

### Transitions \(n=3\to 2\) and polarisation

E1: \(\Delta m=0\) (π, \(\mathbf{E}_\text{light}\parallel\boldsymbol{\mathcal{E}}\)) and \(\Delta m=\pm 1\) (σ).

The line-centre (field-free) Hα is at \(\Delta E_3-\Delta E_2=0\). Shifted components sit at

\[
\frac{\Delta\nu}{(e a_0\mathcal{E}/h)}
=\bigl[\tfrac32\cdot 3\cdot k_3-\tfrac32\cdot 2\cdot k_2\bigr]
= \tfrac92 k_3 - 3 k_2,
\]

\(k=n_1-n_2\). Allowed \((k_3,k_2)\) pairs with compatible \(m\) give the classic symmetric Hα Stark pattern with outermost π components at \(\pm 8\) (in units \(e a_0\mathcal{E}/h\) wait: \(9-3=6\), \(9-(-3)=12\)? Careful.)

Level differences in units of \(e a_0\mathcal{E}\):

- π (\(\Delta m=0\)): \(9-3=6\), \(9-0=9\), \(9-(-3)=12\), \(4.5-3=1.5\), \(4.5-0=4.5\), \(4.5-(-3)=7.5\), \(0-3=-3\), \(0-0=0\), \(0-(-3)=3\), and the sign-reversed copies. Not all survive once \(m\) is tracked.

**What to draw in an exam (this is what is marked):**

1. The five \(n=3\) and three \(n=2\) bars as above.
2. π arrows: \(\Delta m=0\) (same-\(m\) column).
3. σ arrows: \(\Delta m=\pm 1\).
4. Label: π linear \(\parallel\boldsymbol{\mathcal{E}}\), σ linear \(\perp\boldsymbol{\mathcal{E}}\) (or circular about \(\boldsymbol{\mathcal{E}}\) if viewed end-on).

The pattern is **symmetric** about the unshifted line (linear Stark). There is no unshifted π-only Lorentz triplet — hydrogen’s linear Stark is richer than Zeeman.

---

## Problem 13 — Pt ground term, \(\mu\), weak-field span

Configuration: \([\mathrm{Xe}]\,4f^{14}5d^9 6s^1\). Closed \(4f^{14}\) is inert.

Treat \(5d^9\) as a \(d\)-**hole** (\(L=2,S=1/2\)) plus \(6s^1\) (\(l=0,s=1/2\)):

\[
L=2,\qquad S=0\text{ or }1
\quad\Rightarrow\quad {}^1D\text{ and }{}^3D.
\]

Hund: max \(S\) first \(\Rightarrow\) triplet \(^3D\) is lower. The \(d^9\) shell is **more than half full** \(\Rightarrow\) inverted FS: highest \(J\) lies lowest.

\[
J=L+S,L+S-1,\ldots|L-S|=3,2,1
\quad\Rightarrow\quad
\text{GS }=\boxed{{}^3D_3}.
\]

\[
g_J=1+\frac{J(J+1)+S(S+1)-L(L+1)}{2J(J+1)}
=1+\frac{12+2-6}{2\cdot 12}
=1+\frac{8}{24}
=\boxed{\frac43}.
\]

Magnetic moment (effective Bohr magneton number):

\[
\mu=g_J\sqrt{J(J+1)}\,\mu_B
=\frac43\sqrt{12}\,\mu_B
=\boxed{\frac{8\sqrt{3}}{3}\,\mu_B\approx 4.619\,\mu_B}.
\]

Weak field: \(E=g_J\mu_B B m_J\), \(m_J=-3,\ldots,+3\). Extreme components \(\Delta m_J=6\):

\[
\Delta E_\text{span}=6\cdot\frac43\cdot\mu_B B
=\boxed{8\,\mu_B B}.
\]

---

## Problem 14 — jj coupling, \((5/2)^4\)

Four equivalent electrons in a \(j=5/2\) subshell. The subshell holds \(2j+1=6\) electrons, so \((5/2)^4\) is two **holes** in a closed \(j=5/2\) shell.

Two equivalent \(j=5/2\) fermions: Pauli \(\Rightarrow\) only **even** \(J\),

\[
J=0,2,4
\]

(the odd values 1,3,5 would be the symmetric/forbidden set). Hole–particle symmetry: \((5/2)^4\) has the **same** list as \((5/2)^2\).

NIST table (memorise the short one):

\[
(5/2)^2\text{ and }(5/2)^4:\quad J=0,2,4.
\]

**Answer:** \(\boxed{J=0,2,4}\).

Enumeration if they want to see it: \(m_j\in\{\pm 5/2,\pm 3/2,\pm 1/2\}\). Choose 4 distinct \(m_j\) (or choose 2 missing). Possible \(M=\sum m_j\) run from \(+4\) down to \(-4\) in steps of 1, with the multiplicities of a \(J=4\) plus a \(J=2\) plus a \(J=0\).

---

## Problem 15 — Helium \(\lvert\downarrow\downarrow\rangle\) is an eigenstate of \(S^2\) and \(S_z\)

Two-electron spin-down product

\[
\chi=\lvert\beta(1)\beta(2)\rangle
=\begin{pmatrix}0\\1\end{pmatrix}_1\otimes\begin{pmatrix}0\\1\end{pmatrix}_2.
\]

\(\mathbf{S}=\mathbf{S}_1+\mathbf{S}_2\), \(\mathbf{S}_i=(\hbar/2)\boldsymbol{\sigma}_i\), with the given Pauli matrices.

**\(S_z\).** \(\sigma_z\beta=-\beta\), so

\[
S_z\chi=\frac{\hbar}{2}\bigl(\sigma_{z1}+\sigma_{z2}\bigr)\chi
=\frac{\hbar}{2}(-1-1)\chi
=-\hbar\,\chi.
\]

Eigenvalue \(-\hbar\) \(\Rightarrow\) \(M_S=-1\).

**\(S^2\).** Use \(S^2=S_1^2+S_2^2+2\mathbf{S}_1\cdot\mathbf{S}_2\) and \(S_i^2=s(s+1)\hbar^2=(3/4)\hbar^2\),

\[
\mathbf{S}_1\cdot\mathbf{S}_2=\frac{\hbar^2}{4}\,\boldsymbol{\sigma}_1\cdot\boldsymbol{\sigma}_2
=\frac{\hbar^2}{4}(\sigma_{x1}\sigma_{x2}+\sigma_{y1}\sigma_{y2}+\sigma_{z1}\sigma_{z2}).
\]

Act on \(\chi=\lvert\downarrow\downarrow\rangle\):

\[
\begin{align*}
\sigma_x\lvert\downarrow\rangle&=\lvert\uparrow\rangle
 &&\Rightarrow\; \sigma_{x1}\sigma_{x2}\chi=\lvert\uparrow\uparrow\rangle,\\
\sigma_y\lvert\downarrow\rangle&=-i\lvert\uparrow\rangle
 &&\Rightarrow\; \sigma_{y1}\sigma_{y2}\chi=(-i)(-i)\lvert\uparrow\uparrow\rangle=-\lvert\uparrow\uparrow\rangle,\\
\sigma_z\lvert\downarrow\rangle&=-\lvert\downarrow\rangle
 &&\Rightarrow\; \sigma_{z1}\sigma_{z2}\chi=+\chi.
\end{align*}
\]

\[
\boldsymbol{\sigma}_1\cdot\boldsymbol{\sigma}_2\,\chi
=\lvert\uparrow\uparrow\rangle-\lvert\uparrow\uparrow\rangle+\chi
=\chi.
\]

Hence \(\mathbf{S}_1\cdot\mathbf{S}_2\,\chi=(\hbar^2/4)\chi\), and

\[
S^2\chi=\Bigl(\tfrac34+\tfrac34+\tfrac12\Bigr)\hbar^2\chi
=2\hbar^2\chi
=1(1+1)\hbar^2\chi.
\]

So \(\chi\) is \(\lvert S=1,M_S=-1\rangle\), a triplet function, simultaneous eigenstate of \(S^2\) and \(S_z\).

(The other two triplet members are \(\lvert\uparrow\uparrow\rangle\) and the symmetric combination; the singlet is antisymmetric and has \(S^2=0\).)

---

## Problem 16 — Li valence levels vs H

Quantum defects: \(\delta_s=0.4\), \(\delta_p=0.04\), \(\delta_d=\delta_f=0\).

\[
E_{n\ell}(\mathrm{Li})=-13.6~\mathrm{eV}/(n-\delta_\ell)^2,
\qquad
E_n(\mathrm{H})=-13.6~\mathrm{eV}/n^2.
\]

Effective quantum numbers (Li):

|  | \(n=2\) | \(n=3\) | \(n=4\) |
|---|---|---|---|
| \(s\) (\(n^*=n-0.4\)) | 1.6 | 2.6 | 3.6 |
| \(p\) (\(n^*=n-0.04\)) | 1.96 | 2.96 | 3.96 |
| \(d,f\) | — / 3 | 3 | 4 |

Qualitative plot (energy up, more bound down). Draw H on the left, Li on the right:

```
 E=0 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ionisation
      H                 Li
 n=4  ────           4f,4d ────  (on top of H n=4)
                     4p   ──── slightly below
                     4s   ── distinctly below

 n=3  ────           3d ────
                     3p ────
                     3s ──

 n=2  ────           2p ────  (almost H n=2)
                     2s ──    GROUND STATE of Li

 n=1  ────  (H only; Li 1s² is a filled core, not the valence)
```

**Two allowed arrows** (E1, \(\Delta\ell=\pm 1\)):

- \(2p\to 2s\) (Li resonance / D-line analogue),
- \(3d\to 2p\) (or \(3s\to 2p\), \(3p\to 2s\)).

Forbidden: \(3s\to 2s\) (\(\Delta\ell=0\)), \(3d\to 2s\) (\(\Delta\ell=2\)).

---

## Problem 17 — Unsold’s theorem, prove for \(\ell=1\)

**Statement.** For a filled \(\ell\)-subshell (or the sum over \(m\) at fixed \(\ell\)),

\[
\sum_{m=-\ell}^{\ell}\lvert Y_{\ell m}(\theta,\phi)\rvert^2
=\frac{2\ell+1}{4\pi},
\]

independent of angle. The charge density of a closed subshell is spherically symmetric. (That is why closed shells make a central field for the optical electron.)

**Proof, \(\ell=1\), using the given \(\Phi,\Theta\).** Angular wave function \(Y=\Theta(\theta)\Phi(\phi)\).

\[
\Phi=\frac{1}{\sqrt{2\pi}}\quad\text{for all }m,
\qquad
\Theta_{10}=\frac{\sqrt{6}}{2}\cos\theta,
\qquad
\Theta_{1\pm 1}=\frac{\sqrt{3}}{2}\sin\theta.
\]

\[
\begin{align*}
\lvert Y_{10}\rvert^2
&=\frac{1}{2\pi}\cdot\frac{6}{4}\cos^2\theta
=\frac{3}{4\pi}\cos^2\theta,\\[4pt]
\lvert Y_{1\pm 1}\rvert^2
&=\frac{1}{2\pi}\cdot\frac{3}{4}\sin^2\theta
=\frac{3}{8\pi}\sin^2\theta.
\end{align*}
\]

Sum:

\[
\sum_{m=-1}^{1}\lvert Y_{1m}\rvert^2
=\frac{3}{4\pi}\cos^2\theta+2\cdot\frac{3}{8\pi}\sin^2\theta
=\frac{3}{4\pi}(\cos^2\theta+\sin^2\theta)
=\frac{3}{4\pi}
=\frac{2\cdot 1+1}{4\pi}.
\]

Independent of \(\theta\) and \(\phi\). ∎

---

## Problem 18 — True / False with one-line reasons

**(i) At small \(r\), for \(\ell\neq 0\), \(R_{nl}\propto r^{\ell+1}\).**
**FALSE.** The radial function in \(\psi=R_{nl}(r)Y_{\ell m}\) behaves as \(R_{nl}\propto r^{\ell}\). It is \(u(r)=r R_{nl}\) that goes as \(r^{\ell+1}\). (Even for \(\ell=0\), \(R_{n0}(0)\neq 0\).)

**(ii) Series limit of Lyman of H lies in the visible.**
**FALSE.** Lyman limit is \(91.2~\mathrm{nm}\), vacuum UV. Visible starts ~400 nm. (Lyman-\(\alpha\) itself is already 121.6 nm, UV.)

**(iii) Stimulated-emission rates are independent of the intensity of the incident radiation.**
**FALSE.** Stimulated rate \(=B_{21}\rho(\nu)\) (or \(B_{21}I/c\)). Spontaneous \(A_{21}\) is the intensity-independent one.

**(iv) In alkali atoms \(\ell\)-degeneracy is removed because the effective potential is not spherically symmetric.**
**FALSE.** The central-field potential **is** spherically symmetric (that is why \(m\) remains degenerate). \(\ell\)-degeneracy dies because \(V_\text{eff}\) is **not Coulomb \(1/r\)** (core penetration / polarisation). Non-spherical would be crystal fields or \(\mathbf{B}/\boldsymbol{\mathcal{E}}\).

**(v) The energy of an Auger electron depends on the energy of the radiation which created the initial vacancy.**
**FALSE.** \(K_\text{Auger}=E_\text{hole}-E_\text{filler}-E_\text{ejected}\), a combination of binding energies. The ejected electron does not “remember” the photon. (Photoelectrons *do*; that is how you tell them apart.)

**(vi) Atomic transitions forbidden under the dipole approximation are ‘strictly forbidden’.**
**FALSE.** They proceed by M1, E2, higher multipoles, two-photon decay, collisions, hyperfine mixing, … “Strictly forbidden” is reserved for exact-symmetry bans (e.g. \(J=0\to 0\) for one photon). Lecture: “single photon forbidden → small; totally forbidden → 0.”

**(vii) Electrons in high Rydberg states are very strongly bound.**
**FALSE.** \(E_b=13.6~\mathrm{eV}/n^2\to 0\). They are **weakly** bound, huge, and easily ionised (which is why problem 5’s linewidth budget is tight).

Score yourself: the two that people miss under exam stress are **(i)** (confusing \(R\) with \(u\)) and **(iv)** (confusing spherical with Coulomb).

---

## One-line answer key

| # | Answer |
|---|---|
| 1 | \(\bar\nu_\infty=6856.71~\mathrm{cm}^{-1}\), \(\lambda_\infty=1458.4~\mathrm{nm}\) (use \(R_D\), not \(R_\infty\)) |
| 2 | \(104~\mathrm{eV}\) (reduced mass \(220\,m_e\)) |
| 3 | \(\Delta\nu=9.95~\mathrm{MHz}\), \(\Delta E=4.11\times 10^{-8}~\mathrm{eV}\), \(\Delta\lambda=1.15\times 10^{-4}~\text{Å}\) |
| 4 | Lyman/Balmer: no. Paschen/Brackett/Pfund: yes (IR) |
| 5 | \(\lambda_2\approx 600,595,593,592~\mathrm{nm}\); \(r_n=n^2 a_0\); \(E_b=13.6/n^2\); \(\delta E_1+\delta E_2\lesssim 1.1\times 10^{-4}~\mathrm{eV}\) |
| 6 | \(R_\text{ex}=95.2~\mathrm{meV}\); \(n=2..5\): 23.8, 10.6, 5.95, 3.81 meV; hydrogenic series + continuum at \(E_g\) |
| 7 | \(1.555~\mathrm{eV}\) (\(Z^4/n^3\)) |
| 8 | H: \(2.04~\text{Å}\); D: \(1.45~\text{Å}\) |
| 9 | 3 FS lines (no \(\Delta J=2\)); \(g=6/5,4/5,4/3,2/3\); PB → Lorentz triplet; π \(\Delta m=0\), σ \(\Delta m=\pm 1\) |
| 10 | \(^{1,3}P,D,F\) with \(J\) as in the table |
| 11 | \(P_2P_3\approx 10~\mathrm{cm}\) (magnet \(L=0.1~\mathrm{m}\), drift \(\ell=1~\mathrm{m}\), \(v=\sqrt{2kT/M}\)) |
| 12 | \(n=3\): 5 levels at \(0,\pm 9/2,\pm 9\) (\(e a_0\mathcal{E}\)); π/σ as \(\Delta m=0/\pm 1\) |
| 13 | GS \(^3D_3\), \(\mu=(8\sqrt{3}/3)\mu_B\), span \(8\mu_B B\) |
| 14 | \(J=0,2,4\) |
| 15 | \(S_z\chi=-\hbar\chi\), \(S^2\chi=2\hbar^2\chi\) (triplet) |
| 16 | \(ns\) pulled down most; arrows \(2p\to 2s\) and \(3d\to 2p\) |
| 17 | sum \(=3/4\pi\) |
| 18 | F F F F F F F (all seven false) |
