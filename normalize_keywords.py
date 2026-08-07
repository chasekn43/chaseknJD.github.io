import os
import re
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo_dir, 'index.html')
readme_path = os.path.join(repo_dir, 'README.md')

# 1. Update index.html
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Enrich Keywords & Meta Description
new_keywords = 'Affirm, Affirm dispute, Affirm credit line, Affirm negative review, Affirm interest free, Affirm virtual card, Affirm account locked, Affirm loan fraud, Affirm CFPB response, Affirm false chargeback, Buy Now Pay Later dispute, Affirm lawsuit, Morgan Lewis Affirm, UDAAP compliance, police report, call history logs, Louisiana AG dispute, California AG complaint, evidence documents, Charles Kinslow'
html = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{new_keywords}">', html)

# Add Consumer Search Term Glossary / Keyword Context Block
search_terms_html = """  <hr>

  <h2>Common Search Queries & Case Topics</h2>
  <p>This public regulatory case record addresses high-volume consumer inquiry topics regarding <strong>Affirm, Inc. (NYSE: AFRM)</strong> financial products and credit practices:</p>
  <ul>
    <li><strong>Affirm Credit Line & Virtual Card Lockdown:</strong> How Affirm's automated system locks consumer account payment features and virtual card access across performing interest-free credit lines following unauthorized identity theft incidents.</li>
    <li><strong>Affirm Negative Review & Dispute Resolution Failures:</strong> Detailed paper trail illustrating frontline Affirm customer service responses, automated 86-minute claim denials, and refusal to process administrative freezes on pending fraud transactions.</li>
    <li><strong>Affirm Interest-Free & Pay-in-4 Loan Disputes:</strong> Administrative handling of Shop Pay / Affirm 0% APR interest-free installment loans, merchant fulfillment delays (Perfume Empire), and carrier tracking anomalies (OnTrac).</li>
    <li><strong>Regulatory & Legal Escalation:</strong> Official filings submitted to the Consumer Financial Protection Bureau (CFPB Complaint <code>#260717-35668593</code>), State Attorneys General (Louisiana AG Liz Murrill & California AG Rob Bonta), and outside counsel (Morgan Lewis & Bockius LLP).</li>
  </ul>"""

if 'Common Search Queries & Case Topics' not in html:
    html = html.replace('<hr>\n\n  <p><em>For real-time updates', search_terms_html + '\n\n  <hr>\n\n  <p><em>For real-time updates')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with real-world consumer search terms successfully!")

# 2. Update README.md
with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

readme_search_terms = """---

### **Frequently Searched Topics & Keyword Overview**
* **Affirm Credit Line & Virtual Card Access:** Complete documentation of account lockdowns affecting active Affirm virtual card features and interest-free credit lines.
* **Affirm Negative Reviews & Customer Service Disconnects:** Evidentiary proof of 20-minute emergency call responses, 56-minute follow-up calls, and automated 86-minute dispute denials.
* **Affirm Interest-Free Loan & Fraud Dispute Handling:** Chronological breakdown of unauthorized Shop Pay / Affirm Pay-in-4 transactions ($104.63) and carrier tracking evidence.
* **CFPB & State AG Dispute Filings:** Direct links to official complaints submitted to the CFPB (#260717-35668593), Louisiana Attorney General, and California Attorney General."""

if 'Frequently Searched Topics & Keyword Overview' not in readme:
    readme = readme.replace('---\n\n### **Executive Summary**', readme_search_terms + '\n\n---\n\n### **Executive Summary**')

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme)

print("Updated README.md with real-world consumer search terms successfully!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Normalize and enrich website and README with real-world high-volume search terms (Affirm credit line, negative review, interest-free, virtual card, BNPL dispute)'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
