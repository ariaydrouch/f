# PYD411 mid-term report

LaTeX source follows `Sample_BTP_Latex.tex` (same class, preamble,
title-page layout and section structure). The template's blank second
page is omitted. Result figures are included in full, so the compiled
PDF is 4 pages (the instructor allowed one extra page on a 2-page
brief; the extra length is the crawling and quantitative plots).

## Files

```
THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.tex   source
THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.pdf   compiled report
Logo-IITD.jpg                               IIT Delhi seal (replace with the
                                            official file from the template pack
                                            if you have it)
figures/                                    simulation figures
```

Names and adviser are filled in from the submitted draft:
Siddharth Kumar (2023PH10741), Soumik Roy (2023PH10756),
Prof. Sujin B. Babu.

## Figures in the report

| figure | shows |
|---|---|
| Fig. 1 | V2 protrusion shapes + $w_0$ transition (contact, lamella, speed) |
| Fig. 2 | V3 aster / lamellipodium / fan, and the anchoring-vs-flow $2\times2$ |
| Fig. 3 | V4 laboratory-frame crawl, $\phi$ snapshots, diagnostics, soft volume |

## Before submitting

Rename the PDF to `THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.pdf`
(two underscores), e.g. `SOFTMATTER_2023PH10741_2601PYD411_MR.pdf`.
One student uploads before 12:00 noon.

The mid-term slides are `presentation/PYD411_midsem_presentation.pptx`
(8 slides, editable). See `presentation/README.md`.

## Compiling

```bash
cd report
pdflatex THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.tex
pdflatex THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.tex
```
