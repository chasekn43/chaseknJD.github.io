import os
import subprocess

repo = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
new_lines = []
for l in lines:
    if 'Morgan Lewis Outreach & Rule 4.2 Ethics Notice' in l:
        new_lines.append('      <strong>July 24 – August 6, 2026 — Morgan Lewis Outreach & Rule 4.2 Ethics Notice:</strong>')
    elif 'Outside counsel Madison Marshall (Morgan Lewis) asserted representation' in l:
        new_lines.append('      Outside counsel Madison Marshall (Morgan Lewis) asserted representation on July 24 at 4:34 PM ("We have been retained by Affirm... Please direct all future correspondence to me"). After consumer provided notice of Affirm\'s false CFPB disclosures on August 3, counsel went silent while Affirm continued automated debt texts. Rule 4.2 Bar Ethics & Scope Notice served on August 6.')
    else:
        new_lines.append(l)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

p1 = os.path.join(repo, 'update_jul24_morgan.py')
if os.path.exists(p1): os.remove(p1)

subprocess.run(['git', 'add', '-A'], cwd=repo)
subprocess.run(['git', 'commit', '-m', 'Update Morgan Lewis timeline item with exact July 24 at 4:34 PM outreach timestamp'], cwd=repo)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
