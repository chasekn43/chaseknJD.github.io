import os, re
import xml.etree.ElementTree as ET

doc_dir = r'c:\Users\Charwiz43\.gemini\antigravity\scratch\Affirm\regulatory-archive-2026\documents'
local_docs = set(os.listdir(doc_dir))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'href=["\']documents/([^"\'#?]+)["\']'
doc_links = set(re.findall(pattern, html))
missing_docs = [d for d in doc_links if d not in local_docs]

tree = ET.parse('sitemap.xml')
root = tree.getroot()
urls = [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

missing_urls = []
for u in urls:
    rel = u.replace('https://kinslow-regulatory-archive.org/', '').replace('http://kinslow-regulatory-archive.org/', '')
    rel_path = 'index.html' if rel in ('', '/') else rel.replace('/', os.sep)
    if not os.path.exists(rel_path):
        missing_urls.append((u, rel_path))

print('=== AUDIT RESULTS ===')
print(f'Total local documents in /documents: {len(local_docs)}')
print(f'Total documents linked in index.html: {len(doc_links)}')
print(f'Missing doc links: {missing_docs}')
print(f'Total URLs in sitemap.xml: {len(urls)}')
print(f'Missing sitemap files: {missing_urls}')
