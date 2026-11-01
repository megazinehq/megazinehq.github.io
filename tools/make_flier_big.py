"""The big-code flier: one letter page in the site's colours, with one giant eyeball QR code and the
slogan wrapped round it, one word on each side, and the megaZINE logo along the bottom. Crisp vector,
not photocopied. For a colour printer.

    python3 tools/make_flier_big.py            # print/flier-big.pdf

The code carries ?ref=flier-big, so GoatCounter lists it under referrers.
"""
import make_logo_stickers as L
from make_logo_stickers import (TONER, PINK, BLUE, logo, logo_w, eyeball_qr, pdfmetrics, canvas, letter, inch, white, ROOT, S)

WORDS = ["Making", "Yesterday’s", "Tomorrow", "Today"]   # one word per side, clockwise from the top
URL = S.BASE + "?ref=flier-big"
LW, LH = letter
M = 0.4 * inch
B = 0.8 * inch                        # thickness of the word band on each side of the code
PAD = 12                              # white card round the code
FONT = "Sans-BoldItalic"


def side_word(c, word, cx, cy, angle, size, color):
    """A word centred on (cx, cy), turned so the tops of the letters point away from the code."""
    c.saveState(); c.translate(cx, cy); c.rotate(angle)
    c.setFillColor(color); c.setFont(FONT, size)
    c.drawCentredString(0, -size * 0.35, word)
    c.restoreState()


def draw_page(c):
    # the logo along the bottom, as wide as the page allows
    s = 150
    while logo_w(s) > LW - 2 * M:
        s -= 1
    logo_h = s * 0.95
    logo(c, (LW - logo_w(s)) / 2, M + s * 0.12, s)
    # the code fills what is left above the logo
    top_y = LH - M
    bottom_y = M + logo_h + 0.25 * inch
    qs = min(6.2 * inch, top_y - bottom_y - 2 * B - 2 * PAD)
    qx = (LW - qs) / 2
    qy = bottom_y + B + PAD
    c.setFillColor(white); c.setStrokeColor(TONER); c.setLineWidth(2)
    c.rect(qx - PAD, qy - PAD, qs + 2 * PAD, qs + 2 * PAD, stroke=1, fill=1)
    eyeball_qr(c, qx, qy, qs, URL)
    # one size for all four words, small enough that the longest fits a side of the code
    size = 60
    while max(pdfmetrics.stringWidth(w, FONT, size) for w in WORDS) > qs * 0.92:
        size -= 1
    size = min(size, B / 1.25)
    mx, my = LW / 2, qy + qs / 2
    half = qs / 2 + PAD + B / 2
    side_word(c, WORDS[0], mx, my + half, 0, size, TONER)       # top
    side_word(c, WORDS[1], mx + half, my, -90, size, PINK)      # right, reads downward
    side_word(c, WORDS[2], mx, my - half, 180, size, BLUE)      # bottom, upside down
    side_word(c, WORDS[3], mx - half, my, 90, size, TONER)      # left, reads upward


def main():
    out = ROOT / "print" / "flier-big.pdf"
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle("megaZINE big-code flier"); c.setAuthor("megaZINE")
    draw_page(c); c.save()
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
