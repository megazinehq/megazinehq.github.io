"""20 black-and-white megaZINE stickers on two letter sheets, for a laser printer. Matt's creatures are cut
straight from his paintings; everything goes through a copier pass like the flier. Straight cuts only."""
import io, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS = None
REPO = "/Users/mattcrump/Documents/GitHub/megazine/megazinehq.github.io"
ART = os.path.expanduser("~/Media/ClaudeCrumpDraw")
HERE = os.path.dirname(os.path.abspath(__file__)); CUTS = HERE + "/cuts"
OUT = sys.argv[1]; os.makedirs(OUT + "/color", exist_ok=True); sys.argv = sys.argv[:1]
sys.path.insert(0, REPO + "/tools"); os.environ.setdefault("MEGAZINE_FONTS", os.path.expanduser("~/Library/Fonts"))
import make_flier as F
from reportlab.pdfgen import canvas as rlc
import pypdfium2 as pdfium
URL = "https://megazine.org/?ref=sticker"
D = 600
def I(x): return int(round(x * D))
FB = REPO + "/tools/fonts/BowlbyOneSC-Regular.ttf"; L = os.path.expanduser("~/Library/Fonts/Liberation")
bow = lambda s: ImageFont.truetype(FB, int(s)); sb = lambda s: ImageFont.truetype(L + "Sans-Bold.ttf", int(s))
si = lambda s: ImageFont.truetype(L + "Sans-Italic.ttf", int(s)); mono = lambda s: ImageFont.truetype(L + "Mono-Bold.ttf", int(s))
K, W, G = 0, 255, 128
_d = ImageDraw.Draw(Image.new("L", (1, 1)))
def tw(t, f, sp=0): return sum(_d.textlength(c, font=f) + sp for c in t) - sp
def text(im, x, y, t, f, fill=K, sp=0):
    d = ImageDraw.Draw(im)
    for c in t: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + sp
def ctext(im, cx, y, t, f, fill=K, sp=0): text(im, cx - tw(t, f, sp) / 2, y, t, f, fill, sp)
def rtext(im, rx, y, t, f, fill=K, sp=0): text(im, rx - tw(t, f, sp), y, t, f, fill, sp)
def fit(t, mk, w, sp=0):
    s = 900
    while tw(t, mk(s), sp) > w: s -= 2
    return mk(s)
def logo_w(s): return tw("MEGA", bow(s)) + .06 * s + tw("zine", sb(.6 * s))
HAS = [False]
def logo(im, x, y, s, fill=K, slip=G):
    HAS[0] = True
    def draw(ox, oy, c):
        d = ImageDraw.Draw(im); d.text((ox, oy), "MEGA", font=bow(s), fill=c)
        d.text((ox + tw("MEGA", bow(s)) + .06 * s, oy - .03 * s), "zine", font=sb(.6 * s), fill=c)
    if slip is not None: draw(x + .04 * s, y + .035 * s, slip)
    draw(x, y, fill)
def logo_fit(w):
    s = 900
    while logo_w(s) > w: s -= 2
    return s
QR = []
PEND = []
def qr(im, x, y, px, pad=None, frame=True): PEND.append((x, y, px, pad, frame))
def flush(im):
    for a in PEND: qr_now(im, *a)
    if PEND and not HAS[0]:     # no wordmark on this one: hang a small tab off the code
        x0, y0, x1, y1 = QR[-1]; bw = x1 - x0; s = logo_fit(bw * .8); h = int(s * 1.0); y = y0 - h if y0 - h >= 0 else y1
        ImageDraw.Draw(im).rectangle([x0, y, x1, y + h], fill=K, outline=W, width=5); logo(im, x0 + (bw - logo_w(s)) / 2, y + s * .02, s, W, None)
    PEND.clear(); HAS[0] = False
def qr_now(im, x, y, px, pad=None, frame=True):
    """The tear-off tabs' plain code at high error correction, with one eyeball in the middle (the code can spare it)."""
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=1, border=0); q.add_data(URL); q.make(fit=True); m = q.get_matrix(); n = len(m)
    sz = px // n; px = sz * n
    pad = max(int(px * .085), sz * 2) if pad is None else pad
    d = ImageDraw.Draw(im); d.rectangle([x - pad, y - pad, x + px + pad, y + px + pad], fill=W, outline=K if frame else W, width=10 if frame else 0)
    for r_ in range(n):
        for c_ in range(n):
            if m[r_][c_]: d.rectangle([x + c_ * sz, y + r_ * sz, x + (c_ + 1) * sz - 1, y + (r_ + 1) * sz - 1], fill=K)
    c0 = x + px / 2; c1 = y + px / 2; R = sz * 3.6
    d.ellipse([c0 - R - sz * .7, c1 - R - sz * .7, c0 + R + sz * .7, c1 + R + sz * .7], fill=W); eye(im, c0, c1, R, (.15, .1), 2)
    QR.append((x - pad, y - pad, x + px + pad, y + px + pad))
_c = {}
def tone(rgb):
    """Colour to grey for toner: line stays black, saturated paint reads as mid grey so stipple can carry it."""
    a = np.asarray(rgb, dtype=np.float32) / 255; l = a.mean(2); s = a.max(2) - a.min(2)
    return np.clip(1 - np.maximum(1 - l, .42 * s + .25 * (1 - l)) * .95, 0, 1) * (l > .16) 
def creature(im, n, cx, cy, h, rot=0, flip=False, edge=16, edge_col=W):
    if n not in _c: _c[n] = Image.open(f"{CUTS}/{n}.png").convert("RGBA")
    c = _c[n]; c = c.transpose(Image.FLIP_LEFT_RIGHT) if flip else c
    s = h / max(c.size); c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
    pad = edge + 6; g = Image.new("RGBA", (c.width + 2 * pad, c.height + 2 * pad), (255, 255, 255, 0)); g.alpha_composite(c, (pad, pad))
    if rot: g = g.rotate(rot, expand=True, resample=Image.BICUBIC)
    a = np.asarray(g.getchannel("A")) > 90
    gray = Image.fromarray((tone(g.convert("RGB")) * 255).astype("uint8"))
    x, y = int(cx - g.width / 2), int(cy - g.height / 2)
    if edge:
        o = Image.new("L", g.size, edge_col); im.paste(o, (x, y), Image.fromarray((nd.binary_dilation(a, iterations=edge) * 255).astype("uint8")))
    paint(im, gray, g.convert("RGB"), (x, y), Image.fromarray((a * 255).astype("uint8")))
CS = {}
def cs(im):
    if CS.get("size") != im.size: CS.update(size=im.size, rgb=Image.new("RGB", im.size, "white"), tone=Image.new("L", im.size, 0), pm=Image.new("L", im.size, 0))
    return CS
def paint(im, gray, rgb, xy, mask=None):
    c = cs(im); im.paste(gray, xy, mask); c["rgb"].paste(rgb, xy, mask); c["tone"].paste(gray, xy, mask); c["pm"].paste(255, (xy[0], xy[1], xy[0] + gray.width, xy[1] + gray.height), mask)
SC = {"gold": "Golden_pyramid_with_tunnel_celebration", "whale": "Whale_in_the_distance_copy", "meet": "Meeting_of_the_mountains", "bear": "Sleeping_bear_s_spirit_forest_anima_l"}
_s = {}
def scene(k, box, w, h):
    if k not in _s: _s[k] = Image.open(f"{ART}/extracted/{SC[k]}/composite_full.png").convert("RGB")
    im = _s[k]; X, Y = im.size; fx, fy, fw, fh = X * .08, Y * .08, X * .84, Y * .84
    c = im.crop((int(fx + box[0] * fw), int(fy + box[1] * fh), int(fx + box[2] * fw), int(fy + box[3] * fh)))
    s = max(w / c.width, h / c.height); c = c.resize((int(c.width * s) + 2, int(c.height * s) + 2), Image.LANCZOS).crop((0, 0, w, h))
    g = Image.fromarray((tone(c) * 255).astype("uint8")); g.rgb = c; return g
def eye(im, cx, cy, R, look=(.2, .1), seed=0):
    d = ImageDraw.Draw(im); r = random.Random(seed); d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=K)
    ri, rp = R * .62, R * .37; ix, iy = cx + look[0] * R * .3, cy + look[1] * R * .3
    d.ellipse([ix - ri, iy - ri, ix + ri, iy + ri], outline=W, width=max(3, int(R * .07)))
    for j in range(10):
        a = j * math.pi / 5 + r.uniform(-.1, .1)
        d.line([ix + rp * 1.15 * math.cos(a), iy + rp * 1.15 * math.sin(a), ix + ri * .85 * math.cos(a), iy + ri * .85 * math.sin(a)], fill=W, width=max(2, int(R * .04)))
    d.ellipse([ix - rp, iy - rp, ix + rp, iy + rp], fill=K); g = rp * .3
    d.ellipse([ix - rp * .38 - g, iy - rp * .42 - g, ix - rp * .38 + g, iy - rp * .42 + g], fill=W)
def bar(im, y, h, t, fill=K, col=W, sp=5):
    ImageDraw.Draw(im).rectangle([0, y, im.width, y + h], fill=fill)
    f = fit(t, mono, im.width - 90, sp); f = mono(min(f.size, h * .62)); ctext(im, im.width / 2, y + (h - f.size) / 2 - 3, t, f, col, sp)
def wall(im, box, names, h, seed):
    r = random.Random(seed); x0, y0, x1, y1 = box; y = y0 + h * .2
    while y < y1 + h * .2:
        x = x0 + r.uniform(-h * .3, h * .1)
        while x < x1 + h * .3:
            creature(im, r.choice(names), x, y + r.uniform(-h * .1, h * .1), h * r.uniform(.85, 1.2), rot=r.uniform(-14, 14), flip=r.random() < .5, edge=9); x += h * .68
        y += h * .62
S2, BW, BH = I(2.38), I(3.88), I(2.38)   # inside each sticker's own white margin
ALL = ["Golde_13", "Golde_07", "Meeti_09", "Sleep_03", "Whale_00", "Golde_05", "Meeti_16", "Golde_19", "Sleep_05", "Meeti_05", "Whale_16", "Golde_12", "Golde_22", "Golde_18", "Sleep_02", "Meeti_06"]

def a_eye():
    im = Image.new("L", (S2, S2), K); c = S2 // 2; ro, ri = int(S2 * .43), int(S2 * .285)
    art = scene("gold", (.25, .2, .75, .7), S2, S2); m = Image.new("L", (S2, S2), 0); ImageDraw.Draw(m).ellipse([c - ro, c - ro, c + ro, c + ro], fill=255); paint(im, art, art.rgb, (0, 0), m)
    d = ImageDraw.Draw(im)
    for j in range(20):
        a = j * math.pi / 10; d.line([c + ri * math.cos(a), c + ri * math.sin(a), c + ro * math.cos(a), c + ro * math.sin(a)], fill=K, width=14)
    d.ellipse([c - ro, c - ro, c + ro, c + ro], outline=W, width=12); d.ellipse([c - ri, c - ri, c + ri, c + ri], fill=W, outline=K, width=14)
    q = I(.98); qr(im, c - q // 2, c - q // 2, q)
    ctext(im, c, 16, "BETWEEN MONEY", mono(72), W, 6); ctext(im, c, S2 - 100, "AND DOOM", mono(72), W, 6); return im
def a_flier():
    im = Image.new("L", (S2, S2), W); s = logo_fit(S2 - 60); logo(im, 30, 10, s); y = int(s * 1.08); ImageDraw.Draw(im).rectangle([30, y, S2 - 30, y + 12], fill=K)
    f = si(72); rtext(im, S2 - 30, y + 22, "between money and doom", f); q = I(1.05); qr(im, S2 - q - 70, S2 - q - 70, q)
    creature(im, "Golde_13", 390, S2 - 410, 700, rot=8); return im
def a_text(cut, line, rot=0, flip=False):
    def f():
        im = Image.new("L", (S2, S2), W); creature(im, cut, 620, 540, 1040, rot=rot, flip=flip); q = I(1.0); qr(im, S2 - q - 66, S2 - q - 66, q)
        ft = si(92); y = S2 - 300; ls = line.split("\n")
        ImageDraw.Draw(im).rectangle([0, y - 14, max(tw(w, ft) for w in ls) + 64, S2], fill=W)
        for w in ls: text(im, 40, y, w, ft); y += 108
        return im
    return f
def a_black():
    im = Image.new("L", (S2, S2), K); creature(im, "Meeti_09", 640, 700, 1300, rot=-8, edge=20); q = I(1.0); qr(im, S2 - q - 66, S2 - q - 66, q, frame=False)
    f = mono(84); y = S2 - 300; ImageDraw.Draw(im).rectangle([0, y - 16, 560, S2], fill=K)
    for t in ["NO TICKET.", "NO PRICE.", "NO CATCH."]: text(im, 44, y, t, f, W, 2); y += 90
    return im
def a_caution():
    im = Image.new("L", (S2, S2), W); d = ImageDraw.Draw(im); d.polygon([(714, 20), (1390, 735), (38, 735)], fill=K); d.polygon([(714, 130), (1215, 665), (213, 665)], fill=W)
    creature(im, "Golde_19", 714, 450, 340, edge=6); q = I(.92); qr(im, S2 - q - 60, S2 - q - 60, q)
    f = mono(112); y = 790
    for t in ["CAUTION", "SMALL", "STRANGE", "THINGS"]: text(im, 40, y, t, f); y += 145
    return im
def a_stack():
    return t_stack(S2, S2)
def a_hello():
    im = Image.new("L", (S2, S2), K); d = ImageDraw.Draw(im); ctext(im, S2 / 2, 6, "HELLO", bow(210), W); ctext(im, S2 / 2, 250, "I AM BETWEEN", mono(84), W, 4)
    d.rectangle([30, 360, S2 - 30, S2 - 30], fill=W); text(im, 56, 390, "money", si(150)); text(im, 56, 550, "and", si(150)); text(im, 56, 710, "doom", si(150))
    q = I(.95); qr(im, S2 - q - 80, 480, q, frame=False); creature(im, "Golde_19", 330, S2 - 240, 420, edge=8); creature(im, "Sleep_05", 880, S2 - 210, 340, flip=True, edge=8); return im
def a_tab():
    im = Image.new("L", (S2, S2), W); d = ImageDraw.Draw(im); s = logo_fit(S2 - 120); logo(im, 60, 20, s); y = int(s * 1.12); q = I(1.2)
    qr(im, (S2 - q) // 2, y + 80, q, frame=False); ctext(im, S2 / 2, S2 - 150, "TAKE ONE", mono(90), K, 16)
    for x in range(10, S2, 44): d.line([x, S2 - 34, x + 24, S2 - 34], fill=K, width=8)
    creature(im, "Golde_22", 190, y + 320, 400, edge=8); creature(im, "Whale_16", S2 - 180, y + 400, 400, edge=8, flip=True); return im
def a_stamp():
    im = Image.new("L", (S2, S2), W); d = ImageDraw.Draw(im); r = 26; st = 3 * r; m = 70; art = scene("whale", (.1, .05, .85, .55), S2 - 2 * m, S2 - 2 * m); paint(im, art, art.rgb, (m, m))
    for i in range(0, S2, st):
        for p in ((i, 12), (i, S2 - 12), (12, i), (S2 - 12, i)): d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=K)
    q = I(.95); qr(im, S2 - q - 130, S2 - q - 130, q); d.rectangle([m, m, m + 900, m + 150], fill=K); text(im, m + 24, m + 22, "NO PRICE", bow(100), W); return im
def a_first():
    im = Image.new("L", (S2, S2), W); d = ImageDraw.Draw(im); d.rectangle([0, 0, S2, 180], fill=K); ctext(im, S2 / 2, 42, "EVERY MONTH", mono(100), W, 8)
    for x in (260, S2 - 260): d.ellipse([x - 36, 54, x + 36, 126], fill=W) if False else None
    text(im, 40, 150, "1", bow(760)); text(im, 450, 240, "ST", bow(190)); q = I(1.0); qr(im, S2 - q - 66, S2 - q - 66, q); 
    creature(im, "Whale_16", 1120, 470, 520, rot=-6, edge=8); text(im, 40, S2 - 160, "New ones.", si(120)); return im
def a_wall():
    im = Image.new("L", (S2, S2), K); wall(im, (0, 0, S2, S2), ALL, 560, 4); q = I(1.1); qr(im, (S2 - q) // 2, (S2 - q) // 2, q); return im
def b_logo():
    im = Image.new("L", (BW, BH), W); q = I(1.5); s = logo_fit(1280); logo(im, 40, 0, s); y = int(s * 1.08); ImageDraw.Draw(im).rectangle([40, y, 1320, y + 14], fill=K)
    text(im, 40, y + 30, "between money", si(116)); text(im, 40, y + 160, "and doom", si(116)); qr(im, BW - q - 90, (BH - q) // 2, q); creature(im, "Golde_05", 1000, BH - 270, 520, edge=10); return im
def b_two():
    im = Image.new("L", (BW, BH), W); q = I(1.5); qr(im, BW - q - 90, (BH - q) // 2, q); creature(im, "Whale_00", 400, 470, 840); creature(im, "Meeti_16", 1050, 470, 720, flip=True)
    text(im, 44, BH - 300, "Some made by hand.", si(100)); text(im, 44, BH - 170, "Some made with a machine.", si(100)); return im
def b_this():
    im = Image.new("L", (BW, BH), K); d = ImageDraw.Draw(im); text(im, 60, 70, "THIS IS", bow(210), W); text(im, 60, 340, "BETWEEN MONEY", mono(130), W, 4); text(im, 60, 500, "AND DOOM", mono(130), W, 4)
    d.polygon([(60, 900), (900, 900), (900, 800), (1120, 1000), (900, 1200), (900, 1100), (60, 1100)], fill=W); q = I(1.35); qr(im, BW - q - 120, BH - q - 120, q); creature(im, "Golde_13", BW - 480, 220, 380, rot=-7, edge=8); return im
def b_wall():
    im = Image.new("L", (BW, BH), K); wall(im, (0, 0, BW, BH), ALL, 620, 9); q = I(1.4); qr(im, BW - q - 100, (BH - q) // 2, q); s = logo_fit(1180); ImageDraw.Draw(im).rectangle([0, BH - int(s * 1.25), 1240, BH], fill=W); logo(im, 24, BH - int(s * 1.3), s); return im
def b_eyes():
    im = Image.new("L", (BW, BH), W); r = random.Random(3); q = I(1.35); qr(im, BW - q - 90, 290, q); ps = []
    for _ in range(4000):
        R = r.choice([60, 80, 110, 150, 210]); x, y = r.uniform(R + 16, BW - q - 200 - R), r.uniform(R + 16, BH - 240 - R)
        if all(math.hypot(x - a, y - b) > R + c + 12 for a, b, c in ps): ps.append((x, y, R)); eye(im, x, y, R, (r.uniform(.3, 1), r.uniform(-.5, .5)), r.randint(0, 99))
    bar(im, BH - 200, 200, "SMALL STRANGE THINGS"); return im
def b_pano():
    im = Image.new("L", (BW, BH), W); art = scene("meet", (0, .3, 1, .9), BW, BH); paint(im, art, art.rgb, (0, 0)); q = I(1.45); qr(im, BW - q - 100, (BH - q) // 2, q); d = ImageDraw.Draw(im); w = BW - q - 300; s = logo_fit(w - 50); d.rectangle([0, BH - int(s * 1.15), w, BH], fill=W); logo(im, 24, BH - int(s * 1.2), s); return im
def b_free():
    im = Image.new("L", (BW, BH), W); d = ImageDraw.Draw(im); q = I(1.2); qr(im, BW - q - 100, 210, q); text(im, 40, 10, "FREE", bow(300))
    for i, n in enumerate(["Golde_07", "Meeti_05", "Sleep_03"]): creature(im, n, 240 + i * 440, 800, 470, edge=8)
    y = BH - 200
    for x in range(10, BW, 44): d.line([x, y, x + 24, y], fill=K, width=8)
    ctext(im, BW / 2, y + 44, "NO TICKET. NO PRICE. NO CATCH.", mono(92), K, 2); return im
def b_month():
    im = Image.new("L", (BW, BH), K); creature(im, "Golde_12", 760, 720, 1500, rot=-5, edge=22); q = I(1.4); qr(im, BW - q - 90, 90, q, frame=False)
    bar(im, BH - 210, 210, "NEW ONES ON THE 1ST OF EVERY MONTH", fill=W, col=K, sp=1); return im


def copier(g, calm, seed):
    """1-bit toner: blacks and whites hold, greys become grainy stipple, specks and dropouts outside the codes."""
    r = np.random.default_rng(seed); h, w = g.shape; v = g.astype(np.float32) / 255
    grain = nd.gaussian_filter(r.normal(size=(h, w)).astype(np.float32), 1.3); grain /= grain.std()
    ink = v < np.clip(.5 + .24 * grain, .04, .96)
    ink[v < .04] = True; ink[v > .97] = False
    drop = nd.binary_dilation(r.random((h, w)) < .00012, iterations=2) & ~calm; ink &= ~drop
    dust = nd.binary_dilation(r.random((h, w)) < .000012, iterations=2) & ~calm; ink |= dust
    return ink
POOL = """Golde_13 Golde_07 Meeti_09 Whale_00 Golde_05 Meeti_16 Golde_19 Sleep_05 Meeti_05 Whale_16 Golde_12 Golde_22 Golde_18 Sleep_02 Meeti_06 Sleep_03 Golde_16
The_C_08 The_C_28 The_C_31 The_C_34 Habit_04 Habit_05 Habit_06 Habit_12 Habit_13 Habit_14 Habit_17 Habit_22 Habit_33 Habit_36 Habit_43 Habit_46 Habit_55 Habit_59 Habit_60 Habit_40
Where_00 Where_01 Where_11 Where_13 Where_14 Where_15 Where_16 Where_17 Where_20 Where_23 Where_25 Where_26 Where_28 Where_31 Where_43
Modul_00 Modul_07 Modul_20 Modul_22 Modul_24 Modul_25 Modul_27 Modul_28 Modul_29 Modul_30 Modul_32 Modul_35 Modul_36""".split()
random.Random(21).shuffle(POOL); _p = [0]
def pick():
    n = POOL[_p[0] % len(POOL)]; _p[0] += 1; return n
def Q(w, h, k=.42): return max(I(.92), int(min(w, h) * k))
BMD = "between money and doom"
def plate(im, x, y, lines, f, fill=K, bg=W, step=None):
    step = step or int(f.size * 1.16); wd = max(tw(t, f) for t in lines)
    ImageDraw.Draw(im).rectangle([x - 24, y - 12, x + wd + 24, y + step * len(lines) + 8], fill=bg)
    for i, t in enumerate(lines): text(im, x, y + i * step, t, f, fill)
def t_hero(lines, black=False, flip=False):
    def f(w, h):
        im = Image.new("L", (w, h), K if black else W); q = Q(w, h); n = pick()
        creature(im, n, w * .42, h * .42, max(w, h) * .74, rot=random.Random(n).uniform(-9, 9), flip=flip, edge=18 if black else 12); qr(im, w - q - 66, h - q - 66, q)
        ft = si(min(w, h) * .068); y = h - int(ft.size * 1.2) * len(lines) - 26; plate(im, 40, y, lines, ft, W if black else K, K if black else W); return im
    return f
def t_stack(w, h, black=False):
    fg, bg = (W, K) if black else (K, W); im = Image.new("L", (w, h), bg); q = Q(w, h, .4); words = ["BETWEEN", "MONEY", "AND", "DOOM"]; y = 18; pw = w - q - 170 if h < w * 1.15 else w - 60
    for t in words:
        ft = fit(t, bow, pw); ft = bow(min(ft.size, (h * (.25 if h >= w * 1.15 else .245)))) ; text(im, 30, y, t, ft, fg); y += int(ft.size * 1.0)
    qr(im, w - q - 66, h - q - 66, q); return im
def t_mid(w, h):
    im = Image.new("L", (w, h), K); d = ImageDraw.Draw(im); q = Q(w, h, .62); ax = w - q - 170; ft = fit("MONEY", bow, ax * .33); ft = bow(min(ft.size, h * .4))
    text(im, 34, (h - ft.size) / 2 - 20, "MONEY", ft, W); rtext(im, ax, (h - ft.size) / 2 - 20, "DOOM", ft, W); creature(im, pick(), ax * .5, h / 2, min(h * .96, ax * .3), edge=14); qr(im, w - q - 80, (h - q) // 2, q); return im
def t_gauge(w, h):
    im = Image.new("L", (w, h), W); d = ImageDraw.Draw(im); q = Q(w, h, .36); cx, cy = (w - q - 120) * .5, h * .78; R = min(cx - 40, h * .6)
    d.arc([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=K, width=int(R * .1))
    for j in range(11):
        a = math.pi + j * math.pi / 10; r0 = R * (.74 if j % 5 == 0 else .82); d.line([cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + R * .92 * math.cos(a), cy + R * .92 * math.sin(a)], fill=K, width=int(R * .03))
    a = math.pi * 1.54; d.line([cx, cy, cx + R * .78 * math.cos(a), cy + R * .78 * math.sin(a)], fill=K, width=int(R * .05)); ft = mono(R * .17)
    text(im, cx - R, cy + 26, "MONEY", ft); rtext(im, cx + R, cy + 26, "DOOM", ft); creature(im, pick(), cx, cy - R * .05, R * .46, edge=8); qr(im, w - q - 66, (h - q) // 2, q); return im
def t_here(w, h):
    im = Image.new("L", (w, h), W); d = ImageDraw.Draw(im); q = Q(w, h, .62); ax = w - q - 170; y = int(h * .72); d.line([50, y, ax - 40, y], fill=K, width=16); ft = mono(h * .1)
    for x in (50, ax - 40): d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=K)
    text(im, 40, y + 40, "MONEY", ft); rtext(im, ax - 30, y + 40, "DOOM", ft); cx = ax * .55; creature(im, pick(), cx, h * .37, h * .62, edge=10); ctext(im, cx, y + 40, "YOU", ft); qr(im, w - q - 80, (h - q) // 2, q); return im
def t_signs(w, h):
    im = Image.new("L", (w, h), W); d = ImageDraw.Draw(im); q = Q(w, h, .42); ax = w - q - 150; hh = int((h - 90) / 2.6); ft = fit("MONEY", bow, (ax - 60) * .72); ft = bow(min(ft.size, hh * .62))
    def sign(y, t, left):
        x0, x1 = 40, ax - 20
        pts = [(x0 + hh * .45, y), (x1, y), (x1, y + hh), (x0 + hh * .45, y + hh), (x0, y + hh / 2)] if left else [(x0, y), (x1 - hh * .45, y), (x1, y + hh / 2), (x1 - hh * .45, y + hh), (x0, y + hh)]
        d.polygon(pts, fill=K); ctext(im, (x0 + x1) / 2, y + hh * .08, t, ft, W)
    sign(36, "MONEY", True); sign(50 + hh, "DOOM", False); n = pick(); creature(im, n, ax * .5, h - hh * .34, hh * .72, edge=8); qr(im, w - q - 66, (h - q) // 2, q); return im
def t_receipt(w, h):
    im = Image.new("L", (w, h), W); d = ImageDraw.Draw(im); ft = mono(w * .058); y = 30; s = logo_fit(w - 90); logo(im, 45, y, s); y += int(s * 1.15); ctext(im, w / 2, y, "*** RECEIPT ***", ft, K, 2); y += 90
    for a, b in (("MONEY", "0.00"), ("DOOM", "0.00"), ("TICKET", "0.00"), ("CATCH", "0.00"), ("STRANGE THINGS", "FREE")):
        text(im, 40, y, a, ft); rtext(im, w - 40, y, b, ft); y += int(ft.size * 1.35)
    d.line([40, y + 8, w - 40, y + 8], fill=K, width=6); y += 34; text(im, 40, y, "TOTAL", mono(w * .08)); rtext(im, w - 40, y, "0.00", mono(w * .08)); y += 130
    q = int(min(w * .8, h - y - 150)); room = h - y - q - 170; n = pick()
    if room > 240: creature(im, n, w / 2, y + room / 2, room, edge=8)
    qr(im, (w - q) // 2, h - q - 70, q); return im
def t_bubble(w, h, a="money?", b="doom."):
    im = Image.new("L", (w, h), W); d = ImageDraw.Draw(im); q = Q(w, h, .42); ft = si(min(w, h) * .095); r = int(min(w, h) * .12)
    n1, n2 = pick(), pick(); creature(im, n1, w * .24, h * .68, min(w, h) * .55, edge=10); creature(im, n2, w * .6, h * .34 + h * .32, min(w, h) * .5, flip=True, edge=10)
    for cx, cy, t in ((w * .24, h * .14, a), (w * .74, h * .14, b)):
        wd = tw(t, ft) + 70; d.rounded_rectangle([cx - wd / 2, cy - r * .75, cx + wd / 2, cy + r * .75], 50, fill=W, outline=K, width=10); d.polygon([(cx - 30, cy + r * .72), (cx + 30, cy + r * .72), (cx, cy + r * 1.3)], fill=K); ctext(im, cx, cy - ft.size * .6, t, ft)
    qr(im, w - q - 60, h - q - 60, q); return im
def t_big(word):
    def f(w, h):
        im = Image.new("L", (w, h), K); ft = fit(word, bow, w - 70); ft = bow(min(ft.size, h * .33)); text(im, 34, 10, word, ft, W); q = Q(w, h, .46); creature(im, pick(), w * .27, h * .7, min(w * .5, h * .62), rot=-6, edge=16); qr(im, w - q - 66, h - q - 66, q); ctext(im, w * .3, h - 74, BMD, mono(min(w, h) * .042), W) if False else None; return im
    return f
def t_eyeart(key, box, line):
    def f(w, h):
        im = Image.new("L", (w, h), K); s = min(w, h); c, d0 = w // 2, h // 2; ro, ri = int(s * .43), int(s * .285); art = scene(key, box, w, h); m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).ellipse([c - ro, d0 - ro, c + ro, d0 + ro], fill=255); paint(im, art, art.rgb, (0, 0), m); d = ImageDraw.Draw(im)
        for j in range(20):
            a = j * math.pi / 10; d.line([c + ri * math.cos(a), d0 + ri * math.sin(a), c + ro * math.cos(a), d0 + ro * math.sin(a)], fill=K, width=12)
        d.ellipse([c - ro, d0 - ro, c + ro, d0 + ro], outline=W, width=12); q = I(.92); qr(im, c - q // 2, d0 - q // 2, q); ctext(im, c, h - 96, line, mono(66), W, 4); logo(im, 22, -6, logo_fit(s * .36), W, None); return im
    return f
def t_scene(key, box, txt):
    def f(w, h):
        im = Image.new("L", (w, h), W); art = scene(key, box, w, h); paint(im, art, art.rgb, (0, 0)); q = Q(w, h, .46); qr(im, w - q - 80, h - q - 80, q); ft = si(min(w, h) * .075); plate(im, 40, h - int(ft.size * 1.16) * len(txt) - 28, txt, ft); return im
    return f
def t_wall(w, h):
    im = Image.new("L", (w, h), K); wall(im, (0, 0, w, h), [pick() for _ in range(9)], int(min(w, h) * .4), w); q = Q(w, h, .46); qr(im, (w - q) // 2, (h - q) // 2, q); return im
def t_eyes(line):
    def f(w, h):
        im = Image.new("L", (w, h), W); r = random.Random(w + h + len(line)); q = Q(w, h, .5); qr(im, w - q - 80, 210, q); ps = []
        for _ in range(3000):
            R = r.choice([50, 70, 100, 140, 190]); x, y = r.uniform(R + 16, w - q - 190 - R), r.uniform(R + 16, h - 190 - R)
            if all(math.hypot(x - a, y - b) > R + c + 12 for a, b, c in ps): ps.append((x, y, R)); eye(im, x, y, R, (r.uniform(.3, 1), r.uniform(-.5, .5)), r.randint(0, 99))
        bar(im, h - 160, 160, line); return im
    return f
def t_turn(fn):          # a wide design turned for a tall sticker
    def f(w, h):
        im = fn(h, w); flush(im); im = im.rotate(90, expand=True)
        if CS: CS.update(size=im.size, rgb=CS["rgb"].rotate(90, expand=True), tone=CS["tone"].rotate(90, expand=True), pm=CS["pm"].rotate(90, expand=True))
        QR[:] = [(y0, im.height - x1, y1, im.height - x0) for x0, y0, x1, y1 in QR]
        return im
    return f
def t_mini(line=None, black=False):
    def f(w, h):
        im = Image.new("L", (w, h), K if black else W); q = I(.95); creature(im, pick(), w * .42, h * .38, w * .72, edge=12 if black else 8); qr(im, w - q - 58, h - q - 58, q)
        if line:
            ft = si(84); plate(im, 30, h - 104 * len(line) - 16, line, ft, W if black else K, K if black else W, 100)
        return im
    return f
def wrap(fn): return lambda w, h: fn()
BUL = [wrap(a) for a in (a_eye, a_flier, a_text("Golde_16", "Small strange\nthings."), a_text("Golde_19", "Some made\nby hand."), a_text("Meeti_05", "Some made\nwith a machine."), a_stack, a_black, a_caution, a_hello, a_tab, a_stamp, a_first)]
def grid(x, y, cw, ch, fns, cols):
    return [(x + (i % cols) * cw, y + (i // cols) * ch, cw, ch, f) for i, f in enumerate(fns)]
TINTS = ["#ff5fa8", "#27d9ee", "#a8ef5a", "#ffe23a", "#ff9a4e", "#c9a6ff", "#7ff0cf", "#ff6f61"]
def colourise(im, seed):
    """Same sticker, in paint: painted pixels get their colour back, grey and open white take a flat colour."""
    L = np.asarray(im); h, w = L.shape; c = CS if CS.get("size") == im.size else cs(im)
    rgb = np.dstack([L] * 3).copy(); P = (np.asarray(c["pm"]) > 0) & (L == np.asarray(c["tone"])); rgb[P] = np.asarray(c["rgb"])[P]
    t = tuple(int(TINTS[seed % 8][i:i + 2], 16) for i in (1, 3, 5)); u = tuple(int(TINTS[(seed + 3) % 8][i:i + 2], 16) for i in (1, 3, 5))
    calm = np.zeros((h, w), bool)
    for a, b, x1, y1 in QR: calm[max(0, b):y1 + 1, max(0, a):x1 + 1] = True
    rgb[(L > 110) & (L < 150) & ~P] = u
    open_w = (L > 250) & ~P & ~calm; lab, n = nd.label(open_w); edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1]); edge.discard(0)
    rgb[np.isin(lab, list(edge))] = t
    return rgb
def sheet(cells, name):
    PW, PH = I(8.5), I(11); page = np.ones((PH, PW), np.uint8) * 255; cpage = np.ones((PH, PW, 3), np.uint8) * 255; calm = np.zeros((PH, PW), bool); xs, ys = set(), set(); m = I(.06)
    for x, y, cw, ch, fn in cells:
        QR.clear(); CS.clear(); wd, hd = I(cw) - 2 * m, I(ch) - 2 * m; im = fn(wd, hd); flush(im); assert im.size == (wd, hd), im.size
        X, Y = I(x) + m, I(y) + m; page[Y:Y + hd, X:X + wd] = np.asarray(im); cpage[Y:Y + hd, X:X + wd] = colourise(im, X // 7 + Y // 11); xs |= {I(x), I(x + cw)}; ys |= {I(y), I(y + ch)}
        for a, b, c, d in QR: calm[Y + b:Y + d, X + a:X + c] = True
    keep = page.copy(); ink = copier(page, calm, hash(name) % 9999 if False else len(cells) + 11); ink[calm] = keep[calm] < 128
    out = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(out); x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for X in xs: d.line([X, 0, X, max(0, y0 - 20)], fill=0, width=3); d.line([X, y1 + 20, X, PH], fill=0, width=3)
    for Y in ys: d.line([0, Y, max(0, x0 - 20), Y], fill=0, width=3); d.line([x1 + 20, Y, PW, Y], fill=0, width=3)
    out.convert("1", dither=Image.NONE).save(f"{OUT}/{name}.pdf", resolution=D); out.resize((PW // 3, PH // 3), Image.LANCZOS).save(f"{OUT}/{name}-preview.png"); print(name, len(cells))
    c = Image.fromarray(cpage); dc = ImageDraw.Draw(c)
    for X in xs: dc.line([X, 0, X, max(0, y0 - 20)], fill=(0, 0, 0), width=3); dc.line([X, y1 + 20, X, PH], fill=(0, 0, 0), width=3)
    for Y in ys: dc.line([0, Y, max(0, x0 - 20), Y], fill=(0, 0, 0), width=3); dc.line([x1 + 20, Y, PW, Y], fill=(0, 0, 0), width=3)
    c2 = c.resize((PW // 2, PH // 2), Image.LANCZOS); c2.save(f"{OUT}/color/{name}-color.pdf", resolution=300, quality=93); c.resize((PW // 3, PH // 3), Image.LANCZOS).save(f"{OUT}/color/{name}-color-preview.png")
    import json; json.dump([(c[0], c[1], c[2], c[3]) for c in cells], open(f"{OUT}/{name}.json", "w"))
BM2 = ["between money", "and doom"]
S = {}
S["01-squares"] = grid(.5, .5, 2.5, 2.5, BUL, 3)
S["02-bumpers"] = grid(.25, .5, 4, 2.5, [wrap(a) for a in (b_logo, b_two, b_this, b_wall, b_eyes, b_pano, b_free, b_month)], 2)
S["03-big"] = grid(.25, .5, 4, 3.33, [t_hero(BM2), lambda w, h: t_stack(w, h, True), t_gauge, t_wall, t_hero(["small strange", "things"], True), t_signs], 2)
S["04-tall"] = grid(.25, .5, 2, 5, [t_receipt, t_turn(t_mid), lambda w, h: t_stack(w, h), t_turn(t_here), t_turn(t_gauge), t_receipt, t_turn(t_signs), lambda w, h: t_stack(w, h, True)], 4)
S["05-long"] = grid(.25, .5, 8, 2, [t_mid, t_here, t_signs, t_eyes("BETWEEN MONEY AND DOOM"), t_wall], 1)
S["06-portrait"] = grid(.25, .25, 2.667, 3.5, [t_hero(BM2), t_bubble, t_hero(["money"], True), t_hero(["doom"], True), t_receipt, t_hero(["some made", "by hand"]), t_hero(["some made", "with a machine"]), t_bubble, t_hero(BM2, True)], 3)
S["07-poster"] = [(.25, .5, 8, 5, t_hero(BM2, True))] + grid(.25, 5.5, 4, 2.5, [t_gauge, t_bubble, t_here, t_big("DOOM")], 2)
S["08-eyes"] = grid(.5, .5, 2.5, 2.5, [t_eyeart(k, b, l) for k, b, l in [("whale", (.1, .1, .6, .6), "BETWEEN"), ("meet", (.2, .4, .7, .9), "MONEY"), ("bear", (.3, .3, .8, .8), "AND DOOM"), ("gold", (.05, .5, .55, 1), "LOOK"), ("whale", (.4, .4, .9, .9), "SCAN"), ("meet", (.5, .1, 1, .6), "FREE"), ("bear", (.05, .05, .55, .55), "TAKE ONE"), ("gold", (.45, .05, .95, .55), "MONEY"), ("whale", (.05, .5, .55, 1), "DOOM"), ("meet", (.05, .05, .55, .55), "STRANGE"), ("bear", (.5, .5, 1, 1), "NEW 1ST"), ("gold", (.3, .3, .8, .8), "AND DOOM")]], 3)
S["09-black"] = grid(.25, .5, 4, 2.5, [t_big("MONEY"), t_big("DOOM"), t_big("BETWEEN"), t_big("FREE"), t_scene("gold", (0, .05, 1, .7), BM2), t_scene("bear", (0, .3, 1, .95), BM2), t_scene("whale", (0, .3, 1, .95), ["small strange", "things"]), t_scene("meet", (0, 0, 1, .65), ["no ticket", "no price", "no catch"])], 2)
S["10-minis"] = grid(.25, .5, 2, 2, [t_mini(l, b) for l, b in [(["money"], 0), (["doom"], 1), (None, 0), (["between"], 1)] * 5], 4)
for n, c in S.items(): sheet(c, "stickers-" + n)
