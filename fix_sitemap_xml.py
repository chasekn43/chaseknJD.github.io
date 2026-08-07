import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
s_path = os.path.join(repo_dir, 'sitemap.xml')
nojekyll_path = os.path.join(repo_dir, '.nojekyll')

# 1. Create .nojekyll file to bypass GitHub Pages Jekyll processing
with open(nojekyll_path, 'w', encoding='utf-8') as f:
    f.write('')

print("Created .nojekyll file!")

# 2. Re-create sitemap.xml with 100% correct W3C namespace (sitemaps.org)
valid_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Monroe_Police_Report_26-29572.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Fraudulent_Vendor_Emails_and_Tracking.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Mobile_Call_History_Screenshots.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Affirm_Liability_Clearance_July16.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Affirm_Managing_Counsel_Directive_July17.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/CFPB_Complaint_and_Affirm_False_Response.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Morgan_Lewis_Correspondence.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Louisiana_AG_Dispute_Submission.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/California_AG_Dispute_Notice.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

with open(s_path, 'w', encoding='utf-8') as f:
    f.write(valid_sitemap)

print("Updated sitemap.xml with valid sitemaps.org XML schema!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Fix sitemap.xml XML namespace to sitemaps.org and add .nojekyll file for GitHub Pages'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
