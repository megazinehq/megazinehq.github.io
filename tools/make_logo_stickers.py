"""One letter sheet of six colour stickers: the site's logo (ink plus the slipped pink pass) on top,
the big eyeball code underneath, in the site's colours. For a colour laser or inkjet on sticker paper.
Straight cuts along the light grey lines. The code carries ?ref=sticker, same as the other sticker sheets.

    python3 tools/make_logo_stickers.py      # print/stickers/color/stickers-11-logo-color.pdf
"""
import math, random, sys
sys.argv = [sys.argv[0]]
import make_sheet as S
from make_sheet import *  # noqa: F401,F403
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("Logo", str(ROOT / "tools" / "fonts" / "BowlbyOneSC-Regular.ttf")))
TONER, PINK, BLUE, GOLD, PAPER = HexColor("#18181B"), HexColor("#F2369B"), HexColor("#0055B3"), HexColor("#94671A"), HexColor("#FBFBF8")
IRIS = [BLUE] * 5 + [PINK] * 4 + [GOLD] * 2
URL = S.BASE + "?ref=sticker"
OUT = ROOT / "print" / "stickers" / "color" / "stickers-11-logo-color.pdf"
LW, LH = letter
COLS, ROWS = 2, 3
CW, CH = 3.6 * inch, 3.5 * inch
X0, Y0 = (LW - COLS * CW) / 2, (LH - ROWS * CH) / 2


def logo_w(s):
    return pdfmetrics.stringWidth("MEGA", "Logo", s) + 0.06 * s + pdfmetrics.stringWidth("zine", "Sans-Bold", 0.6 * s)


def logo(c, x, y, s):
    """Pink pass first, slightly off and crooked, then the ink on top."""
    def draw(ink, zine):
        c.setFillColor(ink); c.setFont("Logo", s); c.drawString(0, 0, "MEGA")
        c.setFillColor(zine); c.setFont("Sans-Bold", 0.6 * s)
        c.drawString(pdfmetrics.stringWidth("MEGA", "Logo", s) + 0.06 * s, 0.42 * s, "zine")
    c.saveState(); c.translate(x + 0.035 * s, y - 0.03 * s); c.rotate(-0.6); draw(PINK, PINK); c.restoreState()
    c.saveState(); c.translate(x, y); draw(TONER, BLUE); c.restoreState()


def eyeball(c, cx, cy, R, rnd, look=(0, 0)):
    c.setFillColor(TONER); c.circle(cx, cy, R, stroke=0, fill=1)
    ri = R * 0.62 * rnd.uniform(0.94, 1.06); rp = ri * rnd.uniform(0.55, 0.64)
    ix, iy = cx + look[0] * (R - ri) * 0.6, cy + look[1] * (R - ri) * 0.6
    c.setFillColor(rnd.choice(IRIS)); c.circle(ix, iy, ri, stroke=0, fill=1)
    c.setStrokeColor(TONER); c.setLineWidth(max(0.2, R * 0.04))
    for j in range(10):
        a = j * math.pi / 5 + rnd.uniform(-0.1, 0.1)
        c.line(ix + rp * 1.08 * math.cos(a), iy + rp * 1.08 * math.sin(a), ix + ri * 0.9 * math.cos(a), iy + ri * 0.9 * math.sin(a))
    c.setFillColor(TONER); c.circle(ix, iy, rp, stroke=0, fill=1)
    c.setFillColor(white); c.circle(ix - rp * 0.38, iy + rp * 0.42, max(rp * 0.3, 0.5), stroke=0, fill=1)


def eyeball_qr(c, x, y, size, url):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=1, border=0)
    q.add_data(url); q.make(fit=True); m = q.get_matrix(); n = len(m); sz = size / n
    rnd = random.Random(7)
    fin = [(0, 0), (0, n - 7), (n - 7, 0)]
    for r in range(n):
        for k in range(n):
            if m[r][k] and not any(a <= r < a + 7 and b <= k < b + 7 for a, b in fin):
                eyeball(c, x + (k + .5) * sz, y + size - (r + .5) * sz, sz * rnd.uniform(.5, .56), rnd, (rnd.uniform(-1, 1), rnd.uniform(-1, 1)))
    for a, b in fin:
        fx, fy = x + b * sz, y + size - (a + 7) * sz
        c.setFillColor(TONER); c.roundRect(fx, fy, 7 * sz, 7 * sz, .9 * sz, stroke=0, fill=1)
        c.setFillColor(white); c.roundRect(fx + sz, fy + sz, 5 * sz, 5 * sz, .4 * sz, stroke=0, fill=1)
        eyeball(c, fx + 3.5 * sz, fy + 3.5 * sz, sz * 1.55, rnd, (.3, -.2))


def sticker(c, x, y):
    c.setFillColor(PAPER); c.rect(x, y, CW, CH, stroke=0, fill=1)
    s = 60
    while logo_w(s) > CW - 0.5 * inch: s -= 0.5
    logo(c, x + (CW - logo_w(s)) / 2, y + CH - 0.28 * inch - 0.74 * s, s)
    qs = 2.15 * inch; pad = 0.07 * inch
    qx, qy = x + (CW - qs) / 2, y + 0.3 * inch
    c.setFillColor(white); c.rect(qx - pad, qy - pad, qs + 2 * pad, qs + 2 * pad, stroke=0, fill=1)
    eyeball_qr(c, qx, qy, qs, URL)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("megaZINE logo stickers, colour"); c.setAuthor("megaZINE")
    for r in range(ROWS):
        for k in range(COLS):
            sticker(c, X0 + k * CW, Y0 + r * CH)
    c.setStrokeColor(Color(0, 0, 0, alpha=0.25)); c.setLineWidth(0.4)   # cut lines
    for k in range(COLS + 1): c.line(X0 + k * CW, Y0, X0 + k * CW, Y0 + ROWS * CH)
    for r in range(ROWS + 1): c.line(X0, Y0 + r * CH, X0 + COLS * CW, Y0 + r * CH)
    c.save(); print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
