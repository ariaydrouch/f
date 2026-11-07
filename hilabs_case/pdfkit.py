from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white, black

pdfmetrics.registerFont(TTFont("F", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("FB", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("FI", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFontFamily("F", normal="F", bold="FB", italic="FI", boldItalic="FB")

W, H = 960, 540
NAVY = HexColor("#1F3A5F")
TEAL = HexColor("#16908A")
AMBER = HexColor("#E8A02F")
RED = HexColor("#D2453D")
GREEN = HexColor("#2E9E5B")
GRAY = HexColor("#F2F4F7")
MID = HexColor("#C9D0DA")
INK = HexColor("#1B2430")
SOFT = HexColor("#5A6675")
LTEAL = HexColor("#E3F3F1")
LRED = HexColor("#FBE9E7")
LAMB = HexColor("#FDF2DC")
LBLUE = HexColor("#E6EEF8")


def hexs(c):
    return "#%02x%02x%02x" % (int(c.red * 255), int(c.green * 255), int(c.blue * 255))


def para(text, size=9, color=INK, bold=False, align=0, lead=None):
    st = ParagraphStyle("p", fontName="FB" if bold else "F", fontSize=size,
                        leading=lead or size * 1.22, textColor=color, alignment=align)
    return Paragraph(text, st)


class Deck:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=(W, H))
        self.n = 0

    def rect(self, x, yt, w, h, fill=None, stroke=None, r=4, lw=0.8, dash=None):
        c = self.c
        if fill is not None:
            c.setFillColor(fill)
        if stroke is not None:
            c.setStrokeColor(stroke)
            c.setLineWidth(lw)
        if dash:
            c.setDash(*dash)
        c.roundRect(x, H - yt - h, w, h, r, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
        c.setDash()

    def text(self, x, yt, w, s, size=9, color=INK, bold=False, align=0, lead=None):
        p = para(s, size, color, bold, align, lead)
        _, h = p.wrap(w, 1000)
        p.drawOn(self.c, x, H - yt - h)
        return h

    def tsize(self, w, s, size=9, bold=False, lead=None):
        p = para(s, size, INK, bold, 0, lead)
        return p.wrap(w, 1000)[1]

    def line(self, x1, y1, x2, y2, color=MID, lw=0.8, dash=None):
        c = self.c
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        if dash:
            c.setDash(*dash)
        c.line(x1, H - y1, x2, H - y2)
        c.setDash()

    def circle(self, x, yt, r, fill, stroke=None):
        self.c.setFillColor(fill)
        if stroke is not None:
            self.c.setStrokeColor(stroke)
        self.c.circle(x, H - yt, r, fill=1, stroke=1 if stroke is not None else 0)

    def chip(self, x, yt, s, fill=LBLUE, color=NAVY, size=6.5, padx=4, h=11, bold=True):
        w = pdfmetrics.stringWidth(s, "FB" if bold else "F", size) + 2 * padx
        self.rect(x, yt, w, h, fill=fill, r=3)
        self.c.setFillColor(color)
        self.c.setFont("FB" if bold else "F", size)
        self.c.drawString(x + padx, H - yt - h + (h - size) / 2 + 1.2, s)
        return w

    def badge(self, x, yt, n, fill=NAVY, r=7):
        self.circle(x, yt, r, fill)
        self.c.setFillColor(white)
        self.c.setFont("FB", 7.5)
        self.c.drawCentredString(x, H - yt - 2.7, str(n))

    def table(self, x, yt, colw, rows, size=7, header=True, pad=3, zebra=True, hfill=NAVY, col_bold=(0,), fills=None):
        """rows: list of list of str (rich text ok). returns bottom y."""
        y = yt
        for ri, row in enumerate(rows):
            is_h = header and ri == 0
            hs = []
            for ci, cell in enumerate(row):
                p = para(cell, size, white if is_h else INK, bold=is_h or ci in col_bold)
                hs.append((p, p.wrap(colw[ci] - 2 * pad, 1000)[1]))
            rh = max(h for _, h in hs) + 2 * pad
            xx = x
            for ci, (p, h) in enumerate(hs):
                if is_h:
                    f = hfill
                elif fills and fills.get((ri, ci)) is not None:
                    f = fills[(ri, ci)]
                elif zebra and ri % 2 == 0:
                    f = GRAY
                else:
                    f = white
                self.c.setFillColor(f)
                self.c.setStrokeColor(MID)
                self.c.setLineWidth(0.4)
                self.c.rect(xx, H - y - rh, colw[ci], rh, fill=1, stroke=1)
                p.drawOn(self.c, xx + pad, H - y - pad - h)
                xx += colw[ci]
            y += rh
        return y

    def slide(self, title, sub=None, section=""):
        if self.n:
            self.c.showPage()
        self.n += 1
        self.rect(0, 0, W, 6, fill=NAVY, r=0)
        self.text(28, 16, 900, title, 17, NAVY, True, lead=20)
        if sub:
            self.text(28, 40, 900, sub, 9, SOFT)
        self.line(28, 56, W - 28, 56, MID, 0.6)
        self.c.setFillColor(SOFT)
        self.c.setFont("F", 6.5)
        self.c.drawString(28, 10, "HiLabs Product Caselet 2026-27  |  " + section + "  |  all patient data is fictional")
        self.c.drawRightString(W - 28, 10, str(self.n))

    def foot(self, s):
        self.text(28, H - 26, W - 56, s, 5.8, SOFT, lead=7)

    def save(self):
        self.c.showPage()
        self.c.save()
