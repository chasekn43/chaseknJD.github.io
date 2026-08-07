import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo_dir, 'index.html')
readme_path = os.path.join(repo_dir, 'README.md')

# 1. Update index.html
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Document #5 card meta text
html = html.replace(
    'Andy Chen C&D Email #1 (July 17 12:11 PM), #2 (July 17 5:31 PM) & #3 (July 20 4:01 PM) [DOC 5]',
    'Andy Chen C&D Order (July 17 12:11 PM), Contradictory Phone-Only Directive (July 17 5:31 PM) & Countersuit Warning (July 20 4:01 PM) [DOC 5]'
)

# Fix timeline description
old_timeline_item = 'Andy Chen issued a formal Cease & Desist order barring email contact, issued contradictory phone-only payment directives, locked out in-app UI payment tools for performing accounts, and threatened a corporate countersuit.'
new_timeline_item = 'Andy Chen issued a formal Cease & Desist order barring employee email contact, issued contradictory phone-only payment directives, and threatened a corporate countersuit.'
html = html.replace(old_timeline_item, new_timeline_item)

# Fix hero description
old_hero = 'When customer communications came under first-name executive aliases ("Scott from Affirm") before Managing Counsel Andy Chen stepped in with heavy-handed Cease & Desist orders, an account payment lockdown, and corporate countersuit threats'
new_hero = 'When customer communications came under first-name executive aliases ("Scott from Affirm") before Managing Counsel Andy Chen stepped in with a heavy-handed Cease & Desist order, contradictory phone-only payment directives, and corporate countersuit threats'
html = html.replace(old_hero, new_hero)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html: Removed attribution of in-app UI lockout to Andy Chen!")

# 2. Update README.md
with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

readme = readme.replace(
    '[Doc #5] Affirm Managing Counsel Directive',
    '[Doc #5] Affirm Managing Counsel Andy Chen Cease & Desist Order & Contradictory Directives'
)

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme)

print("Updated README.md successfully!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Factual correction: Clarify that UI payment lockout was an automated software feature, not Andy Chen. Andy Chen issued C&D order, contradictory phone-only directives, and countersuit threats.'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
