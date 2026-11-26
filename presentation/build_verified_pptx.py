#!/usr/bin/env python3
"""Keep slides 1-4 of the verified deck exactly.

Slides 5-12 are redrawn in that same style: navy header, teal rule,
Calibri for words, Cambria Math for formulas (as on slides 2-4).

The labels ksoft = 21 and ksoft = 6 are not used. The separations and
turns on that slide are the k_soft = 15 and k_soft = 0 runs, which is
also what slide 8 already says.
"""

import shutil
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

SRC = Path("/home/ubuntu/.cursor/projects/agent-repos-f/uploads/BTP_Midsem_and_Post_Midsem_Typeset_choladeck_0f9e.pptx")
A = Path(__file__).resolve().parent / "verified_assets"
OUT = Path(__file__).resolve().parent / "BTP_Midsem_and_Post_Midsem_Beautified.pptx"

NAVY = RGBColor(0x0B, 0x3D, 0x5C)
TEAL = RGBColor(0x1A, 0x7A, 0x6D)
DARK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x4B, 0x55, 0x63)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xF3, 0xF6, 0xF9)
SOFT = RGBColor(0xE8, 0xF3, 0xF1)
EQBG = RGBColor(0xEF, 0xF5, 0xF7)
MATH = "Cambria Math"
FONT = "Calibri"
W = Inches(13.333)
H = Inches(7.5)


def delete_slide(prs, index):
    sldId = prs.slides._sldIdLst[index]
    prs.part.drop_rel(sldId.get(qn("r:id")))
    prs.slides._sldIdLst.remove(sldId)


def rect(slide, l, t, w, h, fill):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def rrect(slide, l, t, w, h, fill, line=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.shadow.inherit = False
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1.25)
    try:
        sh.adjustments[0] = 0.1
    except Exception:
        pass
    return sh


def tb(slide, l, t, w, h, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    return tf


def fresh(tf, text, size, color, bold=False, align=PP_ALIGN.LEFT, after=2):
    if not tf.paragraphs[0].runs:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(after)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = FONT
    return p


def _base(run, sub=False, sup=False):
    rPr = run._r.get_or_add_rPr()
    rPr.set("baseline", "-25000" if sub else ("30000" if sup else "0"))


def T(text, bold=False, sub=False, sup=False, size=None, color=None):
    d = {"text": text, "bold": bold, "sub": sub, "sup": sup}
    if size:
        d["size"] = size
    if color:
        d["color"] = color
    return d


def mathpara(tf, segs, size=18, color=NAVY, align=PP_ALIGN.CENTER, first=False):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(2)
    p.clear()
    for seg in segs:
        r = p.add_run()
        r.text = seg["text"]
        r.font.size = Pt(seg.get("size", size))
        r.font.bold = seg.get("bold", False)
        r.font.italic = False
        r.font.color.rgb = seg.get("color", color)
        r.font.name = MATH
        if seg.get("sub"):
            _base(r, sub=True)
        elif seg.get("sup"):
            _base(r, sup=True)
    return p


def chrome(slide, title, page):
    rect(slide, 0, 0, W, H, WHITE)
    rect(slide, 0, 0, W, Inches(0.86), NAVY)
    rect(slide, 0, Inches(0.86), W, Inches(0.05), TEAL)
    tf = tb(slide, Inches(0.4), Inches(0.14), Inches(12.5), Inches(0.58), MSO_ANCHOR.MIDDLE)
    fresh(tf, title, 26, WHITE, bold=True, after=0)
    rect(slide, 0, Inches(7.22), W, Inches(0.28), PALE)
    tf = tb(slide, Inches(0.35), Inches(7.22), Inches(10.6), Inches(0.28), MSO_ANCHOR.MIDDLE)
    fresh(tf, "PYD411  ·  End-term  ·  Dept of Physics, IIT Delhi  ·  Siddharth Kumar & Soumik Roy",
          12, MUTED, after=0)
    tf = tb(slide, Inches(11.45), Inches(7.22), Inches(1.55), Inches(0.28), MSO_ANCHOR.MIDDLE)
    fresh(tf, f"{page}  /  12", 12, MUTED, align=PP_ALIGN.RIGHT, after=0)


def fit(slide, path, l, t, max_w, max_h):
    im = Image.open(path)
    aw, ah = im.size
    scale = min(float(max_w) / aw, float(max_h) / ah)
    return slide.shapes.add_picture(
        str(path), Emu(int(l)), Emu(int(t)), Emu(int(aw * scale)), Emu(int(ah * scale))
    )


def formula_card(slide, l, t, w, h, label, lines, note=None, size=16):
    rrect(slide, l, t, w, h, EQBG, TEAL)
    tf = tb(slide, l + Inches(0.14), t + Inches(0.06), w - Inches(0.24), Inches(0.34))
    fresh(tf, label, 14, TEAL, bold=True, after=0)
    body_h = h - Inches(0.42) - (Inches(0.55) if note else Inches(0.06))
    tf = tb(slide, l + Inches(0.1), t + Inches(0.4), w - Inches(0.18), body_h, MSO_ANCHOR.MIDDLE)
    for i, line in enumerate(lines):
        mathpara(tf, line, size=size, first=(i == 0))
    if note:
        tf = tb(slide, l + Inches(0.16), t + h - Inches(0.55), w - Inches(0.28), Inches(0.48))
        fresh(tf, note, 13, DARK, after=0)


def formula_card(slide, l, t, w, h, label, lines, note=None, size=16):
    rrect(slide, l, t, w, h, EQBG, TEAL)
    tf = tb(slide, l + Inches(0.14), t + Inches(0.08), w - Inches(0.24), Inches(0.34))
    fresh(tf, label, 14, TEAL, bold=True, after=0)
    note_h = Inches(0.55) if note else Inches(0)
    tf = tb(slide, l + Inches(0.1), t + Inches(0.44), w - Inches(0.18),
            h - Inches(0.52) - note_h, MSO_ANCHOR.MIDDLE)
    for i, line in enumerate(lines):
        mathpara(tf, line, size=size, first=(i == 0))
    if note:
        tf = tb(slide, l + Inches(0.16), t + h - Inches(0.58), w - Inches(0.28), Inches(0.5))
        fresh(tf, note, 14, DARK, after=0)


def build():
    shutil.copy(SRC, OUT)
    prs = Presentation(str(OUT))
    for i in range(len(prs.slides) - 1, 3, -1):
        delete_slide(prs, i)
    blank = prs.slide_layouts[0]

    # 5
    s = prs.slides.add_slide(blank)
    chrome(s, "Run and tumble in a single cell", 5)
    tf = tb(s, Inches(0.45), Inches(1.12), Inches(12.4), Inches(0.42))
    fresh(tf, "Choose a heading  \u2192  crawl  \u2192  relax  \u2192  choose again", 20, NAVY, bold=True, after=0)
    rrect(s, Inches(0.4), Inches(1.62), Inches(12.55), Inches(0.78), EQBG, TEAL)
    tf = tb(s, Inches(0.5), Inches(1.66), Inches(12.35), Inches(0.7), MSO_ANCHOR.MIDDLE)
    mathpara(tf, [
        T("P", bold=True), T("  \u2190  \u03c6 (cos \u03b8, sin \u03b8)"),
        T("        |"), T("R", bold=True), T("(t) \u2212 "), T("R", bold=True), T("start", sub=True),
        T("|  \u2265  \u2113"), T("target", sub=True),
        T("        C = 4\u03c0A / perimeter"), T("2", sup=True),
    ], size=16, first=True)
    fit(s, A / "image3.png", Inches(0.55), Inches(2.6), Inches(5.2), Inches(4.3))
    s.shapes.add_movie(
        str(A / "media1.mp4"), Inches(7.15), Inches(2.6), Inches(5.4), Inches(3.9),
        poster_frame_image=str(A / "image4.png"), mime_type="video/mp4",
    )
    tf = tb(s, Inches(7.15), Inches(6.6), Inches(5.4), Inches(0.4))
    fresh(tf, "Click the simulation to play", 14, TEAL, bold=True, align=PP_ALIGN.CENTER, after=0)

    # 6
    s = prs.slides.add_slide(blank)
    chrome(s, "Two separate cell fields in a shared flow", 6)
    formula_card(s, Inches(0.35), Inches(1.15), Inches(6.25), Inches(2.75),
                 "One phase\u2013polarization pair per cell", [
                     [T("(\u03c6"), T("1", sub=True), T(", "), T("P", bold=True), T("1", sub=True),
                      T(")     and     (\u03c6"), T("2", sub=True), T(", "),
                      T("P", bold=True), T("2", sub=True), T(")")],
                 ], "Each cell keeps its own crawl and relaxation cycle.")
    formula_card(s, Inches(6.75), Inches(1.15), Inches(6.2), Inches(2.75),
                 "Short-range steric repulsion", [
                     [T("F"), T("rep", sub=True), T(" = "), T("k"), T("rep", sub=True),
                      T(" \u222b \u03c6"), T("1", sub=True), T("2", sup=True),
                      T(" \u03c6"), T("2", sub=True), T("2", sup=True), T(" dA")],
                     [T("\u03bc"), T("rep,i", sub=True), T(" = 2 "), T("k"), T("rep", sub=True),
                      T(" \u03c6"), T("i", sub=True), T(" \u03c6"), T("j", sub=True), T("2", sup=True)],
                 ])
    formula_card(s, Inches(0.35), Inches(4.1), Inches(6.25), Inches(2.9),
                 "One incompressible Stokes solve", [
                     [T("0 = \u2212\u2207p + \u03b7\u2207"), T("2", sup=True), T("v", bold=True),
                      T(" \u2212 \u03be"), T("v", bold=True), T(" + "),
                      T("f", bold=True), T("1", sub=True), T(" + "),
                      T("f", bold=True), T("2", sub=True)],
                     [T("\u2207 \u00b7 "), T("v", bold=True), T(" = 0"),
                      T("        "), T("u", bold=True), T("i", sub=True),
                      T(" = "), T("v", bold=True), T(" + "), T("w"), T("0,i", sub=True),
                      T("P", bold=True), T("i", sub=True)],
                 ])
    formula_card(s, Inches(6.75), Inches(4.1), Inches(6.2), Inches(2.9),
                 "Measure overlap during the walk", [
                     [T("O(t) = \u222b \u03c6"), T("1", sub=True), T(" \u03c6"), T("2", sub=True), T(" dA")],
                 ], "A soft wall confines motion inside the box.")

    # 7
    s = prs.slides.add_slide(blank)
    chrome(s, "Two cells stay distinct during the walk", 7)
    rrect(s, Inches(0.4), Inches(1.15), Inches(6.15), Inches(1.9), PALE, None)
    rect(s, Inches(0.4), Inches(1.15), Inches(0.1), Inches(1.9), TEAL)
    tf = tb(s, Inches(0.65), Inches(1.25), Inches(5.7), Inches(0.35))
    fresh(tf, "Saved 400-unit walk", 16, NAVY, bold=True, after=0)
    tf = tb(s, Inches(0.65), Inches(1.68), Inches(5.7), Inches(1.2))
    fresh(tf, "Minimum centre separation     22.93", 16, DARK, after=3)
    fresh(tf, "Peak overlap integral     1.33", 16, DARK, after=3)
    fresh(tf, "Final overlap integral     \u2248 0", 16, DARK, after=0)
    fit(s, A / "image5.png", Inches(0.5), Inches(3.2), Inches(5.7), Inches(3.75))
    s.shapes.add_movie(
        str(A / "media2.mp4"), Inches(6.55), Inches(1.18), Inches(6.3), Inches(5.4),
        poster_frame_image=str(A / "image6.png"), mime_type="video/mp4",
    )
    tf = tb(s, Inches(6.55), Inches(6.62), Inches(6.3), Inches(0.4))
    fresh(tf, "Click the simulation to play", 14, TEAL, bold=True, align=PP_ALIGN.CENTER, after=0)

    # 8
    s = prs.slides.add_slide(blank)
    chrome(s, "Screened repulsion extends the interaction range", 8)
    formula_card(s, Inches(0.4), Inches(1.2), Inches(12.55), Inches(2.35),
                 "Screened field and area-dependent strength", [
                     [T("(1 \u2212 \u03bb"), T("2", sup=True), T("\u2207"), T("2", sup=True),
                      T(") \u03c8"), T("i", sub=True), T(" = \u03c6"), T("i", sub=True), T("2", sup=True)],
                     [T("A"), T("i", sub=True), T(" = \u222b \u03c6"), T("i", sub=True), T(" dA"),
                      T("        "), T("q"), T("i", sub=True), T(" = "), T("c"), T("i", sub=True),
                      T("A"), T("i", sub=True), T(" / "), T("A"), T("0", sub=True),
                      T("        "), T("A"), T("0", sub=True), T(" = \u03c0"),
                      T("R"), T("0", sub=True), T("2", sup=True)],
                 ], size=18)
    formula_card(s, Inches(0.4), Inches(3.75), Inches(12.55), Inches(2.15),
                 "Contribution to the chemical potential", [
                     [T("\u03bc"), T("rep,i", sub=True), T(" = 2 "), T("k"), T("rep", sub=True),
                      T(" \u03c6"), T("i", sub=True), T("\u03c6"), T("j", sub=True), T("2", sup=True),
                      T(" + 2 "), T("k"), T("soft", sub=True), T(" q"), T("i", sub=True),
                      T("q"), T("j", sub=True), T(" \u03c6"), T("i", sub=True), T("\u03c8"), T("j", sub=True)],
                     [T("f"), T("rep,i", sub=True), T(" = \u2212\u03c6"), T("i", sub=True),
                      T(" \u2207\u03bc"), T("rep,i", sub=True)],
                 ], size=17)
    rrect(s, Inches(0.4), Inches(6.1), Inches(12.55), Inches(0.9), SOFT, None)
    tf = tb(s, Inches(0.55), Inches(6.1), Inches(12.25), Inches(0.9), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Offset tests:     \u03bb = 8          ksoft = 15 or 0", 20, NAVY, bold=True, after=0)

    # 9
    s = prs.slides.add_slide(blank)
    chrome(s, "Steric torque and rotational drag", 9)
    formula_card(s, Inches(0.35), Inches(1.15), Inches(6.25), Inches(2.55),
                 "Torque about the cell centre", [
                     [T("R"), T("i", sub=True), T(" = (\u222b "), T("r", bold=True),
                      T(" \u03c6"), T("i", sub=True), T(" dA) / "), T("A"), T("i", sub=True)],
                     [T("\u03c4"), T("i", sub=True), T(" = \u222b [(r \u2212 "), T("R", bold=True),
                      T("i", sub=True), T(") \u00d7 "), T("f"), T("rep,i", sub=True),
                      T("]"), T("z", sub=True), T(" dA")],
                 ], size=15)
    formula_card(s, Inches(6.75), Inches(1.15), Inches(6.2), Inches(2.55),
                 "Overdamped angular balance", [
                     [T("\u03be"), T("rot,i", sub=True), T(" = \u03be \u222b \u03c6"), T("i", sub=True),
                      T(" |r \u2212 "), T("R", bold=True), T("i", sub=True), T("|"),
                      T("2", sup=True), T(" dA")],
                     [T("\u03c4"), T("i", sub=True), T(" = "), T("\u03be"), T("rot,i", sub=True),
                      T(" \u03c9"), T("i", sub=True)],
                 ], size=15)
    formula_card(s, Inches(0.35), Inches(3.9), Inches(6.25), Inches(2.35),
                 "Polarization update", [
                     [T("(\u2202"), T("t", sub=True), T("P"), T("i", sub=True), T(")"),
                      T("steric", sub=True), T(" = \u03c9"), T("i", sub=True),
                      T(" \u0177 \u00d7 "), T("P", bold=True), T("i", sub=True)],
                 ], size=16)
    tf = tb(s, Inches(0.55), Inches(5.55), Inches(5.85), Inches(0.6))
    fresh(tf, "Steric spin adds to the rotation from fluid vorticity.", 13, DARK, after=0)
    formula_card(s, Inches(6.75), Inches(3.9), Inches(6.2), Inches(2.35),
                 "Rotation measured over an encounter", [
                     [T("\u0394\u03b8"), T("steric", sub=True), T(" = \u222b \u03c9"), T("i", sub=True), T(" dt")],
                 ], size=16)
    tf = tb(s, Inches(6.95), Inches(5.55), Inches(5.8), Inches(0.6))
    fresh(tf, "Mean actin heading is the direction of \u222b \u03c6\u1d62P\u1d62 dA.", 13, DARK, after=0)
    rrect(s, Inches(0.35), Inches(6.4), Inches(12.6), Inches(0.65), SOFT, None)
    tf = tb(s, Inches(0.5), Inches(6.4), Inches(12.3), Inches(0.65), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Substrate drag balances the torque at each time step.", 16, NAVY, bold=True, after=0)

    # 10 — parameter labels corrected to the runs that produced these numbers
    s = prs.slides.add_slide(blank)
    chrome(s, "Offset scattering with and without screening", 10)
    rrect(s, Inches(0.4), Inches(1.12), Inches(6.15), Inches(0.48), TEAL, None)
    tf = tb(s, Inches(0.4), Inches(1.12), Inches(6.15), Inches(0.48), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Screening on     \u00b7     ksoft = 15", 16, WHITE, bold=True, align=PP_ALIGN.CENTER, after=0)
    rrect(s, Inches(6.75), Inches(1.12), Inches(6.15), Inches(0.48), NAVY, None)
    tf = tb(s, Inches(6.75), Inches(1.12), Inches(6.15), Inches(0.48), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Screening off     \u00b7     ksoft = 0", 16, WHITE, bold=True, align=PP_ALIGN.CENTER, after=0)
    s.shapes.add_movie(
        str(A / "media3.mp4"), Inches(0.7), Inches(1.75), Inches(5.5), Inches(3.7),
        poster_frame_image=str(A / "image7.png"), mime_type="video/mp4",
    )
    s.shapes.add_movie(
        str(A / "media4.mp4"), Inches(7.1), Inches(1.75), Inches(5.5), Inches(3.7),
        poster_frame_image=str(A / "image8.png"), mime_type="video/mp4",
    )
    rrect(s, Inches(0.4), Inches(5.65), Inches(6.15), Inches(1.35), PALE, None)
    tf = tb(s, Inches(0.55), Inches(5.78), Inches(5.85), Inches(1.1), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Closest separation  36.80", 18, NAVY, bold=True, after=4)
    fresh(tf, "Actin turn  34.84\u00b0     \u00b7     Steric rotation  0.28\u00b0", 15, DARK, after=0)
    rrect(s, Inches(6.75), Inches(5.65), Inches(6.15), Inches(1.35), PALE, None)
    tf = tb(s, Inches(6.9), Inches(5.78), Inches(5.85), Inches(1.1), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Closest separation  18.25", 18, NAVY, bold=True, after=4)
    fresh(tf, "Actin turn  15.71\u00b0     \u00b7     Steric rotation  1.91\u00b0", 15, DARK, after=0)

    # 11
    s = prs.slides.add_slide(blank)
    chrome(s, "Anchoring and collision geometry", 11)
    rrect(s, Inches(0.4), Inches(1.2), Inches(6.0), Inches(2.45), PALE, None)
    rect(s, Inches(0.4), Inches(1.2), Inches(0.1), Inches(2.45), TEAL)
    tf = tb(s, Inches(0.68), Inches(1.32), Inches(5.5), Inches(0.35))
    fresh(tf, "Same time window, t \u2264 24", 16, NAVY, bold=True, after=0)
    tf = tb(s, Inches(0.68), Inches(1.78), Inches(5.5), Inches(1.7))
    fresh(tf, "With anchoring          17.70\u00b0", 18, DARK, after=4)
    fresh(tf, "Without anchoring          0.43\u00b0", 18, DARK, after=4)
    fresh(tf, "Closest separations          36.80 and 36.40", 15, DARK, after=0)
    rrect(s, Inches(0.4), Inches(3.85), Inches(6.0), Inches(1.85), PALE, None)
    rect(s, Inches(0.4), Inches(3.85), Inches(0.1), Inches(1.85), TEAL)
    tf = tb(s, Inches(0.68), Inches(3.97), Inches(5.5), Inches(0.35))
    fresh(tf, "Unequal radii in an offset encounter", 16, NAVY, bold=True, after=0)
    tf = tb(s, Inches(0.68), Inches(4.42), Inches(5.5), Inches(1.1))
    fresh(tf, "R = 13 turns 12.15\u00b0.", 18, DARK, after=3)
    fresh(tf, "R = 9 turns 44.54\u00b0.", 18, DARK, after=0)
    fit(s, A / "image9.png", Inches(6.6), Inches(1.25), Inches(6.3), Inches(2.15))
    rrect(s, Inches(6.6), Inches(3.6), Inches(6.3), Inches(1.7), SOFT, None)
    tf = tb(s, Inches(6.8), Inches(3.75), Inches(5.95), Inches(1.45), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Head-on symmetry gives negligible torque.", 16, NAVY, bold=True, after=6)
    fresh(tf, "Mean polar order falls to 0.064.", 16, DARK, after=0)

    # 12
    s = prs.slides.add_slide(blank)
    chrome(s, "What changes when two cells meet?", 12)
    rows = [
        ("Run and tumble", "A prescribed heading reset redirects the cell between bursts of crawling."),
        ("Two-cell walk", "Separate fields preserve cell identity. The overlap penalty keeps interpenetration small in the saved run."),
        ("Controlled scattering", "Screened repulsion deflects the paths before contact. Anchoring drives most of the observed actin turn."),
    ]
    y = 1.25
    for name, body in rows:
        rrect(s, Inches(0.45), Inches(y), Inches(12.4), Inches(1.45), PALE, None)
        rect(s, Inches(0.45), Inches(y), Inches(0.1), Inches(1.45), TEAL)
        tf = tb(s, Inches(0.75), Inches(y + 0.12), Inches(11.9), Inches(0.4))
        fresh(tf, name, 18, NAVY, bold=True, after=0)
        tf = tb(s, Inches(0.75), Inches(y + 0.58), Inches(11.9), Inches(0.75))
        fresh(tf, body, 16, DARK, after=0)
        y += 1.6
    tf = tb(s, Inches(0.5), Inches(6.2), Inches(12.2), Inches(0.7))
    fresh(tf, "Thank you    \u00b7    Prof. Sujin B. Babu", 24, TEAL, bold=True, after=0)

    prs.save(str(OUT))
    return OUT


if __name__ == "__main__":
    print(build())
