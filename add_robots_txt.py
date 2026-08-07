import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
robots_path = os.path.join(repo_dir, 'robots.txt')
index_path = os.path.join(repo_dir, 'index.html')

# 1. Create robots.txt in repository root
robots_content = """User-agent: *
Allow: /

Sitemap: https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/sitemap.xml
"""

with open(robots_path, 'w', encoding='utf-8') as f:
    f.write(robots_content)

print("Created robots.txt file with explicit sitemap reference!")

# 2. Add sitemap link to index.html <head>
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

sitemap_link = '<link rel="sitemap" type="application/xml" title="Sitemap" href="sitemap.xml" />'
if 'rel="sitemap"' not in html:
    html = html.replace('<head>', '<head>\n  ' + sitemap_link)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected sitemap link into index.html head tag!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Add robots.txt with explicit sitemap URL and inject sitemap link tag into index.html head'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
