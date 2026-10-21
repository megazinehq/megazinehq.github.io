"""Make the printable megaZINE sheet: one letter-size page that folds into an 8-page mini-zine.

    python3 tools/make_sheet.py            # print/issue-01.pdf (one master) + print/issue-01-numbered.pdf
    python3 tools/make_sheet.py --copies 100

Every code on the paper points at the hub (base_url?go=<id>), never straight at a work,
so links can change later without reprinting. The back-cover code carries the copy number.

The front folds into the booklet and holds 12 works. With more than 12, the sheet gets a back side:
a poster you only see when the zine is unfolded, holding works 13-24 two to a panel. Its panels match
the front's, so no code sits on a fold or the cut. Print duplex.

Imposition (landscape, 4 x 2 panels):   top row, upside down:  5 4 3 2
                                        bottom row, upright:   6 7 8 1
Fold in half lengthwise, then into quarters, cut the centre fold between panels 3/4 and 6/7... see README.
"""
import argparse, io, json, math, os, random
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from reportlab.lib.colors import Color, black, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

# Liberation fonts: Linux path first, then common Mac spots (Homebrew, R's fontLiberation). MEGAZINE_FONTS overrides.
FONT_DIRS = [os.environ.get("MEGAZINE_FONTS", ""), "/usr/share/fonts/truetype/liberation",
             str(Path.home() / "Library/Fonts"), "/Library/Fonts", "/opt/homebrew/share/fonts",
             "/Library/Frameworks/R.framework/Resources/library/fontLiberation/fonts/liberation-fonts"]
FONT_DIR = next((Path(d) for d in FONT_DIRS if d and (Path(d) / "LiberationSans-Regular.ttf").exists()), None)
if FONT_DIR is None:
    raise SystemExit("Liberation fonts not found. Install them (brew install --cask font-liberation) "
                     "or set MEGAZINE_FONTS to the folder that has LiberationSans-Regular.ttf.")
for name, f in [("Sans", "LiberationSans-Regular.ttf"), ("Sans-Bold", "LiberationSans-Bold.ttf"),
                ("Sans-Italic", "LiberationSans-Italic.ttf"), ("Sans-BoldItalic", "LiberationSans-BoldItalic.ttf"),
                ("Mono", "LiberationMono-Regular.ttf"), ("Mono-Bold", "LiberationMono-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / f)))
addMapping("Sans", 0, 0, "Sans"); addMapping("Sans", 1, 0, "Sans-Bold")
addMapping("Sans", 0, 1, "Sans-Italic"); addMapping("Sans", 1, 1, "Sans-BoldItalic")

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "works.json").read_text())
BASE = DATA["zine"]["base_url"].rstrip("/") + "/"
ISSUE = DATA["issues"][-1]
WORKS = {w["id"]: w for w in DATA["works"]}

PW, PH = landscape(letter)
COLS, ROWS = 4, 2
W, H = PW / COLS, PH / ROWS
PAD = 0.24 * inch
GREY = Color(0, 0, 0, alpha=0.55)
LIGHT = Color(0, 0, 0, alpha=0.18)

KIND = {"music": "MUSIC", "game": "GAME", "sound": "SOUND", "tool": "TOOL", "toy": "TOY", "art": "ART", "story": "STORY"}
MADE = {"hands": "MADE BY HAND", "claude": "MADE BY CLAUDE", "both": "HANDS + CLAUDE"}

body = ParagraphStyle("body", fontName="Sans", fontSize=8.6, leading=11.2, alignment=TA_LEFT)
small = ParagraphStyle("small", parent=body, fontSize=7.4, leading=9.4)
type_ = ParagraphStyle("type", fontName="Mono", fontSize=7.6, leading=9.6)
title = ParagraphStyle("title", fontName="Sans-Bold", fontSize=17, leading=17.5)
title_s = ParagraphStyle("title_s", fontName="Sans-Bold", fontSize=12.5, leading=13.5)


def qr_img(data, box=10):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=box, border=0)
    q.add_data(data)
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def para(c, text, style, x, y_top, w, h=None):
    """Draw a paragraph whose top edge is at y_top. Returns the y of its bottom edge."""
    p = Paragraph(text, style)
    _, ph = p.wrap(w, 10_000)
    p.drawOn(c, x, y_top - ph)
    return y_top - ph


def label(c, text, x, y, size=6.6, font="Mono-Bold", spacing=1.1):
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(spacing)
    t.textLine(text)
    t.setCharSpace(0)
    c.drawText(t)


def stamp(c, text, x_right, y, size=6.2):
    """Boxed rubber stamp (used for the copy number on the cover)."""
    c.saveState()
    c.setFont("Mono-Bold", size)
    tw = c.stringWidth(text, "Mono-Bold", size) + 0.4 * len(text)
    c.translate(x_right - tw - 6, y)
    c.rotate(2)
    c.setLineWidth(0.9)
    c.rect(-3, -3, tw + 6, size + 5, stroke=1, fill=0)
    t = c.beginText(0, 0)
    t.setFont("Mono-Bold", size)
    t.setCharSpace(0.4)
    t.textLine(text)
    t.setCharSpace(0)
    c.drawText(t)
    c.restoreState()


SEAL_HOW = {"hands": "BY HAND", "claude": "BY CLAUDE", "both": "HANDS + CLAUDE"}


def seal(c, w, cx, cy, r=21, rot=8):
    """Photocopier version of the gold seal: starburst, maker in the middle, how it was made underneath."""
    who = (w.get("seal") or " & ".join(w.get("makers") or ["?"])).upper()
    how = SEAL_HOW.get(w.get("made"), str(w.get("made", "")).upper())
    c.saveState()
    c.translate(cx, cy)
    c.rotate(rot)
    n = 30
    p = c.beginPath()
    for k in range(n * 2):
        rr = r if k % 2 == 0 else r * 0.9
        a = math.pi * k / n
        x, y = rr * math.sin(a), rr * math.cos(a)
        p.moveTo(x, y) if k == 0 else p.lineTo(x, y)
    p.close()
    c.setFillColor(Color(0, 0, 0, alpha=0.12))
    c.setLineWidth(0.7)
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(white)
    c.circle(0, 0, r * 0.74, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont("Mono-Bold", 3.6)
    c.drawCentredString(0, r * 0.38, "MADE BY")
    fs = 9 if len(who) <= 4 else 7 if len(who) <= 7 else 5.2
    c.setFont("Sans-Bold", fs)
    c.drawCentredString(0, -fs * 0.35, who)
    c.setFont("Mono-Bold", 3.1 if len(how) > 9 else 3.6)
    c.drawCentredString(0, -r * 0.52, how)
    c.restoreState()


def folio(c, n):
    label(c, f"megaZINE {ISSUE['id']}", PAD, PAD * 0.55, size=5.6)
    c.setFont("Mono-Bold", 6.4)
    c.drawRightString(W - PAD, PAD * 0.55, str(n))


def rule(c, y):
    c.setDash(2, 2)
    c.setLineWidth(0.6)
    c.line(PAD, y, W - PAD, y)
    c.setDash()


def first_sentence(t):
    i = t.find(". ")
    return t if i < 0 else t[: i + 1]


def work_block(c, wid, y_top, qr_size, big=False):
    """A work clipping. Big: full blurb, QR below. Small: first sentence, QR to the right. Returns bottom y."""
    w = WORKS[wid]
    x, cw = PAD, W - 2 * PAD
    label(c, KIND.get(w["kind"], w["kind"].upper()), x, y_top - 7)
    seal(c, w, W - PAD - 19, y_top - 20, rot=(sum(map(ord, wid)) % 21) - 10)
    y = para(c, w["title"], title if big else title_s, x, y_top - 14, cw - 44)
    url = f"{BASE}?go={wid}"
    live = [l for l in w["links"] if l.get("url")]
    pending = [l for l in w["links"] if not l.get("url")]
    first = w.get("go") or (live[0] if live else None)  # where ?go=<id> lands
    cta = [(first["label"].upper() + " →", True)] if first else []
    cta += [(f"{l['label']}: {l.get('status', 'soon')}", False) for l in pending]

    if big:
        if w.get("platform"):
            y = para(c, w["platform"], type_, x, y - 2, cw)
        y = para(c, w["blurb"], body, x, y - 5, cw)
        if w.get("idea"):
            y = para(c, "Idea: " + w["idea"], type_, x, y - 3, cw)
        yq = y - 8 - qr_size
        c.drawImage(qr_img(url), x, yq, qr_size, qr_size)
        ty = yq - 11
        for text, strong in cta[:3]:
            c.setFont("Mono-Bold" if strong else "Mono", 7)
            c.drawString(x, ty, text)
            ty -= 10
        return ty + 7

    tw = cw - qr_size - 8
    top = y - 4
    qtop = min(top, y_top - 44)  # keep the code clear of the seal
    c.drawImage(qr_img(url), x + cw - qr_size, qtop - qr_size, qr_size, qr_size)
    ty = top
    if w.get("platform"):
        ty = para(c, w["platform"], type_, x, ty, tw) - 3
    ty = para(c, first_sentence(w["blurb"]), small, x, ty, tw)
    if w.get("idea"):
        ty = para(c, "Idea: " + w["idea"], type_, x, ty - 3, tw)
    for text, strong in cta[:2]:
        ty -= 11
        font = "Mono-Bold" if strong else "Mono"
        while c.stringWidth(text, font, 6.8) > tw and " " in text:
            text = text.rsplit(" ", 1)[0]
        c.setFont(font, 6.8)
        c.drawString(x, ty, text)
    return min(ty - 3, qtop - qr_size)


# ---------------------------------------------------------------- panels

def p_cover(c, copy, run):
    # radio-field arcs: a nod to Aether Wave, drawn from the issue number so every issue differs
    rnd = random.Random(int(ISSUE["id"]) * 7)
    c.saveState()
    c.setLineWidth(0.6)
    for k in range(5):
        cx, cy = rnd.uniform(0.15, 0.85) * W, rnd.uniform(0.08, 0.42) * H
        for r in range(1, 9):
            c.setStrokeColor(Color(0, 0, 0, alpha=max(0.06, 0.5 - r * 0.055)))
            rr = r * (6 + k * 1.6)
            a0 = rnd.uniform(0, 360)
            c.arc(cx - rr, cy - rr, cx + rr, cy + rr, a0, rnd.uniform(70, 160))
    c.restoreState()
    # masthead
    big = 64
    while c.stringWidth("MEGA", "Sans-Bold", big) > W - 2 * PAD:
        big -= 1
    c.setFont("Sans-Bold", big)
    c.saveState()
    c.setFillColor(LIGHT)
    c.drawString(PAD + 2.2, H - PAD - 58, "MEGA")  # misregistered second pass
    c.restoreState()
    c.drawString(PAD, H - PAD - 56, "MEGA")
    c.setFont("Sans-Bold", 22)
    c.drawRightString(W - PAD, H - PAD - 80, "zine")
    c.setLineWidth(2)
    c.line(PAD, H - PAD - 90, W - PAD, H - PAD - 90)
    label(c, f"ISSUE {ISSUE['id']}", PAD, H - PAD - 104, size=8)
    c.setFont("Mono-Bold", 8)
    c.drawRightString(W - PAD, H - PAD - 104, ISSUE["date"].upper())
    para(c, ISSUE["theme"].lower(), ParagraphStyle("th", fontName="Sans-Italic", fontSize=13, leading=15),
         PAD, H - PAD - 114, W - 2 * PAD)
    if copy:
        stamp(c, f"COPY {copy:03d} / {run}", W - PAD, PAD + 4, size=8)
    else:
        label(c, "FREE · TAKE ONE", PAD, PAD + 4, size=7)


def p_intro(c, copy, run):
    y = H - PAD - 4
    label(c, "WHAT?", PAD, y - 7, size=7.4)
    y = para(c, "Matt and I have been using Claude to make weird stuff. AI chatter is all money-making or "
                "doom; the space in between seemed far less seen. So: strange little apps, some useless, "
                "some real tools, some performance pieces, plus our own music and paintings. "
                "<i>– Sysops: Sam and Matt</i>", body, PAD, y - 16, W - 2 * PAD)
    label(c, "HOW TO READ IT", PAD, y - 14, size=7.4)
    y = para(c, "Point your phone at a code. The links live online, so they outlast this paper.", body, PAD, y - 22, W - 2 * PAD)
    rule(c, y - 10)
    if len(ISSUE["works"]) > 10:
        y = work_block(c, ISSUE["works"][10], y - 16, 0.62 * inch)
    if y < PAD + 10 and not copy:
        print(f"warning: page 2 overflows by {PAD + 10 - y:.0f}pt")
    folio(c, 2)


def p_works(ids, n, big=False, qr=None):
    """A panel of works. n is the page number, or a name like "inside 3" for a panel on the back."""
    def draw(c, copy, run):
        size = qr or (1.15 * inch if big else 0.7 * inch)
        y = H - PAD
        for i, wid in enumerate(ids):
            if i:
                rule(c, y - 8)
                y -= 18
            y = work_block(c, wid, y, size, big=big)
        if y < PAD + 10 and not copy:
            print(f"warning: {'page ' if isinstance(n, int) else ''}{n} overflows by {PAD + 10 - y:.0f}pt")
        if isinstance(n, int):
            folio(c, n)
        else:
            label(c, f"megaZINE {ISSUE['id']} · INSIDE", PAD, PAD * 0.55, size=5.6)
    return draw


def p_inside_head(c, copy, run):
    """Top-left panel of the back: you've unfolded it."""
    c.setFont("Sans-Bold", 40)
    c.drawString(PAD, H - PAD - 38, "INSIDE")
    c.setLineWidth(2)
    c.line(PAD, H - PAD - 50, W - PAD, H - PAD - 50)
    label(c, f"megaZINE {ISSUE['id']}", PAD, H - PAD - 64, size=8)
    c.setFont("Mono-Bold", 8)
    c.drawRightString(W - PAD, H - PAD - 64, ISSUE["date"].upper())
    para(c, "You unfolded it. The rest of the issue is in here. Same deal: point your phone at a code. "
            "Fold it back up when you're done and leave it somewhere for the next person.",
         body, PAD, H - PAD - 76, W - 2 * PAD)


def p_inside_foot(c, copy, run):
    """Bottom-right panel of the back: how to get in the next one."""
    label(c, "PUT SOMETHING IN", PAD, H - PAD - 8, size=8)
    y = para(c, "An app, a song, a painting, a story, a thing that does nothing useful. "
                "Dial The Septic Tankz BBS, get validated by the SysOp, and post in megaZINE Submissions. "
                "Every piece gets a seal saying who made it and how.", body, PAD, H - PAD - 20, W - 2 * PAD)
    s = 1.1 * inch
    c.drawImage(qr_img(BASE), PAD, y - 14 - s, s, s)
    c.setFont("Mono-Bold", 7.2)
    c.drawString(PAD, y - 26 - s, BASE.replace("https://", "").rstrip("/"))


def p_back(c, copy, run):
    url = BASE + (f"?copy={copy}" if copy else "")
    extra = ISSUE["works"][11] if len(ISSUE["works"]) > 11 else None
    s = 1.3 * inch if extra else W - 2 * PAD - 0.3 * inch
    label(c, "THE REST LIVES HERE", PAD, H - PAD - 8, size=8)
    yq = H - PAD - 18 - s
    c.drawImage(qr_img(url), (W - s) / 2, yq, s, s)
    c.setFont("Mono-Bold", 7.2)
    c.drawCentredString(W / 2, yq - 12, BASE.replace("https://", "").rstrip("/"))
    y = yq - 12
    if copy:
        c.setFont("Mono", 6.6)
        c.drawCentredString(W / 2, yq - 22, f"this code knows you hold copy {copy}")
        y = yq - 22
    if extra:
        rule(c, y - 10)
        y = work_block(c, extra, y - 20, 0.7 * inch)
    else:
        y = para(c, "Want to put something in the next one? An app, a song, a painting, a story. "
                    "Dial The Septic Tankz BBS, get validated, and post in megaZINE Submissions. "
                    "The site has the number.", small,
                 PAD, yq - 32, W - 2 * PAD)
    if y < PAD + 26 and not copy:
        print(f"warning: page 8 overflows by {PAD + 26 - y:.0f}pt")
    c.setLineWidth(1.6)
    c.line(PAD, PAD + 20, W - PAD, PAD + 20)
    foot = "UNFOLD IT ALL THE WAY FOR THE REST" if len(ISSUE["works"]) > 12 else "FOLD IT · CUT IT · LEAVE IT SOMEWHERE"
    label(c, foot, PAD, PAD + 8, size=5.9, spacing=0.6)


# Pages 3-7 take the issue's first ten works in pairs; page 2 takes the 11th, the back cover the 12th.
_pairs = [ISSUE["works"][k:k + 2] for k in range(0, min(10, len(ISSUE["works"])), 2)]
PANELS = {1: p_cover, 2: p_intro, 8: p_back}
for _n, _ids in zip(range(3, 8), _pairs):
    PANELS[_n] = p_works(_ids, _n)
for _n in range(3, 8):
    PANELS.setdefault(_n, lambda c, copy, run, _n=_n: folio(c, _n))
LAYOUT = [[5, 4, 3, 2],  # top row, drawn upside down
          [6, 7, 8, 1]]  # bottom row

# The back (only when the issue has more than 12): works 13-24 in pairs, read flat, everything upright.
_inside = [ISSUE["works"][k:k + 2] for k in range(12, min(24, len(ISSUE["works"])), 2)]
_cells = [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)]
BACK = {(0, 0): p_inside_head, (1, 3): p_inside_foot}
for _k, (_cell, _ids) in enumerate(zip(_cells, _inside)):
    BACK[_cell] = p_works(_ids, f"inside panel {_k + 1}")
if len(ISSUE["works"]) > 24:
    print(f"note: {len(ISSUE['works']) - 24} works past 24 appear only on the site")


def back(c):
    for (r, col), draw in BACK.items():
        c.saveState()
        c.translate(col * W, PH - (r + 1) * H)
        p = c.beginPath()
        p.rect(0, 0, W, H)
        c.clipPath(p, stroke=0, fill=0)
        draw(c, None, None)
        c.restoreState()
    c.showPage()


def sheet(c, copy=None, run=None):
    for r, row in enumerate(LAYOUT):
        for col, n in enumerate(row):
            x = col * W
            y = PH - (r + 1) * H
            c.saveState()
            if r == 0:
                c.translate(x + W, y + H)
                c.rotate(180)
            else:
                c.translate(x, y)
            p = c.beginPath()
            p.rect(0, 0, W, H)
            c.clipPath(p, stroke=0, fill=0)
            PANELS[n](c, copy, run)
            c.restoreState()
    # fold and cut guides, in the margins only
    c.saveState()
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.5)
    for i in range(1, COLS):
        c.line(i * W, 0, i * W, 8)
        c.line(i * W, PH - 8, i * W, PH)
    c.line(0, H, 8, H)
    c.line(PW - 8, H, PW, H)
    c.setDash(3, 3)
    c.setStrokeColor(GREY)
    c.line(W, H, 3 * W, H)  # the one cut
    c.restoreState()
    c.showPage()
    if len(ISSUE["works"]) > 12:
        back(c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--copies", type=int, default=DATA["zine"].get("print_run", 50))
    a = ap.parse_args()
    out = ROOT / "print"
    out.mkdir(exist_ok=True)
    iid = ISSUE["id"]

    c = canvas.Canvas(str(out / f"issue-{iid}.pdf"), pagesize=(PW, PH))
    c.setTitle(f"megaZINE issue {iid}")
    sheet(c)
    c.save()

    c = canvas.Canvas(str(out / f"issue-{iid}-numbered.pdf"), pagesize=(PW, PH))
    c.setTitle(f"megaZINE issue {iid}, numbered copies 1-{a.copies}")
    for n in range(1, a.copies + 1):
        sheet(c, n, a.copies)
    c.save()
    sides = "double-sided, print duplex" if len(ISSUE["works"]) > 12 else "single-sided"
    print(f"wrote print/issue-{iid}.pdf and print/issue-{iid}-numbered.pdf ({a.copies} copies, {sides})")


if __name__ == "__main__":
    main()
