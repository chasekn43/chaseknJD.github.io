import os
import re
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo_dir, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 10 exponentially connected high-volume search terms
extra_keywords = "Affirm credit limit freeze, Affirm credit bureau reporting dispute, Affirm unauthorized chargeback response, Affirm identity theft investigation review, Affirm pay-in-4 agreement terms, Affirm UDAAP compliance violation, Affirm FCRA credit report dispute, Affirm merchant dispute refund delay, Affirm customer care phone complaint, Affirm legal department cease and desist"

if "Affirm credit limit freeze" not in html:
    old_kw = 'content="Affirm, Affirm dispute, Affirm credit line, Affirm negative review, Affirm interest free, Affirm virtual card, Affirm account locked, Affirm loan fraud, Affirm CFPB response, Affirm false chargeback, Buy Now Pay Later dispute, Affirm lawsuit, Morgan Lewis Affirm, UDAAP compliance, police report, call history logs, Louisiana AG dispute, California AG complaint, evidence documents, Charles Kinslow"'
    new_kw = f'content="Affirm, Affirm dispute, Affirm credit line, Affirm negative review, Affirm interest free, Affirm virtual card, Affirm account locked, Affirm loan fraud, Affirm CFPB response, Affirm false chargeback, Buy Now Pay Later dispute, Affirm lawsuit, Morgan Lewis Affirm, UDAAP compliance, police report, call history logs, Louisiana AG dispute, California AG complaint, evidence documents, Charles Kinslow, {extra_keywords}"'
    html = html.replace(old_kw, new_kw)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected all 10 exponential search terms successfully!")

subprocess.run(['git', 'add', 'index.html'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Inject 10 exponential credit facility search terms into meta keywords tag'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
