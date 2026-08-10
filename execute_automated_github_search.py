"""
Automated Continuous Multi-Engine Search Runner for Chase Kinslow & GitHub Repository
Queries Yahoo, Bing, Google, DuckDuckGo across continuous passes varying keywords while including 'Chase Kinslow'.
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
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

NAME = "Chase Kinslow"
REPO_HANDLE = "chasekn43"
REPO_NAME = "regulatory-archive-2026"

KEYWORD_TOPICS = [
    "regulatory-archive-2026 github",
    "chasekn43 github regulatory archive",
    "regulatory-archive.kinslow.co",
    "kinslow.co public record",
    "CFPB complaint 260717-35668593",
    "Monroe Police Department incident report 26-29572",
    "Kinslow v Affirm public evidentiary record",
    "Morgan Lewis Bockius lawsuit Affirm",
    "Andy Y. Chen Affirm cease and desist",
    "Perfume Empire tracking 1LSDCR10011QF38",
    "Louisiana AG Liz Murrill dispute submission",
    "California AG Rob Bonta dispute notice",
    "FTC fraud web affidavit Affirm",
    "Shop app unauthorized intrusion Affirm",
    "Affirm in-app payment lock BillPay workaround",
    "Scott Williams Affirm Vice President Client Success",
    "CFPB complaint rebuttal Affirm false response"
]

MODIFIERS = [
    "github",
    "public record",
    "evidence vault",
    "case study",
    "dispute documents",
    "legal record"
]

TARGET_INDICATORS = [
    "chasekn43",
    "regulatory-archive-2026",
    "regulatory-archive.kinslow.co",
    "kinslow.co",
    "github.com/chasekn43",
    "260717-35668593",
    "26-29572"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

def clean_text(html_str):
    if not html_str:
        return ""
    cleanr = re.compile(r'<.*?>')
    cleantext = re.sub(cleanr, '', html_str)
    return unescape(cleantext).strip()

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<a class="result__url" href="(.*?)">(.*?)</a>', html)
            for href, title in matches[:10]:
                results.append({"engine": "DuckDuckGo", "title": clean_text(title), "url": clean_text(href)})
    except Exception as e:
        results.append({"engine": "DuckDuckGo", "error": str(e)})
    return results

def search_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<h2><a href="(http[s]?://[^"]+)"[^>]*>(.*?)</a></h2>', html)
            for href, title in matches[:10]:
                results.append({"engine": "Bing", "title": clean_text(title), "url": href})
    except Exception as e:
        results.append({"engine": "Bing", "error": str(e)})
    return results

def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=10"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8', errors='ignore')
            raw_links = re.findall(r'href="/url\?q=(http[s]?://[^&]+)&amp;', html)
            titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html)
            for i, l in enumerate(raw_links[:10]):
                if "google.com" not in l and "youtube.com" not in l:
                    t = clean_text(titles[i]) if i < len(titles) else "Google Result"
                    results.append({"engine": "Google", "title": t, "url": urllib.parse.unquote(l)})
    except Exception as e:
        results.append({"engine": "Google", "error": str(e)})
    return results

def search_yahoo(query):
    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}&nojs=1"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<h3 class="title"[^>]*><a href="(https?://[^"]+)"[^>]*>(.*?)</a></h3>', html)
            for href, title in matches[:10]:
                results.append({"engine": "Yahoo", "title": clean_text(title), "url": href})
    except Exception as e:
        results.append({"engine": "Yahoo", "error": str(e)})
    return results

def run_continuous_automated_search(passes=5, queries_per_pass=4):
    print("=" * 70)
    print(" AUTOMATED GITHUB REPOSITORY SEARCH ENGINE AUDITOR")
    print(f" Target Person: {NAME}")
    print(f" Target Repository: {REPO_HANDLE}/{REPO_NAME}")
    print(f" Search Engines: Yahoo, Bing, Google, DuckDuckGo")
    print(f" Total Continuous Passes: {passes}")
    print("=" * 70 + "\n")
    
    session_history = []
    total_matches = 0
    
    for p in range(1, passes + 1):
        pass_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- PASS #{p}/{passes} [{pass_time}] ---")
        
        # Pick varied keyword combinations always starting with NAME
        selected_topics = random.sample(KEYWORD_TOPICS, min(queries_per_pass, len(KEYWORD_TOPICS)))
        pass_queries = []
        
        for topic in selected_topics:
            mod = random.choice(MODIFIERS)
            q_str = f"{NAME} {topic} {mod}".strip()
            pass_queries.append(q_str)
            
        pass_data = {"pass": p, "timestamp": pass_time, "queries": []}
        
        for q_idx, query in enumerate(pass_queries, 1):
            print(f"\n[{p}.{q_idx}] Executing Multi-Engine Search for: '{query}'")
            query_record = {"query": query, "engines": {}, "matches": []}
            
            # Execute queries across all 4 search engines
            ddg_res = search_duckduckgo(query)
            bing_res = search_bing(query)
            yahoo_res = search_yahoo(query)
            google_res = search_google(query)
            
            query_record["engines"]["DuckDuckGo"] = ddg_res
            query_record["engines"]["Bing"] = bing_res
            query_record["engines"]["Yahoo"] = yahoo_res
            query_record["engines"]["Google"] = google_res
            
            # Audit for repository indicators
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
                print(f"   [🎯 MATCH FOUND] {len(matched_items)} result(s) indexed for target repository:")
                for m in matched_items:
                    print(f"      • [{m['engine']}] ({m['indicator']}) {m['url']}")
            else:
                print(f"   [✓ OK] DDG({len(ddg_res)}), Bing({len(bing_res)}), Yahoo({len(yahoo_res)}), Google({len(google_res)}) processed successfully.")
                
            pass_data["queries"].append(query_record)
            time.sleep(1)
            
        session_history.append(pass_data)
        print(f"\nPass #{p} complete. Resting before Pass #{p+1}...\n")
        time.sleep(2)
        
    log_path = os.path.join(os.path.dirname(__file__), "continuous_search_report.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(session_history, f, indent=2)
        
    print("=" * 70)
    print(f" SEARCH AUDIT COMPLETE: {passes} passes, {passes * queries_per_pass} total search variations.")
    print(f" Total Repository Matches Logged: {total_matches}")
    print(f" Report saved to: {os.path.abspath(log_path)}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    passes_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_continuous_automated_search(passes=passes_arg, queries_per_pass=4)
