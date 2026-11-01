"""The big-code flier: one letter page with the megaZINE logo and one giant eyeball QR code, with the
slogan wrapped round the code, one word on each side. Photocopied like the other flier (--clean skips the copier effects).

    python3 tools/make_flier_big.py            # print/flier-big.pdf
    python3 tools/make_flier_big.py --clean    # crisp vector

The code carries ?ref=flier-big, so GoatCounter lists it under referrers. Same extra pip packages as make_flier.py.
"""
import io, sys
CLEAN = "--clean" in sys.argv
import make_flier as F
from make_flier import *  # noqa: F401,F403
from make_sheet import ROOT, letter, canvas, ImageReader, black, white, inch

WORDS = ["Making", "Yesterday\u2019s", "Tomorrow", "Today"]   # one word per side of the code, clockwise from the top
URL = F.S.BASE + "?ref=flier-big"
LW, LH = letter
M = 0.4 * inch
B = 0.8 * inch                        # thickness of the word band on each side of the code
QS = 6.0 * inch                       # the giant code
QX, QY = (LW - QS) / 2, M + B + 12


def side_word(c, word, cx, cy, angle, size):
    """A word centred on (cx, cy), turned so the tops of the letters point away from the code."""
    c.saveState()
    c.translate(cx, cy)
    c.rotate(angle)
    c.setFillColor(black)
    c.setFont("Sans-BoldItalic", size)
    c.drawCentredString(0, -size * 0.35, word)
    c.restoreState()


def draw_page(c):
    # one size for all four words, small enough that the longest fits the side of the code
    size = 60
    while max(pdfmetrics.stringWidth(w, "Sans-BoldItalic", size) for w in WORDS) > QS * 0.92:
        size -= 1
    size = min(size, B / 1.25)
    mx, my = LW / 2, QY + QS / 2                     # middle of the code
    half = QS / 2 + 12 + B / 2                       # from the middle out to the middle of a band
    side_word(c, WORDS[0], mx, my + half, 0, size)       # top
    side_word(c, WORDS[1], mx + half, my, -90, size)     # right, reads downward
    side_word(c, WORDS[2], mx, my - half, 180, size)     # bottom, upside down
    side_word(c, WORDS[3], mx - half, my, 90, size)      # left, reads upward
    # the logo above, as wide as the page allows
    top_of_words = QY + QS + 12 + B
    s = 150
    while F.wordmark_width(s) > LW - 2 * M:
        s -= 1
    while top_of_words + s * 0.55 + s * 0.75 > LH - M and s > 20:
        s -= 1
    F.wordmark(c, (LW - F.wordmark_width(s)) / 2, top_of_words + s * 0.5, s)
    # the giant code, on a white card with a thin frame
    c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(2)
    c.rect(QX - 12, QY - 12, QS + 24, QS + 24, stroke=1, fill=1)
    F.eyeball_qr(c, QX, QY, QS, URL)


def main():
    out = ROOT / "print" / "flier-big.pdf"
    if CLEAN:
        c = canvas.Canvas(str(out), pagesize=letter); c.setTitle("megaZINE big-code flier"); draw_page(c); c.save()
        print("wrote print/flier-big.pdf (clean)"); return
    base, eyes = io.BytesIO(), io.BytesIO()
    c = canvas.Canvas(base, pagesize=letter); draw_page(c); c.save()
    c = canvas.Canvas(eyes, pagesize=letter); c.setFillColor(white); c.rect(0, 0, 1, 1, stroke=0, fill=1); c.showPage(); c.save()                       # no watermark on this one
    F.TAB_H = 0.0                                                            # photocopy() keeps these zones gentle:
    F.BIG_X, F.BIG_Y, F.BIG = QX, QY, QS                                     # here, the giant code
    img = F.photocopy(base.getvalue(), eyes.getvalue())
    png = io.BytesIO(); img.save(png, format="PNG", optimize=True); png.seek(0)
    f = canvas.Canvas(str(out), pagesize=letter); f.setTitle("megaZINE big-code flier")
    f.drawImage(ImageReader(png), 0, 0, LW, LH); f.save()
    print(f"wrote print/flier-big.pdf (photocopied, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
