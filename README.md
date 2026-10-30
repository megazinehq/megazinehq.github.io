# megaZINE

A collective of weird little apps, sounds, games, paintings and stories. Between money and doom.

Each issue is one sheet of paper folded into an 8-page mini-zine. Every code on the paper points at this site, and the site points at the work, so links can change without reprinting.

## What's here

| Path | What it is |
| --- | --- |
| `index.html` | The site. Built from `tools/page.html`; don't edit it directly. |
| `works.json` | Every work and every issue. This is the only file you edit to add things. |
| `print/issue-01.pdf` | The sheet to photocopy (one master, unnumbered; two pages = front and back). |
| `print/issue-01-numbered.pdf` | 50 numbered copies, each with its own back-cover code. |
| `tools/make_sheet.py` | Regenerates the PDFs from `works.json`. |
| `tools/make_flier.py` | Wall flier with ten tear-off QR tabs (`print/flier.pdf`), run through a fake photocopier (`--clean` skips that). Needs `pypdfium2 numpy pillow scipy` too. The codes carry `?ref=flier`, so GoatCounter lists "flier" under referrers. Uses the logo font in `tools/fonts/` (Bowlby One SC, OFL). |
| `tools/build.py` | Regenerates `index.html` from `tools/page.html`. |
| `tools/page.html` (`eyeqr` script) | The masthead's eyeball QR code for https://megazine.org/: the QR grid (`ROWS`, error correction H) is drawn as eyes that follow the pointer. Keep each finder square a plain dark frame; eyes on the frames stop it scanning. |
| `media/` | Images for works (paintings, screenshots). |
| `CLAUDE.md` | Instructions Claude follows when working in this repo. |
| `.github/workflows/pages.yml` | Publishes the site to GitHub Pages on every push to `main`. |
| `MATT.md` | How Matt (or anyone) adds work by talking to Claude. |
| `HANDOFF.md` | Short notes each editor's Claude leaves for the other, newest first. |
| `QUEUE.md` | The shared to-do list for upcoming issues. `works.json` stays the truth for what's on the site and paper. |

Both editors push to `main`. Pull before starting, push as soon as a change is approved (`git pull --rebase` first), and never force-push. On a conflict, merge `works.json` by hand and regenerate `index.html` and the PDFs instead of merging them. The full steps are under "Two editors, two Claudes" in `CLAUDE.md`.

## Put it online (once)

The repo is `megazinehq/megazinehq.github.io`. **Settings → Pages → Source** is set to **GitHub Actions**, and `.github/workflows/pages.yml` publishes the repo as-is on every push to `main` (run `tools/build.py` before committing so `index.html` is current).

The site is at `https://megazine.org/`, which is `base_url` in `works.json` and the address printed in the codes. The domain is registered at Namecheap and its DNS is in Namecheap's **Advanced DNS**: four `A` records on `@` to GitHub's Pages addresses (`185.199.108.153` to `185.199.111.153`) and a `CNAME` from `www` to `megazinehq.github.io`. The custom domain is set in **Settings → Pages**. `megazinehq.github.io` and `www.megazine.org` both redirect to `megazine.org`.

If the address ever changes, update `base_url` and rerun `make_sheet.py` before printing. Stats only count on the host in `base_url`.

## Add a work

Add an entry to `works` in `works.json`:

```json
{
  "id": "short-id",
  "title": "Name",
  "kind": "game | sound | music | tool | toy | art | painting | story",
  "made": "hands | claude | both",
  "makers": ["Matt"],
  "platform": "Web",
  "image": "media/short-id.jpg",
  "blurb": "Two or three plain sentences. The paper uses the first one.",
  "links": [
    { "label": "Play", "url": "https://..." },
    { "label": "TestFlight", "url": null, "status": "Beta link soon" }
  ]
}
```

Keep blurbs oblique about influences: don't name other people's games, films, brands or characters, and don't use their artwork (see `CLAUDE.md`).

A link with `"url": null` shows as a dashed "coming" button. Fill the URL in later and every printed code for it starts working, no reprint needed.

Work entries can also carry a `book` (a popup picture book, optional PDF): see CLAUDE.md.

`makers` and `made` print the gold seal: "MADE BY MATT · BY HAND". `image` is optional (paintings). Add `"hidden": true` to keep a piece off the site (still being built, or pulled for now) without deleting its entry.

To feature it in an issue, add its `id` to that issue's `works` list (the paper fits 24: 12 in the folded booklet, 12 more on the back of the sheet).

## Monthly issues and back issues

Each issue in `works.json` has a `month` (`"2026-11"`). The site shows the latest issue whose month has arrived; older ones are listed under **Back issues** and open at `megazine.org/?issue=01`. To prepare next month's issue, fill in its `works` and remove `"draft": true`; it goes live on the 1st on its own. To see an issue early (or while it's a draft), open `megazine.org/?preview=02`; previews aren't counted in the stats.

## Outside submissions

Anyone else submits through MEGAzine BBS (`samuelling.github.io/BBS`, formerly The Septic Tankz): make an account (open enrollment for now; otherwise wait for the SysOp to validate it), then post in the **megaZINE Submissions** base using the template in its first post. The SysOp is pinged for each submission. Accepted pieces go into `works.json` with the submitter's name on the seal.

## Links the site understands

- `/?go=townies` jumps straight to that work's first live link (this is what the paper codes use). If the work has no live link yet, it shows its card instead.
- `/?copy=37` shows "You're holding copy 37 of 50" plus a starting point picked from the issue by copy number.
- `/?w=townies` scrolls to and highlights a card.

## Visitor stats

Counts go to [GoatCounter](https://www.goatcounter.com) (free for non-commercial sites, no cookies, no banner needed), only from the live site (the host in `base_url`).

**Our dashboard:** `https://megazine.org/stats/` (unlisted, not indexed). Tiles for the headline numbers, visitors and paper scans per day, scans and clicks by piece, which numbered copies have been picked up, referrers, countries and devices. The deploy workflow refreshes it every hour: `tools/pull_stats.py` asks GoatCounter's API for the last 90 days and writes `stats/stats.json` into the deployed site (it's not committed). Only aggregate counts go in that file.

**Set up once:** the GoatCounter account is `megazine` (code in `zine.goatcounter` in `works.json`). In GoatCounter, your name menu → **API** → create a key that can read statistics, then add it to this repo as the Actions secret `GOATCOUNTER_TOKEN` (Settings → Secrets and variables → Actions). Until then `/stats/` says "Not connected yet".

**GoatCounter's own dashboard:** `https://megazine.goatcounter.com` (log in; add Matt as a user in its settings).

| Path | Means |
| --- | --- |
| `/` | A visit to the site. |
| `/issue/<NN>` | A visit to a back issue. |
| `/scan/<id>` | Someone scanned that work's code on the paper. |
| `/scan/copy-<n>` | Someone scanned the back cover of copy *n*. |
| `/click/<id>` | Someone clicked out to that work from the site. |

## Make the paper

```
pip install qrcode reportlab
python3 tools/make_sheet.py              # 50 numbered copies by default
python3 tools/make_sheet.py --copies 100
python3 tools/make_sheet.py --issue 02   # a specific issue; default is the one live today
python3 tools/make_flier.py             # the tear-off flier (pip install pypdfium2 numpy pillow scipy once)
```

Print on letter paper, landscape, at 100% (no "fit to page"). Black only; it's designed for a photocopier. If the issue has more than 12 pieces the PDF has a back side for each sheet: print **double-sided**. Either flip setting works, because the back is only read with the sheet unfolded.

**The back** is a poster you see when the zine is unfolded all the way: an INSIDE panel, pieces 13–24 two to a panel, and a panel on how to submit. Its panels line up with the front's, so no code lands on a fold or the cut. The back cover tells people to unfold it. Past 24, extra pieces appear only on the site.

**Fold:** the top row prints upside down, which is correct.
1. Fold in half the long way (top to bottom), then unfold.
2. Fold in half the short way, then into quarters, so you have 8 panels. Unfold.
3. Cut along the dashed line in the middle (only between the two centre panels).
4. Refold the long way, push the ends together so the cut opens into a diamond, and flatten into a booklet with the cover on the front.

## To fill in

- `ambit` → App Store URL once Ambit: Quartet clears review.
- `townies` → TestFlight public link for (Water) Townies.
- Matt's work: paintings, his iOS app, anything (see `MATT.md`).
