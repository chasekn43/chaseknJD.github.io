import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo_dir, 'index.html')
readme_path = os.path.join(repo_dir, 'README.md')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_grid = """    <div class="doc-card">
      <div class="doc-title">[Doc #2] 📞 Mobile Call History Screenshots & Telephonic Log</div>
      <div class="doc-meta">Proof of July 7 Emergency Call (20 minutes at 12:55 PM) & July 9 Calls (56 minutes total at 12:21 PM & 2:15 PM)</div>
      <a href="documents/Mobile_Call_History_Screenshots.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">[Doc #3] 🚚 Merchant Fulfillment & OnTrac Carrier Tracking Evidence</div>
      <div class="doc-meta">Order PE270138 Emails, OnTrac Tracking #1LSDCR10011QF38 & 2hr 45min Loading Dock Analysis</div>
      <a href="documents/Fraudulent_Vendor_Emails_and_Tracking.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>"""

new_grid = """    <div class="doc-card">
      <div class="doc-title">[Doc #2] 🚚 Merchant Fulfillment & OnTrac Carrier Tracking Evidence</div>
      <div class="doc-meta">Order PE270138 Emails, OnTrac Tracking #1LSDCR10011QF38 & 2hr 45min Loading Dock Analysis</div>
      <a href="documents/Fraudulent_Vendor_Emails_and_Tracking.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">[Doc #3] 📞 Mobile Call History Screenshots & Telephonic Log</div>
      <div class="doc-meta">Proof of July 7 Emergency Call (20 minutes at 12:55 PM) & July 9 Calls (56 minutes total at 12:21 PM & 2:15 PM)</div>
      <a href="documents/Mobile_Call_History_Screenshots.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>"""

if old_grid in html:
    html = html.replace(old_grid, new_grid)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Swapped Doc 2 and Doc 3 in index.html successfully!")

with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

old_readme_list = """* 📞 **[Doc #2]** [Mobile Call History Screenshots — July 7 (20 min) & July 9 (56 min total)](https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Mobile_Call_History_Screenshots.pdf)
* 🚚 **[Doc #3]** [Merchant Fulfillment & OnTrac Carrier Tracking Evidence (#1LSDCR10011QF38)](https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Fraudulent_Vendor_Emails_and_Tracking.pdf)"""

new_readme_list = """* 🚚 **[Doc #2]** [Merchant Fulfillment & OnTrac Carrier Tracking Evidence (#1LSDCR10011QF38)](https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Fraudulent_Vendor_Emails_and_Tracking.pdf)
* 📞 **[Doc #3]** [Mobile Call History Screenshots — July 7 (20 min) & July 9 (56 min total)](https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Mobile_Call_History_Screenshots.pdf)"""

if old_readme_list in readme:
    readme = readme.replace(old_readme_list, new_readme_list)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    print("Swapped Doc 2 and Doc 3 in README.md successfully!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Reorder Document Vault so Doc #2 (Merchant Fulfillment & Carrier Evidence) precedes Doc #3 (Mobile Call History Screenshots)'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
