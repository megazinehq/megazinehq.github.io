# Matt: how to get your stuff into megaZINE

## Once

1. Make sure you have access to `megazinehq/megazinehq.github.io` on GitHub.
2. Make sure your Claude can reach your GitHub (in the Claude app, GitHub under Settings → Connectors, or use Claude Code on your Mac).
3. Ask Sam to add you to the stats dashboard at megazine.goatcounter.com (or he'll make it public).

## Every time

Sam's Claude works in the same repo, so yours keeps the two in step:

- It pulls before changing anything and reads `HANDOFF.md` for anything Sam's side left in progress.
- Once you approve a change, it pushes straight away (pulling again just before), so nothing finished sits only on your laptop.
- If both sides changed the same thing, it merges `works.json` by hand and regenerates the site and PDFs rather than merging them. It asks you if it can't tell which side is right.
- After pushing, it adds a short note to `HANDOFF.md`.

Paste this to Claude, then tell it what you want to do:

> I'm Matt Crump, co-editor of megaZINE with Sam Ling. The repo is github.com/megazinehq/megazinehq.github.io. Please add it to this session, read CLAUDE.md in it, and follow it.

Then just talk normally, e.g.:

- "Add my painting *Name*. Here's the photo. Made by hand."
- "Add my iOS app *Name*, TestFlight link is …, made with Claude."
- "Start Issue 02: theme *…*, with these pieces …"
- "Put my two newest pieces in Issue 02."

Claude will ask if you don't say: how it was made (by hand, by Claude, or both) and where it lives (a link, or a photo for paintings).

Descriptions stay oblique about influences: no names of other people's games, films, brands or characters, and no borrowed artwork. Claude will reword if you mention them.

## How the site works

- **The address** is megazine.org (the old megazinehq.github.io address redirects there).
- **The eyeball QR** left of the title is a working code for megazine.org, drawn as eyes that follow the pointer and blink. It's generated in the page from the QR grid (the `eyeqr` script at the end of `tools/page.html`); if the address ever changes, regenerate the grid there.
- **The issue** is the current lineup. Its cards appear in a new random order on every visit, so nobody's piece is always first.
- **Monthly issues:** the site shows the issue for the current month; earlier ones stay up under **Back issues** (`megazine.org/?issue=01`). Next month's issue can be built ahead as a draft and goes live on the 1st once it has pieces and isn't marked draft.
- **Pulled for now:** a finished piece can be hidden from the site without deleting it ("pull X for now").
- **Seals:** every piece gets a gold megaZINE seal: "MADE BY MATT" plus how it was made. It's the one rule.
- **Paintings** show their photo on the card.
- **Links can wait.** A link marked "soon" shows as a dashed button; fill it in later and every printed code for that piece starts working, no reprint.

## Other people's work

Outsiders submit through MEGAzine BBS (formerly The Septic Tankz): they dial in, make an account (open enrollment is on for now, so no wait; Sam can switch validation back on), and they post in the **megaZINE Submissions** message base (its first post has the template). To accept one, tell Claude "add <title> from <handle>'s BBS submission" and paste or summarize the post; it goes in with their name on the seal.

## The paper

- One letter-size sheet folds into an 8-page mini-zine. The booklet fits **12** pieces from the current issue; with more, the back of the sheet becomes a poster you see when you unfold it, with room for **12 more** (24 in all). Past 24, pieces appear only on the site. An issue with more than 12 prints double-sided.
- Every code on the paper goes through the site first, so links can change after printing.
- If you change the current issue, Claude regenerates `print/issue-NN.pdf` (one master) and `print/issue-NN-numbered.pdf` (numbered copies, each with its own back-cover code).

## Stats

**megazine.org/stats/** is our own readers dashboard, refreshed hourly: visitors per day, paper scans and clicks by piece, which numbered copies have been picked up, and where people came from. GoatCounter's dashboard (megazine.goatcounter.com) has the raw counts: visits (`/`), back issues (`/issue/NN`), paper scans per piece (`/scan/<id>`), back-cover scans per copy (`/scan/copy-<n>`), and clicks out (`/click/<id>`).
