import urllib.request
import urllib.parse
import urllib.error
import random
import time
import re
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "search_continuous.log")

# Setup Logging
def log_message(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {msg}\n"
    print(log_line.strip())
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"Failed writing to log: {e}")

# Data sources for query generation (broad tangential regulatory & fintech keywords)
names = [
    "Charles W. Kinslow IV",
    "Charles W. Kinslow",
    "Charles Kinslow IV",
    "Charles Kinslow",
    "Chase Kinslow",
    "chasekn",
    "kinslow"
]

keywords = [
    "4q8isr1",
    "LinkedIn",
    "fintech",
    "BNPL",
    "merchant dispute",
    "CFPB",
    "Administrative Procedures Act",
    "customer service",
    "refund delays",
    "lines of credit",
    "point-of-sale financing",
    "APA challenge consumer finance",
    "credit line dispute regulation z",
    "CFPB complaint BNPL merchant",
    "regulation z",
    "consumer fraud protection bureau",
    "lockout",
    "credit",
    "frozen accounts",
    "regulatory",
    "security freeze",
    "credit lock",
    "frozen credit file",
    "FCRA dispute",
    "billing error notice",
    "unauthorized billing charge",
    "account lockout dispute",
    "suspended credit line",
    "merchant settlement dispute",
    "Fair Credit Reporting Act dispute",
    "Truth in Lending Act disclosure",
    "Regulation E error resolution",
    "adverse action notice credit denial",
    "CFPB complaint portal",
    "merchant chargeback clearing friction",
    "arbitrary account suspension fintech",
    "CFPB regulatory circular",
    "Dodd-Frank Title X UDAAP compliance",
    "Regulation Z 12 C.F.R. 1026",
    "merchant cancellation refund dispute",
    "holder in due course rule retail finance",
    "point-of-sale financing error resolution",
    "credit reporting disputes retail credit",
    "unsolicited marketing SMS compliance",
    "automated fraud rejection audit",
    "merchant refund clearing delays",
    "managing counsel cease and desist directive",
    "outside counsel representation ethics notice",
    "Rule 4.2 ethical notice consumer finance",
    "unsolicited team email outreach"
]

# Engine configuration with urls
engines = [
    {"name": "Google", "url": "https://www.google.com/search?q={}"},
    {"name": "Bing", "url": "https://www.bing.com/search?q={}"},
    {"name": "Yahoo", "url": "https://search.yahoo.com/search?p={}"},
    {"name": "DuckDuckGo", "url": "https://html.duckduckgo.com/html/?q={}"}
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
]

# Custom Redirect Handler to disable automatic redirect following.
class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect Blocked (Suspected CAPTCHA/ISP Hijack)", headers, fp)
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

# Thread-safe engine-specific verified pools
verified_pools = {
    "Google": set(),
    "Bing": set(),
    "Yahoo": set(),
    "DuckDuckGo": set()
}
verified_lock = threading.Lock()

# Cache variables for raw proxy list to avoid API rate-limiting
raw_proxies_cache = []
last_fetch_time = 0
cache_lock = threading.Lock()

def generate_random_ip():
    return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

def get_raw_proxies():
    global last_fetch_time, raw_proxies_cache
    now = time.time()
    
    with cache_lock:
        if now - last_fetch_time < 90 and raw_proxies_cache:
            log_message("[VALIDATOR] Using cached raw proxies (API cooldown active)...")
            return raw_proxies_cache

    proxy_urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=yes&anonymity=anonymous",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=yes&anonymity=elite",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
    ]
    raw_list = []
    for url in proxy_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(user_agents)})
            with urllib.request.urlopen(req, timeout=8) as response:
                content = response.read().decode('utf-8', errors='ignore')
                found = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}\b', content)
                raw_list.extend(found)
        except Exception as e:
            log_message(f"[API ERROR] Proxy fetch failed for {url}: {e}")
            
    with cache_lock:
        if raw_list:
            raw_proxies_cache = list(set(raw_list))
            last_fetch_time = now
        return raw_proxies_cache

def test_single_proxy(proxy):
    # Strict 1.5s timeout for validation checks
    timeout = 1.5
    
    # We test Bing, DuckDuckGo, Google, and Yahoo with active queries
    tests = [
        {"name": "Google", "url": "https://www.google.com/search?q=test"},
        {"name": "Bing", "url": "https://www.bing.com/search?q=test"},
        {"name": "Yahoo", "url": "https://search.yahoo.com/search?p=test"},
        {"name": "DuckDuckGo", "url": "https://html.duckduckgo.com/html/?q=test"}
    ]
    
    # Randomize test execution order to avoid sequential hotspotting
    random.shuffle(tests)
    
    for test in tests:
        name = test["name"]
        test_url = test["url"]
        try:
            proxy_support = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_support, NoRedirectHandler())
            req = urllib.request.Request(test_url, headers={'User-Agent': random.choice(user_agents)})
            with opener.open(req, timeout=timeout) as resp:
                if resp.status == 200:
                    with verified_lock:
                        verified_pools[name].add(proxy)
                    log_message(f"[VALIDATOR SUCCESS] Proxy {proxy} verified for {name}")
        except Exception:
            # Silent filter of noisy validator drops to keep stdout clean
            pass

def proxy_validator_thread():
    while True:
        with verified_lock:
            counts = {name: len(pool) for name, pool in verified_pools.items()}
            
        # Replenish if any engine pool is low
        if any(count < 15 for count in counts.values()):
            raw_proxies = get_raw_proxies()
            if raw_proxies:
                local_list = list(raw_proxies)
                random.shuffle(local_list)
                with ThreadPoolExecutor(max_workers=45) as executor:
                    executor.map(test_single_proxy, local_list[:150])
                
        time.sleep(10)

query_counter = 0
recent_queries = []

def generate_query():
    global query_counter, recent_queries
    query_counter += 1
    
    for _ in range(50):
        # Every query is branded: pair a name variation (Kinslow/Chase) with a keyword
        name = random.choice(names)
        
        linkedin_keywords = ["linkedin", "linkedin profile", "regulatory-archive-2026", "bnpl dispute", "kinslow bnpl"]
        kw = random.choice(keywords + linkedin_keywords)
        
        if random.random() < 0.5:
            query = f"{name} {kw}"
        else:
            query = f'"{name}" "{kw}"'
        
        # Avoid running similar queries consecutively
        words = set(query.lower().replace('"', '').split())
        is_duplicate = False
        for old_q in recent_queries:
            old_words = set(old_q.lower().replace('"', '').split())
            if len(words) > 0 and len(old_words) > 0:
                intersection = words.intersection(old_words)
                # If more than 70% word overlap, reject to maintain variety
                if len(intersection) / max(len(words), 1) > 0.7:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            recent_queries.append(query)
            if len(recent_queries) > 20:
                recent_queries.pop(0)
            return query
            
    # Fallback
    return f"{random.choice(names)} kinslow bnpl"

def main():
    log_message("Continuous search simulator initialized with SSL filtering, Redirect blocking, and zero sleep.")
    
    # Start the validator thread
    validator = threading.Thread(target=proxy_validator_thread, daemon=True)
    validator.start()
    
    log_message("Waiting for validator thread to verify active SSL proxies...")
    for _ in range(30):
        with verified_lock:
            # Wait until we have at least some verified proxies
            total_verified = sum(len(pool) for pool in verified_pools.values())
            if total_verified > 0:
                break
        time.sleep(1)
        
    while True:
        query = generate_query()
        
        # Bias engine weights: Bing 45%, DuckDuckGo 45%, Google 5%, Yahoo 5%
        engine = random.choices(
            engines, 
            weights=[5, 45, 5, 45], 
            k=1
        )[0]
        
        success = False
        max_attempts = 20
        
        for attempt in range(1, max_attempts + 1):
            with verified_lock:
                available_engines = [e for e in engines if len(verified_pools[e["name"]]) > 0]
                
            if not available_engines:
                log_message(f"[QUERY PAUSE] No verified proxies available for any engine. Waiting...")
                time.sleep(2)
                continue
                
            # If the selected engine's pool is empty, dynamically fall back to another verified engine
            active_engine = engine
            if active_engine["name"] not in [e["name"] for e in available_engines]:
                active_engine = random.choice(available_engines)
                
            with verified_lock:
                proxies_list = list(verified_pools[active_engine["name"]])
                
            proxy = random.choice(proxies_list)
            ua = random.choice(user_agents)
            
            encoded_query = urllib.parse.quote_plus(query)
            search_url = active_engine["url"].format(encoded_query)
            
            fake_ip = generate_random_ip()
            headers = {
                "User-Agent": ua,
                "X-Forwarded-For": fake_ip,
                "Client-IP": fake_ip,
                "Via": fake_ip
            }
            
            proxy_support = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_support, NoRedirectHandler())
            urllib.request.install_opener(opener)
            
            start_time = time.time()
            try:
                req = urllib.request.Request(search_url, headers=headers)
                with urllib.request.urlopen(req, timeout=4.0) as response:
                    html = response.read()
                    elapsed = time.time() - start_time
                    log_message(f"[QUERY SUCCESS] {active_engine['name']} ({proxy}) returned {response.status} (Length: {len(html)}, Time: {elapsed:.2f}s) for query: '{query}' (Attempt {attempt})")
                    success = True
                    break
            except Exception as e:
                elapsed = time.time() - start_time
                log_message(f"[QUERY ATTEMPT FAILED] {active_engine['name']} ({proxy}) failed in {elapsed:.2f}s (Attempt {attempt}/{max_attempts}): {e}")
                with verified_lock:
                    if proxy in verified_pools[active_engine["name"]]:
                        verified_pools[active_engine["name"]].remove(proxy)
                        
        if not success:
            log_message(f"[QUERY ABORTED] Query '{query}' failed to execute after {max_attempts} attempts.")
            
        # Random sleep delay between search iterations to emulate human browse pacing
        time.sleep(random.uniform(5.0, 15.0))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("Search simulator stopped by user.")
        sys.exit(0)
