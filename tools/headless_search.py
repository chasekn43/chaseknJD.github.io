from playwright.sync_api import sync_playwright
import sys, json, urllib.parse, os

query = sys.argv[1] if len(sys.argv) > 1 else 'Chase Kinslow CFPB Reg Z Affirm dispute merchant refund regulatory archive'
results = {'google': [], 'bing': []}
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Google
        g_url = 'https://www.google.com/search?q=' + urllib.parse.quote_plus(query) + '&hl=en'
        page.goto(g_url, timeout=30000)
        page.wait_for_timeout(2500)
        seen = set()
        for a in page.query_selector_all('a'):
            href = a.get_attribute('href') or ''
            if href.startswith('/url?q='):
                url = urllib.parse.unquote(href.split('/url?q=')[1].split('&')[0])
                title = a.inner_text().strip()
                if url and url not in seen:
                    results['google'].append({'title': title, 'url': url})
                    seen.add(url)
        # Bing
        b_url = 'https://www.bing.com/search?q=' + urllib.parse.quote_plus(query)
        page.goto(b_url, timeout=30000)
        page.wait_for_timeout(2500)
        for a in page.query_selector_all('li.b_algo h2 a'):
            href = a.get_attribute('href') or ''
            title = a.inner_text().strip()
            if href:
                results['bing'].append({'title': title, 'url': href})
        browser.close()
except Exception as e:
    results['error'] = str(e)

out_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'headless_results.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(json.dumps(results, indent=2, ensure_ascii=False))
