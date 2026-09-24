# PYD411 mid-term slides

Editable 16:9 PowerPoint, 8 slides, written for the 8 + 2 minute slot.

```
PYD411_midsem_presentation.pptx   open this in PowerPoint / Google Slides / LibreOffice
build_midsem_pptx.py              rebuilds the .pptx from the figures
assets/                           PNGs of the report figures (and the IITD logo)
```

Open `PYD411_midsem_presentation.pptx` and edit any text box, table cell, or picture.
To rebuild after changing copy or swapping a PNG:

```bash
python3 presentation/build_midsem_pptx.py
```

## Slide list

1. Title
2. What makes a crawling cell move? (biology ↔ model fields, two-column)
3. Free energy roles + Stokes force balance + four-version table
4. How the cell is simulated — the per-timestep update loop (φ, P, active
   force, velocity, transport, back to φ), using the exact evolution
   equations from the report/implementation
5. Versions 1 and 2 (protrusion + \(w_0\) plots)
6. Version 3 (aster / fan + anchoring-vs-flow 2×2)
7. Version 4 — the reduction from Stokes to Darcy, and the crawl
8. Four take-homes
9. Future work and questions

Every slide has a speaker note (open the Notes pane in PowerPoint /
Google Slides to see it).

Numbers are consistency-checked against the report: thickness is
reported as \(h/h_0\approx0.87\) (≈13% thinning), the ≈5× speed-up is
described as the overall runtime improvement (it includes the larger
stable time-step, not just the ms/step ratio), all lengths/times are
plain model units (no physical unit is claimed), and the "choose their
own direction" polarity item is listed only as future work.
