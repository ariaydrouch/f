#!/usr/bin/env python3
"""Build the PYD411 mid-term PowerPoint (8 slides, 16:9, editable).

Same navy/teal academic theme as before. Content follows the detailed
slide-by-slide prompt supplied for this revision: real equations with
proper subscripts/bold vectors, the four-version table, real result
figures, and speaker notes on every slide. All numbers are consistency
checked (see the corrections noted inline).
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ASSETS = Path(__file__).resolve().parent / "assets"
OUT = Path(__file__).resolve().parent / "PYD411_midsem_presentation.pptx"

NAVY = RGBColor(0x0B, 0x3D, 0x5C)
TEAL = RGBColor(0x1A, 0x7A, 0x6D)
GOLD = RGBColor(0xB8, 0x86, 0x0B)
DARK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x4B, 0x55, 0x63)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF3, 0xF6, 0xF9)
LINE = RGBColor(0xD0, 0xD7, 0xDE)
SOFT = RGBColor(0xE8, 0xF3, 0xF1)
EQBG = RGBColor(0xEF, 0xF5, 0xF7)

FONT = "Calibri"


# ----------------------------------------------------------------- helpers --

def add_box(slide, l, t, w, h, fill, line=None, line_w=0.75):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    return sh


def add_round(slide, l, t, w, h, fill, line=None, line_w=1.0, radius=0.08):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    try:
        sh.adjustments[0] = radius
    except Exception:
        pass
    return sh


def textbox(slide, l, t, w, h, anchor=None):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.02)
    if anchor is not None:
        tf.vertical_anchor = anchor
    return box, tf


def _set_run(run, text, size, bold, color, italic=False, font=FONT):
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font


def para(tf, text, size=16, bold=False, color=DARK, align=PP_ALIGN.LEFT,
         space_after=6, space_before=0, italic=False, font=FONT, first=False,
         line_spacing=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    if line_spacing:
        p.line_spacing = line_spacing
    p.clear()
    r = p.add_run()
    _set_run(r, text, size, bold, color, italic, font)
    return p


def _subscript(run, sub=True, sup=False):
    rPr = run._r.get_or_add_rPr()
    rPr.set("baseline", "-25000" if sub else ("30000" if sup else "0"))


def mathpara(tf, segments, size=18, color=NAVY, align=PP_ALIGN.CENTER,
             space_after=4, space_before=0, first=False, font="Cambria Math"):
    """segments: list of dicts with text/bold/italic/sub/sup keys."""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.clear()
    for seg in segments:
        r = p.add_run()
        sz = seg.get("size", size)
        _set_run(r, seg["text"], sz, seg.get("bold", False), seg.get("color", color),
                 seg.get("italic", False), seg.get("font", font))
        if seg.get("sub"):
            _subscript(r, sub=True)
        elif seg.get("sup"):
            _subscript(r, sub=False, sup=True)
    return p


def T(text, bold=False, italic=False, sub=False, sup=False, size=None, color=None):
    d = {"text": text, "bold": bold, "italic": italic, "sub": sub, "sup": sup}
    if size:
        d["size"] = size
    if color:
        d["color"] = color
    return d


def bullet(tf, text, size=15, color=DARK, level=0, space_after=5, bold=False):
    p = tf.add_paragraph()
    p.level = level
    p.space_after = Pt(space_after)
    r = p.add_run()
    _set_run(r, text, size, bold, color)
    return p


def eqbox(slide, l, t, w, h, lines, size=18, fill=EQBG, border=TEAL,
          align=PP_ALIGN.CENTER, line_gap=3):
    """A bordered box containing one or more mathpara lines.
    `lines` is a list of segment-lists (each a full mathpara line)."""
    add_round(slide, l, t, w, h, fill, border, 1.25, radius=0.12)
    box, tf = textbox(slide, l, t, w, h, anchor=MSO_ANCHOR.MIDDLE)
    for i, segs in enumerate(lines):
        mathpara(tf, segs, size=size, align=align, first=(i == 0),
                 space_after=line_gap)
    return box


def header_bar(slide, title, subtitle=None):
    add_box(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.86), NAVY)
    add_box(slide, Inches(0), Inches(0.86), Inches(13.333), Inches(0.05), TEAL)
    box, tf = textbox(slide, Inches(0.4), Inches(0.10), Inches(12.4), Inches(0.46))
    para(tf, title, 25, True, WHITE, first=True, space_after=0)
    if subtitle:
        box2, tf2 = textbox(slide, Inches(0.4), Inches(0.50), Inches(12.4), Inches(0.32))
        para(tf2, subtitle, 12.5, False, RGBColor(0xC5, 0xD4, 0xDE), first=True, space_after=0)


def footer(slide, page, n=8):
    add_box(slide, Inches(0), Inches(7.22), Inches(13.333), Inches(0.28), LIGHT)
    box, tf = textbox(slide, Inches(0.35), Inches(7.22), Inches(10.5), Inches(0.26))
    para(tf, "PYD411  ·  Mid-term  ·  Dept of Physics, IIT Delhi  ·  Siddharth Kumar & Soumik Roy",
         11, False, MUTED, first=True, space_after=0)
    box2, tf2 = textbox(slide, Inches(11.6), Inches(7.22), Inches(1.4), Inches(0.26))
    para(tf2, f"{page} / {n}", 11, False, MUTED, PP_ALIGN.RIGHT, first=True, space_after=0)


def _png_size(path):
    import struct
    with open(path, "rb") as f:
        sig = f.read(8)
        if sig[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(path)
        f.read(4)
        if f.read(4) != b"IHDR":
            raise ValueError("no IHDR")
        w, h = struct.unpack(">II", f.read(8))
    return w, h


def picture(slide, name, l, t, w, h=None):
    """Place a picture; if w and h are both given, fit inside the box
    (keep aspect ratio) and centre it."""
    path = ASSETS / name
    if h is None:
        return slide.shapes.add_picture(str(path), l, t, width=w)
    iw, ih = _png_size(path)
    aspect = iw / ih
    box_a = w / h
    if aspect > box_a:
        pw, ph = w, w / aspect
    else:
        ph, pw = h, h * aspect
    pl = int(l + (w - pw) / 2)
    pt = int(t + (h - ph) / 2)
    return slide.shapes.add_picture(str(path), pl, pt, int(pw), int(ph))


def notes(slide, text):
    ns = slide.notes_slide
    ns.notes_text_frame.text = text


# --------------------------------------------------------------- slide 1 --

def slide_title(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), NAVY)
    add_box(s, Inches(0), Inches(0), Inches(0.18), Inches(7.5), TEAL)
    add_box(s, Inches(0), Inches(6.85), Inches(13.333), Inches(0.65), RGBColor(0x08, 0x30, 0x48))
    if (ASSETS / "Logo-IITD.jpg").exists():
        s.shapes.add_picture(str(ASSETS / "Logo-IITD.jpg"),
                              Inches(11.55), Inches(0.28), Inches(1.35), Inches(1.35))
    box, tf = textbox(s, Inches(0.7), Inches(0.45), Inches(10.5), Inches(0.4))
    para(tf, "PYD411  ·  Mid-term evaluation  ·  Bachelor's Thesis Project",
         16, False, RGBColor(0xA8, 0xC5, 0xD4), first=True, space_after=0)

    box, tf = textbox(s, Inches(0.7), Inches(1.55), Inches(11.6), Inches(1.7))
    para(tf, "Phase-Field Modelling", 40, True, WHITE, first=True, space_after=2)
    para(tf, "of Crawling Cells", 40, True, WHITE, space_after=10)
    para(tf, "Towards a Tractable Two-Dimensional Model", 22, False, RGBColor(0x7E, 0xD9, 0xC8))

    box, tf = textbox(s, Inches(0.7), Inches(4.15), Inches(11), Inches(2.3))
    para(tf, "Siddharth Kumar   ·   2023PH10741", 20, True, WHITE, first=True, space_after=4)
    para(tf, "Soumik Roy   ·   2023PH10756", 20, True, WHITE, space_after=12)
    para(tf, "Adviser:  Prof. Sujin B. Babu", 18, False, RGBColor(0xC5, 0xD4, 0xDE), space_after=6)
    para(tf, "Department of Physics, IIT Delhi   ·   2026 - 27, Semester I", 16, False,
         RGBColor(0xA8, 0xC5, 0xD4))

    box, tf = textbox(s, Inches(0.7), Inches(6.95), Inches(12), Inches(0.4))
    para(tf, "8 minutes  ·  8 slides  ·  2 minutes for discussion",
         13, False, RGBColor(0xA8, 0xC5, 0xD4), first=True, space_after=0)

    notes(s, "We are modelling crawling cells using a phase-field description "
              "coupled to actin polarization, with the longer-term goal of "
              "extending the model from one cell to many interacting cells.")


# --------------------------------------------------------------- slide 2 --

def slide_biology(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "What makes a crawling cell move?")
    footer(s, 2)

    # LEFT column -- physical mechanisms
    lx, lw = Inches(0.35), Inches(6.15)
    add_round(s, lx, Inches(1.05), lw, Inches(0.34), NAVY)
    box, tf = textbox(s, lx, Inches(1.05), lw, Inches(0.34), anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "PHYSICAL MECHANISMS", 13, True, WHITE, PP_ALIGN.CENTER, first=True, space_after=0)

    blocks = [
        ("Actin treadmilling",
         ["Polymerises at the front, depolymerises at the rear",
          "Produces protrusive transport"], TEAL),
        ("Myosin contractility",
         ["Generates active contractile stress",
          "Helps retract the cell rear"], GOLD),
        ("Adhesion",
         ["Focal adhesions couple the cell to the substrate",
          "Coarse-grained as friction"], TEAL),
    ]
    y = Inches(1.50)
    bh = Inches(1.28)
    for name, lines, accent in blocks:
        add_round(s, lx, y, lw, bh, LIGHT)
        add_box(s, lx, y, Inches(0.10), bh, accent)
        b2, tf2 = textbox(s, lx + Inches(0.28), y + Inches(0.08), lw - Inches(0.4), bh - Inches(0.16))
        para(tf2, name, 16, True, NAVY, first=True, space_after=4)
        for ln in lines:
            bullet(tf2, "\u2022  " + ln, 13, DARK, space_after=2)
        y = y + bh + Inches(0.14)

    add_round(s, lx, y + Inches(0.02), lw, Inches(0.95), SOFT)
    b3, tf3 = textbox(s, lx + Inches(0.16), y + Inches(0.10), lw - Inches(0.32), Inches(0.80))
    para(tf3, "Keratocyte fragments without a nucleus can still polarise "
              "and crawl \u2014 mechanics provides a major part of the "
              "behaviour.", 12.5, False, DARK, first=True, space_after=0)

    # RIGHT column -- model representation
    rx, rw = Inches(6.72), Inches(6.28)
    add_round(s, rx, Inches(1.05), rw, Inches(0.34), NAVY)
    box, tf = textbox(s, rx, Inches(1.05), rw, Inches(0.34), anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "MODEL REPRESENTATION", 13, True, WHITE, PP_ALIGN.CENTER, first=True, space_after=0)

    yy = Inches(1.50)
    eqbox(s, rx, yy, rw, Inches(0.62),
          [[T("Phase field   "), T("\u03c6", italic=True, size=22), T("(x, t)")]],
          size=16)
    b, tf = textbox(s, rx, yy + Inches(0.64), rw, Inches(0.30))
    para(tf, "\u03c6 \u2248 1 inside cell,   \u03c6 \u2248 0 outside", 13, False, MUTED,
         PP_ALIGN.CENTER, first=True, space_after=0)

    yy2 = yy + Inches(1.02)
    eqbox(s, rx, yy2, rw, Inches(0.62),
          [[T("Actin polarization   "), T("P", bold=True, size=22), T("(x, t)")]],
          size=16)

    yy3 = yy2 + Inches(0.80)
    eqbox(s, rx, yy3, rw, Inches(0.62),
          [[T("u", bold=True, size=22), T("  =  "), T("v", bold=True, size=22),
            T("  +  w"), T("0", sub=True), T("P", bold=True, size=22)]],
          size=20)
    b, tf = textbox(s, rx, yy3 + Inches(0.64), rw, Inches(0.44))
    para(tf, "w\u2080P: treadmilling transport      v: friction/active-stress velocity",
         12, False, MUTED, PP_ALIGN.CENTER, first=True, space_after=0)

    yy4 = yy3 + Inches(1.10)
    eqbox(s, rx, yy4, rw, Inches(0.60),
          [[T("\u03c3"), T("act", sub=True), T("  =  \u2212\u03b6 \u03c6 "),
            T("P", bold=True, size=20), T("P", bold=True, size=20)]],
          size=18)
    b, tf = textbox(s, rx, yy4 + Inches(0.62), rw, Inches(0.30))
    para(tf, "convention: \u03b6 < 0  is contractile", 12, False, MUTED,
         PP_ALIGN.CENTER, first=True, space_after=0)

    yy5 = yy4 + Inches(0.98)
    eqbox(s, rx, yy5, Inches(3.0), Inches(0.58),
          [[T("\u2212\u03be "), T("v", bold=True, size=20)]], size=20)
    b, tf = textbox(s, rx + Inches(3.15), yy5, rw - Inches(3.15), Inches(0.58),
                     anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "strong adhesion \u2192 larger \u03be", 12.5, False, DARK, first=True, space_after=0)

    box, tf = textbox(s, Inches(0.35), Inches(7.02), Inches(12.6), Inches(0.22))
    para(tf, "Tjhung et al., Nat. Commun. 2015  \u00b7  Leoni & Sens, PRL 2017",
         9.5, False, MUTED, PP_ALIGN.CENTER, first=True, space_after=0)

    notes(s, "We represent the cell by its shape field phi and the actin "
              "organisation by P. Treadmilling gives w0 P, active myosin "
              "stress gives the force that contributes to v, and substrate "
              "adhesion is coarse-grained as friction.")


# --------------------------------------------------------------- slide 3 --

def slide_model(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "The model: shape, polarity and mechanics")
    footer(s, 3)

    eqbox(s, Inches(0.35), Inches(1.02), Inches(12.63), Inches(0.62),
          [[T("F", italic=True, size=20), T("  =  F"), T("interface", sub=True, size=15),
            T("  +  F"), T("polar", sub=True, size=15), T("  +  F"), T("Frank", sub=True, size=15),
            T("  +  F"), T("anchor", sub=True, size=15), T("  +  F"), T("area/volume", sub=True, size=15)]],
          size=18)

    items = [
        ("Double-well", "separates cell (\u03c6\u22481) from outside (\u03c6\u22480)"),
        ("Surface tension", "gives the cell boundary an energetic cost"),
        ("Polar order", "favours |P| inside the cell"),
        ("Frank elasticity", "penalises strong spatial variation of P"),
        ("Anchoring \u03b2", "couples P to the cell edge and controls morphology"),
    ]
    y0 = Inches(1.80)
    rh = Inches(0.40)
    for i, (name, desc) in enumerate(items):
        y = y0 + i * rh
        b, tf = textbox(s, Inches(0.45), y, Inches(12.4), rh)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(0)
        r1 = p.add_run()
        _set_run(r1, f"{name}:  ", 14, True, TEAL)
        r2 = p.add_run()
        _set_run(r2, desc, 14, False, DARK)

    eqbox(s, Inches(0.35), Inches(3.92), Inches(9.0), Inches(0.62),
          [[T("0  =  \u2212\u2207p  +  \u03b7\u2207"), T("2", sup=True), T("v", bold=True, size=18),
            T("  \u2212  \u03be"), T("v", bold=True, size=18), T("  +  f", bold=True, italic=True)]],
          size=17)
    eqbox(s, Inches(9.55), Inches(3.92), Inches(3.43), Inches(0.62),
          [[T("Re  \u223c  10"), T("\u22125", size=13)]], size=18)
    b, tf = textbox(s, Inches(0.35), Inches(4.58), Inches(12.63), Inches(0.26))
    para(tf, "Stokes force balance \u2014 inertia is negligible at the cell scale",
         12.5, False, MUTED, PP_ALIGN.CENTER, first=True, space_after=0)

    rows = [
        ["Ver.", "Geometry", "Force balance", "Area / volume"],
        ["1", "Plane", "v = 0", "drifts 4.5%"],
        ["2", "Vertical slice + wall", "Brinkman / screened in z", "fixed"],
        ["3", "Plane", "incompressible Stokes", "fixed"],
        ["4", "Plane", "friction-dominated  v = f/\u03be", "soft volume"],
    ]
    table_shape = s.shapes.add_table(5, 4, Inches(0.35), Inches(5.02), Inches(12.63), Inches(1.75))
    table = table_shape.table
    table.columns[0].width = Inches(0.95)
    table.columns[1].width = Inches(3.55)
    table.columns[2].width = Inches(4.68)
    table.columns[3].width = Inches(3.45)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if i == 0 else (SOFT if i % 2 == 0 else WHITE)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.name = FONT
                    r.font.size = Pt(13)
                    r.font.bold = (i == 0) or (j == 0)
                    r.font.color.rgb = WHITE if i == 0 else DARK

    b, tf = textbox(s, Inches(0.35), Inches(6.86), Inches(12.63), Inches(0.32))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r1 = p.add_run()
    _set_run(r1, "One ingredient at a time \u2192 identify what controls the behaviour.   ", 13, True, NAVY)
    r2 = p.add_run()
    _set_run(r2, "Goal: many interacting cells \u2192 avoid a global Stokes solve.", 13, False, MUTED)

    notes(s, "The free energy controls the shape and polarisation, while the "
              "force balance determines motion. We progressively added physics "
              "so we could identify what was essential before simplifying the "
              "model for many-cell simulations.")


# --------------------------------------------------------------- slide 4 --

def slide_v12(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "From a translating disc to a leading protrusion")
    footer(s, 4)

    lx, lw = Inches(0.32), Inches(4.35)
    add_round(s, lx, Inches(1.02), lw, Inches(1.85), LIGHT)
    b, tf = textbox(s, lx + Inches(0.14), Inches(1.10), lw - Inches(0.28), Inches(1.70))
    para(tf, "Version 1", 16, True, NAVY, first=True, space_after=4)
    mathpara(tf, [T("v", bold=True), T(" = 0,   \u03b6 = \u03b2 = 0")], size=14,
             color=DARK, align=PP_ALIGN.LEFT, space_after=4)
    bullet(tf, "\u2022  Uniform P \u2192 uniform u \u2014 cell translates", 12.5, DARK, space_after=2)
    bullet(tf, "\u2022  Shape cannot change", 12.5, DARK, space_after=2)
    bullet(tf, "\u2022  Area falls 4.5% (non-conservative advection)", 12.5, DARK, space_after=0)

    add_round(s, lx, Inches(3.00), lw, Inches(3.75), SOFT)
    b, tf = textbox(s, lx + Inches(0.14), Inches(3.08), lw - Inches(0.28), Inches(3.60))
    para(tf, "Version 2", 16, True, TEAL, first=True, space_after=4)
    para(tf, "Vertical y\u2013z slice; substrate at z = 0. Treadmilling "
              "restricted to a layer of thickness \u03bb:", 12.5, False, DARK, space_after=6)
    mathpara(tf, [T("w(z) = "), T("w"), T("0", sub=True), T("/2 \u00b7 [1\u2212tanh((z\u2212\u03bb)/w"),
                  T("\u03c4", sub=False, size=13), T(")]")], size=13, color=NAVY,
             align=PP_ALIGN.LEFT, space_after=8)
    para(tf, "Near-wall material moves ahead \u2192 tension pulls the "
              "interface back \u2192 protrusion emerges.", 12.5, False, DARK, space_after=0)

    rx, rw = Inches(4.85), Inches(8.15)
    picture(s, "fig_v2_shapes.png", rx, Inches(1.00), rw, Inches(2.55))

    rows = [
        ["w\u2080", "Shape", "Contact", "Speed"],
        ["0.3", "cap", "44.0", "0.050"],
        ["2.0", "protrusion", "63.0", "0.432"],
    ]
    table_shape = s.shapes.add_table(3, 4, rx, Inches(3.65), Inches(5.55), Inches(0.90))
    table = table_shape.table
    table.columns[0].width = Inches(1.00)
    table.columns[1].width = Inches(2.05)
    table.columns[2].width = Inches(1.25)
    table.columns[3].width = Inches(1.25)
    for i in range(3):
        table.rows[i].height = Inches(0.30)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if i == 0 else (SOFT if i % 2 else WHITE)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.name = FONT
                    r.font.size = Pt(12.5)
                    r.font.bold = i == 0
                    r.font.color.rgb = WHITE if i == 0 else DARK

    eqbox(s, rx + Inches(5.75), Inches(3.65), Inches(2.40), Inches(0.90),
          [[T("w"), T("0", sub=True), T("*"), T(" \u2248 0.8")],
           [T("M\u03b5"), T("2", sup=True), T("/\u03bb \u2248 0.75", size=13)]],
          size=17, line_gap=3)

    picture(s, "fig_v2_transition.png", rx, Inches(4.95), rw, Inches(1.80))

    b, tf = textbox(s, rx, Inches(6.82), rw, Inches(0.30))
    para(tf, "Volume error  10\u207b\u00b9\u2076", 12.5, False, MUTED, PP_ALIGN.CENTER,
         first=True, space_after=0)

    notes(s, "Version 1 showed that uniform polarity can translate a cell but "
              "cannot deform it. Introducing a spatial gradient in "
              "treadmilling near the substrate produces the leading "
              "protrusion, with a transition near w0 approximately 0.8.")


# --------------------------------------------------------------- slide 5 --

def slide_v3(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "Full Stokes model: anchoring controls shape")
    footer(s, 5)

    lx, lw = Inches(0.32), Inches(3.55)
    add_round(s, lx, Inches(1.00), lw, Inches(1.65), LIGHT)
    b, tf = textbox(s, lx + Inches(0.14), Inches(1.08), lw - Inches(0.28), Inches(1.50))
    para(tf, "Passive check", 15, True, NAVY, first=True, space_after=4)
    bullet(tf, "\u2022  Ellipse \u2192 circle", 12.5, DARK, space_after=2)
    bullet(tf, "\u2022  Energy decreases", 12.5, DARK, space_after=2)
    bullet(tf, "\u2022  Flow vanishes", 12.5, DARK, space_after=2)
    bullet(tf, "\u2022  Volume error = 0", 12.5, DARK, space_after=0)

    picture(s, "fig_v3_morph.png", Inches(4.00), Inches(1.00), Inches(9.00), Inches(3.15))
    b, tf = textbox(s, Inches(4.00), Inches(4.18), Inches(9.00), Inches(0.26))
    para(tf, "Two active morphologies at  w\u2080 = 1", 12.5, True, MUTED,
         PP_ALIGN.CENTER, first=True, space_after=0)

    add_round(s, lx, Inches(2.78), lw, Inches(1.62), SOFT)
    b, tf = textbox(s, lx + Inches(0.14), Inches(2.84), lw - Inches(0.28), Inches(0.80))
    para(tf, "Strong anchoring", 13, True, TEAL, first=True, space_after=2)
    para(tf, "Radial actin aster,  |\u27e8P\u27e9| = 0,  speed = 0",
         12, False, DARK, space_after=2)
    para(tf, "Symmetry must break for motility", 11, False, MUTED, space_after=0)

    add_round(s, lx, Inches(4.52), lw, Inches(1.30), SOFT)
    b, tf = textbox(s, lx + Inches(0.14), Inches(4.58), lw - Inches(0.28), Inches(0.85))
    para(tf, "Moderate anchoring", 13, True, TEAL, first=True, space_after=2)
    para(tf, "Lamellipodial fan", 12, False, DARK, space_after=2)
    para(tf, "Aspect ratio = 2.91,  speed = 0.843 \u2248 w\u2080", 12, False, DARK, space_after=0)

    # 2x2 table as a real table (boxed look)
    tx = Inches(4.35)
    ty = Inches(4.42)
    add_round(s, tx, ty, Inches(4.70), Inches(1.62), EQBG, TEAL, 1.25, radius=0.10)
    hdr_tf_box, hdr_tf = textbox(s, tx, ty + Inches(0.06), Inches(4.70), Inches(0.28))
    para(hdr_tf, "aspect ratio", 12, True, NAVY, PP_ALIGN.CENTER, first=True, space_after=0)
    tbl = s.shapes.add_table(3, 3, tx + Inches(0.15), ty + Inches(0.36), Inches(4.40), Inches(1.15)).table
    tbl.cell(0, 0).text = ""
    tbl.cell(0, 1).text = "flow off"
    tbl.cell(0, 2).text = "flow on"
    tbl.cell(1, 0).text = "\u03b2 = 0"
    tbl.cell(1, 1).text = "1.07"
    tbl.cell(1, 2).text = "1.61"
    tbl.cell(2, 0).text = "\u03b2 = 0.25"
    tbl.cell(2, 1).text = "2.85"
    tbl.cell(2, 2).text = "2.92"
    for i in range(3):
        for j in range(3):
            c = tbl.cell(i, j)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            if i == 0 or j == 0:
                c.fill.fore_color.rgb = NAVY
                txtcolor = WHITE
            else:
                c.fill.fore_color.rgb = GOLD if (i, j) == (2, 2) else SOFT
                txtcolor = DARK
            for p in c.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.name = FONT
                    r.font.size = Pt(14)
                    r.font.bold = True
                    r.font.color.rgb = txtcolor

    b, tf = textbox(s, Inches(9.20), Inches(4.42), Inches(3.80), Inches(1.62), anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "Flow added on top of anchoring changes aspect ratio "
              "by only ~2%.", 13, False, DARK, first=True, space_after=0)

    picture(s, "fig_v3_decomp.png", Inches(0.32), Inches(6.14), Inches(3.55), Inches(0.85))

    b, tf = textbox(s, Inches(4.10), Inches(6.14), Inches(8.90), Inches(0.90))
    para(tf, "No planar pseudopod / phagocytic cup: these require 3D structure.",
         12.5, True, DARK, first=True, space_after=4)
    para(tf, "Constant \u03be cannot reproduce the biphasic adhesion\u2013speed "
              "mechanism of Leoni & Sens.", 11.5, False, MUTED, space_after=0)

    notes(s, "The full model shows that anchoring of the polarization at the "
              "boundary is the dominant control on planar shape. Adding "
              "hydrodynamic flow changes the elongated shape by only about "
              "two percent, motivating a friction-dominated reduction.")


# --------------------------------------------------------------- slide 6 --

def slide_v4(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "Version 4 \u2014 crawling without a Stokes solve")
    footer(s, 6)

    # left column: the reduction, stacked equations
    lx, lw = Inches(0.32), Inches(4.55)
    eqbox(s, lx, Inches(1.00), lw, Inches(0.55),
          [[T("\u03b7 / (\u03be R"), T("2", sup=True), T(")  \u2248  0.006")]], size=18)
    b, tf = textbox(s, lx, Inches(1.57), lw, Inches(0.30))
    para(tf, "friction dominates viscosity at the cell scale", 11.5, False, MUTED,
         PP_ALIGN.CENTER, first=True, space_after=0)

    eqbox(s, lx, Inches(1.96), lw, Inches(0.50),
          [[T("0 = \u2212\u2207p + \u03b7\u2207"), T("2", sup=True), T("v", bold=True, size=15),
            T(" \u2212 \u03be"), T("v", bold=True, size=15), T(" + f", bold=True, italic=True, size=15)]],
          size=13.5)
    b, tf = textbox(s, lx, Inches(2.48), lw, Inches(0.26))
    para(tf, "\u21d3", 20, True, TEAL, PP_ALIGN.CENTER, first=True, space_after=0)
    eqbox(s, lx, Inches(2.76), lw, Inches(0.52),
          [[T("v", bold=True, size=20), T("  =  f", bold=True, italic=True, size=20), T(" / \u03be")]],
          size=18, fill=SOFT)

    b, tf = textbox(s, lx, Inches(3.34), lw, Inches(0.24))
    para(tf, "\u21d3", 20, True, TEAL, PP_ALIGN.CENTER, first=True, space_after=0)
    eqbox(s, lx, Inches(3.60), lw, Inches(0.50),
          [[T("f"), T("act", sub=True), T(" = \u2212\u03b6 \u2207\u00b7(\u03c6", size=14),
            T("P", bold=True, size=15), T("P", bold=True, size=15), T(")", size=14)]],
          size=14)

    b, tf = textbox(s, lx, Inches(4.12), lw, Inches(0.24))
    para(tf, "\u21d3", 20, True, TEAL, PP_ALIGN.CENTER, first=True, space_after=0)
    eqbox(s, lx, Inches(4.38), lw, Inches(0.52),
          [[T("v", bold=True, size=17), T("  =  \u2212(\u03b6/\u03be) \u2207\u00b7(\u03c6", size=13),
            T("P", bold=True, size=14), T("P", bold=True, size=14), T(")", size=13)]],
          size=13, fill=SOFT)

    eqbox(s, lx, Inches(5.05), lw, Inches(0.50),
          [[T("u", bold=True, size=19), T("  =  "), T("v", bold=True, size=19),
            T("  +  w"), T("0", sub=True), T("P", bold=True, size=19)]],
          size=17)

    b, tf = textbox(s, lx, Inches(5.62), lw, Inches(0.65))
    para(tf, "No global Stokes / pressure solve \u2014 only local "
              "finite-difference stencils.", 12, True, NAVY, PP_ALIGN.CENTER,
         first=True, space_after=0, line_spacing=1.05)

    # right column: results
    rx, rw = Inches(5.05), Inches(7.95)
    picture(s, "fig_v4_montage.png", rx, Inches(1.00), rw, Inches(1.32))
    picture(s, "fig_v4_snapshots.png", rx, Inches(2.36), rw, Inches(1.32))
    picture(s, "fig_v4_diagnostics.png", rx, Inches(3.72), rw, Inches(0.85))

    add_round(s, rx, Inches(4.65), rw, Inches(2.55), LIGHT)
    b, tf = textbox(s, rx + Inches(0.20), Inches(4.75), rw - Inches(0.40), Inches(2.38))
    para(tf, "Travel 239.9  \u00b7  Time 299  (model units)  \u00b7  Speed 0.801  "
              "\u00b7  Aspect \u223c 3.2",
         13, True, NAVY, first=True, space_after=5)
    para(tf, "y\u1d04\u1d0d = 0  \u00b7  Area +15%  \u00b7  h/h\u2080 \u2248 0.87  "
              "(\u2248 13% thinning)", 13, True, NAVY, space_after=5)
    para(tf, "Volume conserved; projected area is allowed to change.",
         12, False, DARK, space_after=4)
    mathpara(tf, [T("k"), T("A", sub=True), T(" = 0  \u21d2  unbounded spreading / inflation")],
             size=12, color=DARK, align=PP_ALIGN.LEFT, space_after=5)
    para(tf, "V3 and V4 agree to within 0.2% in the comparable "
              "(flow-off, rigid-area) limit.", 12, False, MUTED, space_after=5)
    para(tf, "Cost/step: 2.70 \u2192 1.10 ms   \u00b7   stable dt: 0.01 \u2192 0.03",
         12, False, DARK, space_after=5)
    para(tf, "Overall runtime \u2248 5\u00d7 faster, including the larger "
              "stable time-step.", 12.5, True, TEAL, space_after=3,
         line_spacing=1.05)
    para(tf, "Local formulation \u2014 a practical starting point for many "
              "cells.", 12, False, DARK, space_after=0)

    notes(s, "At the cell scale the viscous contribution is only about zero "
              "point six percent of friction, so we use a friction-dominated "
              "force balance. The active stress gives a local velocity, "
              "eliminating the global Stokes solve. The resulting cell "
              "crawls steadily, reproduces the comparable full-model result, "
              "and is substantially cheaper.")


# --------------------------------------------------------------- slide 7 --

def slide_learn(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "What the simulations establish")
    footer(s, 7)

    items = [
        ("01", "A spatial gradient in treadmilling can generate a leading protrusion.",
         "V2"),
        ("02", "Planar morphology is controlled mainly by polarization anchoring.",
         "V3  \u00b7  flow adds ~2%"),
        ("03", "The friction-dominated model retains crawling behaviour.",
         "V4  \u00b7  speed 0.801  \u00b7  0.2% agreement  \u00b7  ~5\u00d7 faster  \u00b7  local"),
        ("04", "Volume conservation is more appropriate than rigid projected-area conservation.",
         "k\u2090 = 5: area +15%      k\u2090 = 0: inflation, crawling lost"),
    ]
    for i, (num, claim, ev) in enumerate(items):
        y = Inches(1.15 + i * 1.18)
        add_round(s, Inches(0.40), y, Inches(12.50), Inches(1.06), LIGHT)
        add_box(s, Inches(0.40), y, Inches(0.12), Inches(1.06), TEAL)
        box, tf = textbox(s, Inches(0.65), y + Inches(0.06), Inches(0.70), Inches(0.90))
        para(tf, num, 22, True, TEAL, first=True, space_after=0)
        box, tf = textbox(s, Inches(1.40), y + Inches(0.08), Inches(11.25), Inches(0.90))
        para(tf, claim, 16, True, NAVY, first=True, space_after=4)
        para(tf, ev, 12.5, False, MUTED)

    add_round(s, Inches(0.40), Inches(5.98), Inches(12.50), Inches(1.05), NAVY)
    box, tf = textbox(s, Inches(0.60), Inches(6.10), Inches(12.10), Inches(0.85))
    para(tf, "Take-home: a verified local single-cell model now reproduces "
              "crawling without a global Stokes solve \u2014 providing a "
              "computational base for many-cell simulations.",
         16, True, WHITE, first=True, space_after=0, line_spacing=1.05)

    notes(s, "The main outcome is not simply a faster simulation. We "
              "identified which mechanisms control the observed behaviour "
              "and reduced the model while retaining the essential "
              "single-cell crawling dynamics.")


# --------------------------------------------------------------- slide 8 --

def slide_next(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "From one cell to many")
    footer(s, 8)

    items = [
        ("1", "Two cells", "One field pair per cell + repulsive overlap."),
        ("2", "Collisions", "Head-on and glancing interactions."),
        ("3", "Polarity", "Allow cells to choose their own direction."),
        ("4", "Adhesion", "Load-dependent friction \u03be."),
        ("5", "Collectives", "Tens of cells: jamming and neighbour alignment."),
    ]
    for i, (n, title, body) in enumerate(items):
        x = Inches(0.32 + i * 2.58)
        add_round(s, x, Inches(1.15), Inches(2.48), Inches(2.35), LIGHT)
        box, tf = textbox(s, x + Inches(0.10), Inches(1.25), Inches(2.28), Inches(2.15))
        para(tf, f"{n}  {title}", 16, True, TEAL, first=True, space_after=8)
        para(tf, body, 12.5, False, DARK)

    add_round(s, Inches(0.32), Inches(3.75), Inches(12.68), Inches(3.20), NAVY)
    box, tf = textbox(s, Inches(0.60), Inches(3.95), Inches(12.15), Inches(2.85))
    para(tf, "Thank you \u2014 Questions", 32, True, WHITE, first=True, space_after=16)
    para(tf, "Siddharth Kumar  (2023PH10741)     \u00b7     Soumik Roy  (2023PH10756)",
         16, False, WHITE, space_after=8)
    para(tf, "Adviser: Prof. Sujin B. Babu     \u00b7     Department of Physics, IIT Delhi",
         15, False, RGBColor(0xC5, 0xD4, 0xDE))

    notes(s, "The immediate next step is two-cell interaction, followed by "
              "collisions and dynamic polarity. The ultimate goal is to "
              "study collective behaviour using the local formulation.")


# ---------------------------------------------------------------- main ----

def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_title(prs)
    slide_biology(prs)
    slide_model(prs)
    slide_v12(prs)
    slide_v3(prs)
    slide_v4(prs)
    slide_learn(prs)
    slide_next(prs)
    prs.save(OUT)
    print(f"Wrote {OUT}  ({OUT.stat().st_size/1024:.0f} KB, {len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
