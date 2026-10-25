"""Make the megaZINE wall flier: one letter page, sparse and a little mysterious, with a row of
tear-off tabs along the bottom. Each tab is the logo over a QR code to the site.

    python3 tools/make_flier.py            # writes print/flier.pdf

Print on paper, cut the dashed lines between tabs (not through the top line), tape up.
The QR codes carry ?ref=flier, so GoatCounter lists "flier" under referrers.
"""
import random, sys
sys.argv = [sys.argv[0]]  # make_sheet reads --issue from argv at import; the flier has no issue
import make_sheet as S
from make_sheet import *  # noqa: F401,F403  (fonts, qr_img, label, colours)

TABS = 10
URL = S.BASE + "?ref=flier"
LW, LH = letter
M = 0.25 * inch
TAB_H = 1.6 * inch
tab_w = (LW - 2 * M) / TABS


def logo(c, cx, y, mega=15):
    """MEGA over zine, centred on cx; y is the baseline of MEGA."""
    c.setFillColor(black)
    c.setFont("Sans-Bold", mega)
    c.drawCentredString(cx, y, "MEGA")
    c.setFont("Sans-Bold", mega * 0.42)
    c.drawRightString(cx + c.stringWidth("MEGA", "Sans-Bold", mega) / 2, y - mega * 0.5, "zine")


def main():
    c = canvas.Canvas(str(ROOT / "print" / "flier.pdf"), pagesize=letter)
    c.setTitle("megaZINE flier")

    # radio-field arcs, drawn once, drifting off the lower right
    rnd = random.Random(11)
    c.saveState()
    c.setLineWidth(0.6)
    for k in range(5):
        cx, cy = rnd.uniform(0.2, 0.9) * LW, rnd.uniform(0.25, 0.6) * LH
        for r in range(1, 10):
            c.setStrokeColor(Color(0, 0, 0, alpha=max(0.05, 0.4 - r * 0.04)))
            rr = r * (8 + k * 2)
            c.arc(cx - rr, cy - rr, cx + rr, cy + rr, rnd.uniform(0, 360), rnd.uniform(70, 160))
    c.restoreState()

    # masthead
    big = 150
    while c.stringWidth("MEGA", "Sans-Bold", big) > LW - 2 * M - 8:
        big -= 1
    top = LH - M - big * 0.82
    c.setFillColor(LIGHT)
    c.setFont("Sans-Bold", big)
    c.drawString(M + 4, top - 3, "MEGA")
    c.setFillColor(black)
    c.drawString(M, top, "MEGA")
    c.setFont("Sans-Bold", big * 0.34)
    c.drawRightString(LW - M, top - big * 0.36, "zine")
    c.setLineWidth(3)
    c.line(M, top - big * 0.46, LW - M, top - big * 0.46)

    # the words: few, and they don't explain
    y = top - big * 0.46 - 70
    lines = [("Small strange things.", 30), ("Some made by hand.", 30),
             ("Some made with a machine.", 30), ("Every one signed.", 30)]
    c.setFont("Sans-Italic", 30)
    for text, size in lines:
        c.setFont("Sans-Italic", size)
        c.drawString(M, y, text)
        y -= size * 1.5
    y -= 22
    label(c, "NO TICKET. NO PRICE. NO CATCH.", M, y, size=9)
    y -= 15
    label(c, "NEW ONES ON THE 1ST OF EVERY MONTH.", M, y, size=9)

    # tear-off tabs
    ty = M + TAB_H
    label(c, "TAKE ONE", M, ty + 8, size=8)
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    c.setDash(3, 3)
    c.line(M, ty, LW - M, ty)                     # the fold-and-tear line
    for i in range(TABS + 1):
        x = M + i * tab_w
        c.line(x, ty, x, M)                       # cuts between tabs
    c.setDash()
    qr = qr_img(URL)
    qs = tab_w - 8
    for i in range(TABS):
        cx = M + (i + 0.5) * tab_w
        logo(c, cx, ty - 22)
        c.drawImage(qr, cx - qs / 2, ty - 22 - 14 - qs, qs, qs)
        label(c, "SCAN", cx - 9, M + 7, size=5.5, spacing=0.8)
    c.save()
    print("wrote print/flier.pdf")


if __name__ == "__main__":
    main()
