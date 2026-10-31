# megaZINE: notes for Claude

megaZINE is a collective run by two editors, **Sam Ling** (GitHub `samuelling`) and **Matt Crump**. It collects weird little things: apps, toys, tools, demos, music, paintings, stories. Some made with Claude, some by hand. Each issue is one sheet of paper folded into an 8-page mini-zine; every code on the paper points at this site (`https://megazine.org/`, served by GitHub Pages from repo `megazinehq/megazinehq.github.io`), and the site points at the work.

Whoever you're talking to is one of the two editors. Ask which one if it matters (it does for `makers` and the seal).

## Two editors, two Claudes

Sam and Matt each work here through their own Claude. Before changing anything:

1. Pull. The other editor may have pushed minutes ago.
2. Read the editor's guide: `SAM.md` when working with Sam (if it exists), `MATT.md` when working with Matt.
3. Read the top of `HANDOFF.md`, and `QUEUE.md` for what's coming.

When the editor approves a change:

4. Push it straight away. Don't leave finished work sitting uncommitted on one machine. If you stop partway, push what's done, or say in `HANDOFF.md` what's still in progress locally and where.
5. Pull again right before pushing, with `git pull --rebase`, so the other side's commits go in first.
6. If a pull collides: merge `works.json` and the docs by hand, keeping both sides' changes. Never merge the generated files (`index.html`, `print/*.pdf`); take either side, then rerun `tools/build.py` and `tools/make_sheet.py` and commit the results. If you can't tell which side is right, ask the editor.
7. Never force-push to `main`.

After pushing, add a dated line or two at the top of `HANDOFF.md`: who you worked with, what changed, and anything left unfinished or that the other Claude should know (a link still missing, a page that's tight on the paper). Keep it short; git history has the details.

`QUEUE.md` is the one shared to-do list for upcoming issues; `works.json` stays the truth for what's actually on the site and paper. Update the queue in the same commit as any change that affects it, and mention it in `HANDOFF.md`. When a piece goes into `works.json` and an issue, take its line out of the queue.

## The one rule

Every work says who made it and how. `makers` and `made` in `works.json` drive the gold **megaZINE seal** on the site and the black-and-white seal on the paper:
- `made`: `"hands"` (no AI), `"claude"` (Claude did the making), `"both"`.
- `makers`: first names as they should appear on the seal, e.g. `["Matt"]`, `["Sam", "Matt"]`. Optional `seal` overrides the text in the middle (keep it under ~10 characters).

Never guess `made`. Ask.

## Files

| Path | Edit? | What |
| --- | --- | --- |
| `works.json` | **Yes**, this is where almost all changes go | Every work and every issue. |
| `QUEUE.md` | **Yes** | The shared to-do list that feeds `works.json`: one section per upcoming issue, plus Unassigned. |
| `tools/page.html` | For site design changes | The site's source (a fragment, no `<html>`/`<head>`). |
| `index.html` | **Never by hand** | Built from `tools/page.html` by `python3 tools/build.py`. |
| `tools/make_sheet.py` | For paper layout changes | Builds `print/issue-NN.pdf` and `print/issue-NN-numbered.pdf`. |
| `media/` | Add files | Images for works (paintings, screenshots). Keep each under ~1 MB, JPG or WebP. |
| `print/` | Generated | Commit regenerated PDFs with the change that caused them. |

## A work entry

```json
{
  "id": "kebab-case-id",
  "title": "Name",
  "kind": "game | sound | music | tool | toy | art | painting | story",
  "made": "hands | claude | both",
  "makers": ["Matt"],
  "platform": "Web",
  "image": "media/kebab-case-id.jpg",
  "blurb": "Two or three plain sentences. The paper prints only the first one, so make it stand alone.",
  "links": [
    { "label": "Play", "url": "https://..." },
    { "label": "TestFlight", "url": null, "status": "Beta link soon" }
  ]
}
```

- `image` is optional; it shows on the site's card (good for paintings). The paper is text-only.
- A link with `"url": null` renders as a dashed "coming" button. The first link with a URL is where `?go=<id>` (the paper's code) sends people, unless the work has `"go": {"label": "...", "url": "..."}`, e.g. a page listing every streaming service for an album.
- `"book": {"label": "Open the book", "pages": [{"src": "media/x-1.jpg", "alt": "..."}], "pdf": "media/x.pdf"}` makes the card open a popup picture book (page-turn, arrow keys, swipe) with an optional PDF download. `?go=<id>` for a book with no live link opens the book on the site; the paper's code says "Open the book".
- `"hidden": true` keeps a piece off the site entirely (still being built, or pulled for now) without losing its entry. Take it out of every issue's `works` list too. There is no workshop list any more.
- Credit kids' ideas with `"idea": "Name"` (first names only).

## Issues

Issues are monthly. Each has `id` ("02"), `month` ("2026-11"), `date` ("November 2026"), optional `theme` (a subject for the issue; the tagline in `zine.tagline` always shows up top), and `works` (the lineup, in paper order). The site shows the **latest issue whose month has arrived** (viewer's local time), skipping any with `"draft": true` or no works; every earlier live issue appears under **Back issues** at `?issue=NN`. So the next issue can be built ahead of time: fill its `works`, remove `"draft"`, and it goes live by itself on the 1st. `?preview=NN` shows any issue that has works, ahead of its month or while it's a draft, and isn't counted in GoatCounter: send editors that link to look at a coming issue. A piece can appear in more than one issue.

The paper fits **24**. The folded booklet takes the first 12: pages 3–7 take the first ten in pairs, page 2 takes the 11th, the back cover the 12th. With more than 12, the sheet gets a back side (print duplex): a poster seen only when the zine is unfolded, with works 13–24 two to a panel, and the back cover says to unfold it. More than 24 and the extras appear only on the site. Never change the `id` of a work that's in a printed issue: the paper's codes use it.

## After any change

```
python3 tools/build.py                 # rebuild index.html
pip install qrcode reportlab           # once
python3 tools/make_sheet.py            # only if an issue's lineup or text changed
python3 tools/make_sheet.py --issue 02 # print a specific issue (default: the one live today)
```

`make_sheet.py` prints a warning if a page overflows; shorten the first sentence of that work's blurb rather than shrinking type. Then commit with a plain message saying what changed and push to `main`; the `Deploy to GitHub Pages` workflow (`.github/workflows/pages.yml`) redeploys in about a minute.

## Outside submissions

People other than the editors submit through the BBS (repo `samuelling/BBS`, MEGAzine BBS, formerly The Septic Tankz; work id `septic-tankz` stays because it's in printed Issue 01): they make an account (open enrollment for now; the SysOp can require validation again), and they post in the **megaZINE Submissions** message base using the template in its first post (title, what, link, how it was made, seal name). The SysOp gets a Slack/Telegram ping for each one. When an editor accepts one, add it to `works.json` with the submitter's seal name in `makers`, and tell them by board e-mail. Don't take submissions any other way.

## Site behaviour worth knowing

- An issue's cards are shuffled on every visit; the order in its `works` list only matters for the paper.
- The back-cover code is `?issue=NN&copy=N`, so a copy of an old issue opens that issue; work codes (`?go=<id>`) don't depend on the issue.
- Back issues are counted in GoatCounter as `/issue/NN`.
- Visits, paper scans (`/scan/<id>`, `/scan/copy-<n>`) and clicks out (`/click/<id>`) are counted in GoatCounter under the code in `zine.goatcounter`. Don't add other trackers or cookies.
- `/stats/` is the editors' readers dashboard (`stats/index.html`). The deploy workflow runs hourly and on every push; its `tools/pull_stats.py` step reads GoatCounter's API with the `GOATCOUNTER_TOKEN` secret and writes `stats/stats.json` into the deployed site only. Never commit that file, and keep it to aggregate counts.

## Keep the docs in step

`MATT.md` is the guide Matt follows to work with this repo through Claude, and `README.md` is the reference for both editors. Whenever a change alters how things work (new or renamed fields in `works.json`, new sections or behaviour on the site, paper capacity or layout rules, build steps, stats, access), update `MATT.md` and `README.md` in the same commit. Content-only changes (adding or editing a work) don't need it.

## Voice

Plain, dry, short. No hype, no "revolutionary". Blurbs describe what the thing does, in present tense, as a person would tell a friend.

## Other people's names stay off the page

Be oblique about anything a piece borrows from. Blurbs, titles, seals, images and the paper never name or depict other people's games, characters, films, songs, screensavers, brands or products as inspiration ("like X", "a remake of Y", "X-style"). Describe what our piece does instead: "a night skyline from an old screensaver", not the screensaver's name; "a city builder", not the game it echoes. No logos, screenshots or artwork from other works. Naming a platform or store something runs on or is sold through (iPhone, App Store, Spotify) is fine.

This is the default, not a ban. An editor can bend it for a specific piece when the reference matters to the piece (a Geocities-style homepage in HomeBlocks, a parody photo, comics that draw famous characters). Don't bend it on your own: say what the rule would cut, ask the editor, and note the exception in `HANDOFF.md`. Photos of real people and other people's artwork are the editor's call on rights, so flag that when you add them.
