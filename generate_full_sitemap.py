import os
import datetime

def generate_sitemap(repo_dir):
    base_url = 'https://kinslow-regulatory-archive.org/'
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    entries = []
    
    # 1. Main Hubs
    entries.append((base_url, '1.0', 'daily'))
    entries.append((base_url + 'press-kit.html', '0.9', 'weekly'))
    entries.append((base_url + 'press-release.html', '0.9', 'weekly'))
    entries.append((base_url + 'llms.txt', '0.9', 'daily'))
    
    # 2. Tools
    tools_dir = os.path.join(repo_dir, 'tools')
    if os.path.exists(tools_dir):
        for f in sorted(os.listdir(tools_dir)):
            if f.endswith('.html'):
                entries.append((f'{base_url}tools/{f}', '0.9', 'weekly'))
                
    # 3. Topics (Whitepapers)
    topics_dir = os.path.join(repo_dir, 'topics')
    if os.path.exists(topics_dir):
        for f in sorted(os.listdir(topics_dir)):
            if f.endswith('.html'):
                entries.append((f'{base_url}topics/{f}', '0.85', 'weekly'))
                
    # 4. Guides
    guides_dir = os.path.join(repo_dir, 'guides')
    if os.path.exists(guides_dir):
        for f in sorted(os.listdir(guides_dir)):
            if f.endswith('.html'):
                entries.append((f'{base_url}guides/{f}', '0.85', 'weekly'))
                
    # 5. Documents (PDFs & Exhibits)
    docs_dir = os.path.join(repo_dir, 'documents')
    if os.path.exists(docs_dir):
        for f in sorted(os.listdir(docs_dir)):
            if f.endswith('.pdf') or f.endswith('.md') or f.endswith('.zip'):
                entries.append((f'{base_url}documents/{f}', '0.8', 'monthly'))
                
    # 6. Articles
    articles_dir = os.path.join(repo_dir, 'articles')
    if os.path.exists(articles_dir):
        for f in sorted(os.listdir(articles_dir)):
            if f.endswith('.md'):
                entries.append((f'{base_url}articles/{f}', '0.75', 'monthly'))
                
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for url, priority, freq in entries:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{url}</loc>')
        xml_lines.append(f'    <lastmod>{today}</lastmod>')
        xml_lines.append(f'    <changefreq>{freq}</changefreq>')
        xml_lines.append(f'    <priority>{priority}</priority>')
        xml_lines.append('  </url>')
        
    xml_lines.append('</urlset>')
    xml_content = '\n'.join(xml_lines)
    
    sitemap_file = os.path.join(repo_dir, 'sitemap.xml')
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f'Generated sitemap with {len(entries)} URLs at {sitemap_file}')

generate_sitemap(r'C:\Users\Charwiz43\OneDrive\Desktop\SEO ENGINE\regulatory-archive-worker')
generate_sitemap(r'C:\Users\Charwiz43\OneDrive\Desktop\SEO ENGINE\regulatory-archive-2026')
