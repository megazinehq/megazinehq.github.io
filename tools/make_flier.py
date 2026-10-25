"""Make the megaZINE wall flier: one letter page, sparse and a little mysterious, with a row of
tear-off tabs along the bottom. Each tab is the logo over a QR code to the site. The page is then
run through a fake photocopier (toner grain, uneven density, specks, streaks, a slightly crooked
sheet) so it looks like the hundredth copy of a copy.

    pip install qrcode reportlab pypdfium2 numpy pillow scipy     # once
    python3 tools/make_flier.py            # print/flier.pdf, photocopied
    python3 tools/make_flier.py --clean    # print/flier.pdf, crisp vector, no copier effects

Print on paper, cut the dashed lines between tabs (not through the top line), tape up.
The QR codes carry ?ref=flier, so GoatCounter lists "flier" under referrers.
"""
import io, math, random, sys
CLEAN = "--clean" in sys.argv
sys.argv = [sys.argv[0]]  # make_sheet reads --issue from argv at import; the flier has no issue
import make_sheet as S
from make_sheet import *  # noqa: F401,F403  (fonts, qr_img, label, colours)

# The website's logo face (Bowlby One SC, SIL Open Font License; licence text sits beside it).
pdfmetrics.registerFont(TTFont("Logo", str(ROOT / "tools" / "fonts" / "BowlbyOneSC-Regular.ttf")))

TABS = 10
URL = S.BASE + "?ref=flier"
LW, LH = letter
M = 0.25 * inch
TAB_H = 1.6 * inch
tab_w = (LW - 2 * M) / TABS
MIS = Color(0, 0, 0, alpha=0.5)   # the "pink" misregistered pass, in black and white


def wordmark_width(size):
    return pdfmetrics.stringWidth("MEGA", "Logo", size) + 0.06 * size + pdfmetrics.stringWidth("zine", "Sans-Bold", 0.6 * size)


def wordmark(c, x, y, size):
    """The site logo: MEGA big, zine small and raised after it, plus an offset second pass
    like a sheet that slipped in the copier. (x, y) is the left end of MEGA's baseline."""
    def draw(col):
        c.setFillColor(col)
        c.setFont("Logo", size)
        c.drawString(0, 0, "MEGA")
        c.setFont("Sans-Bold", 0.6 * size)
        c.drawString(pdfmetrics.stringWidth("MEGA", "Logo", size) + 0.06 * size, 0.42 * size, "zine")
    c.saveState()
    c.translate(x + 0.035 * size, y - 0.03 * size)
    c.rotate(-0.6)
    draw(MIS)
    c.restoreState()
    c.saveState()
    c.translate(x, y)
    draw(black)
    c.restoreState()


def eye(c, cx, cy, r, tilt=0, seed=0):
    """An eyeball like the ones in the front-page code: a round dark globe, an iris with spokes, a
    pupil, a glint, sometimes a vein. No lids. Drawn faint so it stays a watermark."""
    rnd = random.Random(seed)
    c.saveState()
    c.translate(cx, cy)
    c.rotate(tilt)
    globe = c.beginPath()
    globe.circle(0, 0, r)
    c.setFillColor(Color(0, 0, 0, alpha=0.10))
    c.circle(0, 0, r, stroke=0, fill=1)
    c.setStrokeColor(Color(0, 0, 0, alpha=0.9))
    c.setLineWidth(max(0.5, r * 0.03))
    c.circle(0, 0, r, stroke=1, fill=0)
    c.clipPath(globe, stroke=0, fill=0)
    if rnd.random() < 0.6:                              # a vein or two creeping in from the edge
        c.setStrokeColor(Color(0, 0, 0, alpha=0.8))
        c.setLineWidth(max(0.5, r * 0.05))
        for _ in range(rnd.randint(2, 4)):
            t = rnd.uniform(0, 6.283)
            p = c.beginPath()
            p.moveTo(r * 0.98 * math.cos(t), r * 0.98 * math.sin(t))
            p.curveTo(r * 0.8 * math.cos(t + 0.3), r * 0.8 * math.sin(t + 0.3),
                      r * 0.7 * math.cos(t - 0.05), r * 0.7 * math.sin(t - 0.05),
                      r * 0.6 * math.cos(t - 0.1), r * 0.6 * math.sin(t - 0.1))
            c.drawPath(p, stroke=1, fill=0)
    ix, iy = r * rnd.uniform(-0.15, 0.15), r * rnd.uniform(-0.15, 0.15)   # where it's looking
    ri = r * 0.62
    rp = ri * 0.6
    c.setFillColor(Color(0, 0, 0, alpha=0.08))
    c.setStrokeColor(Color(0, 0, 0, alpha=0.9))
    c.setLineWidth(max(0.5, r * 0.035))
    c.circle(ix, iy, ri, stroke=1, fill=1)
    for j in range(10):
        a = j * math.pi / 5 + rnd.uniform(-0.1, 0.1)
        c.line(ix + rp * 1.08 * math.cos(a), iy + rp * 1.08 * math.sin(a),
               ix + ri * 0.9 * math.cos(a), iy + ri * 0.9 * math.sin(a))
    c.setFillColor(Color(0, 0, 0, alpha=0.7))
    c.circle(ix, iy, rp, stroke=0, fill=1)
    c.setFillColor(white)
    c.circle(ix - rp * 0.38, iy + rp * 0.42, max(rp * 0.3, 0.9), stroke=0, fill=1)
    c.restoreState()


def layout():
    """Masthead size and baseline, shared by the page and the eye scatter."""
    big = 200
    while wordmark_width(big) > LW - 2 * M - 8:
        big -= 1
    return big, LH - M - big * 0.9


def scatter_eyes(n=30, seed=5):
    """Eyeballs spread over the open page, never touching each other, the logo or the tabs."""
    big, top = layout()
    lo, hi = M + TAB_H + 26, top - big * 0.2 - 8
    rnd = random.Random(seed)
    placed = []
    for _ in range(4000):
        r = rnd.choice([16, 18, 22, 26, 30, 36, 44, 54, 70, 95])
        x, y = rnd.uniform(M + r, LW - M - r), rnd.uniform(lo + r, hi - r)
        if all(math.hypot(x - px, y - py) > r + pr + 7 for px, py, pr, *_ in placed):
            placed.append((x, y, r, rnd.uniform(0, 360), rnd.randint(0, 9999)))
        if len(placed) >= n:
            break
    return placed


def draw_eyes(c):
    for x, y, r, tilt, seed in scatter_eyes():
        eye(c, x, y, r, tilt, seed)


def draw_page(c, layer="all"):
    """layer: 'all' (clean vector page), 'base' (no eyes) or 'eyes' (only the eyes)."""
    if layer == "eyes":
        draw_eyes(c)
        return
    if layer == "all":
        draw_eyes(c)

    big, top = layout()
    wordmark(c, M, top, big)
    c.setStrokeColor(black)
    c.setLineWidth(3)
    c.line(M, top - big * 0.2, LW - M, top - big * 0.2)

    c.setFillColor(black)
    c.setFont("Sans-Italic", 20)
    c.drawRightString(LW - M, top - big * 0.2 - 28, S.DATA["zine"]["tagline"].lower())
    y = top - big * 0.2 - 82
    for text in ["Small strange things.", "Some made by hand.", "Some made with a machine.", "Every one signed."]:
        c.setFillColor(black)
        c.setFont("Sans-Italic", 30)
        c.drawString(M, y, text)
        y -= 45
    y -= 22
    label(c, "NO TICKET. NO PRICE. NO CATCH.", M, y, size=9)
    y -= 15
    label(c, "NEW ONES ON THE 1ST OF EVERY MONTH.", M, y, size=9)

    ty = M + TAB_H
    label(c, "TAKE ONE", M, ty + 8, size=8)
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    c.setDash(3, 3)
    c.line(M, ty, LW - M, ty)
    for i in range(TABS + 1):
        x = M + i * tab_w
        c.line(x, ty, x, M)
    c.setDash()
    qr = qr_img(URL)
    qs = tab_w - 8
    s = 20
    while wordmark_width(s) > tab_w - 6:
        s -= 0.5
    for i in range(TABS):
        cx = M + (i + 0.5) * tab_w
        wordmark(c, cx - wordmark_width(s) / 2, ty - 8 - s * 0.74, s)
        c.drawImage(qr, cx - qs / 2, ty - 8 - s * 0.74 - 12 - qs, qs, qs)
        label(c, "SCAN", cx - 9, M + 7, size=5.5, spacing=0.8)


def photocopy(pdf_bytes, eyes_bytes, dpi=300, seed=7):
    """Rasterise the clean page and degrade it like a tired copier. Returns a 1-bit PIL image."""
    import numpy as np, pypdfium2 as pdfium
    from PIL import Image
    from scipy import ndimage as nd
    rng = np.random.default_rng(seed)
    page = pdfium.PdfDocument(pdf_bytes)[0]
    img = page.render(scale=dpi / 72).to_pil().convert("L")
    g = np.asarray(img, dtype=np.float32) / 255.0
    h, w = g.shape
    yy = np.arange(h)[:, None] / h
    tab_zone = (yy > 1 - (M + TAB_H + 0.5 * inch) / LH).astype(np.float32)   # keep the QR row gentler
    calm = 1.0 - 0.7 * tab_zone

    g = nd.gaussian_filter(g, 0.7)                                    # toner spread
    low = nd.gaussian_filter(rng.normal(size=(h, w)).astype(np.float32), 120)
    low = low / (np.abs(low).max() + 1e-6)                            # blotchy density, -1..1
    band = nd.gaussian_filter(rng.normal(size=(h, 1)).astype(np.float32), 14)
    band = band / (np.abs(band).max() + 1e-6)                         # horizontal banding
    grain = nd.gaussian_filter(rng.normal(size=(h, w)).astype(np.float32), 0.9)
    grain = grain / (grain.std() + 1e-6)
    thr = 0.55 + (0.12 * low + 0.04 * band) * calm + 0.07 * grain * calm
    ink = g < thr

    # the eyeball watermark: toner that barely took. Darkness becomes a thin random stipple.
    e = np.asarray(pdfium.PdfDocument(eyes_bytes)[0].render(scale=dpi / 72).to_pil().convert("L"),
                   dtype=np.float32) / 255.0
    e = nd.gaussian_filter(e, 0.8)
    ink |= rng.random((h, w)) < (1.0 - e) * 0.42 * (0.6 + 0.4 * (low * 0.5 + 0.5))

    # dust, hairs, and a few dropouts inside solid black
    for _ in range(260):
        x, y, r = int(rng.integers(0, w)), int(rng.integers(0, int(h * 0.82))), int(rng.integers(1, 4))
        ink[max(0, y - r):y + r, max(0, x - r):x + r] = True
    for _ in range(14):
        x, y = int(rng.integers(0, w)), int(rng.integers(0, int(h * 0.82)))
        dx, dy = rng.normal(0, 25), rng.normal(0, 25)
        for t in np.linspace(0, 1, 60):
            ink[int(np.clip(y + dy * t, 0, h - 1)), int(np.clip(x + dx * t, 0, w - 1))] = True
    holes = rng.random((h, w)) < 0.0008
    ink &= ~nd.binary_dilation(holes, iterations=1) | (tab_zone > 0)
    # toner streaks running down the sheet
    for _ in range(2):
        x = int(rng.integers(int(w * 0.1), int(w * 0.95)))
        t0 = int(rng.integers(0, int(h * 0.6))); t1 = t0 + int(rng.integers(h // 10, h // 4))
        ink[t0:t1, x:x + 1] |= rng.random((t1 - t0, 1)) < 0.5

    out = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8), "L")
    out = out.rotate(0.35, resample=Image.BICUBIC, fillcolor=255)      # the sheet sat a bit crooked
    a = np.asarray(out).copy()
    # dark smear down the left edge and along the top, like the copier lid not closing
    edge = nd.gaussian_filter(rng.normal(size=(h, 1)).astype(np.float32), 30)
    edge = 14 + 12 * edge / (np.abs(edge).max() + 1e-6)
    cols = np.arange(w)[None, :]
    a[np.broadcast_to(cols < edge, a.shape)] = 0
    a[: int(5 + 3 * rng.random()), :] = 0
    return Image.fromarray(a, "L").convert("1")


def main():
    out = ROOT / "print" / "flier.pdf"
    clean = canvas.Canvas(io.BytesIO() if not CLEAN else str(out), pagesize=letter)
    clean.setTitle("megaZINE flier")
    draw_page(clean)
    if CLEAN:
        clean.save()
        print("wrote print/flier.pdf (clean)")
        return
    layers = {}
    for name in ("base", "eyes"):
        layers[name] = io.BytesIO()
        c = canvas.Canvas(layers[name], pagesize=letter)
        draw_page(c, name)
        c.save()
    img = photocopy(layers["base"].getvalue(), layers["eyes"].getvalue())
    png = io.BytesIO()
    img.save(png, format="PNG", optimize=True)
    png.seek(0)
    f = canvas.Canvas(str(out), pagesize=letter)
    f.setTitle("megaZINE flier")
    f.drawImage(ImageReader(png), 0, 0, LW, LH)
    f.save()
    print(f"wrote print/flier.pdf (photocopied, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
