# Handoff

Notes between Sam's Claude and Matt's Claude. Newest first. A line or two per session: who, what changed, what's unfinished.

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
