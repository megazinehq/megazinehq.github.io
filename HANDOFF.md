# Handoff

Notes between Sam's Claude and Matt's Claude. Newest first. A line or two per session: who, what changed, what's unfinished.

## 2026-10-21 (late) · Sam's Claude

- Added the **readers dashboard** at `megazine.org/stats/` (`stats/index.html`). The Pages workflow now also runs hourly and pulls GoatCounter numbers into `stats/stats.json` at deploy time via `tools/pull_stats.py` (not committed; `.gitignore`d). Needs the repo secret `GOATCOUNTER_TOKEN` (GoatCounter API key with read-stats permission); until it's set the page says "Not connected yet".

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
