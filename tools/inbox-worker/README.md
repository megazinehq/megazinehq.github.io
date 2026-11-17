# megaZINE inbox Worker

Runs the test for `/contact/` (draws the squares, keeps the answer, signs a one-use pass), then hands each note to the BBS, where it becomes board e-mail to the SysOps and sets off the board's Slack ping. It keeps a copy, which the editors can read on `/stats/`. Needs a Cloudflare account, the same one the BBS Worker (`bbs`) is on: `wrangler.toml` binds to that Worker's `Outside` entrypoint, so the BBS has to be deployed with it first.

**It deploys itself.** The `Deploy inbox Worker` workflow (`.github/workflows/inbox.yml`) puts it on Cloudflare whenever this folder or `contact/squares.js` changes on `main`, or when run by hand from the repo's Actions tab. It needs these repository secrets (GitHub: Settings → Secrets and variables → Actions):

- `CLOUDFLARE_API_TOKEN`: a Cloudflare API token made from the "Edit Cloudflare Workers" template (Cloudflare dashboard → My Profile → API Tokens).
- `INBOX_ADMIN_KEY`: a long passphrase you make up. `/stats/` asks for it to open the Inbox.
- `SLACK_WEBHOOK` (optional): a Slack incoming-webhook address, pinged only for a note the BBS could not take. The BBS does the normal ping itself.
- `CLOUDFLARE_ACCOUNT_ID` (optional): only if the token can see more than one account.

The first run makes the KV storage (`megazine-inbox`) and writes its id into `wrangler.toml` for that run only; the placeholder in the repo stays. The run's summary shows the Worker's address. Until the first two secrets exist, a run does nothing and says so.

Then, once:
1. In `contact/index.html`, set `API` to that address (no trailing slash).
2. In `stats/index.html`, set `INBOX_URL` to the same address.
3. Unhide the `fingergun-captcha` work when you want it in an issue.

By hand instead, from this folder: `npx wrangler kv namespace create INBOX` (paste the id into `wrangler.toml`), `npx wrangler secret put ADMIN_KEY`, optionally `npx wrangler secret put SLACK_WEBHOOK`, then `npx wrangler deploy`.

The drawings come from `../../contact/squares.js`, which wrangler bundles in.

Notes are kept a year, no IP addresses are stored (only one-hour counters per address for rate limiting), and only `https://megazine.org` can post. The fallback Slack ping carries the sender's name, reply email and message; the BBS's own ping carries the name and the start of the message. Changing `ADMIN_KEY` also cancels any test in progress.
