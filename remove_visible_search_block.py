import os
import re
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo_dir, 'index.html')
readme_path = os.path.join(repo_dir, 'README.md')

# 1. Clean index.html
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove visible High-Volume Consumer Search Topics block
target_block = """  <!-- Real-World Search Topics -->
  <h2>🔍 High-Volume Consumer Search Topics Addressed</h2>
  <div style="background: #111827; padding: 20px; border-radius: 8px; border: 1px solid var(--border); font-size: 14px; color: var(--text-muted);">
    <p><strong style="color: #fff;">Affirm Credit Line & Virtual Card Lockdown:</strong> How Affirm's automated engine freezes UI payment access for performing accounts and virtual card features after fraud events.</p>
    <p><strong style="color: #fff;">Affirm Negative Reviews & Support Disconnect:</strong> Proof of 20-min emergency calls, 56-min follow-up calls, and automated 86-minute dispute denials.</p>
    <p><strong style="color: #fff;">Affirm Interest-Free & Pay-in-4 Disputes:</strong> Detailed analysis of Shop Pay / Affirm 0% APR installment loans, loading dock transit windows, and carrier proof-of-delivery photo anomalies.</p>
  </div>"""

if target_block in html:
    html = html.replace(target_block, '')
else:
    # Use regex to strip any variant
    html = re.sub(r'<!-- Real-World Search Topics -->.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<h2>.*?High-Volume Consumer Search Topics.*?</h2>.*?</div>', '', html, flags=re.DOTALL)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Removed visible search topics section from index.html successfully!")

# 2. Clean README.md
with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

readme_block = """---

### **Frequently Searched Topics & Keyword Overview**
* **Affirm Credit Line & Virtual Card Access:** Complete documentation of account lockdowns affecting active Affirm virtual card features and interest-free credit lines.
* **Affirm Negative Reviews & Customer Service Disconnects:** Evidentiary proof of 20-minute emergency call responses, 56-minute follow-up calls, and automated 86-minute dispute denials.
* **Affirm Interest-Free Loan & Fraud Dispute Handling:** Chronological breakdown of unauthorized Shop Pay / Affirm Pay-in-4 transactions ($104.63) and carrier tracking evidence.
* **CFPB & State AG Dispute Filings:** Direct links to official complaints submitted to the CFPB (#260717-35668593), Louisiana Attorney General, and California Attorney General."""

if readme_block in readme:
    readme = readme.replace(readme_block, '')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    print("Removed visible search topics section from README.md successfully!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Remove visible search topics section and keep keywords strictly in HTML head tags and meta elements'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
