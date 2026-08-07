import os
import re
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo_dir, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

narrative = """<p class="hero-desc">The True Firsthand Record: What happens when an unauthorized fraudulent purchase hits your account, and you do everything humanly possible to stop it? After calling Affirm Customer Support within 86 minutes and alerting the merchant while the box sat static on a Texas loading dock 36.5 miles from the carrier hub, Affirm issued an 86-minute automated denial—ignoring written promises of a 30-day review. When customer communications came under first-name executive aliases ("Scott from Affirm") before Managing Counsel Andy Chen stepped in with heavy-handed Cease & Desist orders, an account payment lockdown, and corporate countersuit threats, Affirm topped it off by submitting false disclosures to federal regulators. Here is the complete paper trail.</p>"""

text_new = re.sub(r'<p class="hero-desc">.*?</p>', narrative, text, flags=re.DOTALL)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text_new)

p1 = os.path.join(repo_dir, 'force_narrative.py')
if os.path.exists(p1): os.remove(p1)

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Update hero description to exact firsthand narrative story'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
