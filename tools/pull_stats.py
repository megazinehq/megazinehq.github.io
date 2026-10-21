"""Fetch visitor counts from GoatCounter and write stats/stats.json for the dashboard at /stats/.

Runs in the Pages deploy workflow (on every push and hourly). Needs a GoatCounter API key
with permission to read statistics, stored as the repo secret GOATCOUNTER_TOKEN.
Without the key, or if GoatCounter is unreachable, it leaves the previous file alone and
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
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "stats" / "stats.json"
DAYS = 90


def main():
    token = os.environ.get("GOATCOUNTER_TOKEN", "").strip()
    data = json.loads((ROOT / "works.json").read_text())
    code = (data.get("zine") or {}).get("goatcounter")
    if not token or not code:
        print("pull_stats: no GOATCOUNTER_TOKEN or site code; leaving stats as they are")
        return
    base = f"https://{code}.goatcounter.com/api/v0"
    end = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)
    start = end - dt.timedelta(days=DAYS)
    rng = {"start": start.strftime("%Y-%m-%dT%H:%M:%SZ"), "end": end.strftime("%Y-%m-%dT%H:%M:%SZ")}

    def get(path, **params):
        q = urllib.parse.urlencode({**rng, **params})
        req = urllib.request.Request(f"{base}{path}?{q}", headers={
            "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        time.sleep(0.3)  # GoatCounter allows 4 requests a second
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)

    try:
        total = get("/stats/total")
        # The site has a few dozen paths at most (/, /issue/NN, /scan/..., /click/...).
        hits = get("/stats/hits", daily="true", limit=100).get("hits") or []
        lists = {k: (get(f"/stats/{k}", limit=12).get("stats") or [])
                 for k in ["toprefs", "browsers", "systems", "sizes", "locations"]}
    except Exception as e:  # never break the deploy over stats
        print(f"pull_stats: GoatCounter request failed ({e}); leaving stats as they are", file=sys.stderr)
        return

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
