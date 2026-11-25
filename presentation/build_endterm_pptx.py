#!/usr/bin/env python3
"""PYD411 end-term slides. 16:9, navy/teal, editable.

Title + 8 content slides + thank you.
No four-cell material. Numbers are the ones already in the end-term report.
"""

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ASSETS = Path(__file__).resolve().parent / "endterm_assets"
OUT = Path(__file__).resolve().parent / "SPCP_2023PH10741_2601PYD411_FP.pptx"

NAVY = RGBColor(0x0B, 0x3D, 0x5C)
TEAL = RGBColor(0x1A, 0x7A, 0x6D)
GOLD = RGBColor(0x8A, 0x5A, 0x00)
DARK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x4B, 0x55, 0x63)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF4, 0xF7, 0xFA)
LINE = RGBColor(0xD0, 0xD7, 0xDE)
SOFT = RGBColor(0xE7, 0xF3, 0xF1)

FONT = "Calibri"
W = Inches(13.333)
H = Inches(7.5)
TOTAL = 10  # title + 8 content + thank you


def rect(slide, l, t, w, h, fill, line=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.shadow.inherit = False
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1)
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


def _p(tf, first):
    return tf.paragraphs[0] if first else tf.add_paragraph()


def add_text(tf, text, size, color, bold=False, align=PP_ALIGN.LEFT, before=0, after=2, italic=False):
    p = _p(tf, not tf.paragraphs[0].text and len(tf.paragraphs) == 1 and tf.paragraphs[0].runs == [])
    # The check above is unreliable once a run exists. Use a flag via empty first para.
    p.alignment = align
    p.space_before = Pt(before)
    p.space_after = Pt(after)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = FONT
    return p


def fresh(tf, text, size, color, bold=False, align=PP_ALIGN.LEFT, before=0, after=3, italic=False):
    if tf.paragraphs[0].text == "" and len(tf.paragraphs) == 1 and not tf.paragraphs[0].runs:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(before)
    p.space_after = Pt(after)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = FONT
    return p


def footer(slide, n):
    rect(slide, 0, Inches(7.18), W, Inches(0.32), NAVY)
    tf = tb(slide, Inches(0.32), Inches(7.18), Inches(10.4), Inches(0.32), MSO_ANCHOR.MIDDLE)
    fresh(tf, "PYD411   ·   End-term   ·   Dept of Physics, IIT Delhi   ·   Siddharth Kumar & Soumik Roy",
          12, WHITE, after=0)
    tf2 = tb(slide, Inches(11.2), Inches(7.18), Inches(1.85), Inches(0.32), MSO_ANCHOR.MIDDLE)
    fresh(tf2, f"{n}   /   {TOTAL}", 12, WHITE, align=PP_ALIGN.RIGHT, after=0)


def chrome(slide, title, kicker):
    rect(slide, 0, 0, W, H, LIGHT)
    rect(slide, 0, 0, W, Inches(0.08), TEAL)
    tf = tb(slide, Inches(0.38), Inches(0.16), Inches(12.5), Inches(0.24))
    fresh(tf, kicker, 12, TEAL, bold=True, after=0)
    tf = tb(slide, Inches(0.36), Inches(0.38), Inches(12.6), Inches(0.46))
    fresh(tf, title, 26, NAVY, bold=True, after=0)
    return Inches(1.00)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def fit(slide, path, l, t, max_w, max_h):
    im = Image.open(path)
    aw, ah = im.size
    scale = min(float(max_w) / aw, float(max_h) / ah)
    w = int(aw * scale)
    h = int(ah * scale)
    return slide.shapes.add_picture(str(path), Emu(int(l)), Emu(int(t)), Emu(w), Emu(h))


def stat(slide, l, t, w, h, big, label, fill=WHITE):
    rrect(slide, l, t, w, h, fill, LINE)
    tf = tb(slide, l + Inches(0.08), t + Inches(0.06), w - Inches(0.16), Inches(0.42))
    fresh(tf, big, 22, NAVY, bold=True, after=0)
    tf = tb(slide, l + Inches(0.08), t + Inches(0.46), w - Inches(0.16), h - Inches(0.52))
    fresh(tf, label, 12, DARK, after=0)


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # ========== 1 TITLE ==========
    s = prs.slides.add_slide(blank)
    rect(s, 0, 0, W, H, WHITE)
    rect(s, 0, 0, Inches(0.22), H, NAVY)
    rect(s, Inches(0.22), 0, Inches(0.08), H, TEAL)
    tf = tb(s, Inches(0.7), Inches(1.35), Inches(12), Inches(0.32))
    fresh(tf, "PYD411     ·     END-TERM EVALUATION     ·     B.TECH PROJECT", 14, TEAL, bold=True, after=0)
    tf = tb(s, Inches(0.7), Inches(1.85), Inches(12), Inches(1.5))
    fresh(tf, "Phase-field modelling of crawling cells", 36, NAVY, bold=True, after=0)
    fresh(tf, "From one cell to a collision", 26, TEAL, bold=True, before=6, after=0)
    tf = tb(s, Inches(0.7), Inches(4.0), Inches(11), Inches(1.5))
    fresh(tf, "Siddharth Kumar     2023PH10741", 20, DARK, bold=True, after=2)
    fresh(tf, "Soumik Roy     2023PH10756", 20, DARK, bold=True, after=8)
    fresh(tf, "Adviser: Prof. Sujin B. Babu", 18, MUTED, after=2)
    fresh(tf, "Department of Physics, IIT Delhi     ·     2026–27, Semester I", 16, MUTED, after=0)
    notes(s, (
        "One sentence: this is the same project as the mid-term, and the new part is two cells that meet "
        "without becoming one cell. Do not open with a biology lecture."
    ))

    # ========== 2 SINGLE CELL ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "What one cell already does", "MID-TERM  ·  THE BASE THIS TALK STANDS ON")
    footer(s, 2)
    fit(s, ASSETS / "fig_v3_morph.png", Inches(0.28), Inches(1.05), Inches(5.15), Inches(4.45))
    fit(s, ASSETS / "fig_v2_shapes.png", Inches(5.55), Inches(1.05), Inches(7.4), Inches(2.55))
    fit(s, ASSETS / "fig_v4_montage.png", Inches(5.55), Inches(3.70), Inches(7.4), Inches(1.75))
    # three short lines under, full width above footer
    bits = [
        ("V2", "Wall layer. w₀ = 0.3: cap, speed 0.050. w₀ = 2.0: thin front, speed 0.432. Volume error 10⁻¹⁶."),
        ("V3", "Aster: speed 0. Fan: aspect 2.91, speed 0.843. Anchoring 2.85; with flow, 2.92. Flow adds ~2%."),
        ("V4", "η/(ξR²) ≈ 0.006. Speed 0.801, travel 239.9. Area +15%, h/h₀ ≈ 0.87. kₐ = 0 inflates ~14×."),
    ]
    x = Inches(0.32)
    for tag, body in bits:
        rrect(s, x, Inches(5.68), Inches(4.15), Inches(1.38), WHITE, LINE)
        tf = tb(s, x + Inches(0.08), Inches(5.74), Inches(3.95), Inches(0.28))
        fresh(tf, tag, 13, TEAL, bold=True, after=0)
        tf = tb(s, x + Inches(0.08), Inches(6.02), Inches(3.95), Inches(0.95))
        fresh(tf, body, 12, DARK, after=0)
        x = Emu(x + Inches(4.28))
    notes(s, (
        "One minute, then move on. V2: the protrusion exists only when treadmilling is stronger near the wall. "
        "V3: in the top view the fan is set by anchoring. The flow on top of anchoring changes the aspect ratio from 2.85 to 2.92, about 2 percent. "
        "The aster has zero mean polarization and zero speed. "
        "V4: for a single cell, friction dominates viscosity, ratio about 0.006, so the Stokes solve is not needed. "
        "Area grows about 15 percent and h/h0 is about 0.87. Do not say the thickness falls by 15 percent. "
        "If kA is zero the cell inflates about 14 times and crawling stops. "
        "The sentence that opens the next slide: a collision is different, because the cells push each other through the fluid."
    ))

    # ========== 3 TWO-CELL RULES ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "Two cells: two fields, one flow", "WHAT CHANGES, AND WHY")
    footer(s, 3)
    rules = [
        ("Not one shared φ", "A single phase field joins the cells into one region as soon as they touch. Each cell keeps its own φ and its own P."),
        ("One Stokes solve", "Both forces go in together. That is how one cell pushes the other. The single-cell Darcy law does not do this."),
        ("Contact repulsion", "F_rep = k_rep ∫ φ₁² φ₂². It is zero until the interfaces overlap, so a larger k_rep cannot steer them early."),
        ("A range, and a charge", "F_soft = k_soft q₁ q₂ ∫ φ₁² ψ₂, with q = area / reference area. Same structure as a product of two cell properties."),
    ]
    positions = [(0.35, 1.12), (6.85, 1.12), (0.35, 3.15), (6.85, 3.15)]
    for (title, body), (x, y) in zip(rules, positions):
        rrect(s, Inches(x), Inches(y), Inches(6.15), Inches(1.85), WHITE, LINE)
        rect(s, Inches(x), Inches(y), Inches(0.08), Inches(1.85), TEAL)
        tf = tb(s, Inches(x + 0.22), Inches(y + 0.12), Inches(5.75), Inches(0.4))
        fresh(tf, title, 18, NAVY, bold=True, after=0)
        tf = tb(s, Inches(x + 0.22), Inches(y + 0.55), Inches(5.75), Inches(1.15))
        fresh(tf, body, 14, DARK, after=0)
    rrect(s, Inches(0.35), Inches(5.18), Inches(12.65), Inches(1.82), SOFT, None)
    tf = tb(s, Inches(0.55), Inches(5.30), Inches(12.25), Inches(1.55))
    fresh(tf, "Overdamped torque, not stored angular momentum", 16, NAVY, bold=True, after=2)
    fresh(tf, "τ = ξ_rot ω,    with    ξ_rot = ξ ∫ φ |r − r_cm|² dA  =  5.1×10⁴ for these cells.", 15, DARK, after=2)
    fresh(tf, "A force along the line of centres does not torque a round cell. Head-on, the torque has to be zero. We do not add a spin by hand.", 14, DARK, after=0)
    notes(s, (
        "This is the slide to be ready to write on the board. "
        "Separate fields, because one field merges. "
        "One Stokes solve on the sum of the forces, because the professor’s point was that viscosity matters when they collide. "
        "The contact term only acts where both interfaces are occupied, so making it stronger does not steer them before they touch. "
        "The long-range piece has strength proportional to the product of the two areas. Doubling one charge doubles the force on both. "
        "There is no inertia. Torque sets a rotation rate against substrate friction. xi_rot is computed, 5.1 times 10 to the 4, not chosen. "
        "If they ask why head-on has no torque: the force passes through the centre."
    ))

    # ========== 4 CONTACT ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "They meet, and they stay two cells", "CONTACT REPULSION ONLY")
    footer(s, 4)
    fit(s, ASSETS / "offset_collision.png", Inches(0.28), Inches(1.05), Inches(8.15), Inches(4.55))
    stats = [
        ("2.07", "Peak overlap in the closed-box walk. About 8.7 if the penalty is absent at nominal contact."),
        ("18.3", "Closest separation when they keep pushing. Contact distance is 26. Overlap then peaks at 3.9."),
        ("16°", "Heading change in that push. The rigid rotation from τ/ξ_rot is 1.9° of it."),
        ("8.8°", "Fixed headings, off centre: 0° to −8.8°, and 180° to 171°. Flat until they touch."),
    ]
    y = Inches(1.08)
    for big, label in stats:
        stat(s, Inches(8.55), y, Inches(4.45), Inches(1.40), big, label)
        y = Emu(y + Inches(1.48))
    notes(s, (
        "Walk through the figure left to right: paths meet and separate, separation falls through 26, overlap rises to about 3.9, headings move about 16 degrees. "
        "The dashed curve on the right of the figure is the rigid rotation, 1.9 degrees. Most of the 16 is the shared flow and anchoring on the flattened edge, which was already in Version 3. "
        "The 2.07 is a different run: the walk in which they redirect. The non-interacting pair at nominal contact is about 8.7. "
        "The 8.8 degree pair is the controlled check with headings fixed and a vertical offset. Both angles sit still until overlap turns on."
    ))

    # ========== 5 AVOIDANCE + VIDEO ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "Give the repulsion a range, and they miss", "k_soft = 15,   λ = 8,   SAME OFFSET")
    footer(s, 5)
    fit(s, ASSETS / "offset_avoidance.png", Inches(0.25), Inches(1.05), Inches(8.05), Inches(4.15))
    s.shapes.add_movie(
        str(ASSETS / "offset_avoidance.mp4"),
        Inches(8.45), Inches(1.15), Inches(4.55), Inches(4.25),
        poster_frame_image=str(ASSETS / "poster_avoidance.png"),
        mime_type="video/mp4",
    )
    tf = tb(s, Inches(8.45), Inches(5.42), Inches(4.55), Inches(0.28))
    fresh(tf, "Click to play  ·  4.4 s  ·  arrows are P", 12, TEAL, bold=True, after=0)
    # three numbers along the bottom of the figure
    row = [
        ("36.8", "Closest separation. Contact is at 26. Overlap stays 0."),
        ("35°", "Each heading turns away from the other cell."),
        ("0.28°", "Rigid rotation from the torque over the whole run."),
    ]
    x = Inches(0.28)
    for big, label in row:
        stat(s, x, Inches(5.35), Inches(2.65), Inches(1.68), big, label, SOFT)
        x = Emu(x + Inches(2.72))
    notes(s, (
        "Play the clip. They start pointed at each other with a vertical offset and bend apart. "
        "Closest approach 36.8, contact would be 26, overlap zero. "
        "Headings turn 35 degrees. The rigid-body rotation from torque over xi_rot is 0.28 degrees. "
        "Do not say the torque spun them by 35 degrees. The next slide is that distinction. "
        "λ = 8 and k_soft = 15 were chosen so this offset misses and k_soft = 0 still collides. They are not derived constants."
    ))

    # ========== 6 ANCHORING ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "The heading turns because the edge does", "SAME RUN, ANCHORING SWITCHED OFF")
    footer(s, 6)
    trio = [
        ("35°", "Heading change", "Anchoring on. The cell deforms, and P stays normal to the new edge."),
        ("0.28°", "Rigid rotation", "∫ ω dt from τ = ξ_rot ω. Real, and too small to see."),
        ("0.4°", "Anchoring off", "The heading barely moves. They still miss: closest separation 36.4."),
    ]
    x = Inches(0.4)
    for big, title, body in trio:
        rrect(s, x, Inches(1.35), Inches(4.05), Inches(3.55), WHITE, LINE)
        rect(s, x, Inches(1.35), Inches(4.05), Inches(0.10), TEAL)
        tf = tb(s, x + Inches(0.2), Inches(1.65), Inches(3.65), Inches(0.9))
        fresh(tf, big, 40, NAVY, bold=True, after=0)
        tf = tb(s, x + Inches(0.2), Inches(2.6), Inches(3.65), Inches(0.4))
        fresh(tf, title, 16, TEAL, bold=True, after=0)
        tf = tb(s, x + Inches(0.2), Inches(3.15), Inches(3.65), Inches(1.4))
        fresh(tf, body, 15, DARK, after=0)
        x = Emu(x + Inches(4.25))
    rrect(s, Inches(0.4), Inches(5.15), Inches(12.5), Inches(1.8), NAVY, None)
    tf = tb(s, Inches(0.65), Inches(5.35), Inches(12.05), Inches(1.45))
    fresh(tf, "The force deflects the centres. Anchoring turns the heading.", 22, WHITE, bold=True, after=6)
    fresh(tf, "Head-on, symmetry forbids a torque. The peak torque is 10⁻⁶. The centres stop at 28.7 and separate. |⟨P⟩| falls from 1 to 0.06. That is a loss of order, not a reversal.", 15, WHITE, after=0)
    notes(s, (
        "This is the question to expect. The 35 degrees is not the rigid spin. "
        "Switching beta to zero cuts the heading change to 0.4 degrees, and the cells still miss, separation 36.4. "
        "So the path bends because of the force, and the heading follows the deformed boundary. "
        "Head-on is the control: torque at the level of 10 to the minus 6, separation 28.7, no overlap. "
        "Mean polarization falls to 0.06 while the local magnitude dips to about 0.67 and recovers to 0.85. "
        "Do not describe that as the cell turning around."
    ))

    # ========== 7 GLANCING ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "A free walk, and a forced glancing meeting", "REPULSION STRENGTH 60  ·  TIME 400  ·  SHARED STOKES")
    footer(s, 7)
    fit(s, ASSETS / "two_cell_steric_paths.png", Inches(0.25), Inches(1.05), Inches(4.05), Inches(4.05))
    fit(s, ASSETS / "two_cell_glancing_paths.png", Inches(4.40), Inches(1.05), Inches(4.05), Inches(4.05))
    fit(s, ASSETS / "two_cell_glancing_response.png", Inches(8.55), Inches(1.05), Inches(4.45), Inches(4.05))
    rrect(s, Inches(0.28), Inches(5.22), Inches(6.25), Inches(1.8), WHITE, LINE)
    tf = tb(s, Inches(0.42), Inches(5.32), Inches(5.95), Inches(1.6))
    fresh(tf, "Left  ·  repulsion only", 14, TEAL, bold=True, after=2)
    fresh(tf, "Closest centres 22.9, contact is at 26. Overlap integral peaks at 1.33 and is zero at the end.", 13, DARK, after=0)
    rrect(s, Inches(6.7), Inches(5.22), Inches(6.25), Inches(1.8), WHITE, LINE)
    tf = tb(s, Inches(6.84), Inches(5.32), Inches(5.95), Inches(1.6))
    fresh(tf, "Right  ·  impact parameter 5", 14, TEAL, bold=True, after=2)
    fresh(tf, "Centres come within 0.55. Overlap integral peaks at 4.18, final value 0.051. Torque 5.41. Spin 4.0° per unit time.", 13, DARK, after=0)
    notes(s, (
        "Left plot is the free walk. They choose directions, move, and relax. Closest approach 22.9, so they never quite reach the contact distance of 26. "
        "Overlap integral 1.33 at most, and zero at the end. Pointwise product peaks at 0.079. "
        "Right plot is started 50 apart with impact parameter 5, so the first meeting is glancing, and the tangential contact law is on. "
        "Friction 0.35 and spin coupling 1.2 are chosen coefficients, not measured constants. Say that before anyone asks. "
        "Centres get within 0.55, so this is a deep encounter, not a gentle miss. They still leave as two cells: final overlap integral 0.051. "
        "Peak torque 5.41. Peak spin 0.070 per unit time, which is 4.0 degrees per unit time. The torque and the spin traces rise and fall together. "
        "Jumps in the heading are the decide-move-relax rule assigning a new direction. Do not attribute the whole angle change to the torque."
    ))

    # ========== 8 WALK VIDEO ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "Walking in a closed box", "REPULSION ONLY  ·  EACH CELL PICKS A DIRECTION")
    footer(s, 8)
    s.shapes.add_movie(
        str(ASSETS / "two_cell_walk.mp4"),
        Inches(0.4), Inches(1.15), Inches(5.5), Inches(5.5),
        poster_frame_image=str(ASSETS / "poster_walk.png"),
        mime_type="video/mp4",
    )
    tf = tb(s, Inches(6.15), Inches(1.25), Inches(6.7), Inches(5.5))
    fresh(tf, "What the clip shows", 20, NAVY, bold=True, after=8)
    fresh(tf, "Two cells, one periodic box, a soft wall drawn dashed. Arrows are the polarization.", 16, DARK, after=8)
    fresh(tf, "Each cell is in a move phase or a relax phase. The title on the frame says which, and the heading in degrees.", 16, DARK, after=8)
    fresh(tf, "They elongate, turn, and stay two cells. In this run the centres never come closer than 22.9.", 16, DARK, after=8)
    fresh(tf, "13.5 seconds. Play the opening, then one later stretch. You do not need the whole clip.", 16, TEAL, bold=True, after=0)
    notes(s, (
        "Click the video. The opening frame has cell 1 heading about 31 degrees and cell 2 about 288 degrees, both in MOVE. "
        "Later frames show them elongated and pointed differently, still inside the wall. "
        "This is the repulsion-only walk, not the forced glancing run on the previous slide. "
        "If a question comes on merging: the overlap integral peaks at 1.33 and returns to zero. "
        "The redirect when overlap crosses 1.5 is a rule we imposed, not a result derived from the free energy. Say that if asked."
    ))

    # ========== 9 CLAIMS ==========
    s = prs.slides.add_slide(blank)
    chrome(s, "Four statements we can defend", "AND THREE WE WILL NOT MAKE")
    footer(s, 9)
    claims = [
        ("1", "A treadmilling gradient at a wall makes a protrusion. Without it the cell only translates, and loses 4.5% of its area."),
        ("2", "In the top view the fan is set by anchoring. The flow adds about 2%. The aster does not crawl."),
        ("3", "One cell can drop the Stokes solve. A collision cannot: the cells have to share one flow."),
        ("4", "Contact repulsion does not steer them early. A ranged repulsion with strength q₁q₂ does. The visible turn is anchoring, not the rigid spin."),
    ]
    y = Inches(1.08)
    for num, text in claims:
        rrect(s, Inches(0.35), y, Inches(12.6), Inches(0.92), WHITE, LINE)
        rect(s, Inches(0.35), y, Inches(0.7), Inches(0.92), NAVY)
        tf = tb(s, Inches(0.35), y, Inches(0.7), Inches(0.92), MSO_ANCHOR.MIDDLE)
        fresh(tf, num, 20, WHITE, bold=True, align=PP_ALIGN.CENTER, after=0)
        tf = tb(s, Inches(1.2), y, Inches(11.55), Inches(0.92), MSO_ANCHOR.MIDDLE)
        fresh(tf, text, 15, DARK, after=0)
        y = Emu(y + Inches(1.02))
    rrect(s, Inches(0.35), Inches(5.25), Inches(12.6), Inches(1.75), SOFT, None)
    tf = tb(s, Inches(0.55), Inches(5.38), Inches(12.2), Inches(1.5))
    fresh(tf, "We will not claim", 14, TEAL, bold=True, after=3)
    fresh(tf, "That head-on contact reverses a healthy polarity.   ·   That the glancing-law coefficients 0.35 and 1.2 are anything but numbers we chose.", 14, DARK, after=0)
    notes(s, (
        "Read the four statements slowly. If a question lands, go back to the slide that has the figure. "
        "The third statement is the one Prof. Babu asked for: viscosity stays in the collision. "
        "The fourth is the one that is easy to overclaim. 35 degrees is anchoring. 0.28 degrees is the rigid spin. "
        "The glancing law uses friction 0.35 and spin coupling 1.2 because we set them. "
        "Do not bring up a four-cell run. It is not part of this project."
    ))

    # ========== 10 THANK YOU ==========
    s = prs.slides.add_slide(blank)
    rect(s, 0, 0, W, H, NAVY)
    rect(s, 0, 0, W, Inches(0.12), TEAL)
    tf = tb(s, Inches(0.7), Inches(1.7), Inches(12), Inches(1.0))
    fresh(tf, "Thank you.", 48, WHITE, bold=True, after=0)
    tf = tb(s, Inches(0.7), Inches(2.9), Inches(11.5), Inches(1.6))
    fresh(tf, "Siddharth Kumar     2023PH10741", 20, WHITE, after=2)
    fresh(tf, "Soumik Roy     2023PH10756", 20, WHITE, after=8)
    fresh(tf, "Adviser: Prof. Sujin B. Babu", 18, RGBColor(0xD6, 0xE4, 0xEA), after=0)
    tf = tb(s, Inches(0.7), Inches(5.15), Inches(11.8), Inches(1.3))
    fresh(tf, "These slides were drafted with an AI assistant.", 15, RGBColor(0xD6, 0xE4, 0xEA), italic=True, after=4)
    fresh(tf, "The runs, the numbers, and the interpretation are ours.", 15, RGBColor(0xD6, 0xE4, 0xEA), italic=True, after=0)
    notes(s, (
        "Stop. The acknowledgement is on the slide because the evaluation asks for it. "
        "Do not apologise for it. If a question starts, answer from the figure, not from a new calculation."
    ))

    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    print(build())
