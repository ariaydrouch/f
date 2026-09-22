# PYD411 mid-term report

LaTeX source follows `Sample_BTP_Latex.tex` (same class, preamble,
title-page layout and section structure). The template's blank second
page is omitted so the PDF stays within the mid-term limit of two pages
plus one extra page permitted by the instructor.

## Files

```
THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.tex   source
THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.pdf   compiled report (3 pages)
Logo-IITD.jpg                               IIT Delhi seal (replace with the
                                            official file from the template pack
                                            if you have it)
figures/                                    simulation figures
```

## Before submitting

1. Search the `.tex` for `FILLME` and put in
   - your name and full entry number (uncomment the second student line if needed);
   - the adviser's name (title block **and** Acknowledgements);
   - academic year if it is not 2026--2027, Semester I.
2. Rename the PDF exactly as required (two underscores):

   `THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.pdf`

   Example: `SOFTMATTER_2024PHZXXXX_2601PYD411_MR.pdf`.

3. One student uploads, before 12:00 noon.

## Compiling

```bash
cd report
pdflatex THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.tex
pdflatex THEME_FULL-ENTRY-NUMBER_2601PYD411_MR.tex
```

Verified with pdfTeX 3.141592653 (TeX Live 2023): 3 pages, no undefined
references. Only the packages already loaded by the template are used.
