import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
v_filename = 'google169507de43bc15cc.html'
v_path = os.path.join(repo_dir, v_filename)

with open(v_path, 'w', encoding='utf-8') as f:
    f.write('google-site-verification: google169507de43bc15cc.html')

print("Created Google Verification file:", v_filename)

index_path = os.path.join(repo_dir, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

v_tag = '<meta name="google-site-verification" content="google169507de43bc15cc" />'
if 'google-site-verification' not in html:
    html = html.replace('<head>', '<head>\n  ' + v_tag)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected google-site-verification meta tag into index.html!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Add Google Search Console verification file google169507de43bc15cc.html and meta tag'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
