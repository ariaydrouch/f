# PYL7590 cheat sheet — change log

Audited against Lectures 13–14, 15–16, 17, 18–19, 20, 21–22, 23 and 24, and the 25 Nov 2025 paper (`Major_2025`). Body text is 7.4 pt on exactly two A4 pages, two columns, with a vertical rule.

## Corrected to the lecture notation

- **HIO** now uses the slide update: \(g_{n+1}=g'_n\) where support and positivity hold, and \(g_{n+1}=g_n-\beta g'_n\) otherwise. The illustration value \(\beta=0.9\) is stated. Positivity is the lecture rule (real part inside the support, then negatives set to 0). Twin image and non-centrosymmetric support are included.
- **Four-step phase shifting** is the lecture set (109): \(R, Re^{i\pi/2}, Re^{i\pi}, Re^{i3\pi/2}\), with \(\Delta\varphi=\varphi_r-\varphi_o\) and \(\arctan[(H_4-H_2)/(H_3-H_1)]\). `atan2` is only the quadrant implementation of that arctan.
- **FTM** now includes the requirements that were missing: low-bandwidth object, carrier \(R=R_0 e^{i2\pi f_0 x}\), non-overlap \(3B\le f_0\), and camera sampling \(1/(4p)\ge f_0\ge 3B\). The lecture point that a single hologram still contains full resolution, and that the loss is from the FTM filter, is stated.
- **OTF** is the lecture definition \(\mathcal{F}\{|h|^2\}/\mathcal{F}\{|h|^2\}(0,0)\). MTF \(=|\mathrm{OTF}|\) is kept as the contrast-only reading.
- **Propagation** uses the written Fresnel formula (132). The exact \(k_z\) factor is kept as one line and labelled as not the formula printed in (132).
- **Cubic-phase OTF** is slide (175) as printed: \(\exp[-i\alpha^2 u/(12\beta)+i\beta^3/4]\), with \(\gamma=3\). A derivation check is added: expanding \((x\pm u/2)^3\) produces \(\beta u^3/4\), not \(\beta^3\).
- **SIM** spectrum is the lecture form (181). It is the same as the old \(m/4\) coefficients. Nine frames (three angles, three phases) and the generalized Wiener filter (187) are added. The one-image Wiener filter is identified as that formula with \(N=1\) and \(K=S_{\mathrm{noise}}/S_{\mathrm{obj}}\).
- **Filtered backprojection** now has the Ram–Lak steps: ramp \(|\nu|\), inverse FT, back-project. The old sheet only said “filter, then back-project.”
- **Lensless pixel size** keeps ideal Nyquist \(p\le\lambda/(2\sin\theta)\) and adds the lecture camera rule of about four pixels per fringe.

## Added from the slides

- Transport of intensity equation (139), constant-amplitude solution, inverse Laplacian (143), defocus approximation (144), and the general solution (147).
- Fourier ptychography, including the tilt shift (154) and real-space ptychography (155).
- Defocus diversity and the GS chain across planes.
- Optimization fringe analysis (117)–(119) and the single-pixel phase accuracy bound \(\Delta\varphi\sim 1/\sqrt{N}\), plus the lecture remark that sparsity can beat that single-pixel limit.
- Wirtinger / coded diffraction cost (150)–(151) and complexity \(\zeta\) from \(|G|\) alone (152)–(153).
- Non-interferometric versus interferometric list as summarized on the slides.
- Rotating-PSF Laguerre–Gaussian condition from Lecture 23.

## Retained

PSF/OTF imaging model, Wiener deconvolution, open-shutter versus coded-shutter comparison, lensless \(z\) search, GS loop, inline twin image and focus metric, projection-slice proof in the exam’s \(g,G\) notation, common-line theorem, DOE phase-only design and \(\Delta x\approx 26.6\,\mu\mathrm{m}\), Alvarez derivation through \(1/f=2A\delta\lambda/\pi\), stochastic localization and plenoptic notes, and the 2025 question checklist.

## Not added, on purpose

Correlation / ghost imaging does not appear in the attached lectures or in the 2025 paper. Phase unwrapping is only the TIE statement that the phase is already unwrapped because \(\arctan\) is never used; the slides postpone a dedicated unwrapping lecture. No unwrapping algorithm was invented.
