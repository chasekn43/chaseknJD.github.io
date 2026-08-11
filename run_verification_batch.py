import urllib.parse
import urllib.request
import re
import json
import random
import sys
import time
from html import unescape
from datetime import datetime

# Ensure stdout handles utf-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

queries = [
    "Chase Kinslow Fintech BNPL merchant dispute",
    "Charles W. Kinslow IV CFPB Administrative Procedures Act",
    "Chase Kinslow customer service refund delays",
    "Charles W. Kinslow IV point of sale lines of credit",
    "Chase Kinslow Buy Now Pay Later loan dispute",
    "Charles W. Kinslow IV Regulation Z billing error",
    "Chase Kinslow Kinslow v Affirm",
    "Charles W. Kinslow IV Kinslow v Affirm"
]

TARGET_INDICATORS = [
    "chasekn43",
    "regulatory-archive-2026",
    "regulatory-archive.kinslow.co",
    "kinslow.co",
    "kinslow"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
]

def clean_text(html_str):
    cleanr = re.compile(r'<.*?>')
    cleantext = re.sub(cleanr, '', html_str)
    return unescape(cleantext).strip()

def decode_redirect_url(url):
    try:
        if "uddg=" in url:
            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            if "uddg" in parsed:
                return parsed["uddg"][0]
        if "r.search.yahoo.com" in url and "/RU=" in url:
            match = re.search(r'/RU=([^/]+)/', url)
            if match:
                return urllib.parse.unquote(match.group(1))
    except Exception:
        pass
    return url

def fetch_with_metrics(url, extractor):
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    start_time = time.time()
    results = []
    error = None
    status_code = 200
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            status_code = response.getcode()
            html = response.read().decode('utf-8', errors='ignore')
            results = extractor(html)
    except Exception as e:
        error = str(e)
        status_code = getattr(e, 'code', 500) if hasattr(e, 'code') else 500

    elapsed_ms = round((time.time() - start_time) * 1000, 2)
    
    # Check target hits
    hits = 0
    hit_details = []
    for r in results:
        combined = f"{r.get('title', '')} {r.get('url', '')} {r.get('snippet', '')}".lower()
        matched = [ind for ind in TARGET_INDICATORS if ind in combined]
        if matched:
            hits += 1
            hit_details.append({"title": r.get("title"), "url": r.get("url"), "matched_indicators": matched})

    return {
        "response_time_ms": elapsed_ms,
        "status_code": status_code,
        "results_count": len(results),
        "target_hits": hits,
        "hit_details": hit_details,
        "error": error,
        "raw_results": results
    }

def extract_duckduckgo(html):
    results = []
    raw_matches = re.findall(r'<a class="result__url" href="(.*?)">(.*?)</a>', html)
    snippets = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
    for i, (l_href, l_title) in enumerate(raw_matches):
        snip = clean_text(snippets[i]) if i < len(snippets) else ""
        results.append({"title": clean_text(l_title), "url": decode_redirect_url(clean_text(l_href)), "snippet": snip})
    return results

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    return fetch_with_metrics(url, extract_duckduckgo)

def extract_google(html):
    results = []
    raw_links = re.findall(r'href="/url\?q=(http[s]?://[^&]+)&', html)
    titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html)
    for i, l in enumerate(raw_links):
        if "google.com" not in l and "youtube.com" not in l:
            t = clean_text(titles[i]) if i < len(titles) else "Google Result"
            results.append({"title": t, "url": urllib.parse.unquote(l), "snippet": ""})
    return results

def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=10"
    return fetch_with_metrics(url, extract_google)

def extract_bing(html):
    results = []
    matches = re.findall(r'h2><a href="(http[s]?://[^"]+)"[^>]*>(.*?)</a></h2>', html)
    for href, title in matches:
        results.append({"title": clean_text(title), "url": decode_redirect_url(href), "snippet": ""})
    return results

def search_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    return fetch_with_metrics(url, extract_bing)

def extract_yahoo(html):
    results = []
    matches = re.findall(r'<h3 class="title"[^>]*><a href="(https?://r\.search\.yahoo\.com/[^"]+)"[^>]*>(.*?)</a></h3>', html)
    if not matches:
        matches = re.findall(r'href="(https?://r\.search\.yahoo\.com/[^"]+)"[^>]*>(.*?)</a>', html)
    for href, title in matches:
        results.append({"title": clean_text(title), "url": decode_redirect_url(href), "snippet": ""})
    return results

def search_yahoo(query):
    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}"
    return fetch_with_metrics(url, extract_yahoo)

all_results = {}
engine_stats = {
    "Google": {"queries": 0, "total_time_ms": 0, "total_results": 0, "total_hits": 0, "errors": 0},
    "Bing": {"queries": 0, "total_time_ms": 0, "total_results": 0, "total_hits": 0, "errors": 0},
    "Yahoo": {"queries": 0, "total_time_ms": 0, "total_results": 0, "total_hits": 0, "errors": 0},
    "DuckDuckGo": {"queries": 0, "total_time_ms": 0, "total_results": 0, "total_hits": 0, "errors": 0}
}

print(f"Starting Multi-Engine Keyword Verification Sweep at {datetime.now().isoformat()}...")
for q in queries:
    print(f"Running sweep for query: '{q}'")
    q_res = {
        "Google": search_google(q),
        "Bing": search_bing(q),
        "Yahoo": search_yahoo(q),
        "DuckDuckGo": search_duckduckgo(q)
    }
    all_results[q] = q_res

    for engine, res in q_res.items():
        engine_stats[engine]["queries"] += 1
        engine_stats[engine]["total_time_ms"] += res["response_time_ms"]
        engine_stats[engine]["total_results"] += res["results_count"]
        engine_stats[engine]["total_hits"] += res["target_hits"]
        if res["error"]:
            engine_stats[engine]["errors"] += 1

output_data = {
    "timestamp": datetime.now().isoformat(),
    "queries_executed": len(queries),
    "engine_summary": engine_stats,
    "detailed_results": all_results
}

with open("query_verification_run.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("\n--- SWEEP SUMMARY METRICS ---")
for engine, stats in engine_stats.items():
    avg_time = round(stats["total_time_ms"] / stats["queries"], 2) if stats["queries"] > 0 else 0
    hit_rate = round((stats["total_hits"] / stats["queries"]) * 100, 2) if stats["queries"] > 0 else 0
    print(f"Engine: {engine:<12} | Avg Latency: {avg_time:>7.1f}ms | Total Results: {stats['total_results']:>3} | Target Hits: {stats['total_hits']:>3} | Hit Rate per Query: {hit_rate:>5.1f}% | Errors: {stats['errors']}")

print("\nSearch verification sweep complete. Saved to query_verification_run.json.")

