<?xml version="1.0" encoding="UTF-8"?>
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
</xsl:stylesheet>