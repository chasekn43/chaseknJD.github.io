import os
import subprocess
from pypdf import PdfWriter, PdfReader

desktop_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Affirm'
scratch_dir = r'c:\Users\Charwiz43\.gemini\antigravity\scratch\Affirm'
repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
dst_pdf = os.path.join(repo_dir, 'documents', 'Affirm_Managing_Counsel_Directive_July17.pdf')
index_path = os.path.join(repo_dir, 'index.html')

# 1. Merge all Cease & Desist / Threat files
merger = PdfWriter()
files_to_merge = [
    os.path.join(scratch_dir, 'Managing Counsel Cease and Desist July 17.pdf'),
    os.path.join(desktop_dir, 'Gmail - Cease and Desist 2.pdf'),
    os.path.join(desktop_dir, 'Gmail - Cease and Desist3.pdf'),
    os.path.join(scratch_dir, 'Managing Counsel Countersuit Threat.pdf'),
    os.path.join(scratch_dir, 'Managing Counsel Call Directive July 17.pdf')
]

for fpath in files_to_merge:
    if os.path.exists(fpath):
        reader = PdfReader(fpath)
        print(f'Adding {os.path.basename(fpath)} ({len(reader.pages)} pgs)')
        for page in reader.pages:
            merger.add_page(page)

with open(dst_pdf, 'wb') as out:
    merger.write(out)

print('Merged Document 3 PDF successfully! Size:', os.path.getsize(dst_pdf))

# 2. Update index.html to reflect broader term indicating vitriol & threats
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_card = """    <div class="doc-card">
      <div class="doc-title">🔒 Affirm Managing Counsel Directive & UI Lock</div>
      <div class="doc-meta">Scott Williams Directive | July 17, 2026</div>
      <a href="documents/Affirm_Managing_Counsel_Directive_July17.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>"""

new_card = """    <div class="doc-card">
      <div class="doc-title">🔒 Affirm Managing Counsel Hostile Directives, Countersuit Threats & Account Lockdown</div>
      <div class="doc-meta">Scott Williams Cease & Desist Orders, Hostile Communications & UI Lockdown Compilation (July 17)</div>
      <a href="documents/Affirm_Managing_Counsel_Directive_July17.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>"""

if old_card in html:
    html = html.replace(old_card, new_card)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated index.html Document 3 card successfully!')
else:
    print('Notice: Could not find exact old_card string, replacing via regex')
    import re
    html = re.sub(r'<div class="doc-title">🔒 Affirm Managing Counsel Directive & UI Lock</div>\s*<div class="doc-meta">.*?</div>',
                  '<div class="doc-title">🔒 Affirm Managing Counsel Hostile Directives, Countersuit Threats & Account Lockdown</div>\n      <div class="doc-meta">Scott Williams Cease & Desist Orders, Hostile Communications & UI Lockdown Compilation (July 17)</div>',
                  html)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Expand Document #3 compilation to include Gmail Cease and Desist 2 and 3 and update card title to reflect hostile directives and countersuit threats'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print('Git push stdout:', p.stdout)
print('Git push stderr:', p.stderr)
