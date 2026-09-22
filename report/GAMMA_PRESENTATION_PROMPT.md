# Gamma prompt — PYD411 mid-term slides

Copy everything between the lines into Gamma (Paste text / Generate).
Target: **8 slides**, **8 minutes** talking + 2 minutes questions.
Do **not** ask Gamma for 10–12 slides: you will run over time.

Suggested change from the original plan: put cell biology and parameters on
**one** slide, not three. In 8 minutes the committee wants the versions and
the numbers (protrusion, aster/fan, crawl, 2% flow, 5× speed-up). Biology
is the motivation, not the talk.

After Gamma builds the deck, replace the image boxes with the PDFs in
`report/figures/` (listed under each slide).

---

```
Create an 8-slide academic mid-term presentation for an IIT Delhi Physics BTP (course PYD411). Total speaking time is 8 minutes, plus 2 minutes for questions, so every slide must be sparse: short headings, 3–5 bullets max, large readable figures, no paragraphs.

Title: Phase-Field Modelling of Crawling Cells
Subtitle: Towards a Tractable Two-Dimensional Model
Students: Siddharth Kumar (2023PH10741), Soumik Roy (2023PH10756)
Adviser: Prof. Sujin B. Babu
Dept of Physics, IIT Delhi · 2026–27, Semester I · Mid-term evaluation

Tone: clean scientific talk, not a startup pitch. White or very light background, dark navy/teal accents, IIT Delhi academic look. Use simple diagrams and leave clearly labelled IMAGE PLACEHOLDERS where our simulation figures go. Do not invent extra simulations, papers, or numbers. Use only the facts below. Put a one-line speaker note under each slide (what to say in ~60 seconds).

Do not make more than 8 slides. Do not add an agenda slide, a “thank you” quote slide, or a references dump. One closing slide is enough.

SLIDE 1 — Title
Course, title, subtitle, both names and entry numbers, adviser, department.

SLIDE 2 — What a crawling cell is, and how we encode it
One slide only (not three). Left: the three mechanical ingredients of a real cell. Right: the matching symbols in our model.
• Actin filaments treadmill: polymerise at the front, depolymerise at the rear → they push the membrane forward. In the model this is the polarization field P and the treadmilling speed w0. The cell is carried by u = v + w0 P.
• Myosin motors walk on actin and generate a contractile stress that retracts the rear. In the model this is the active stress σ_act = −ζ φ P P, with ζ < 0 for contractility.
• Focal adhesions grip the substrate. Averaged over many binding/unbinding events this is just a friction −ξ v (Leoni & Sens). Strong adhesion = large ξ.
Also introduce the phase field φ (=1 inside the cell, 0 outside) and the interface width ε. One line of motivation: keratocyte fragments with no nucleus still polarise and crawl, so a lot of this is mechanics, not signalling. Papers to name once: Tjhung et al., Nat. Commun. 2015; Leoni & Sens, PRL 2017.
Optional tiny diagram: a cell with front labelled “actin treadmill / w0 P”, rear labelled “myosin / ζ”, belly labelled “adhesion / ξ”.

SLIDE 3 — The model, and four versions
Keep equations tiny. Show:
φ (cell), P (actin), v (cytoplasm), u = v + w0 P.
Free-energy idea in words, not the full integral: double-well + surface tension + polar order inside the cell + Frank elasticity + anchoring β (P wants to point outward at the edge). β is the main shape parameter.
Force balance: Stokes, 0 = −∇p + η∇²v − ξv + f, because Reynolds number ~ 10^{-5}.
Then a four-row table (this is the spine of the talk):
Ver | Geometry | Force balance | Area
1 | plane | v = 0 | drifts 4.5%
2 | vertical slice + wall | Brinkman / screened in z | fixed exactly
3 | plane | incompressible Stokes | fixed exactly
4 | plane | friction-dominated (Darcy), v = f/ξ | soft volume
One sentence: we add one ingredient at a time so we know what each one does. Goal of the project is many cells; Stokes is too expensive for that, which is why Version 4 exists.

SLIDE 4 — Versions 1 and 2: from a translating disc to a protrusion
Version 1 (one breath): disc with uniform P and v = 0. It translates but cannot change shape (uniform P ⇒ uniform u). Area falls 4.5% because advection was not conservative.
Version 2 (the result): side-view y–z slice, wall at z = 0. Treadmilling only in a layer of thickness λ next to the substrate, w(z) = (w0/2)[1 − tanh((z−λ)/wτ)]. Near-wall material runs out ahead; tension pulls it back; that competition is the protrusion. Volume conserved to 10^{-16}.
Numbers to put on the slide:
• w0 = 0.3 → hemispherical cap, contact 44.0, speed 0.050
• w0 = 2.0 → thin leading protrusion, contact 63.0, speed 0.432
• Transition near w0 ≈ 0.8, matching M ε²/λ ≈ 0.75
IMAGE PLACEHOLDERS (use our files after export):
• fig_v2_shapes.pdf — two side-view cells
• fig_v2_transition.pdf — contact / lamella / speed vs w0

SLIDE 5 — Version 3, briefly: shapes and what actually sets them
Top-view full model, spectral Stokes. Passive check (say in one clause): an ellipse relaxes to a circle, energy falls, flow dies, volume error = 0.
Two morphologies, varying only β and ζ at w0 = 1:
• Strong outward anchoring → radial actin aster, |⟨P⟩| = 0, speed = 0 (fried egg / not motile). Motility needs P to break symmetry.
• Moderate anchoring → lamellipodial fan elongated ACROSS the path, aspect 2.91, speed 0.843 ≈ w0.
Pseudopod and phagocytic cup do not appear: they need the third dimension; Version 2 already has the vertical protrusion.
Key control (put as a 2×2 or four bars — this is the Version 3 takeaway):
neither 1.07 | flow only 1.61 | anchoring only 2.85 | both 2.92.
Flow on top of anchoring adds only ~2%. Speed is always ~0.80–0.85, set by w0⟨P⟩, almost independent of friction ξ. That last point disagrees with Leoni & Sens (biphasic speed): their mechanism needs mechanosensitive bonds, which a constant ξ cannot see.
IMAGE PLACEHOLDERS: fig_v3_morph.pdf and fig_v3_decomp.pdf

SLIDE 6 — Version 4, briefly: the cell that actually crawls
This is the slide to linger on. Because η/(ξ R²) ≈ 0.006, friction — not viscosity — balances the active forces, so Stokes collapses to the local Darcy law v = f/ξ. No FFT, no pressure, every operation is a local stencil.
Main result, laboratory frame: a circular seed becomes a fan and crawls in a straight line. Travel 239.9 length units in time 299 at steady speed 0.801.
Diagnostics (small numbers on the slide): y_cm = 0, speed flat at 0.801, aspect → ~3.2, area +15% and thickness −15% (volume conserved, area free). Soft kA = 5; kA = 0 inflates 14× and stops crawling. Where V3 and V4 can be compared (flow off, rigid area) they agree to 0.2%. Cost: 2.70 → 1.10 ms/step, dt 0.01 → 0.03, about 5× faster. This locality is what we need for many cells.
IMAGE PLACEHOLDERS (these are the most important pictures in the talk):
• fig_v4_montage.pdf — outlines along x, coloured by time
• fig_v4_snapshots.pdf — φ at t = 0, 100, 299
• fig_v4_diagnostics.pdf — CM, speed, aspect, area/thickness
Optional if space: fig_v4_area.pdf (kA sweep)

SLIDE 7 — What we learned
Four bullets only, each tied to a figure:
1. A z-gradient in treadmilling is enough for a leading protrusion (V2).
2. In the plane, shape is set by anchoring of P, not by hydrodynamics (~2%).
3. The cheap Darcy model crawls at speed 0.801 and matches the full model to 0.2% where they overlap, ~5× faster and local.
4. Conserve volume, not projected area; dropping the constraint entirely is not viable.
One boxed take-home sentence: “We now have a verified, local single-cell model that crawls, and it is cheap enough to go to many cells.”

SLIDE 8 — Next, and questions
Five short future items (do not expand):
1. Two distinguishable cells with a repulsive overlap.
2. Head-on and glancing collisions — is contact inhibition a prediction?
3. Spontaneous polarity so a cell can choose its own direction.
4. Load-dependent friction, to recover the biphasic speed of Leoni & Sens.
5. Tens of cells: jamming and neighbour alignment.
Footer: Thank you — questions. Repeat names and adviser.

Constraints for Gamma:
• Exactly 8 slides.
• Prefer two-column layouts (text | figure).
• No clip-art cells, no DNA helices, no stock photos of microscopes.
• Leave empty image frames with the filenames above written inside them so I can drop in our PDFs.
• Do not write the full free-energy functional on a slide.
• Do not add citations as a last wall of text; mention Tjhung 2015 and Leoni & Sens 2017 only where they earn a point.
```

---

## After Gamma exports

Drop these into the placeholders, in order:

| slide | file |
|---|---|
| 4 | `figures/fig_v2_shapes.pdf`, `figures/fig_v2_transition.pdf` |
| 5 | `figures/fig_v3_morph.pdf`, `figures/fig_v3_decomp.pdf` |
| 6 | `figures/fig_v4_montage.pdf`, `figures/fig_v4_snapshots.pdf`, `figures/fig_v4_diagnostics.pdf` |

Rehearse once with a timer. If you are over 8 minutes, cut Slide 2 to 20 seconds and spend the time on Slides 5–6.
