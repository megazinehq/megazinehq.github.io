# Handoff

Notes between Sam's Claude and Matt's Claude. Newest first. A line or two per session: who, what changed, what's unfinished.

## 2026-10-25 (3) · Sam's Claude

- Flier restyled: site logo face (Bowlby One SC, bundled in `tools/fonts/`), eyeball watermark, the tagline, and a photocopier pass (rasterised, so `flier.pdf` is an image; `--clean` gives vector). New deps for the flier only: pypdfium2, numpy, pillow, scipy.

## 2026-10-25 (2) · Sam's Claude

- New **`tools/make_flier.py`** → `print/flier.pdf`: a letter-page wall flier (big logo, four lines of mystery) with ten tear-off tabs, each the logo over a QR to megazine.org?ref=flier. Not tied to any issue. README updated; MATT.md doesn't cover print tools beyond the sheet, so unchanged.

## 2026-10-25 · Sam's Claude

- Moved **Animal Sanctuary** from Issue 02 to a new **Issue 03** (December 2026, not draft, no theme yet). Issue 02 is Metamers, Ambit, ChairQuest, Last Skip, HomeBlocks. Issue 03 PDFs generated too. Anything else for December goes in its `works`.

## 2026-10-24 · Sam's Claude

- Added **HomeBlocks** (toy, both, Sam) to Issue 02 as the 6th piece: the standalone 90s-homepage site from Big Apple Sam, at samuelling.github.io/Big-Apple-Sam/web/ (each resident's page links to their window in the city and back). Issue 02 PDFs regenerated, no overflow.

## 2026-10-23 (6) · Sam's Claude

- **Animal Sanctuary** credit is now makers Maya, Sam, Emmy (dropped the separate `idea` field). PDFs regenerated.

## 2026-10-23 (5) · Sam's Claude

- Took **Titanosaur** out of Issue 02 for now (entry kept, not hidden). Issue 02 is Metamers, Ambit, Animal Sanctuary, ChairQuest, Last Skip. PDFs regenerated.

## 2026-10-23 (4) · Sam's Claude

- Dashboard visitors now use GoatCounter's site-wide per-day counts (deduped across pages) and are labeled "visitor-days". Docs unchanged (no structural change).

## 2026-10-23 (3) · Sam's Claude

- Added **Last Skip** (phone rock-skipper, Sam, made: both) to Issue 02, now 6 pieces. PDFs regenerated.

## 2026-10-23 (2) · Sam's Claude

- "Between money and doom" is the zine's tagline, not an issue theme. The site header and the paper cover now always show `zine.tagline`; an issue's `theme` is optional (cleared on both issues). Printed Issue 01 looks the same. Docs updated.

## 2026-10-23 · Sam's Claude

- Added **ChairQuest** (Matt, made: both, web version at crumplab.github.io/ChairQuest) as a work and to Issue 02. Matt: please check the blurb and that you're happy with the seal. Issue 02 is now Metamers, Ambit, Animal Sanctuary, Titanosaur, ChairQuest. Ambit's App Store button is still "In review". PDFs regenerated.

## 2026-10-22 (night) · Sam's Claude

- **Townies** blurb now ends "To see its innards, open Help → Behind the Scenes." Paper unchanged (first sentence only).

## 2026-10-22 (morning, 4) · Sam's Claude

- The BBS is now **MEGAzine BBS** (was The Septic Tankz; its elite side is now the Septic Tank). Updated the work's title and blurb in `works.json` (id `septic-tankz` unchanged, it's on printed Issue 01), the submissions text on the site, and CLAUDE/MATT/README. The board has open enrollment on for now, so submitters don't wait for validation. Issue 01 PDFs regenerated. The blurb now also mentions Matt's ChairQuest, which is a door game on the board (first sentence unchanged, so the paper didn't change).

## 2026-10-22 (morning, 3) · Sam's Claude

- Added **Titanosaur** (Thunderblitz album, made by hands) to Issue 02 and unhid it. Issue 02 is now Metamers, Ambit, Animal Sanctuary, Titanosaur. PDFs regenerated.

## 2026-10-22 (morning, 2) · Sam's Claude

- Issue 02 (Nov) now: Metamers, Ambit: Quartet, Animal Sanctuary (both unhidden). Animal Sanctuary links to its Pages build; Ambit's App Store button is still "In review": swap in the real link when approved. PDFs regenerated.

## 2026-10-22 (morning) · Sam's Claude

- Issue 02 (November) is no longer a draft: it holds just **Metamers** so far and goes live by itself on 1 Nov. Theme still empty; add more pieces and a theme before then. Print PDFs for 02 regenerated.

## 2026-10-22 · Sam's Claude

- Added **Metamers** (Sam's paper generator, toy, both) to `works.json` and to draft Issue 02 only; Issue 01 untouched. `made: both` assumed, as for Sam's other pieces: confirm.

## 2026-10-21 (night) · Sam's Claude

- The masthead logo **jitters** every 3.5–9 s (a 0.34 s copier-slip hop, sometimes twice): `@keyframes logo-jit-*` and a small script at the end of `tools/page.html`. Off with reduced motion.
- **Bell Weather** now offers the norns script as a download: `downloads/bellweather-norns.zip` (from private repo `samuelling/bellweather`, v1.3.0). That version adds a **location** param (auto from the network, Watertown, or custom lat/lon) so a downloaded copy plays its own weather. To update the zip: zip the repo's `bellweather.lua`, `lib/`, `README.md`, `LICENSE` under a top folder `bellweather/`.

## 2026-10-21 (night) · Matt's Claude

- Added Matt's **PCASynth and PCAWave** (sound, both; one entry for the two synth plug-ins) to Issue 01 as the 12th piece, on the back cover. Issue 01 is full on the booklet now; a 13th piece turns the sheet double-sided. PDFs regenerated, no overflow.

## 2026-10-21 (afternoon, later) · Sam's Claude

- **Big Apple Sam** now has a **Mac screen saver** download (second link, the signed and notarized `.dmg` from the repo's rolling `latest` release, so it always points at the newest build). Platform reads "Web · Mac screen saver"; the paper code still goes to the web version. Issue 01 PDFs regenerated, no overflow.

## 2026-10-21 (evening) · Sam's Claude

- **Ambit: Quartet** is hidden and out of Issue 01 until it's on the App Store. To bring it back: remove `"hidden"`, set its App Store link, add `ambit` to the issue's `works`. Issue 01 is 11 pieces; **Bell Weather** moved last so it lands on page 2 (MINERVA Space Echo overflowed there by 9pt).

## 2026-10-21 (evening) · Matt's Claude

- Added steps 4–7 to "Two editors, two Claudes" in `CLAUDE.md` (also MATT.md, README): push as soon as a change is approved, `git pull --rebase` right before pushing, merge `works.json` by hand on a conflict but regenerate `index.html` and the PDFs, never force-push.

## 2026-10-21 (late) · Matt's Claude

- Added Matt's **MINERVA Space Echo** (sound, both) to Issue 01 as the 12th piece, on the back cover; PDFs regenerated, no overflow. The title keeps "Space Echo" at Matt's call, an editor's exception to the no-product-names rule; the blurb stays oblique. October copies printed before this don't have it.

## 2026-10-21 (late) · Sam's Claude

- Added the **readers dashboard** at `megazine.org/stats/` (`stats/index.html`). The Pages workflow now also runs hourly and pulls GoatCounter numbers into `stats/stats.json` at deploy time via `tools/pull_stats.py` (not committed; `.gitignore`d). Needs the repo secret `GOATCOUNTER_TOKEN` (GoatCounter API key with read-stats permission); until it's set the page says "Not connected yet". Sam added the secret at 13:21; dashboard connected.

## 2026-10-21 (afternoon) · Sam's Claude

- **Monthly issues:** each issue has a `month`; the site shows the latest one whose month has arrived, and older ones sit under **Back issues** (`?issue=NN`). **Issue 02 (November 2026) is an empty draft**: fill `theme` and `works`, remove `"draft"`, and it goes live Nov 1 by itself. `make_sheet.py --issue NN` prints a specific issue; back-cover codes now carry `?issue=NN&copy=N`.
- Removed the **In the workshop** section; its entries are now `"hidden": true`. Removed the **Paper first** block.
- Everett is on the seals: **Toilet Goalie** (EVERETT) and **Brick Ninja** (EVERETT & SAM, idea credit: Maya for the secret doors); both blurbs say a five-year-old vibe coded them. Seal names now shrink to fit the ring, on the site and the paper.

## 2026-10-21 · Sam's Claude

- Masthead line now reads just "Issue 01 · October 2026  Free" (dropped "one sheet of paper · the rest is online").
- **what?** is back under the eyeball QR, centred (`.qr-col` in `tools/page.html`); its note opens under the logo row. The tagline now sits at the right end of the top line, level with the issue number; the This issue heading has no tagline.
- The **what?** note is signed "– Sysops: Sam and Matt" (site and paper page 2) and opens as a blue-tinted window with a pink offset shadow.
- Added an **eyeball QR code** for megazine.org to the left of the masthead title, as tall as the title. Every dark module is an eye that follows the pointer, wanders when idle and blinks (the three giant eyes every few seconds, a few small ones constantly, and a ripple or all-at-once blink every 6–11 s; blinks run even with reduced motion); it sits on its own paper sticker so it scans in dark mode too. Tested with two decoders at phone and desktop sizes, with eyes looking anywhere and all shut. Lives in `tools/page.html` (CSS under the logo, script at the end).
- Moved **what?** to the far right of the logo row (drops under the title on phones). Its note now opens as a panel under the button, over the page, and closes on an outside click or Escape.

## 2026-10-21 · Matt's Claude

- Moved the site to **megazinehq.github.io** with an Actions deploy (`.github/workflows/pages.yml`), then to **megazine.org** (DNS at Namecheap, see README). `base_url` and the paper's codes use megazine.org; stats now count on the host in `base_url`.
- The paper can go **double-sided**: past 12 pieces, the back of the sheet becomes a poster seen when unfolded, holding 13–24. Print duplex then. `make_sheet.py` also finds the Liberation fonts on a Mac.
- Added Matt's **Rehearsal Loop** to Issue 01 (App Store link still to come).
- HTTPS is on and enforced for megazine.org, so the regenerated PDFs are fine to print. Deploys stuck at "waiting" on the `github-pages` environment this afternoon; cancelling the queue and running the workflow by hand (`gh workflow run pages.yml`) cleared it.

## 2026-10-21 · Sam's Claude

- Pulled **Animal Sanctuary** into the workshop and hid **Titanosaur** with a new `"hidden": true` flag (finished piece, off the site for now; entry kept). Issue 01 is 11 pieces, single-sided.
- Moved **Bell Weather** to the end of the lineup so it lands on page 2; Rehearsal Loop's text overflowed there.
- Installed the Claude GitHub app on the megazinehq org so both Claudes can push.
- The old repo `samuelling/megazine` is now only a redirect: `samuelling.github.io/megazine/…` forwards to the same path on megazine.org, keeping `?go=` and `?copy=`. Don't put site content there.
- Still open: Ambit's App Store link (in review), Townies' TestFlight link. (The BBS README now links megazine.org.)
