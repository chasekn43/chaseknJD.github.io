"""
Automated Continuous Multi-Engine Search Runner (robust fetch + parsing)
"""

import os
import sys
import time
import json
import random
import urllib.request
import urllib.parse
import re
from html import unescape
from datetime import datetime

# Enforce UTF-8 encoding
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Safety defaults (can be overridden by .search_safety/config.json)
MAX_CONCURRENCY = 3
MAX_BROWSERS = 1
MAX_RUNTIME = 30 * 60
MAX_QUERIES = 200
REQUEST_TIMEOUT = 10
NO_BROWSER = True
HEADLESS = True
MAX_RETRIES = 3
BACKOFF_BASE = 1.5

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, ".search_safety", "config.json")
if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as cf:
            cfg = json.load(cf)
        MAX_CONCURRENCY = int(cfg.get("max_concurrency", MAX_CONCURRENCY))
        MAX_BROWSERS = int(cfg.get("max_browsers", MAX_BROWSERS))
        MAX_RUNTIME = int(cfg.get("max_runtime", MAX_RUNTIME))
        MAX_QUERIES = int(cfg.get("max_queries", MAX_QUERIES))
        REQUEST_TIMEOUT = float(cfg.get("request_timeout", REQUEST_TIMEOUT))
        NO_BROWSER = bool(cfg.get("no_browser", NO_BROWSER))
        HEADLESS = bool(cfg.get("headless", HEADLESS))
    except Exception as e:
        print(f"Failed to load safety config: {e}")

LOG_DIR = os.path.join(script_dir, "logs")
RAW_DIR = os.path.join(LOG_DIR, "raw_html")
os.makedirs(RAW_DIR, exist_ok=True)

NAMES = ["Chase Kinslow", "Charles W. Kinslow IV"]
REPO_HANDLE = "chasekn43"
REPO_NAME = "regulatory-archive-2026"

KEYWORD_TOPICS = [
    "Fintech BNPL merchant dispute",
    "CFPB Administrative Procedures Act",
    "Customer service refund delays BNPL",
    "Point of sale lines of credit dispute",
    "Buy Now Pay Later Regulation Z billing error",
]

MODIFIERS = ["public record", "case study", "dispute documents", "evidence vault"]

TARGET_INDICATORS = ["chasekn43", "regulatory-archive-2026", "kinslow"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
]

# helper logging

def log_message(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(os.path.join(LOG_DIR, "runner.log"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

# network fetch with retries, backoff, and raw HTML saving

def fetch_url(url, engine_name, query_slug):
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    attempt = 0
    while attempt < MAX_RETRIES:
        attempt += 1
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                # save raw html for debugging
                safe_slug = re.sub(r'[^a-z0-9_-]', '_', query_slug.lower())[:64]
                filename = f"{engine_name}_{safe_slug}_{int(time.time())}_{attempt}.html"
                path = os.path.join(RAW_DIR, filename)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(html)
                return html
        except urllib.error.HTTPError as e:
            log_message(f"HTTPError from {engine_name} for {url}: {e.code} {e.reason}")
            # on 429 or 503 treat as rate-limit and back off longer
            if e.code in (429, 503):
                sleep_t = BACKOFF_BASE ** attempt
                log_message(f"Rate limit-like response, backing off {sleep_t}s")
                time.sleep(sleep_t)
                continue
            else:
                # other HTTP errors probably mean no results or blocking
                return None
        except Exception as ex:
            log_message(f"Fetch error ({engine_name}) attempt {attempt} for {url}: {ex}")
            time.sleep(BACKOFF_BASE ** attempt)
            continue
    return None

# robust parsing: try multiple engine-specific patterns, then fallback to generic href extraction

def parse_results_from_html(html, engine):
    results = []
    if not html:
        return results
    try:
        if engine == 'DuckDuckGo':
            matches = re.findall(r'<a[^>]+class="result__a"[^>]*href="(http[^\"]+)"[^>]*>(.*?)</a>', html, re.I|re.S)
            if matches:
                for href, title in matches[:15]:
                    results.append({'engine': 'DuckDuckGo', 'title': unescape(re.sub('<.*?>','', title)).strip(), 'url': href})
                return results
        if engine == 'Bing':
            matches = re.findall(r'<li class="b_algo".*?<h2>\s*<a href="(http[^\"]+)"[^>]*>(.*?)</a>', html, re.I|re.S)
            if matches:
                for href, title in matches[:15]:
                    results.append({'engine': 'Bing', 'title': unescape(re.sub('<.*?>','', title)).strip(), 'url': href})
                return results
        if engine == 'Google':
            raw_links = re.findall(r'href="/url\?q=(http[s]?://[^&]+)&', html)
            titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.I|re.S)
            for i, l in enumerate(raw_links[:15]):
                t = unescape(re.sub('<.*?>','', titles[i])).strip() if i < len(titles) else ''
                results.append({'engine': 'Google', 'title': t, 'url': urllib.parse.unquote(l)})
            if results:
                return results
        if engine == 'Yahoo':
            matches = re.findall(r'<h3[^>]*>\s*<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.I|re.S)
            if matches:
                for href, title in matches[:15]:
                    results.append({'engine': 'Yahoo', 'title': unescape(re.sub('<.*?>','', title)).strip(), 'url': href})
                return results
        # Generic fallback: find any http(s) links
        hrefs = re.findall(r'href=["\'](http[s]?:\/\/[^"\'>]+)["\']', html, re.I)
        # try to find surrounding anchor text if possible
        for href in hrefs[:30]:
            # naive title extract: find the anchor tag with this href
            m = re.search(r'<a[^>]+href=["\']' + re.escape(href) + r'["\'][^>]*>(.*?)</a>', html, re.I|re.S)
            title = unescape(re.sub('<.*?>','', m.group(1))).strip() if m else ''
            results.append({'engine': engine, 'title': title, 'url': href})
        return results
    except Exception as e:
        log_message(f"Parsing error for engine {engine}: {e}")
        return results

# per-engine search using fetch + parse

def search_generic(engine_name, url_template, query):
    encoded = urllib.parse.quote(query)
    url = url_template.format(encoded)
    html = fetch_url(url, engine_name, query)
    if html is None:
        log_message(f"No HTML returned by {engine_name} for query: {query}")
        return []
    return parse_results_from_html(html, engine_name)

# wrappers for the four engines

def search_duckduckgo(query):
    return search_generic('DuckDuckGo', "https://html.duckduckgo.com/html/?q={}", query)

def search_bing(query):
    return search_generic('Bing', "https://www.bing.com/search?q={}", query)

def search_google(query):
    return search_generic('Google', "https://www.google.com/search?q={}&num=10", query)

def search_yahoo(query):
    return search_generic('Yahoo', "https://search.yahoo.com/search?p={}&nojs=1", query)

# main run logic (keeps prior structure but uses new fetch/parse)

def run_continuous_automated_search(passes=3, queries_per_pass=4):
    print("=" * 70)
    print(" AUTOMATED GITHUB REPOSITORY SEARCH ENGINE AUDITOR")
    print(f" Target Person Variants: {', '.join(NAMES)}")
    print(f" Target Repository: {REPO_HANDLE}/{REPO_NAME}")
    print(f" Search Engines: Yahoo, Bing, Google, DuckDuckGo")
    print(f" Total Continuous Passes: {passes}")
    print("=" * 70 + "\n")

    session_history = []
    total_matches = 0
    total_queries = 0
    start_time = time.time()

    for p in range(1, passes + 1):
        pass_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- PASS #{p}/{passes} [{pass_time}] ---")

        selected_topics = random.sample(KEYWORD_TOPICS, min(queries_per_pass, len(KEYWORD_TOPICS)))
        pass_queries = []
        for topic in selected_topics:
            name_val = random.choice(NAMES)
            mod = random.choice(MODIFIERS)
            q_str = f"{name_val} {topic} {mod}".strip()
            pass_queries.append(q_str)

        pass_data = {"pass": p, "timestamp": pass_time, "queries": []}

        for q_idx, query in enumerate(pass_queries, 1):
            if total_queries >= MAX_QUERIES:
                print(f"[SAFETY] Max queries reached ({total_queries} >= {MAX_QUERIES}). Stopping.")
                break
            if time.time() - start_time > MAX_RUNTIME:
                print(f"[SAFETY] Max runtime exceeded ({time.time() - start_time:.1f}s > {MAX_RUNTIME}s). Stopping.")
                break

            print(f"\n[{p}.{q_idx}] Executing Multi-Engine Search for: '{query}'")
            query_record = {"query": query, "engines": {}, "matches": []}

            ddg_res = search_duckduckgo(query)
            bing_res = search_bing(query)
            yahoo_res = search_yahoo(query)
            google_res = search_google(query)

            total_queries += 1

            query_record["engines"]["DuckDuckGo"] = ddg_res
            query_record["engines"]["Bing"] = bing_res
            query_record["engines"]["Yahoo"] = yahoo_res
            query_record["engines"]["Google"] = google_res

            all_results = ddg_res + bing_res + yahoo_res + google_res
            matched_items = []
            for item in all_results:
                url = item.get("url", "")
                title = item.get("title", "")
                combined = (url + " " + title).lower()
                for ind in TARGET_INDICATORS:
                    if ind.lower() in combined:
                        matched_items.append({"engine": item.get("engine"), "indicator": ind, "url": url, "title": title})
                        break

            query_record["matches"] = matched_items
            if matched_items:
                total_matches += len(matched_items)
                print(f"   [MATCH FOUND] {len(matched_items)} result(s) indexed for target repository:")
                for m in matched_items:
                    print(f"      • [{m['engine']}] ({m['indicator']}) {m['url']}")
            else:
                print(f"   [OK] DDG({len(ddg_res)}), Bing({len(bing_res)}), Yahoo({len(yahoo_res)}), Google({len(google_res)}) processed.")

            pass_data["queries"].append(query_record)
            time.sleep(1)

        session_history.append(pass_data)
        print(f"\nPass #{p} complete. Resting before Pass #{p+1}...\n")
        time.sleep(2)

    log_path = os.path.join(os.path.dirname(__file__), "continuous_search_report.json")
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(session_history, f, indent=2)
    except Exception as e:
        log_message(f"Failed saving report: {e}")

    print("=" * 70)
    print(f" SEARCH AUDIT COMPLETE: {passes} passes, {total_queries} total search variations.")
    print(f" Total Repository Matches Logged: {total_matches}")
    print(f" Report saved to: {os.path.abspath(log_path)}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    passes_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_continuous_automated_search(passes=passes_arg, queries_per_pass=4)
