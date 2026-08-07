import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
sitemap_path = os.path.join(repo_dir, 'sitemap.xml')
index_path = os.path.join(repo_dir, 'index.html')

# 1. Create XML Sitemap for Googlebot & Bingbot
sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Monroe_Police_Report_26-29572.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Fraudulent_Vendor_Emails_and_Tracking.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Mobile_Call_History_Screenshots.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Affirm_Liability_Clearance_July16.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Affirm_Managing_Counsel_Directive_July17.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/CFPB_Complaint_and_Affirm_False_Response.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Morgan_Lewis_Correspondence.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Louisiana_AG_Dispute_Submission.pdf</loc>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/California_AG_Dispute_Notice.pdf</loc>
    <priority>0.8</priority>
  </url>
</urlset>"""

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print("Created sitemap.xml for Google Search Console!")

# 2. Enrich index.html body text & headings with broad high-volume consumer terms
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update page title to hit broad searches
html = html.replace('<title>The True Record: Kinslow v. Affirm, Inc. | Corporate Overreach & Fraud Breakdown</title>',
                    '<title>Affirm BNPL Dispute, Credit Line, Score Impact & Merchant Refund Record | Kinslow v. Affirm</title>')

# Enrich Hero Description to hit broad search terms
old_desc = 'The True Firsthand Account: Executive Aliases, Heavy-Handed Directives, Account Payment Lockouts, and False Regulatory Disclosures.'
new_desc = 'The True Firsthand Record: Documenting Affirm Buy Now Pay Later (BNPL) loan disputes, credit line freezes, credit score impacts, merchant refund delays (Perfume Empire), executive aliases, Andy Chen legal directives, and false CFPB disclosures.'
html = html.replace(old_desc, new_desc)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Enriched index.html title & hero text with broad consumer search terms!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Add sitemap.xml and enrich title and hero copy with broad consumer search terms (Affirm credit line, BNPL dispute, credit score impact, merchant refund)'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
