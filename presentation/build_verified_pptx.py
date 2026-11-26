#!/usr/bin/env python3
"""Beautify the verified choladeck without changing its statements.

Same 12 slides, same sentences, same formulas. Formulas are set in
Cambria Math with subscripts. Slide 4 is pulled back onto the page.
"""

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

A = Path(__file__).resolve().parent / "verified_assets"
OUT = Path(__file__).resolve().parent / "BTP_Midsem_and_Post_Midsem_Beautified.pptx"

NAVY = RGBColor(0x0B, 0x3D, 0x5C)
TEAL = RGBColor(0x1A, 0x7A, 0x6D)
DARK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x4B, 0x55, 0x63)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF4, 0xF7, 0xFA)
LINE = RGBColor(0xD0, 0xD7, 0xDE)
SOFT = RGBColor(0xE7, 0xF3, 0xF1)
EQBG = RGBColor(0xEF, 0xF5, 0xF7)
MATH = "Cambria Math"
FONT = "Calibri"
W = Inches(13.333)
H = Inches(7.5)


def rect(slide, l, t, w, h, fill, line=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.shadow.inherit = False
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1.0)
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
        sh.line.width = Pt(1.15)
    try:
        sh.adjustments[0] = 0.08
    except Exception:
        pass
    return sh


def tb(slide, l, t, w, h, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    return tf


def fresh(tf, text, size, color, bold=False, align=PP_ALIGN.LEFT, before=0, after=3, italic=False, font=FONT):
    if tf.paragraphs[0].text == "" and not tf.paragraphs[0].runs:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(before)
    p.space_after = Pt(after)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = font
    return p


def _base(run, sub=False, sup=False):
    rPr = run._r.get_or_add_rPr()
    rPr.set("baseline", "-25000" if sub else ("30000" if sup else "0"))


def T(text, bold=False, italic=True, sub=False, sup=False, size=None, color=None):
    d = {"text": text, "bold": bold, "italic": italic, "sub": sub, "sup": sup}
    if size:
        d["size"] = size
    if color:
        d["color"] = color
    return d


def mathpara(tf, segs, size=18, color=NAVY, align=PP_ALIGN.CENTER, first=False, after=1):
    if first and tf.paragraphs[0].text == "" and not tf.paragraphs[0].runs:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(after)
    p.clear()
    for seg in segs:
        r = p.add_run()
        r.text = seg["text"]
        r.font.size = Pt(seg.get("size", size))
        r.font.bold = seg.get("bold", False)
        r.font.italic = seg.get("italic", True)
        r.font.color.rgb = seg.get("color", color)
        r.font.name = MATH
        if seg.get("sub"):
            _base(r, sub=True)
        elif seg.get("sup"):
            _base(r, sup=True)
    return p


def eqbox(slide, l, t, w, h, label, lines, size=17):
    rrect(slide, l, t, w, h, EQBG, TEAL)
    if label:
        tf = tb(slide, l + Inches(0.1), t + Inches(0.04), w - Inches(0.16), Inches(0.26))
        fresh(tf, label, 12, TEAL, bold=True, after=0)
        top = t + Inches(0.28)
        hh = h - Inches(0.34)
    else:
        top = t
        hh = h
    tf = tb(slide, l + Inches(0.08), top, w - Inches(0.14), hh, MSO_ANCHOR.MIDDLE)
    for i, line in enumerate(lines):
        mathpara(tf, line, size=size, first=(i == 0))
    return tf


def mid_footer(slide, n, total):
    rect(slide, 0, Inches(7.18), W, Inches(0.32), NAVY)
    label = "Mid-term" if n <= 4 else "End-term"
    tf = tb(slide, Inches(0.32), Inches(7.18), Inches(10.5), Inches(0.32), MSO_ANCHOR.MIDDLE)
    fresh(tf, f"PYD411   ·   {label}   ·   Dept of Physics, IIT Delhi   ·   Siddharth Kumar & Soumik Roy",
          12, WHITE, after=0)
    tf = tb(slide, Inches(11.2), Inches(7.18), Inches(1.85), Inches(0.32), MSO_ANCHOR.MIDDLE)
    fresh(tf, f"{n}   /   {total}", 12, WHITE, align=PP_ALIGN.RIGHT, after=0)


def title_bar(slide, title, subtitle=None):
    rect(slide, 0, 0, W, H, LIGHT)
    rect(slide, 0, 0, W, Inches(0.92), NAVY)
    rect(slide, 0, Inches(0.92), W, Inches(0.06), TEAL)
    tf = tb(slide, Inches(0.4), Inches(0.12), Inches(12.4), Inches(0.42))
    fresh(tf, title, 26, WHITE, bold=True, after=0)
    if subtitle:
        tf = tb(slide, Inches(0.42), Inches(0.52), Inches(12.4), Inches(0.32))
        fresh(tf, subtitle, 14, RGBColor(0xD6, 0xE4, 0xEA), after=0)


def fit(slide, path, l, t, max_w, max_h):
    im = Image.open(path)
    aw, ah = im.size
    scale = min(float(max_w) / aw, float(max_h) / ah)
    return slide.shapes.add_picture(str(path), Emu(int(l)), Emu(int(t)), Emu(int(aw * scale)), Emu(int(ah * scale)))


def card(slide, l, t, w, h):
    rrect(slide, l, t, w, h, WHITE, LINE)
    rect(slide, l, t, Inches(0.08), h, TEAL)


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # ----- 1 title (their words) -----
    s = prs.slides.add_slide(blank)
    rect(s, 0, 0, W, H, WHITE)
    rect(s, 0, 0, Inches(0.18), H, NAVY)
    rect(s, 0, Inches(6.85), W, Inches(0.65), NAVY)
    s.shapes.add_picture(str(A / "image2.jpg"), Inches(11.55), Inches(0.28), Inches(1.35), Inches(1.35))
    tf = tb(s, Inches(0.7), Inches(0.55), Inches(10.5), Inches(0.35))
    fresh(tf, "PYD411  ·  Mid-term evaluation  ·  B.Tech Project", 16, TEAL, bold=True, after=0)
    tf = tb(s, Inches(0.7), Inches(1.7), Inches(11.2), Inches(2.1))
    fresh(tf, "Phase-Field Modelling", 40, NAVY, bold=True, after=0)
    fresh(tf, "of Crawling Cells", 40, NAVY, bold=True, after=4)
    fresh(tf, "Towards a Tractable Two-Dimensional Model", 22, TEAL, after=0)
    tf = tb(s, Inches(0.7), Inches(4.3), Inches(11), Inches(2.0))
    fresh(tf, "Siddharth Kumar   ·   2023PH10741", 20, DARK, bold=True, after=2)
    fresh(tf, "Soumik Roy   ·   2023PH10756", 20, DARK, bold=True, after=8)
    fresh(tf, "Adviser:  Prof. Sujin B. Babu", 18, MUTED, after=2)
    fresh(tf, "Department of Physics, IIT Delhi   ·   2026 - 27, Semester I", 16, MUTED, after=0)

    # ----- 2 biology / model representation -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "What makes a crawling cell move?")
    mid_footer(s, 2, 9)
    rect(s, Inches(0.35), Inches(1.15), Inches(6.15), Inches(0.36), TEAL)
    tf = tb(s, Inches(0.45), Inches(1.15), Inches(5.9), Inches(0.36), MSO_ANCHOR.MIDDLE)
    fresh(tf, "PHYSICAL MECHANISMS", 14, WHITE, bold=True, after=0)
    blocks = [
        (1.62, "Actin treadmilling", ["Polymerises at the front, depolymerises at the rear", "Produces protrusive transport"]),
        (3.02, "Myosin contractility", ["Generates active contractile stress", "Helps retract the cell rear"]),
        (4.42, "Adhesion", ["Focal adhesions couple the cell to the substrate", "Coarse-grained as friction"]),
    ]
    for y, name, bullets in blocks:
        card(s, Inches(0.35), Inches(y), Inches(6.15), Inches(1.28))
        tf = tb(s, Inches(0.58), Inches(y + 0.08), Inches(5.75), Inches(1.1))
        fresh(tf, name, 16, NAVY, bold=True, after=1)
        for b in bullets:
            fresh(tf, "•  " + b, 13, DARK, after=0)
    rrect(s, Inches(0.35), Inches(5.82), Inches(6.15), Inches(1.15), SOFT, None)
    tf = tb(s, Inches(0.5), Inches(5.92), Inches(5.85), Inches(0.95), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Keratocyte fragments without a nucleus can still polarise and crawl — mechanics provides a major part of the behaviour.", 14, DARK, after=0)

    rect(s, Inches(6.72), Inches(1.15), Inches(6.25), Inches(0.36), NAVY)
    tf = tb(s, Inches(6.82), Inches(1.15), Inches(6.0), Inches(0.36), MSO_ANCHOR.MIDDLE)
    fresh(tf, "MODEL REPRESENTATION", 14, WHITE, bold=True, after=0)
    eqbox_specs = [
        (1.62, 0.85, "Phase field", [[T("\u03c6(x, t)")]], "\u03c6 \u2248 1 inside cell,    \u03c6 \u2248 0 outside"),
        (2.55, 0.85, "Actin polarization", [[T("P", bold=True), T("(x, t)")]], None),
        (3.48, 1.05, None, [[T("u", bold=True), T("  =  "), T("v", bold=True), T("  +  "), T("w"), T("0", sub=True), T("P", bold=True)]],
         "w\u2080P: treadmilling transport      v: friction/active-stress velocity"),
        (4.62, 1.05, None, [[T("\u03c3"), T("act", sub=True), T("  =  \u2212\u03b6 \u03c6 "), T("PP", bold=True)]],
         "convention:  \u03b6 < 0  is contractile"),
    ]
    for y, h, lab, lines, note in eqbox_specs:
        rrect(s, Inches(6.72), Inches(y), Inches(6.25), Inches(h), EQBG, TEAL)
        tf = tb(s, Inches(6.82), Inches(y + 0.02), Inches(6.05), Inches(h - 0.28), MSO_ANCHOR.MIDDLE)
        if lab:
            fresh(tf, lab, 12, TEAL, bold=True, align=PP_ALIGN.CENTER, after=0)
        mathpara(tf, lines[0], size=20, first=False)
        if note:
            fresh(tf, note, 11, MUTED, align=PP_ALIGN.CENTER, after=0)
    rrect(s, Inches(6.72), Inches(5.78), Inches(3.0), Inches(0.7), WHITE, LINE)
    tf = tb(s, Inches(6.72), Inches(5.78), Inches(3.0), Inches(0.7), MSO_ANCHOR.MIDDLE)
    mathpara(tf, [T("\u2212\u03be "), T("v", bold=True)], size=20, first=True)
    rrect(s, Inches(9.85), Inches(5.78), Inches(3.12), Inches(0.7), SOFT, None)
    tf = tb(s, Inches(9.95), Inches(5.78), Inches(2.95), Inches(0.7), MSO_ANCHOR.MIDDLE)
    fresh(tf, "strong adhesion \u2192 larger \u03be", 13, DARK, align=PP_ALIGN.CENTER, after=0)
    tf = tb(s, Inches(0.35), Inches(6.82), Inches(12.6), Inches(0.28))
    fresh(tf, "Tjhung et al., Nat. Commun. 2015  ·  Leoni & Sens, PRL 2017", 12, MUTED, after=0)

    # ----- 3 model -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "The model: shape, polarity and mechanics")
    mid_footer(s, 3, 9)
    eqbox(s, Inches(0.35), Inches(1.15), Inches(12.63), Inches(0.85), None, [[
        T("F", italic=True), T("  =  "), T("F"), T("interface", sub=True, size=13),
        T("  +  "), T("F"), T("polar", sub=True, size=13),
        T("  +  "), T("F"), T("Frank", sub=True, size=13),
        T("  +  "), T("F"), T("anchor", sub=True, size=13),
        T("  +  "), T("F"), T("area/volume", sub=True, size=13),
    ]], size=22)
    roles = [
        "Double-well:  separates cell (\u03c6\u22481) from outside (\u03c6\u22480)",
        "Surface tension:  gives the cell boundary an energetic cost",
        "Polar order:  favours |P| inside the cell",
        "Frank elasticity:  penalises strong spatial variation of P",
        "Anchoring \u03b2:  couples P to the cell edge and controls morphology",
    ]
    y = 2.15
    for role in roles:
        tf = tb(s, Inches(0.5), Inches(y), Inches(12.3), Inches(0.36))
        fresh(tf, role, 16, DARK, after=0)
        y += 0.38
    eqbox(s, Inches(0.35), Inches(4.15), Inches(8.7), Inches(0.85), None, [[
        T("0  =  \u2212\u2207p  +  \u03b7\u2207"), T("2", sup=True), T("v", bold=True),
        T("  \u2212  \u03be"), T("v", bold=True), T("  +  "), T("f", bold=True),
    ]], size=22)
    rrect(s, Inches(9.2), Inches(4.15), Inches(3.78), Inches(0.85), NAVY, None)
    tf = tb(s, Inches(9.2), Inches(4.15), Inches(3.78), Inches(0.85), MSO_ANCHOR.MIDDLE)
    mathpara(tf, [T("Re", italic=True), T("  \u223c  10"), T("\u22125", sup=True)], size=22, color=WHITE, first=True)
    tf = tb(s, Inches(0.4), Inches(5.10), Inches(12.5), Inches(0.32))
    fresh(tf, "Stokes force balance — inertia is negligible at the cell scale", 15, MUTED, after=0)
    # table
    rows = [
        ["Ver.", "Geometry", "Force balance", "Area / volume"],
        ["1", "Plane", "v = 0", "drifts 4.5%"],
        ["2", "Vertical slice + wall", "Brinkman / screened in z", "fixed"],
        ["3", "Plane", "incompressible Stokes", "fixed"],
        ["4", "Plane", "friction-dominated   v = f/\u03be", "soft volume"],
    ]
    table = s.shapes.add_table(5, 4, Inches(0.35), Inches(5.48), Inches(12.63), Inches(1.35)).table
    widths = [1.1, 3.3, 4.6, 3.63]
    for i, w in enumerate(widths):
        table.columns[i].width = Inches(w)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            run = p.add_run()
            run.text = val
            run.font.size = Pt(12)
            run.font.name = FONT
            run.font.bold = r == 0
            run.font.color.rgb = WHITE if r == 0 else DARK
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if r == 0 else (SOFT if r % 2 == 0 else WHITE)
    tf = tb(s, Inches(0.35), Inches(6.78), Inches(12.63), Inches(0.32))
    fresh(tf, "One ingredient at a time \u2192 identify what controls the behaviour.   Goal: many interacting cells \u2192 avoid a global Stokes solve.", 13, DARK, after=0)

    # ----- 4 simulation loop, rebuilt on the page -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "How the cell is simulated", "Coupled evolution of cell shape, actin polarity and active motion")
    mid_footer(s, 4, 9)
    rrect(s, Inches(3.4), Inches(1.12), Inches(6.5), Inches(0.42), NAVY, None)
    tf = tb(s, Inches(3.4), Inches(1.12), Inches(6.5), Inches(0.42), MSO_ANCHOR.MIDDLE)
    mathpara(tf, [T("\u03c6"), T("n", sup=True), T(",   "), T("P", bold=True), T("n", sup=True)], size=18, color=WHITE, first=True)
    tf = tb(s, Inches(6.3), Inches(1.52), Inches(0.7), Inches(0.22))
    fresh(tf, "\u2193", 16, TEAL, bold=True, align=PP_ALIGN.CENTER, after=0)
    eqbox(s, Inches(2.3), Inches(1.74), Inches(8.7), Inches(0.78), "FREE ENERGY", [[
        T("\u03bc = \u03b4F/\u03b4\u03c6", size=16), T("      "), T("\u03b4F/\u03b4"), T("P", bold=True, size=16),
    ]], size=16)
    # left column
    eqbox(s, Inches(0.28), Inches(2.64), Inches(6.35), Inches(1.05), "UPDATE P    (P\u207f \u2192 P\u207f\u207a\u00b9)", [[
        T("\u2202"), T("t", sub=True), T("P", bold=True), T(" + ("), T("u", bold=True), T("\u00b7\u2207)"), T("P", bold=True),
        T(" = \u2212"), T("\u03a9", bold=True), T("\u00b7"), T("P", bold=True),
        T(" + \u03c7"), T("D", bold=True), T("\u00b7"), T("P", bold=True), T(" \u2212 "), T("h", bold=True), T("/\u0393"),
    ]], size=13)
    tf = tb(s, Inches(0.4), Inches(3.72), Inches(6.1), Inches(0.28))
    fresh(tf, "advection + relaxation terms  ·  P: local direction & strength of actin", 11, MUTED, after=0)
    eqbox(s, Inches(0.28), Inches(4.02), Inches(6.35), Inches(0.72), None, [[
        T("f"), T("act", sub=True), T(" = \u2212\u03b6 \u2207\u00b7(\u03c6"), T("PP", bold=True), T(")"),
    ]], size=16)
    tf = tb(s, Inches(0.4), Inches(4.72), Inches(6.1), Inches(0.24))
    fresh(tf, "polarised actomyosin stress drives cytoplasmic motion", 11, MUTED, after=0)
    rrect(s, Inches(0.28), Inches(5.00), Inches(3.1), Inches(0.95), WHITE, TEAL)
    tf = tb(s, Inches(0.36), Inches(5.04), Inches(2.95), Inches(0.88))
    fresh(tf, "Full model", 12, TEAL, bold=True, after=0)
    mathpara(tf, [T("0=\u2212\u2207p+\u03b7\u2207"), T("2", sup=True), T("v", bold=True), T("\u2212\u03bev", bold=True), T("+"), T("f", bold=True)], size=11)
    fresh(tf, "\u2192 solve Stokes", 11, DARK, after=0)
    rrect(s, Inches(3.5), Inches(5.00), Inches(3.13), Inches(0.95), WHITE, TEAL)
    tf = tb(s, Inches(3.58), Inches(5.04), Inches(2.98), Inches(0.88))
    fresh(tf, "Version 4", 12, TEAL, bold=True, after=0)
    mathpara(tf, [T("v", bold=True), T(" = "), T("f", bold=True), T("/\u03be = \u2212(\u03b6/\u03be)\u2207\u00b7(\u03c6"), T("PP", bold=True), T(")")], size=11)
    tf = tb(s, Inches(0.28), Inches(5.96), Inches(6.35), Inches(0.22))
    fresh(tf, "V4: local velocity — no global pressure / Stokes solve", 11, MUTED, after=0)
    eqbox(s, Inches(0.28), Inches(6.18), Inches(6.35), Inches(0.85), None, [[
        T("u", bold=True), T("  =  "), T("v", bold=True), T("  +  "), T("w"), T("0", sub=True), T("P", bold=True),
    ]], size=16)
    # right
    rrect(s, Inches(6.85), Inches(2.64), Inches(6.15), Inches(2.55), EQBG, TEAL)
    tf = tb(s, Inches(7.0), Inches(2.72), Inches(5.85), Inches(2.4))
    fresh(tf, "UPDATE \u03c6    (\u03c6\u207f \u2192 \u03c6\u207f\u207a\u00b9)", 13, TEAL, bold=True, after=2)
    mathpara(tf, [
        T("\u2202"), T("t", sub=True), T("\u03c6 + \u2207\u00b7(\u03c6"), T("u", bold=True),
        T(") = \u2212M[\u03bc \u2212 \u039b g(\u03c6)]", size=14),
    ], size=15)
    fresh(tf, "uses  u  (transport) and  \u03bc  (from the free energy)", 12, DARK, before=4, after=1)
    fresh(tf, "\u03c6 determines the cell boundary and therefore the cell shape.", 12, DARK, after=1)
    fresh(tf, "g(\u03c6) = \u03c6(1\u2212\u03c6),    \u039b soft projected-area restoring term", 12, DARK, after=0)
    rrect(s, Inches(6.85), Inches(5.35), Inches(6.15), Inches(0.7), SOFT, None)
    tf = tb(s, Inches(6.95), Inches(5.38), Inches(5.95), Inches(0.64), MSO_ANCHOR.MIDDLE)
    fresh(tf, "\u21bb   \u03c6\u207f\u207a\u00b9, P\u207f\u207a\u00b9   \u2192   next timestep (t+\u0394t)   \u2192   back to  \u03c6\u207f, P\u207f", 12, NAVY, bold=True, after=0)
    tf = tb(s, Inches(6.85), Inches(6.15), Inches(6.15), Inches(0.9))
    fresh(tf, "Shape \u03c6, polarity P  \u2192  active force  \u2192  velocity v  \u2192  transport u  \u2192  shape update  \u2192  repeat", 13, NAVY, bold=True, after=2)
    fresh(tf, "This loop is repeated for every timestep.", 13, DARK, after=0)

    # ----- 5 run and tumble -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "Run and tumble in a single cell")
    mid_footer(s, 5, 12)
    tf = tb(s, Inches(0.45), Inches(1.15), Inches(12.2), Inches(0.4))
    fresh(tf, "Choose a heading  \u2192  crawl  \u2192  relax  \u2192  choose again", 20, NAVY, bold=True, after=0)
    eqbox(s, Inches(0.4), Inches(1.65), Inches(12.5), Inches(0.85), None, [[
        T("P", bold=True), T("  \u2190  \u03c6 (cos \u03b8, sin \u03b8)"),
        T("      |"), T("R", bold=True), T("(t) \u2212 "), T("R", bold=True), T("start", sub=True), T("|  \u2265  \u2113"), T("target", sub=True),
        T("      C = 4\u03c0A / perimeter"), T("2", sup=True),
    ]], size=16)
    fit(s, A / "image3.png", Inches(0.55), Inches(2.7), Inches(4.3), Inches(4.0))
    s.shapes.add_movie(str(A / "media1.mp4"), Inches(7.3), Inches(2.7), Inches(4.3), Inches(3.7),
                       poster_frame_image=str(A / "image4.png"), mime_type="video/mp4")
    tf = tb(s, Inches(7.3), Inches(6.45), Inches(4.5), Inches(0.35))
    fresh(tf, "Click the simulation to play", 14, TEAL, bold=True, align=PP_ALIGN.CENTER, after=0)

    # ----- 6 two fields -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "Two separate cell fields in a shared flow")
    mid_footer(s, 6, 12)
    pairs = [
        (0.4, 1.2, "One phase–polarization pair per cell", [
            [T("(\u03c6"), T("1", sub=True), T(", "), T("P", bold=True), T("1", sub=True),
             T(")    and    (\u03c6"), T("2", sub=True), T(", "), T("P", bold=True), T("2", sub=True), T(")")],
        ], "Each cell keeps its own crawl and relaxation cycle."),
        (6.85, 1.2, "Short-range steric repulsion", [
            [T("F"), T("rep", sub=True), T(" = "), T("k"), T("rep", sub=True),
             T(" \u222b \u03c6"), T("1", sub=True), T("2", sup=True), T(" \u03c6"), T("2", sub=True), T("2", sup=True), T(" dA")],
            [T("\u03bc"), T("rep,i", sub=True), T(" = 2 "), T("k"), T("rep", sub=True),
             T(" \u03c6"), T("i", sub=True), T(" \u03c6"), T("j", sub=True), T("2", sup=True)],
        ], None),
        (0.4, 3.7, "One incompressible Stokes solve", [
            [T("0 = \u2212\u2207p + \u03b7\u2207"), T("2", sup=True), T("v", bold=True),
             T(" \u2212 \u03be"), T("v", bold=True), T(" + "), T("f", bold=True), T("1", sub=True),
             T(" + "), T("f", bold=True), T("2", sub=True)],
            [T("\u2207\u00b7"), T("v", bold=True), T(" = 0"),
             T("          "), T("u", bold=True), T("i", sub=True),
             T(" = "), T("v", bold=True), T(" + "), T("w"), T("0,i", sub=True), T("P", bold=True), T("i", sub=True)],
        ], None),
        (6.85, 3.7, "Measure overlap during the walk", [
            [T("O(t) = \u222b \u03c6"), T("1", sub=True), T("\u03c6"), T("2", sub=True), T(" dA")],
        ], "A soft wall confines motion inside the box."),
    ]
    for x, y, lab, lines, note in pairs:
        rrect(s, Inches(x), Inches(y), Inches(6.1), Inches(2.25), WHITE, LINE)
        rect(s, Inches(x), Inches(y), Inches(0.08), Inches(2.25), TEAL)
        tf = tb(s, Inches(x + 0.22), Inches(y + 0.08), Inches(5.7), Inches(0.35))
        fresh(tf, lab, 15, NAVY, bold=True, after=0)
        tf = tb(s, Inches(x + 0.15), Inches(y + 0.45), Inches(5.8), Inches(1.15), MSO_ANCHOR.MIDDLE)
        for i, line in enumerate(lines):
            mathpara(tf, line, size=16, first=(i == 0))
        if note:
            tf = tb(s, Inches(x + 0.22), Inches(y + 1.65), Inches(5.7), Inches(0.5))
            fresh(tf, note, 13, DARK, after=0)

    # ----- 7 walk -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "Two cells stay distinct during the walk")
    mid_footer(s, 7, 12)
    rrect(s, Inches(0.4), Inches(1.2), Inches(6.3), Inches(1.7), WHITE, LINE)
    tf = tb(s, Inches(0.58), Inches(1.3), Inches(6.0), Inches(0.32))
    fresh(tf, "Saved 400-unit walk", 16, NAVY, bold=True, after=0)
    tf = tb(s, Inches(0.58), Inches(1.68), Inches(6.0), Inches(1.1))
    fresh(tf, "Minimum centre separation    22.93", 16, DARK, after=2)
    fresh(tf, "Peak overlap integral    1.33", 16, DARK, after=2)
    fresh(tf, "Final overlap integral    \u2248 0", 16, DARK, after=0)
    fit(s, A / "image5.png", Inches(0.55), Inches(3.05), Inches(5.6), Inches(3.9))
    s.shapes.add_movie(str(A / "media2.mp4"), Inches(6.7), Inches(1.25), Inches(6.1), Inches(5.15),
                       poster_frame_image=str(A / "image6.png"), mime_type="video/mp4")
    tf = tb(s, Inches(6.7), Inches(6.45), Inches(6.1), Inches(0.4))
    fresh(tf, "Click the simulation to play", 14, TEAL, bold=True, align=PP_ALIGN.CENTER, after=0)

    # ----- 8 screened -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "Screened repulsion extends the interaction range")
    mid_footer(s, 8, 12)
    eqbox(s, Inches(0.4), Inches(1.2), Inches(12.5), Inches(1.7), "Screened field and area-dependent strength", [
        [T("(1 \u2212 \u03bb"), T("2", sup=True), T("\u2207"), T("2", sup=True), T(") \u03c8"), T("i", sub=True),
         T(" = \u03c6"), T("i", sub=True), T("2", sup=True)],
        [T("A"), T("i", sub=True), T(" = \u222b \u03c6"), T("i", sub=True), T(" dA"),
         T("       "), T("q"), T("i", sub=True), T(" = "), T("c"), T("i", sub=True),
         T("A"), T("i", sub=True), T(" / "), T("A"), T("0", sub=True),
         T("       "), T("A"), T("0", sub=True), T(" = \u03c0"), T("R"), T("0", sub=True), T("2", sup=True)],
    ], size=18)
    eqbox(s, Inches(0.4), Inches(3.1), Inches(12.5), Inches(1.7), "Contribution to the chemical potential", [
        [T("\u03bc"), T("rep,i", sub=True), T(" = 2 "), T("k"), T("rep", sub=True),
         T(" \u03c6"), T("i", sub=True), T("\u03c6"), T("j", sub=True), T("2", sup=True),
         T(" + 2 "), T("k"), T("soft", sub=True), T(" q"), T("i", sub=True), T("q"), T("j", sub=True),
         T(" \u03c6"), T("i", sub=True), T("\u03c8"), T("j", sub=True)],
        [T("f"), T("rep,i", sub=True), T(" = \u2212\u03c6"), T("i", sub=True),
         T(" \u2207\u03bc"), T("rep,i", sub=True)],
    ], size=18)
    rrect(s, Inches(0.4), Inches(5.05), Inches(12.5), Inches(0.7), SOFT, None)
    tf = tb(s, Inches(0.55), Inches(5.05), Inches(12.2), Inches(0.7), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Offset tests:   \u03bb = 8        ksoft = 15 or 0", 18, NAVY, bold=True, after=0)

    # ----- 9 torque -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "Steric torque and rotational drag")
    mid_footer(s, 9, 12)
    boxes = [
        (0.35, 1.15, "Torque about the cell centre", [
            [T("R"), T("i", sub=True), T(" = (\u222b "), T("r", bold=True), T(" \u03c6"), T("i", sub=True),
             T(" dA) / "), T("A"), T("i", sub=True)],
            [T("\u03c4"), T("i", sub=True), T(" = \u222b [(r \u2212 "), T("R", bold=True), T("i", sub=True),
             T(") \u00d7 "), T("f"), T("rep,i", sub=True), T("]"), T("z", sub=True), T(" dA")],
        ]),
        (6.85, 1.15, "Overdamped angular balance", [
            [T("\u03be"), T("rot,i", sub=True), T(" = \u03be \u222b \u03c6"), T("i", sub=True),
             T(" |r \u2212 "), T("R", bold=True), T("i", sub=True), T("|"), T("2", sup=True), T(" dA")],
            [T("\u03c4"), T("i", sub=True), T(" = "), T("\u03be"), T("rot,i", sub=True), T(" \u03c9"), T("i", sub=True)],
        ]),
        (0.35, 3.45, "Polarization update", [
            [T("(\u2202"), T("t", sub=True), T("P"), T("i", sub=True), T(")"), T("steric", sub=True),
             T(" = \u03c9"), T("i", sub=True), T("  \u0177 \u00d7 "), T("P", bold=True), T("i", sub=True)],
        ]),
        (6.85, 3.45, "Rotation measured over an encounter", [
            [T("\u0394\u03b8"), T("steric", sub=True), T(" = \u222b \u03c9"), T("i", sub=True), T(" dt")],
        ]),
    ]
    for x, y, lab, lines in boxes:
        rrect(s, Inches(x), Inches(y), Inches(6.15), Inches(2.1), EQBG, TEAL)
        tf = tb(s, Inches(x + 0.12), Inches(y + 0.06), Inches(5.9), Inches(0.3))
        fresh(tf, lab, 13, TEAL, bold=True, after=0)
        tf = tb(s, Inches(x + 0.1), Inches(y + 0.38), Inches(5.95), Inches(1.15), MSO_ANCHOR.MIDDLE)
        for i, line in enumerate(lines):
            mathpara(tf, line, size=15, first=(i == 0))
    tf = tb(s, Inches(0.5), Inches(5.6), Inches(5.8), Inches(0.7))
    fresh(tf, "Steric spin adds to the rotation from fluid vorticity.", 14, DARK, after=0)
    tf = tb(s, Inches(7.0), Inches(5.6), Inches(5.8), Inches(0.7))
    fresh(tf, "Mean actin heading is the direction of \u222b \u03c6\u1d62P\u1d62 dA.", 14, DARK, after=0)
    rrect(s, Inches(0.35), Inches(6.35), Inches(12.65), Inches(0.65), SOFT, None)
    tf = tb(s, Inches(0.5), Inches(6.35), Inches(12.3), Inches(0.65), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Substrate drag balances the torque at each time step.", 16, NAVY, bold=True, after=0)
    # small torque trace from the previous deck, does not replace any sentence
    # placed? the cards fill the slide. Skip adding here to avoid covering text.

    # ----- 10 scattering videos -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "Offset scattering with and without screening")
    mid_footer(s, 10, 12)
    rrect(s, Inches(0.4), Inches(1.15), Inches(6.15), Inches(0.42), TEAL, None)
    tf = tb(s, Inches(0.4), Inches(1.15), Inches(6.15), Inches(0.42), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Screening on    ·    ksoft = 21", 16, WHITE, bold=True, align=PP_ALIGN.CENTER, after=0)
    rrect(s, Inches(6.75), Inches(1.15), Inches(6.15), Inches(0.42), NAVY, None)
    tf = tb(s, Inches(6.75), Inches(1.15), Inches(6.15), Inches(0.42), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Screening off    ·    ksoft = 6", 16, WHITE, bold=True, align=PP_ALIGN.CENTER, after=0)
    s.shapes.add_movie(str(A / "media3.mp4"), Inches(0.7), Inches(1.7), Inches(5.5), Inches(3.85),
                       poster_frame_image=str(A / "image7.png"), mime_type="video/mp4")
    s.shapes.add_movie(str(A / "media4.mp4"), Inches(7.05), Inches(1.7), Inches(5.5), Inches(3.85),
                       poster_frame_image=str(A / "image8.png"), mime_type="video/mp4")
    rrect(s, Inches(0.4), Inches(5.7), Inches(6.15), Inches(1.25), WHITE, LINE)
    tf = tb(s, Inches(0.55), Inches(5.82), Inches(5.85), Inches(1.05), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Closest separation  36.80", 16, NAVY, bold=True, after=2)
    fresh(tf, "Actin turn  34.84°    ·    Steric rotation  0.28°", 14, DARK, after=0)
    rrect(s, Inches(6.75), Inches(5.7), Inches(6.15), Inches(1.25), WHITE, LINE)
    tf = tb(s, Inches(6.9), Inches(5.82), Inches(5.85), Inches(1.05), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Closest separation  18.25", 16, NAVY, bold=True, after=2)
    fresh(tf, "Actin turn  15.71°    ·    Steric rotation  1.91°", 14, DARK, after=0)

    # ----- 11 anchoring -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "Anchoring and collision geometry")
    mid_footer(s, 11, 12)
    card(s, Inches(0.4), Inches(1.2), Inches(5.7), Inches(2.35))
    tf = tb(s, Inches(0.62), Inches(1.32), Inches(5.3), Inches(0.35))
    fresh(tf, "Same time window, t \u2264 24", 16, NAVY, bold=True, after=0)
    tf = tb(s, Inches(0.62), Inches(1.75), Inches(5.3), Inches(1.6))
    fresh(tf, "With anchoring      17.70°", 18, DARK, after=4)
    fresh(tf, "Without anchoring      0.43°", 18, DARK, after=4)
    fresh(tf, "Closest separations      36.80 and 36.40", 15, DARK, after=0)
    card(s, Inches(0.4), Inches(3.7), Inches(5.7), Inches(1.7))
    tf = tb(s, Inches(0.62), Inches(3.82), Inches(5.3), Inches(0.35))
    fresh(tf, "Unequal radii in an offset encounter", 16, NAVY, bold=True, after=0)
    tf = tb(s, Inches(0.62), Inches(4.25), Inches(5.3), Inches(1.0))
    fresh(tf, "R = 13 turns 12.15°.", 18, DARK, after=2)
    fresh(tf, "R = 9 turns 44.54°.", 18, DARK, after=0)
    fit(s, A / "image9.png", Inches(6.3), Inches(1.25), Inches(6.6), Inches(2.15))
    rrect(s, Inches(6.3), Inches(3.55), Inches(6.6), Inches(1.55), SOFT, None)
    tf = tb(s, Inches(6.45), Inches(3.7), Inches(6.3), Inches(1.3), MSO_ANCHOR.MIDDLE)
    fresh(tf, "Head-on symmetry gives negligible torque.", 16, NAVY, bold=True, after=4)
    fresh(tf, "Mean polar order falls to 0.064.", 16, DARK, after=0)

    # ----- 12 close -----
    s = prs.slides.add_slide(blank)
    title_bar(s, "What changes when two cells meet?")
    mid_footer(s, 12, 12)
    closes = [
        ("Run and tumble", "A prescribed heading reset redirects the cell between bursts of crawling."),
        ("Two-cell walk", "Separate fields preserve cell identity. The overlap penalty keeps interpenetration small in the saved run."),
        ("Controlled scattering", "Screened repulsion deflects the paths before contact. Anchoring drives most of the observed actin turn."),
    ]
    y = 1.2
    for name, body in closes:
        card(s, Inches(0.45), Inches(y), Inches(12.4), Inches(1.35))
        tf = tb(s, Inches(0.7), Inches(y + 0.1), Inches(11.9), Inches(0.35))
        fresh(tf, name, 18, NAVY, bold=True, after=0)
        tf = tb(s, Inches(0.7), Inches(y + 0.5), Inches(11.9), Inches(0.7))
        fresh(tf, body, 16, DARK, after=0)
        y += 1.5
    tf = tb(s, Inches(0.5), Inches(5.85), Inches(12.3), Inches(0.5))
    fresh(tf, "Thank you    ·    Prof. Sujin B. Babu", 22, TEAL, bold=True, after=0)

    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    print(build())
