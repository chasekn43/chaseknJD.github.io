import urllib.parse
import urllib.request
import re
import json
import random
import sys
from html import unescape
from datetime import datetime

# Ensure stdout handles utf-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

queries = [
    "Chase Kinslow regulatory-archive-2026 github",
    "Chase Kinslow Affirm CFPB complaint 260717-35668593",
    "Chase Kinslow Monroe Police Department report 26-29572",
    "Chase Kinslow Kinslow v Affirm public evidentiary record",
    "Chase Kinslow Morgan Lewis Bockius lawsuit Affirm"
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

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8', errors='ignore')
            raw_matches = re.findall(r'<a class="result__url" href="(.*?)">(.*?)</a>', html)
            snippets = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
            for i, (l_href, l_title) in enumerate(raw_matches):
                snip = clean_text(snippets[i]) if i < len(snippets) else ""
                results.append({"title": clean_text(l_title), "url": decode_redirect_url(clean_text(l_href)), "snippet": snip})
    except Exception as e:
        results.append({"error": str(e)})
    return results

def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=10"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8', errors='ignore')
            raw_links = re.findall(r'href="/url\?q=(http[s]?://[^&]+)&', html)
            titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html)
            for i, l in enumerate(raw_links):
                if "google.com" not in l and "youtube.com" not in l:
                    t = clean_text(titles[i]) if i < len(titles) else "Google Result"
                    results.append({"title": t, "url": urllib.parse.unquote(l), "snippet": ""})
    except Exception as e:
        results.append({"error": str(e)})
    return results

def search_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<h2><a href="(http[s]?://[^"]+)"[^>]*>(.*?)</a></h2>', html)
            for href, title in matches:
                results.append({"title": clean_text(title), "url": decode_redirect_url(href), "snippet": ""})
    except Exception as e:
        results.append({"error": str(e)})
    return results

def search_yahoo(query):
    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}
    req = urllib.request.Request(url, headers=headers)
    results = []
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<h3 class="title"[^>]*><a href="(https?://r\.search\.yahoo\.com/[^"]+)"[^>]*>(.*?)</a></h3>', html)
            if not matches:
                matches = re.findall(r'href="(https?://r\.search\.yahoo\.com/[^"]+)"[^>]*>(.*?)</a>', html)
            for href, title in matches:
                results.append({"title": clean_text(title), "url": decode_redirect_url(href), "snippet": ""})
    except Exception as e:
        results.append({"error": str(e)})
    return results

all_results = {}
for q in queries:
    print(f"Running multi-engine verification for: {q}")
    all_results[q] = {
        "DuckDuckGo": search_duckduckgo(q),
        "Google": search_google(q),
        "Bing": search_bing(q),
        "Yahoo": search_yahoo(q)
    }

with open("query_verification_run.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print("Search query execution finished successfully.")
