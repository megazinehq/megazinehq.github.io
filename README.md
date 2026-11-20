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
| `print/street-team/` | Two zips of the sticker sheets (black and white, colour) for the Street Team Pack's download links. Rebuild with `python3 tools/make_street_team.py` after any sticker sheet changes. |
| `tools/make_flier_big.py` | The second flier, `print/flier-big.pdf`, in the site's colours and crisp (not photocopied): one giant QR code made of tiny QR codes (every dark square is a little code) with "Making Yesterday's Tomorrow Today" in all caps along each of its four sides, pink dots at the corners, and the logo along the bottom. For a colour printer. Codes carry `?ref=flier-big`. `python3 tools/make_flier_big.py doom` makes `print/flier-big-doom.pdf`, the same layout with "BETWEEN MONEY AND DOOM" and `?ref=flier-big-doom`. |
| `print/stickers/` | Ten letter-size sticker sheets for a laser printer, black and white, with colour versions in `color/`. Straight cuts only. Each sheet's codes carry its own `?ref=sticker-NN-name` (labels: `sticker-avery-NN-colour`); the first run, printed before this, says plain `?ref=sticker`. Scripts are in `src/`; they read Matt's art from his own machine. Sheet 11 (colour only, `color/stickers-11-logo-color.pdf`) is six logo-over-eyeball-code stickers, made by `tools/make_logo_stickers.py`. `avery-5260/` has three black-and-white sheets for Avery 5260 address labels (30 to a sheet, built by `src/labels.py`), plus an alignment test to print on plain paper first. |
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

`makers` and `made` print the gold seal: "MADE BY MATT · BY HAND". With more than one maker, the seal puts one name to a line ("SAM / & MATT / & JENN"), sized to fit, on the site and the paper; three is the comfortable most. `image` is optional (paintings). Add `"hidden": true` to keep a piece off the site (still being built, or pulled for now) without deleting its entry.

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

**Our dashboard:** `https://megazine.org/stats/` (unlisted, not indexed). Tiles for the headline numbers, visitors and paper scans per day, scans and clicks by piece, which numbered copies have been picked up, referrers, countries and devices. The deploy workflow refreshes it every hour: `tools/pull_stats.py` asks GoatCounter's API for the last 90 days and writes `stats/stats.json` into the deployed site (it's not committed). Only aggregate counts go in that file. It also has a dotted world map (a glowing dot per country; tap one for its regions), and the referrer, country, browser and page lists open up (▸) to their detail: a country's regions, a browser's versions, each page's referrers. GoatCounter keeps no city, only a country and, for the countries ticked under Settings → Data collection → Regions, a region (a US state, say). `stats/world.json` is the static map data (land dots and country centres).

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

**Seasonal decoration.** Every December issue (month `YYYY-12`) gets string lights on the site, in classic C9 colours: they swag across the logo, fall off the last letter, run along the rule under the masthead and drop down the right margin. During Hanukkah (any year, worked out from the Hebrew calendar; a night runs 4 pm to 4 pm in the viewer's local time) the last eight bulbs on the drape are blue, and one more flickers each night. `"decor": "none"` on an issue turns them off. Try variants with `?preview=NN&hanukkah=1..8`, `&hanukkah=0` (none) or `&lights=off`. It is drawn in `tools/page.html` (the `xmasLights` script); the paper has none.

## Contact form (`/contact/`)

On the site, a quiet "Send comment" link sits in the footer, and from the December 2026 issue on a large **comment card** sits above the footer (shown whenever the issue on screen is December 2026 or later, so `?preview=03` shows it now).

The way to write to the editors without making a BBS account. First a test: nine small moving drawings, and an ask such as "shoot every square with an animal" (the categories are animals, vehicles, plants and instruments). There are two ways to shoot, chosen by a toggle, each with a three-picture tutorial. **Finger gun:** MediaPipe hand tracking reads the webcam, the fingertip steers the cross-hairs and dropping the thumb fires. **Head:** face tracking instead; the nose steers and opening the mouth fires. Shooting the Done bar hands in the answer. The first time in either mode you point at two dots (about half a second each) so the aim fits you; the fit is kept in the browser, and "Calibrate again" redoes it. The camera picture never leaves the page. There is no mouse option; the page tells anyone who would rather not use a webcam, or has no fingers or face, to use the BBS. Then name, reply email and message.

The page does not grade itself. The inbox Worker (`tools/inbox-worker/`, Cloudflare Worker + KV, deployed by the `Deploy inbox Worker` workflow from repository secrets; setup in its README) draws each round from `contact/squares.js`, keeps the answer, and gives a signed pass that works once for one note, only for a right answer that took longer than a second and a half. Each set of squares gets one try; 30 tries and 5 notes an hour per address. A note that gets through is handed to the BBS (Worker `bbs`, repo `samuelling/BBS`) over a service binding to its `Outside` entrypoint, which has no public address. There it becomes board e-mail from `megaZINE.org` to every SysOp, with the sender's name, reply address and message, and the board's own Slack/Telegram ping goes out. It is e-mail rather than a message base because every caller can read the bases. A copy is kept in the Worker: the editors can also read notes in the **Inbox** section of `/stats/` by entering the Worker's `ADMIN_KEY` (kept for the tab only), and reply by email or delete. If the BBS cannot be reached the copy is all there is, and the Worker pings Slack itself if it has a `SLACK_WEBHOOK` secret. `GET /about` on the Worker reports whether the line to the BBS is up. Notes are kept a year; no addresses are stored.

While `API` in `contact/index.html` and `INBOX_URL` in `stats/index.html` are empty, the page runs as a preview (it draws and checks its own squares and says nothing was sent) and the Inbox section stays hidden. The drawings are public in this repo, so someone determined could write a program to recognise them: this keeps out passing bots, not a person who wants in. Credited to Sam, Matt and Jenn; its entry in `works.json` is hidden until the inbox is live.

`/contact/?about=hands-key` opens the form with the message already laid out for asking for an Invisible Hands key (app, website, what it moves, how much). The Invisible Hands site links there. The editors issue keys on that site's `/keys/` page (repo `samuelling/InvisibleHands`) and reply to the sender.
