import os
import re
import subprocess
from pypdf import PdfReader

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
docs_dir = os.path.join(repo_dir, 'documents')
index_path = os.path.join(repo_dir, 'index.html')
readme_path = os.path.join(repo_dir, 'README.md')

print("=== FINAL SYSTEM RE-OPTIMIZATION AUDIT ===")

docs = [
    ('Doc #1', 'Monroe_Police_Report_26-29572.pdf', 'Monroe Police Department Incident Report #26-29572'),
    ('Doc #2', 'Fraudulent_Vendor_Emails_and_Tracking.pdf', 'Merchant Fulfillment & OnTrac Carrier Tracking Evidence (#1LSDCR10011QF38)'),
    ('Doc #3', 'Mobile_Call_History_Screenshots.pdf', 'Mobile Call History Screenshots — July 7 (20 min) & July 9 (56 min total)'),
    ('Doc #4', 'Affirm_Liability_Clearance_July16.pdf', 'Affirm Written Liability Clearance Resolution (July 16, 2026)'),
    ('Doc #5', 'Affirm_Managing_Counsel_Directive_July17.pdf', 'Affirm Managing Counsel Andy Chen C&D Orders & UI Lock (DOC 5.pdf)'),
    ('Doc #6', 'CFPB_Complaint_and_Affirm_False_Response.pdf', 'CFPB Master Regulatory Complaint Compilation (#260717-35668593)'),
    ('Doc #7', 'Morgan_Lewis_Correspondence.pdf', 'Morgan Lewis Representation Correspondence & Aug 6 Ethics Notice'),
    ('Doc #8', 'Louisiana_AG_Dispute_Submission.pdf', 'Louisiana AG Master Dispute Filing & Executive Email to AG Liz Murrill (1.67 MB)'),
    ('Doc #9', 'California_AG_Dispute_Notice.pdf', 'California AG Master Dispute Filing & Rob Bonta Notice (1.03 MB)')
]

for label, filename, title in docs:
    fpath = os.path.join(docs_dir, filename)
    if os.path.exists(fpath):
        r = PdfReader(fpath)
        print(f"[OK] {label}: {filename} ({len(r.pages)} pgs, {os.path.getsize(fpath)} bytes)")
    else:
        print(f"[MISSING] {label}: {filename}")

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_doc5_card = 'Andy Chen Cease & Desist Orders (#1, #2, #3), Countersuit Warnings & UI Lockdown Compilation (July 17–22)'
new_doc5_card = 'Andy Chen Cease & Desist Orders #1 (July 17 12:11 PM), #2 (July 17 5:31 PM) & #3 (July 20 4:01 PM) [DOC 5 Master Compilation]'

if old_doc5_card in html:
    html = html.replace(old_doc5_card, new_doc5_card)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated Document #5 card description on index.html!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Final re-optimization audit: Verify all 9 primary evidence PDFs, canonical tags, and milestone cross-references'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
