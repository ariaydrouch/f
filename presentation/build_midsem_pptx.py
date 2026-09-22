#!/usr/bin/env python3
"""Build the PYD411 mid-term PowerPoint (8 slides, 16:9, editable)."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsmap, qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

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


def set_run(run, text, size=16, bold=False, color=DARK, font="Calibri"):
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_box(slide, l, t, w, h, fill, line=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    return sh


def add_round(slide, l, t, w, h, fill):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    # slightly tighter corners
    try:
        sh.adjustments[0] = 0.08
    except Exception:
        pass
    return sh


def tb(slide, l, t, w, h, text, size=16, bold=False, color=DARK,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri"):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.set(qn("a:lIns"), "0")
        # keep small insets
    except Exception:
        pass
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    set_run(p.add_run() if p.runs else p.runs[0] if False else _first_run(p),
            text, size, bold, color, font)
    # python-pptx: paragraph already has an empty run after add? Use clean way
    return box


def _first_run(p):
    if p.runs:
        return p.runs[0]
    return p.add_run()


def textbox(slide, l, t, w, h):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.02)
    return box, tf


def para(tf, text, size=16, bold=False, color=DARK, align=PP_ALIGN.LEFT,
         space_after=6, space_before=0, font="Calibri", first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.clear()
    r = p.add_run()
    set_run(r, text, size, bold, color, font)
    return p


def bullet(tf, text, size=15, color=DARK, level=0, space_after=5):
    p = tf.add_paragraph()
    p.level = level
    p.space_after = Pt(space_after)
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    set_run(r, text, size, False, color)
    return p


def header_bar(slide, title, subtitle=None):
    add_box(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.92), NAVY)
    add_box(slide, Inches(0), Inches(0.92), Inches(13.333), Inches(0.06), TEAL)
    box, tf = textbox(slide, Inches(0.4), Inches(0.12), Inches(12.4), Inches(0.48))
    para(tf, title, 26, True, WHITE, first=True, space_after=0)
    if subtitle:
        box2, tf2 = textbox(slide, Inches(0.4), Inches(0.52), Inches(12.4), Inches(0.34))
        para(tf2, subtitle, 13, False, RGBColor(0xC5, 0xD4, 0xDE), first=True, space_after=0)


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
    """Place a picture. If w and h are both given, fit inside the box
    (keep aspect) and centre it."""
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


def style_table(table, header=True):
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            # vertical center
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(13 if i else 13)
                    r.font.bold = (i == 0) or False
                    r.font.color.rgb = WHITE if i == 0 else DARK
            fill = NAVY if i == 0 else (SOFT if i % 2 == 0 else WHITE)
            # set fill
            solid = etree.SubElement(tcPr, qn("a:solidFill"))
            srgb = etree.SubElement(solid, qn("a:srgbClr"))
            srgb.set("val", f"{int(fill):06X}" if False else _hex(fill))
    # simpler fill via cell.fill
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if i == 0 else (SOFT if i % 2 == 0 else WHITE)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(13)
                    r.font.bold = i == 0
                    r.font.color.rgb = WHITE if i == 0 else DARK


def _hex(c):
    return f"{c[0]:02X}{c[1]:02X}{c[2]:02X}"


def slide_title(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), NAVY)
    add_box(s, Inches(0), Inches(0), Inches(0.18), Inches(7.5), TEAL)
    add_box(s, Inches(0), Inches(6.85), Inches(13.333), Inches(0.65), RGBColor(0x08, 0x30, 0x48))
    if (ASSETS / "Logo-IITD.jpg").exists():
        s.shapes.add_picture(str(ASSETS / "Logo-IITD.jpg"),
                             Inches(11.55), Inches(0.28), Inches(1.35), Inches(1.35))
    box, tf = textbox(s, Inches(0.7), Inches(0.45), Inches(10.5), Inches(0.4))
    para(tf, "PYD411  ·  Bachelor’s Thesis Project  ·  Mid-term evaluation",
         16, False, RGBColor(0xA8, 0xC5, 0xD4), first=True, space_after=0)
    box, tf = textbox(s, Inches(0.7), Inches(1.55), Inches(11.6), Inches(1.7))
    para(tf, "Phase-Field Modelling", 40, True, WHITE, first=True, space_after=2)
    para(tf, "of Crawling Cells", 40, True, WHITE, space_after=10)
    para(tf, "Towards a tractable two-dimensional model", 22, False, RGBColor(0x7E, 0xD9, 0xC8))

    box, tf = textbox(s, Inches(0.7), Inches(4.15), Inches(11), Inches(2.3))
    para(tf, "Siddharth Kumar   ·   2023PH10741", 20, True, WHITE, first=True, space_after=4)
    para(tf, "Soumik Roy   ·   2023PH10756", 20, True, WHITE, space_after=12)
    para(tf, "Adviser:  Prof. Sujin B. Babu", 18, False, RGBColor(0xC5, 0xD4, 0xDE), space_after=6)
    para(tf, "Dept of Physics, IIT Delhi   ·   2026 – 2027, Semester I", 16, False,
         RGBColor(0xA8, 0xC5, 0xD4))

    box, tf = textbox(s, Inches(0.7), Inches(6.95), Inches(12), Inches(0.4))
    para(tf, "8 minutes  ·  8 slides  ·  2 minutes for discussion",
         13, False, RGBColor(0xA8, 0xC5, 0xD4), first=True, space_after=0)


def slide_cell(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "What a crawling cell is — and how we write it down",
               "Three mechanical ingredients. Keratocyte fragments with no nucleus still crawl, so a lot of this is mechanics.")
    footer(s, 2)

    cards = [
        ("Actin treadmill",
         "Filaments polymerise at the front and depolymerise at the rear, pushing the membrane forward.",
         "Model: polarisation P  and  treadmilling speed  w₀",
         "The cell is carried by   u = v + w₀ P"),
        ("Myosin contractility",
         "Motors walk on actin and squeeze the rear so the body can follow the protrusion.",
         "Model: active stress   σ = −ζ φ P P",
         "ζ < 0  is contractile (actomyosin)"),
        ("Focal adhesions",
         "Linkers grip the substrate. Averaged over bind/unbind this is just a drag (Leoni & Sens, PRL 2017).",
         "Model: friction   −ξ v",
         "Strong adhesion  =  large ξ"),
    ]
    x0 = 0.38
    w = 4.05
    gap = 0.18
    for i, (title, bio, model, extra) in enumerate(cards):
        x = Inches(x0 + i * (w + gap))
        add_round(s, x, Inches(1.22), Inches(w), Inches(4.55), LIGHT)
        add_box(s, x, Inches(1.22), Inches(w), Inches(0.12), TEAL if i != 1 else GOLD)
        box, tf = textbox(s, x + Inches(0.14), Inches(1.42), Inches(w - 0.28), Inches(0.45))
        para(tf, title, 18, True, NAVY, first=True, space_after=0)
        box, tf = textbox(s, x + Inches(0.14), Inches(1.92), Inches(w - 0.28), Inches(1.45))
        para(tf, bio, 14, False, MUTED, first=True, space_after=0)
        add_round(s, x + Inches(0.14), Inches(3.50), Inches(w - 0.28), Inches(2.05), WHITE)
        box, tf = textbox(s, x + Inches(0.22), Inches(3.58), Inches(w - 0.44), Inches(1.90))
        para(tf, model, 14, True, TEAL, first=True, space_after=8)
        para(tf, extra, 14, False, DARK)

    add_round(s, Inches(0.38), Inches(5.92), Inches(12.55), Inches(1.12), SOFT)
    box, tf = textbox(s, Inches(0.55), Inches(6.00), Inches(12.2), Inches(1.0))
    para(tf, "Also in the model:  φ = 1 inside the cell, 0 outside  ·  ε = interface width  ·  β = anchoring of P at the edge (the main shape parameter).",
         14, False, DARK, first=True, space_after=3)
    para(tf, "We follow Tjhung, Tiribocchi, Marenduzzo & Cates, Nat. Commun. 6, 5420 (2015). Adhesion as friction: Leoni & Sens, PRL 118, 228101 (2017).",
         13, False, MUTED)


def slide_model(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "The model, built in four stages",
               "Add one ingredient at a time. The long-term goal is many cells — Stokes is too expensive for that.")
    footer(s, 3)

    add_round(s, Inches(0.38), Inches(1.20), Inches(12.55), Inches(1.55), LIGHT)
    box, tf = textbox(s, Inches(0.55), Inches(1.28), Inches(12.2), Inches(1.42))
    para(tf, "Fields:   φ  (cell)     P  (actin)     v  (cytoplasm)     u = v + w₀ P",
         17, True, NAVY, first=True, space_after=6)
    para(tf, "Free energy (in words): double well + surface tension + polar order only inside the cell + Frank elasticity + anchoring β.",
         14, False, DARK, space_after=4)
    para(tf, "Force balance is Stokes (Re ~ 10⁻⁵):   0 = −∇p + η ∇²v − ξ v + f.   Version 4 drops viscosity:  v = f / ξ  (Darcy / friction-dominated).",
         14, False, DARK)

    rows = [
        ["Ver.", "Geometry", "Force balance", "Area / volume"],
        ["1", "Plane, free space", "v = 0  (no flow)", "Drifts by 4.5%"],
        ["2", "Vertical slice + wall", "Brinkman, screened in z", "Fixed exactly"],
        ["3", "Plane (top view)", "Incompressible Stokes", "Fixed exactly"],
        ["4", "Plane (top view)", "Friction-dominated, local", "Soft volume  (k_A)"],
    ]
    table_shape = s.shapes.add_table(5, 4, Inches(0.38), Inches(2.95), Inches(12.55), Inches(3.15))
    table = table_shape.table
    table.columns[0].width = Inches(1.15)
    table.columns[1].width = Inches(3.55)
    table.columns[2].width = Inches(4.55)
    table.columns[3].width = Inches(3.30)
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
                    r.font.name = "Calibri"
                    r.font.size = Pt(14)
                    r.font.bold = i == 0 or j == 0
                    r.font.color.rgb = WHITE if i == 0 else DARK

    box, tf = textbox(s, Inches(0.38), Inches(6.22), Inches(12.55), Inches(0.85))
    para(tf, "Versions 2 and 3 are complementary, not a sequence: the protrusion is a near-substrate (side-view) structure; the catalogued cell shapes are top-view shapes. Version 4 is the model the multi-cell work will sit on.",
         14, False, MUTED, first=True, space_after=0)


def slide_v12(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "Versions 1 and 2  —  a translating disc, then a protrusion",
               "Version 2 is a side view: treadmilling only next to the wall.")
    footer(s, 4)

    add_round(s, Inches(0.32), Inches(1.18), Inches(4.15), Inches(2.55), LIGHT)
    box, tf = textbox(s, Inches(0.44), Inches(1.26), Inches(3.92), Inches(2.40))
    para(tf, "Version 1  ·  baseline", 16, True, NAVY, first=True, space_after=6)
    para(tf, "v = ζ = β = 0. A disc with uniform P translates but cannot change shape: uniform P gives uniform u.",
         13, False, DARK, space_after=4)
    para(tf, "Area falls 4.5% — advection was not conservative. That is fixed from Version 2 on.",
         13, False, MUTED)

    add_round(s, Inches(0.32), Inches(3.85), Inches(4.15), Inches(3.20), LIGHT)
    box, tf = textbox(s, Inches(0.44), Inches(3.93), Inches(3.92), Inches(3.05))
    para(tf, "Version 2  ·  the protrusion", 16, True, TEAL, first=True, space_after=6)
    para(tf, "w(z) confined to a layer of thickness λ at the wall. Near-wall material runs out; tension pulls it back.",
         13, False, DARK, space_after=4)
    para(tf, "w₀ = 0.3   cap, contact 44, speed 0.050", 13, True, DARK, space_after=2)
    para(tf, "w₀ = 2.0   thin protrusion, contact 63, speed 0.432", 13, True, DARK, space_after=4)
    para(tf, "Transition near w₀ ≈ 0.8  ≈  Mε²/λ. Volume error 10⁻¹⁶.",
         13, False, MUTED)

    picture(s, "fig_v2_shapes.png", Inches(4.65), Inches(1.18), Inches(8.30), Inches(3.15))
    picture(s, "fig_v2_transition.png", Inches(4.65), Inches(4.45), Inches(8.30), Inches(2.55))


def slide_v3(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "Version 3  —  top-view shapes, and what actually sets them",
               "Full Stokes model. Passive check: ellipse → circle, energy falls, flow dies, volume error = 0.")
    footer(s, 5)

    add_round(s, Inches(0.30), Inches(1.16), Inches(4.35), Inches(3.55), LIGHT)
    box, tf = textbox(s, Inches(0.42), Inches(1.24), Inches(4.12), Inches(3.40))
    para(tf, "Two morphologies  (w₀ = 1)", 15, True, NAVY, first=True, space_after=6)
    para(tf, "Strong anchoring → radial aster.  |⟨P⟩| = 0, speed = 0. Motility needs P to break symmetry.",
         13, False, DARK, space_after=6)
    para(tf, "Moderate anchoring → lamellipodial fan, elongated across the path. Aspect 2.91, speed 0.843 ≈ w₀.",
         13, False, DARK, space_after=6)
    para(tf, "No plane pseudopod or phagocytic cup: those need z. Version 2 already has the vertical protrusion.",
         13, False, MUTED)

    add_round(s, Inches(0.30), Inches(4.82), Inches(4.35), Inches(2.22), SOFT)
    box, tf = textbox(s, Inches(0.42), Inches(4.90), Inches(4.12), Inches(2.08))
    para(tf, "The 2 × 2  (the takeaway)", 15, True, TEAL, first=True, space_after=5)
    para(tf, "Neither  1.07    Flow only  1.61", 14, True, DARK, space_after=2)
    para(tf, "Anchoring only  2.85    Both  2.92", 14, True, DARK, space_after=5)
    para(tf, "Flow on top of anchoring adds ~2%. Speed ~0.80–0.85, set by w₀⟨P⟩, almost independent of ξ.",
         12, False, MUTED)

    picture(s, "fig_v3_morph.png", Inches(4.80), Inches(1.16), Inches(8.15), Inches(3.55))
    picture(s, "fig_v3_decomp.png", Inches(4.80), Inches(4.82), Inches(8.15), Inches(2.22))


def slide_v4(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "Version 4  —  the cell that crawls, without Stokes",
               "η / (ξ R²) ≈ 0.006  →  friction, not viscosity, balances the force.  v = f / ξ  is local algebra.")
    footer(s, 6)

    picture(s, "fig_v4_montage.png", Inches(0.32), Inches(1.14), Inches(8.55), Inches(2.05))
    picture(s, "fig_v4_snapshots.png", Inches(0.32), Inches(3.22), Inches(8.55), Inches(2.05))
    picture(s, "fig_v4_diagnostics.png", Inches(0.32), Inches(5.30), Inches(8.55), Inches(1.75))

    add_round(s, Inches(9.05), Inches(1.14), Inches(3.95), Inches(5.91), LIGHT)
    box, tf = textbox(s, Inches(9.18), Inches(1.22), Inches(3.70), Inches(5.75))
    para(tf, "Main result", 16, True, TEAL, first=True, space_after=8)
    para(tf, "Travel  239.9", 22, True, NAVY, space_after=0)
    para(tf, "in time 299", 14, False, MUTED, space_after=8)
    para(tf, "Steady speed  0.801", 20, True, NAVY, space_after=10)
    para(tf, "Disc → fan, then a straight crawl.  y_cm = 0. Aspect → ~3.2.",
         13, False, DARK, space_after=8)
    para(tf, "Area +15%, thickness −15%  (volume conserved).",
         13, False, DARK, space_after=8)
    para(tf, "V3 vs V4 (same limit):  0.2%", 14, True, DARK, space_after=4)
    para(tf, "Cost  2.70 → 1.10 ms/step,  ~5×.  k_A = 0 inflates 14× and stops.",
         13, False, MUTED, space_after=8)
    para(tf, "Local stencil  →  many cells become affordable.",
         13, True, TEAL)


def slide_learn(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "What we take from the mid-term",
               "Each claim is tied to a figure in the report.")
    footer(s, 7)

    items = [
        ("01", "A z-gradient in treadmilling is enough for a leading protrusion.",
         "Version 2  ·  transition at w₀ ≈ Mε²/λ ≈ 0.75"),
        ("02", "In the plane, shape is set by anchoring of P, not by the flow.",
         "Version 3  ·  anchoring 2.85  →  both 2.92  (~2%)"),
        ("03", "The cheap Darcy model crawls, and matches the full model where they overlap.",
         "Version 4  ·  speed 0.801  ·  0.2%  ·  ~5× faster  ·  local"),
        ("04", "Conserve volume, not projected area. Dropping the constraint is not viable.",
         "k_A = 5 spreads 15%  ·  k_A = 0 inflates 14× and stops"),
    ]
    for i, (num, claim, ev) in enumerate(items):
        y = Inches(1.20 + i * 1.18)
        add_round(s, Inches(0.40), y, Inches(12.50), Inches(1.08), LIGHT)
        add_box(s, Inches(0.40), y, Inches(0.12), Inches(1.08), TEAL)
        box, tf = textbox(s, Inches(0.65), y + Inches(0.08), Inches(0.70), Inches(0.90))
        para(tf, num, 22, True, TEAL, first=True, space_after=0)
        box, tf = textbox(s, Inches(1.40), y + Inches(0.10), Inches(11.25), Inches(0.88))
        para(tf, claim, 17, True, NAVY, first=True, space_after=4)
        para(tf, ev, 13, False, MUTED)

    add_round(s, Inches(0.40), Inches(5.95), Inches(12.50), Inches(1.10), NAVY)
    box, tf = textbox(s, Inches(0.60), Inches(6.10), Inches(12.10), Inches(0.85))
    para(tf, "Take-home: we now have a verified, local single-cell model that crawls — cheap enough to go to many cells.",
         18, True, WHITE, first=True, space_after=0)


def slide_next(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_box(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)
    header_bar(s, "What is next  —  and questions",
               "Version 4 was built so that none of this needs a Stokes solve.")
    footer(s, 8)

    items = [
        ("1", "Two cells", "One field pair per cell and a repulsive overlap, so they stay distinguishable."),
        ("2", "Collisions", "Head-on and glancing. Is contact inhibition a prediction?"),
        ("3", "Polarity", "A conserved polarity so a cell can choose its own direction."),
        ("4", "Adhesion", "Load-dependent ξ, to test the biphasic speed of Leoni & Sens."),
        ("5", "Collectives", "Tens of cells: jamming and neighbour alignment."),
    ]
    for i, (n, title, body) in enumerate(items):
        x = Inches(0.32 + i * 2.58)
        add_round(s, x, Inches(1.20), Inches(2.48), Inches(2.55), LIGHT)
        box, tf = textbox(s, x + Inches(0.10), Inches(1.30), Inches(2.28), Inches(2.35))
        para(tf, f"{n}  {title}", 16, True, TEAL, first=True, space_after=8)
        para(tf, body, 12, False, DARK)

    add_round(s, Inches(0.32), Inches(3.95), Inches(12.68), Inches(3.05), NAVY)
    box, tf = textbox(s, Inches(0.60), Inches(4.15), Inches(12.15), Inches(2.70))
    para(tf, "Thank you.", 32, True, WHITE, first=True, space_after=8)
    para(tf, "Questions and discussion  ·  2 minutes", 18, False, RGBColor(0x7E, 0xD9, 0xC8), space_after=14)
    para(tf, "Siddharth Kumar  (2023PH10741)     ·     Soumik Roy  (2023PH10756)",
         16, False, WHITE, space_after=6)
    para(tf, "Adviser: Prof. Sujin B. Babu     ·     Dept of Physics, IIT Delhi",
         15, False, RGBColor(0xC5, 0xD4, 0xDE))


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_title(prs)
    slide_cell(prs)
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
