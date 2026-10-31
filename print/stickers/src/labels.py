"""Black-and-white megaZINE stickers on Avery 5260 address labels (or 5160/8160): 30 to a letter sheet, 1 x 2 5/8 in,
three across, ten down. Reuses the helpers in stickers.py. Usage: labels.py OUT CUTS"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT_, CUTS_ = sys.argv[1], sys.argv[2]
src = open(HERE + "/stickers.py").read().split("BM2 = [")[0]
exec(compile(src, "stickers.py", "exec")); CUTS = CUTS_; OUT = OUT_
LX, LY, PX, PY, LW, LH, M = 3 / 16, .5, 2.75, 1, 2.625, 1, .05      # Avery's layout, inches; M keeps art off the die cut
Q = I(.78)
TAG = "between money and doom"
def bg(w, h, black): return Image.new("L", (w, h), K if black else W)
def side(im, cut, h, black):
    """A creature in the left 380 px, whatever its shape, so it never runs into the words."""
    c = Image.open(f"{CUTS}/{cut}.png"); creature(im, cut, 195, h / 2, 490 if c.height * .75 >= c.width else 360, edge=10 if black else 7)
def code(im, w, h): qr(im, w - Q - 34, (h - Q) // 2, Q, 22, False)
def area(w): return w - Q - 90
def c_logo(cut, black=False):
    def f(w, h):
        im = bg(w, h, black); fg, sl = (W, None) if black else (K, G); code(im, w, h); side(im, cut, h, black)
        a = area(w) - 390; s = logo_fit(a); x = 400; logo(im, x, 110, s, fg, sl); ft = fit(TAG, si, a); text(im, x, 130 + s * 1.15, TAG, ft, fg); return im
    return f
def c_word(word, black=False):
    def f(w, h):
        im = bg(w, h, black); fg, sl = (W, None) if black else (K, G); code(im, w, h); a = area(w) - 30
        ft = fit(word, bow, a); ft = bow(min(ft.size, 290)); text(im, 28, 20, word, ft, fg)
        s = logo_fit(380); logo(im, 30, h - s * 1.28, s, fg, sl); ft2 = fit(TAG, si, a - 420); text(im, 440, h - ft2.size * 1.9, TAG, ft2, fg); return im
    return f
def c_line(lines, cut, black=False):
    def f(w, h):
        im = bg(w, h, black); fg, sl = (W, None) if black else (K, G); code(im, w, h); side(im, cut, h, black)
        a = area(w) - 390; x = 400; ft = si(min(fit(l, si, a).size for l in lines)); ft = si(min(ft.size, 96)); y = 50
        for l in lines: text(im, x, y, l, ft, fg); y += ft.size * 1.14
        s = logo_fit(a * .62); logo(im, x, h - s * 1.3, s, fg, sl); return im
    return f
def c_eyes(black=False):
    def f(w, h):
        im = bg(w, h, black); fg, sl = (W, None) if black else (K, G); code(im, w, h); a = area(w); n = 5; R = a / n / 2 - 8
        for i in range(n):
            cx = 30 + R + i * (2 * R + 12)
            if black: ImageDraw.Draw(im).ellipse([cx - R - 7, 34 - 7, cx + R + 7, 34 + 2 * R + 7], fill=W)
            eye(im, cx, 34 + R, R, ((i - 2) * .5, .2), i + 3)
        y = 34 + 2 * R + 26; s = logo_fit(a * .4); logo(im, 30, y, s, fg, sl); ft = fit(TAG, si, a * .58); text(im, 30 + a * .42, y + 10, TAG, ft, fg); return im
    return f
def c_scene(k, box, black=False):
    def f(w, h):
        im = bg(w, h, K); a = w - Q - 90; art = scene(k, box, a, h); paint(im, art, art.rgb, (0, 0)); d = ImageDraw.Draw(im)
        d.rectangle([a, 0, w, h], fill=W); code(im, w, h); s = logo_fit(a * .62); ph = int(s * 1.42); d.rectangle([0, 0, a * .62 + 40, ph], fill=K); logo(im, 20, s * .02, s, W, None)
        ft = fit(TAG, si, a * .8); pw = tw(TAG, ft) + 40; d.rectangle([0, h - ft.size * 1.4, pw, h], fill=W); text(im, 20, h - ft.size * 1.32, TAG, ft, K); return im
    return f
C = ALL
BM = ["between money", "and doom"]
def mix(black, *cuts):
    n = len(cuts); it = iter(range(30)); c = lambda: cuts[next(it) % n]
    lines = [BM, ["small strange", "things"], BM, ["some made", "by hand"], BM, ["some made", "with a machine"], BM, ["no ticket, no price,", "no catch"], BM, ["take one"]]
    words = ["MONEY", "DOOM", "BETWEEN", "DOOM", "MONEY", "FREE", "DOOM", "AND", "MONEY", "DOOM"]
    return [f for i in range(10) for f in ((c_logo(c(), black) if i % 2 == 0 else c_eyes(black)), c_word(words[i], black), c_line(lines[i], c(), black))]
Sh = {
 "01-white": mix(False, *C),
 "02-black": mix(True, *C[8:], *C[:8]),
 "03-paintings": [c_scene(k, (x, y, x + .55, y + .2)) for k, x, y in [(("gold", "whale", "bear")[i % 3], .03 + (i * .137) % .42, .04 + (i * .263) % .74) for i in range(30)]],
}
def build(name, fns):
    PW, PH = I(8.5), I(11); page = np.ones((PH, PW), np.uint8) * 255; calm = np.zeros((PH, PW), bool); inside = np.zeros((PH, PW), bool); cells = []; m = I(M)
    for i, fn in enumerate(fns):
        cx, cy = LX + (i % 3) * PX, LY + (i // 3) * PY; QR.clear(); CS.clear(); wd, hd = I(LW) - 2 * m, I(LH) - 2 * m; im = fn(wd, hd); flush(im); assert im.size == (wd, hd), im.size
        X, Y = I(cx) + m, I(cy) + m; page[Y:Y + hd, X:X + wd] = np.asarray(im); inside[Y:Y + hd, X:X + wd] = True; cells.append((cx, cy, LW, LH))
        for a, b, c, d in QR: calm[Y + b:Y + d, X + a:X + c] = True
    keep = page.copy(); ink = copier(page, calm, 41); ink[calm] = keep[calm] < 128; ink[~inside] = False
    out = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)); out.convert("1", dither=Image.NONE).save(f"{OUT}/{name}.pdf", resolution=D)
    out.resize((PW // 3, PH // 3), Image.LANCZOS).save(f"{OUT}/{name}-preview.png"); import json; json.dump(cells, open(f"{OUT}/{name}.json", "w")); print(name, len(fns))
def grid_test():
    """Print this on plain paper and hold it against a label sheet to check the alignment."""
    PW, PH = I(8.5), I(11); t = Image.new("L", (PW, PH), W); d = ImageDraw.Draw(t); f = mono(40)
    for i in range(30):
        x, y = I(LX + (i % 3) * PX), I(LY + (i // 3) * PY); d.rounded_rectangle([x, y, x + I(LW), y + I(LH)], radius=I(.07), outline=K, width=4); d.text((x + 40, y + 40), f"{i + 1}", font=f, fill=K)
    d.text((I(.19), I(.2)), "Avery 5260 alignment test. Print at 100% on plain paper, hold against a label sheet to the light.", font=mono(34), fill=K)
    t.convert("1", dither=Image.NONE).save(f"{OUT}/alignment-test.pdf", resolution=D)
for n, c in Sh.items(): build("stickers-avery-" + n, c)
grid_test()
