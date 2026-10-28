"""Fetch visitor counts from GoatCounter and write stats/stats.json for the dashboard at /stats/.

Runs in the Pages deploy workflow (on every push and hourly). Needs a GoatCounter API key
with permission to read statistics, stored as the repo secret GOATCOUNTER_TOKEN.
Without the key, or if GoatCounter is unreachable, it retries, then keeps the last published file and
exits cleanly so the deploy still goes out.

Only aggregate counts are written: paths, days, referrer domains, browsers, screen sizes,
countries. Nothing that identifies a visitor.

    GOATCOUNTER_TOKEN=... python3 tools/pull_stats.py
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "stats" / "stats.json"
DAYS = 90


def keep_last_published(data):
    """The deploy starts from a fresh checkout, so a failed pull would blank the dashboard until the
    next good one. Carry over the file the live site is serving, if there is one."""
    base = (data.get("zine") or {}).get("base_url", "").rstrip("/")
    if not base or OUT.exists():
        return
    try:
        with urllib.request.urlopen(f"{base}/stats/stats.json", timeout=20) as r:
            body = r.read()
        json.loads(body)
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_bytes(body)
        print("pull_stats: kept the stats file the live site already has", file=sys.stderr)
    except Exception as e:
        print(f"pull_stats: no earlier stats file to keep ({e})", file=sys.stderr)


def main():
    token = os.environ.get("GOATCOUNTER_TOKEN", "").strip()
    data = json.loads((ROOT / "works.json").read_text())
    code = (data.get("zine") or {}).get("goatcounter")
    if not token or not code:
        print("pull_stats: no GOATCOUNTER_TOKEN or site code; leaving stats as they are")
        keep_last_published(data)
        return
    base = f"https://{code}.goatcounter.com/api/v0"
    end = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)
    start = end - dt.timedelta(days=DAYS)
    rng = {"start": start.strftime("%Y-%m-%dT%H:%M:%SZ"), "end": end.strftime("%Y-%m-%dT%H:%M:%SZ")}

    def get(path, **params):
        q = urllib.parse.urlencode({**rng, **params})
        req = urllib.request.Request(f"{base}{path}?{q}", headers={
            "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        for attempt in range(4):  # GoatCounter now and then answers 404/5xx for a moment; try again
            time.sleep(0.3 + attempt * 2)  # it allows 4 requests a second
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:
                if e.code not in (404, 429, 500, 502, 503, 504) or attempt == 3:
                    raise
            except urllib.error.URLError:
                if attempt == 3:
                    raise

    failed = []

    def safe(path, fallback, **params):
        """One request; on any error note it and carry on, so one bad view doesn't sink the rest."""
        try:
            return get(path, **params)
        except Exception as e:
            body = ""
            if hasattr(e, "read"):
                try:
                    body = " " + e.read(300).decode("utf-8", "replace").strip().replace("\n", " ")
                except Exception:
                    pass
            failed.append(f"{path} ({e}){body}")
            return fallback

    total = safe("/stats/total", None)
    if total is None:
        print(f"pull_stats: GoatCounter unreachable or key refused: {failed[0]}", file=sys.stderr)
        keep_last_published(data)
        return
    # The site has a few dozen paths at most (/, /issue/NN, /scan/..., /click/...).
    hits = safe("/stats/hits", {}, daily="true", limit=100).get("hits") or []
    lists = {k: (safe(f"/stats/{k}", {}, limit=12).get("stats") or [])
             for k in ["toprefs", "browsers", "systems", "sizes", "locations"]}
    for f in failed:
        print(f"pull_stats: skipped {f}", file=sys.stderr)

    def daily(stats):
        return {s["day"]: s.get("daily", 0) for s in stats or [] if s.get("daily")}

    paths = [{"path": h["path"], "event": bool(h.get("event")), "count": h.get("count", 0),
              "days": daily(h.get("stats"))} for h in hits]
    out = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": rng["start"][:10], "end": (end - dt.timedelta(seconds=1)).strftime("%Y-%m-%d"), "days": DAYS},
        "total": total.get("total", 0),
        "total_events": total.get("total_events", 0),
        "days": daily(total.get("stats")),
        "paths": paths,
        **{k: [{"name": s.get("name") or "(unknown)", "count": s.get("count", 0)} for s in v] for k, v in lists.items()},
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(f"pull_stats: wrote {OUT.relative_to(ROOT)} ({len(paths)} paths, {out['total']} visitors in {DAYS} days)")


if __name__ == "__main__":
    main()
