import urllib.request
import urllib.parse
import random
import time
import re
import os
import sys
import json
from html import unescape
from datetime import datetime

# Enforce UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "search_continuous.log")
json_report_path = os.path.join(script_dir, "continuous_search_report.json")

def log_message(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {msg}"
    print(log_line, flush=True)
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"Failed writing to log: {e}")

names = [
    "Chase Kinslow",
    "Charles W. Kinslow IV",
    "Charles W. Kinslow",
    "Charles Kinslow IV",
    "Charles Kinslow"
]

keywords = [
    "regulatory-archive-2026",
    "chasekn43 github",
    "regulatory-archive.kinslow.co",
    "kinslow.co public evidence",
    "CFPB complaint 260717-35668593",
    "Monroe Police Department report 26-29572",
    "Affirm dispute archive",
    "Kinslow v Affirm public evidentiary record",
    "Morgan Lewis Bockius lawsuit Affirm",
    "Andy Chen Affirm cease and desist",
    "Perfume Empire tracking 1LSDCR10011QF38",
    "California AG Rob Bonta dispute notice",
    "Louisiana AG Liz Murrill dispute submission",
    "FTC fraud web affidavit Affirm",
    "Shop app unauthorized intrusion Affirm",
    "Affirm in-app payment lock BillPay workaround",
    "Scott Williams Affirm Vice President Client Success"
]

target_indicators = [
    "chasekn43",
    "regulatory-archive-2026",
    "regulatory-archive.kinslow.co",
    "kinslow.co",
    "github.com/chasekn43",
    "260717-35668593",
    "26-29572"
]

engines = [
    {"name": "Google", "url": "https://www.google.com/search?q={}&num=10"},
    {"name": "Bing", "url": "https://www.bing.com/search?q={}"},
    {"name": "Yahoo", "url": "https://search.yahoo.com/search?p={}&nojs=1"},
    {"name": "DuckDuckGo", "url": "https://html.duckduckgo.com/html/?q={}"}
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

def generate_random_ip():
    return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

def get_proxy_list():
    log_message("Fetching public HTTP proxy list...")
    proxy_urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http"
    ]
    proxies = []
    for url in proxy_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(user_agents)})
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('utf-8', errors='ignore')
                found = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}\b', content)
                proxies.extend(found)
        except Exception:
            pass
            
    proxies = list(set(proxies))
    log_message(f"Retrieved {len(proxies)} unique public proxies.")
    return proxies

def clean_text(html_str):
    if not html_str:
        return ""
    cleanr = re.compile(r'<.*?>')
    cleantext = re.sub(cleanr, '', html_str)
    return unescape(cleantext).strip()

def generate_query():
    name = random.choice(names)
    kw = random.choice(keywords)
    mode = random.choice(["combo", "site", "exact", "keyword"])
    
    if mode == "combo":
        return f"{name} {kw}"
    elif mode == "site":
        return f"site:chasekn43.github.io/regulatory-archive-2026/ {name}"
    elif mode == "exact":
        return f'"{name}" "{kw}"'
    else:
        return f"{name} {kw} github"

def check_matches(html):
    matches = []
    html_lower = html.lower()
    for ind in target_indicators:
        if ind.lower() in html_lower:
            matches.append(ind)
    return matches

def execute_search_query(engine, query, proxy=None):
    encoded_query = urllib.parse.quote_plus(query)
    search_url = engine["url"].format(encoded_query)
    
    fake_ip = generate_random_ip()
    headers = {
        "User-Agent": random.choice(user_agents),
        "X-Forwarded-For": fake_ip,
        "Client-IP": fake_ip,
        "Via": fake_ip,
        "X-Real-IP": fake_ip,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    start_time = time.time()
    try:
        req = urllib.request.Request(search_url, headers=headers)
        if proxy:
            proxy_support = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_support)
            with opener.open(req, timeout=8) as response:
                html = response.read().decode('utf-8', errors='ignore')
        else:
            with urllib.request.urlopen(req, timeout=8) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
        elapsed = time.time() - start_time
        matches = check_matches(html)
        return {
            "success": True,
            "engine": engine["name"],
            "query": query,
            "fake_ip": fake_ip,
            "proxy": proxy or "Direct (IP Spoofed)",
            "length": len(html),
            "elapsed": round(elapsed, 2),
            "matches": matches
        }
    except Exception as e:
        return {
            "success": False,
            "engine": engine["name"],
            "query": query,
            "fake_ip": fake_ip,
            "proxy": proxy or "Direct (IP Spoofed)",
            "error": str(e)
        }

def run_search_passes(passes=3, delay_range=(2, 5)):
    log_message("=" * 70)
    log_message(f"STARTING AUTOMATED MULTI-ENGINE CONTINUOUS SEARCH (Passes: {passes})")
    log_message(f"Engines: Google, Bing, Yahoo, DuckDuckGo")
    log_message("=" * 70)
    
    proxies = get_proxy_list()
    history = []
    total_hits = 0

    for pass_num in range(1, passes + 1):
        log_message(f"\n--- PASS #{pass_num}/{passes} @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        pass_data = {"pass": pass_num, "queries": []}
        
        # Pick 4 distinct queries per pass
        selected_queries = [generate_query() for _ in range(4)]
        
        for q_idx, query in enumerate(selected_queries, 1):
            log_message(f"\n[{pass_num}.{q_idx}] Executing search for: '{query}'")
            query_record = {"query": query, "results": []}
            
            for engine in engines:
                proxy = random.choice(proxies) if proxies else None
                res = execute_search_query(engine, query, proxy=proxy)
                
                # Fallback to direct spoofed IP if proxy failed
                if not res["success"] and proxy:
                    res = execute_search_query(engine, query, proxy=None)
                    
                query_record["results"].append(res)
                
                if res["success"]:
                    matches_str = f" Matches: {res['matches']}" if res['matches'] else " No direct hits"
                    log_message(f"   ✓ [{engine['name']}] (IP: {res['fake_ip']}) - {res['length']} bytes in {res['elapsed']}s.{matches_str}")
                    if res['matches']:
                        total_hits += len(res['matches'])
                else:
                    log_message(f"   ✗ [{engine['name']}] Error: {res.get('error')}")
                    
                time.sleep(random.uniform(0.5, 1.5))
                
            pass_data["queries"].append(query_record)
            
        history.append(pass_data)
        
        # Save snapshot
        with open(json_report_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
            
        if pass_num < passes:
            sleep_time = random.randint(*delay_range)
            log_message(f"Pass #{pass_num} complete. Resting {sleep_time}s before next pass...")
            time.sleep(sleep_time)
            
    log_message("\n" + "=" * 70)
    log_message(f"SEARCH AUTOMATION COMPLETE: Executed {passes} passes across 4 search engines.")
    log_message(f"Total Target Indicator Matches Found: {total_hits}")
    log_message(f"Report saved to: {json_report_path}")
    log_message("=" * 70 + "\n")
    return history

if __name__ == "__main__":
    passes_arg = 3
    if len(sys.argv) > 1:
        try:
            passes_arg = int(sys.argv[1])
        except ValueError:
            pass
    run_search_passes(passes=passes_arg)

