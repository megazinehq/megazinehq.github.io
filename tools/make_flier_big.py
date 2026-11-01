"""The big-code flier: one letter page in the site's colours with one giant QR code made of tiny QR
codes (every dark square of the big code is itself a little code), the slogan said once along each
side of it, and the megaZINE logo along the bottom. Crisp vector, not photocopied. For a colour printer.

    python3 tools/make_flier_big.py            # print/flier-big.pdf

The code carries ?ref=flier-big, so GoatCounter lists it under referrers.
"""
import make_logo_stickers as L
import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L
from PIL import Image
from reportlab.lib.utils import ImageReader
from make_logo_stickers import (TONER, PINK, BLUE, logo, logo_w, pdfmetrics, canvas, letter, inch, white, ROOT, S)

SLOGAN = "Making Yesterday’s Tomorrow Today"             # said once along every side of the code
URL = S.BASE + "?ref=flier-big"
LW, LH = letter
M = 0.4 * inch
B = 0.55 * inch                       # thickness of the slogan band on each side of the code
PAD = 30                              # white card round the code (the quiet zone)
FONT = "Sans-BoldItalic"


def mini_code(data=S.BASE, px=8):
    """One small QR code as an image, reused for every dark square of the big code."""
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_L, box_size=1, border=0)
    q.add_data(data); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    im = Image.new("L", (n * px, n * px), 255)
    for r in range(n):
        for k in range(n):
            if m[r][k]:
                im.paste(0, (k * px, r * px, (k + 1) * px, (r + 1) * px))
    return ImageReader(im)


def qr_of_qrs(c, x, y, size, url, pad=0.22):
    """The big code: every dark square is a black frame round a tiny code. The three corner squares
    stay solid, and the high error correction plus the frames keep it scanning like a plain code."""
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=1, border=0)
    q.add_data(url); q.make(fit=True)
    m = q.get_matrix(); n = len(m); sz = size / n
    tiny = mini_code()
    finders = [(0, 0), (0, n - 7), (n - 7, 0)]
    for r in range(n):
        for k in range(n):
            if not m[r][k]:
                continue
            cx, cy = x + k * sz, y + size - (r + 1) * sz
            c.setFillColor(TONER)
            c.rect(cx, cy, sz + 0.3, sz + 0.3, stroke=0, fill=1)
            if not any(a <= r < a + 7 and b <= k < b + 7 for a, b in finders):
                p = sz * pad
                c.drawImage(tiny, cx + p, cy + p, sz - 2 * p, sz - 2 * p)


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
    qs = min(LW - 2 * M - 2 * B - 2 * PAD, top_y - bottom_y - 2 * B - 2 * PAD)
    qx = (LW - qs) / 2
    qy = bottom_y + B + PAD
    c.setFillColor(white); c.setStrokeColor(TONER); c.setLineWidth(2)
    c.rect(qx - PAD, qy - PAD, qs + 2 * PAD, qs + 2 * PAD, stroke=1, fill=1)
    qr_of_qrs(c, qx, qy, qs, URL)
    # the slogan once on each side, sized to run the full length of the code
    size = 40
    while pdfmetrics.stringWidth(SLOGAN, FONT, size) > qs:
        size -= 0.25
    size = min(size, B / 1.3)
    mx, my = LW / 2, qy + qs / 2
    half = qs / 2 + PAD + B / 2
    side_word(c, SLOGAN, mx, my + half, 0, size, TONER)       # top
    side_word(c, SLOGAN, mx + half, my, -90, size, PINK)      # right, reads downward
    side_word(c, SLOGAN, mx, my - half, 180, size, BLUE)      # bottom, upside down
    side_word(c, SLOGAN, mx - half, my, 90, size, TONER)      # left, reads upward


def main():
    out = ROOT / "print" / "flier-big.pdf"
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle("megaZINE big-code flier"); c.setAuthor("megaZINE")
    draw_page(c); c.save()
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
