"""
Search visibility tracker for kinslow-regulatory-archive.org.

Pulls real ranking data from the official webmaster APIs instead of
scraping search engine result pages:

  * Google  -> Search Console Search Analytics API
  * Bing    -> Bing Webmaster Tools API

Bing's index also serves DuckDuckGo, Yahoo and Ecosia web results, so
the Bing figures below effectively cover those engines too. There is no
DuckDuckGo or Yahoo webmaster API to query, and scraping them is both
blocked (403) and unnecessary: if you rank in Bing, you rank in DDG.

Both report actual impressions, clicks, CTR and average position for the
queries your site genuinely ranks on. That is ground truth from the
engine, and it is strictly better data than a parsed SERP.

Credentials
-----------
Google : service account JSON at GSC_KEY_FILE (default google_console_key.json).
         The service account email must be added to the Search Console
         property under Settings -> Users and permissions.
Bing   : API key in the BING_WEBMASTER_API_KEY environment variable
         (or a .env file alongside this script). Optional - skipped if absent.

Usage
-----
    python rank_tracker.py                 # last 28 days
    python rank_tracker.py --days 7
    python rank_tracker.py --check-auth    # verify credentials only
"""

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "sc-domain:kinslow-regulatory-archive.org"
BING_SITE = "https://kinslow-regulatory-archive.org"
GSC_KEY_FILE = os.environ.get("GSC_KEY_FILE", os.path.join(HERE, "google_console_key.json"))
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

KEYWORD_FILES = ["keywords.txt", "keywords_targeted.txt"]
QUERY_BANK = "archive_200_queries.json"
OUT_JSON = os.path.join(HERE, "rank_tracking_results.json")
OUT_MD = os.path.join(HERE, "rank_tracking_report.md")

# GSC caps a single Search Analytics response at 25k rows.
GSC_ROW_LIMIT = 25000
# GSC data lags roughly 2-3 days; skip the freshest days to avoid partial rows.
GSC_LAG_DAYS = 3


def load_env_file():
    """Load simple KEY=value pairs from a local .env, without overriding real env vars."""
    path = os.path.join(HERE, ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def load_tracked_terms():
    """Collect the tracked keyword and query bank, de-duplicated, order preserved."""
    terms, seen = [], set()

    for name in KEYWORD_FILES:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                term = line.strip()
                if term and not term.startswith("#") and term.lower() not in seen:
                    seen.add(term.lower())
                    terms.append(term)

    bank = os.path.join(HERE, QUERY_BANK)
    if os.path.exists(bank):
        try:
            with open(bank, encoding="utf-8") as fh:
                data = json.load(fh)
            queries = data.get("queries", []) if isinstance(data, dict) else data
            for q in queries:
                q = (q or "").strip()
                if q and q.lower() not in seen:
                    seen.add(q.lower())
                    terms.append(q)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[WARN] Could not read {QUERY_BANK}: {exc}")

    return terms


def gsc_service():
    """Build an authenticated Search Console client, or return None with a reason."""
    if not os.path.exists(GSC_KEY_FILE):
        print(f"[SKIP] Google: service account key not found at {GSC_KEY_FILE}")
        return None
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("[SKIP] Google: pip install google-api-python-client google-auth")
        return None
    try:
        creds = service_account.Credentials.from_service_account_file(GSC_KEY_FILE, scopes=SCOPES)
        return build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    except Exception as exc:
        print(f"[SKIP] Google: could not authenticate ({exc})")
        return None


def fetch_google(service, days):
    """Pull per-query performance rows from Search Console."""
    end = dt.date.today() - dt.timedelta(days=GSC_LAG_DAYS)
    start = end - dt.timedelta(days=days)
    body = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": ["query"],
        "rowLimit": GSC_ROW_LIMIT,
    }
    try:
        resp = service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
    except Exception as exc:
        msg = str(exc)
        if "does not own" in msg or "403" in msg:
            print("[FAIL] Google: 403 - the service account is not a user on this property.")
            print("       Add its client_email in Search Console -> Settings -> Users and permissions.")
        else:
            print(f"[FAIL] Google Search Console query failed: {exc}")
        return None

    rows = [
        {
            "query": r["keys"][0],
            "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0.0) * 100, 2),
            "position": round(r.get("position", 0.0), 1),
        }
        for r in resp.get("rows", [])
    ]
    print(f"[ OK ] Google: {len(rows)} ranking queries ({start} to {end})")
    return {"start": start.isoformat(), "end": end.isoformat(), "rows": rows}


def fetch_bing(days):
    """Pull per-query stats from Bing Webmaster Tools, if an API key is configured."""
    api_key = os.environ.get("BING_WEBMASTER_API_KEY") or os.environ.get("BING_API_KEY")
    if not api_key or api_key.startswith("replace-with"):
        print("[SKIP] Bing: set BING_WEBMASTER_API_KEY to include Bing data.")
        return None

    url = (
        "https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats"
        f"?siteUrl={urllib.parse.quote(BING_SITE, safe='')}&apikey={urllib.parse.quote(api_key)}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "rank-tracker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        print(f"[FAIL] Bing: HTTP {exc.code} - verify the API key and that the site is verified.")
        return None
    except Exception as exc:
        print(f"[FAIL] Bing: {exc}")
        return None

    rows = [
        {
            "query": e.get("Query", ""),
            "clicks": e.get("Clicks", 0),
            "impressions": e.get("Impressions", 0),
            "position": e.get("AvgClickPosition", 0),
        }
        for e in payload.get("d", []) or []
    ]
    print(f"[ OK ] Bing: {len(rows)} ranking queries")
    return {"rows": rows}


def match_tracked(rows, terms):
    """Split engine rows into tracked terms vs. unexpected discoveries."""
    by_query = {r["query"].lower(): r for r in rows}
    tracked, missing = [], []
    for term in terms:
        hit = by_query.get(term.lower())
        (tracked if hit else missing).append(hit or {"query": term, "position": None})
    tracked_set = {t.lower() for t in terms}
    discovered = [r for r in rows if r["query"].lower() not in tracked_set]
    return tracked, missing, discovered


def write_report(results, terms):
    google = results.get("google")
    rows = google["rows"] if google else []
    tracked, missing, discovered = match_tracked(rows, terms) if google else ([], [], [])

    lines = [
        "# Search Visibility Report",
        "",
        f"Generated: {results['generated_at']}",
        f"Source: official webmaster APIs (no SERP scraping)",
        "",
    ]

    if google:
        ranking = sorted([r for r in tracked if r.get("position")], key=lambda r: r["position"])
        total_clicks = sum(r["clicks"] for r in rows)
        total_impr = sum(r["impressions"] for r in rows)
        lines += [
            "## Google Search Console",
            "",
            f"- Window: {google['start']} to {google['end']}",
            f"- Ranking queries: **{len(rows)}**",
            f"- Total clicks: **{total_clicks}** / impressions: **{total_impr}**",
            f"- Tracked terms ranking: **{len(ranking)}** of {len(terms)}",
            "",
        ]
        if ranking:
            lines += [
                "### Tracked terms currently ranking",
                "",
                "| Query | Position | Impressions | Clicks | CTR % |",
                "|---|---|---|---|---|",
            ]
            lines += [
                f"| {r['query']} | {r['position']} | {r['impressions']} | {r['clicks']} | {r['ctr']} |"
                for r in ranking[:50]
            ]
            lines.append("")
        if discovered:
            top = sorted(discovered, key=lambda r: -r["impressions"])[:25]
            lines += [
                "### Untracked queries you rank for (consider adding)",
                "",
                "| Query | Position | Impressions |",
                "|---|---|---|",
            ]
            lines += [f"| {r['query']} | {r['position']} | {r['impressions']} |" for r in top]
            lines.append("")
        lines += [f"- Tracked terms with no impressions yet: **{len(missing)}**", ""]
    else:
        lines += ["## Google Search Console", "", "_No data - credentials unavailable._", ""]

    bing = results.get("bing")
    if bing:
        rows_b = bing["rows"]
        clicks_b = sum(r.get("clicks", 0) for r in rows_b)
        impr_b = sum(r.get("impressions", 0) for r in rows_b)
        lines += [
            "## Bing Webmaster Tools",
            "",
            "_Bing's index also serves DuckDuckGo, Yahoo and Ecosia web results,_",
            "_so these figures effectively cover those engines as well._",
            "",
            f"- Ranking queries: **{len(rows_b)}**",
            f"- Total clicks: **{clicks_b}** / impressions: **{impr_b}**",
            "",
        ]
        if rows_b:
            top_b = sorted(rows_b, key=lambda r: -r.get("impressions", 0))[:25]
            lines += ["| Query | Impressions | Clicks |", "|---|---|---|"]
            lines += [
                f"| {r['query']} | {r.get('impressions', 0)} | {r.get('clicks', 0)} |"
                for r in top_b
            ]
            lines.append("")
    else:
        lines += ["## Bing Webmaster Tools", "", "_No data - API key not configured._", ""]

    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"[ OK ] Report written to {os.path.basename(OUT_MD)}")


def main():
    parser = argparse.ArgumentParser(description="Track search visibility via official webmaster APIs.")
    parser.add_argument("--days", type=int, default=28, help="lookback window in days (default 28)")
    parser.add_argument("--check-auth", action="store_true", help="verify credentials and exit")
    args = parser.parse_args()

    load_env_file()
    print("=== Search visibility tracker ===")
    print(f"Property: {SITE_URL}\n")

    terms = load_tracked_terms()
    print(f"[ OK ] Tracking {len(terms)} keywords and queries")

    service = gsc_service()
    if args.check_auth:
        bing_key = os.environ.get("BING_WEBMASTER_API_KEY") or os.environ.get("BING_API_KEY")
        print(f"\nGoogle credentials: {'present' if service else 'MISSING'}")
        print(f"Bing API key      : {'present' if bing_key else 'MISSING'}")
        return 0 if service else 1

    results = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "property": SITE_URL,
        "tracked_terms": len(terms),
        "google": fetch_google(service, args.days) if service else None,
        "bing": fetch_bing(args.days),
    }

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    print(f"[ OK ] Raw data written to {os.path.basename(OUT_JSON)}")

    write_report(results, terms)
    return 0 if (results["google"] or results["bing"]) else 1


if __name__ == "__main__":
    sys.exit(main())
