# megaZINE inbox Worker

Runs the finger-gun test for `/contact/` (draws the squares, keeps the answer, signs a one-use pass), stores the notes, pings Slack, and shows the notes to the editors on `/stats/`. Needs a Cloudflare account.

One-time setup, from this folder:

```
npx wrangler kv namespace create INBOX     # copy the id it prints into wrangler.toml
npx wrangler secret put ADMIN_KEY          # make up a long passphrase; this is what /stats/ asks for
npx wrangler secret put SLACK_WEBHOOK      # optional: a Slack incoming-webhook address (the BBS's one works) to be pinged per note
npx wrangler deploy                        # prints https://megazine-inbox.<you>.workers.dev
```

Then:
1. In `contact/index.html`, set `API` to that URL (no trailing slash).
2. In `stats/index.html`, set `INBOX_URL` to the same URL.
3. Unhide the `fingergun-captcha` work when you want it in an issue.

The drawings come from `../../contact/squares.js`, which wrangler bundles in. Run `npx wrangler deploy` again after changing this Worker or that file.

Notes are kept a year, no IP addresses are stored (only one-hour counters per address for rate limiting), and only `https://megazine.org` can post. The Slack ping carries the sender's name, reply email and message. Changing `ADMIN_KEY` also cancels any test in progress.
