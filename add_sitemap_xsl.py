import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
xsl_path = os.path.join(repo_dir, 'sitemap.xsl')
s_path = os.path.join(repo_dir, 'sitemap.xml')

# 1. Create a modern XSL stylesheet for human browser viewing
xsl_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
                xmlns:html="http://www.w3.org/TR/REC-html40"
                xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="en">
    <head>
      <title>XML Sitemap | Kinslow v. Affirm Public Evidence Vault</title>
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b0f19; color: #f0f4f8; padding: 40px 20px; max-width: 900px; margin: 0 auto; }
        h1 { color: #ffffff; font-size: 24px; margin-bottom: 8px; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 24px; }
        table { width: 100%; border-collapse: collapse; background: #161f30; border-radius: 8px; overflow: hidden; border: 1px solid #23324a; }
        th { background: #1e293b; color: #38bdf8; text-align: left; padding: 12px 16px; font-size: 13px; font-weight: 700; border-bottom: 1px solid #23324a; }
        td { padding: 12px 16px; border-bottom: 1px solid #23324a; font-size: 13px; color: #cbd5e1; }
        tr:hover { background: #1c273c; }
        a { color: #0084ff; text-decoration: none; font-weight: 600; }
        a:hover { text-decoration: underline; }
      </style>
    </head>
    <body>
      <h1>🗺️ XML Sitemap Directory</h1>
      <p>Official Index of 10 Evidentiary Assets in <strong>Kinslow v. Affirm, Inc.</strong></p>
      <table>
        <thead>
          <tr>
            <th>URL / Resource Link</th>
            <th>Priority</th>
            <th>Frequency</th>
            <th>Last Modified</th>
          </tr>
        </thead>
        <tbody>
          <xsl:for-each select="sitemap:urlset/sitemap:url">
            <tr>
              <td><a href="{sitemap:loc}" target="_blank"><xsl:value-of select="sitemap:loc"/></a></td>
              <td><xsl:value-of select="sitemap:priority"/></td>
              <td><xsl:value-of select="sitemap:changefreq"/></td>
              <td><xsl:value-of select="sitemap:lastmod"/></td>
            </tr>
          </xsl:for-each>
        </tbody>
      </table>
    </body>
    </html>
  </xsl:template>
</xsl:stylesheet>"""

with open(xsl_path, 'w', encoding='utf-8') as f:
    f.write(xsl_content)

print("Created sitemap.xsl stylesheet!")

# 2. Update sitemap.xml to link sitemap.xsl stylesheet
valid_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="sitemap.xsl"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Monroe_Police_Report_26-29572.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Fraudulent_Vendor_Emails_and_Tracking.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Mobile_Call_History_Screenshots.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Affirm_Liability_Clearance_July16.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Affirm_Managing_Counsel_Directive_July17.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/CFPB_Complaint_and_Affirm_False_Response.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Morgan_Lewis_Correspondence.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/Louisiana_AG_Dispute_Submission.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/documents/California_AG_Dispute_Notice.pdf</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

with open(s_path, 'w', encoding='utf-8') as f:
    f.write(valid_sitemap)

print("Linked sitemap.xsl in sitemap.xml!")

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Add sitemap.xsl stylesheet so sitemap.xml renders as a styled HTML table in human browsers while maintaining 100% W3C validity for Googlebot'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
