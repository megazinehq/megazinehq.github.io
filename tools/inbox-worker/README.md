# megaZINE inbox Worker

Receives inquiries from `/contact/` and shows them to the editors on `/stats/`. Needs a Cloudflare account (Workers Paid is fine; the free tier works too).

One-time setup, from this folder:

```
npx wrangler kv namespace create INBOX     # copy the id it prints into wrangler.toml
npx wrangler secret put ADMIN_KEY          # make up a long passphrase; this is what /stats/ asks for
npx wrangler deploy                        # prints https://megazine-inbox.<you>.workers.dev
```

Then:
1. In `contact/index.html`, set `ENDPOINT` to `<that URL>/inquiry`.
2. In `stats/index.html`, set `INBOX_URL` to `<that URL>` (no trailing slash).
3. Link `/contact/` from the site and unhide the `fingergun-captcha` work.

Messages are kept a year, no IP addresses are stored (only a one-hour counter per address for rate limiting), and only `https://megazine.org` can post.
