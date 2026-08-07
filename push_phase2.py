import os
import subprocess

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
index_path = os.path.join(repo_dir, 'index.html')

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="120; url=https://www.linkedin.com/in/chasekn/">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Affirm BNPL Fraud Dispute & Primary Evidence Vault | Kinslow v. Affirm, Inc. Case Study</title>
  <meta name="description" content="Official public case record, police report, CFPB complaint filings, and primary evidence documents for Affirm, Inc. (NYSE: AFRM) BNPL loan dispute. CFPB Complaint #260717-35668593.">
  <meta name="keywords" content="Affirm, Affirm dispute, Affirm account locked, Affirm loan fraud, Affirm CFPB response, Affirm false chargeback, Buy Now Pay Later dispute, Affirm lawsuit, Morgan Lewis Affirm, UDAAP compliance, police report, Louisiana AG dispute, evidence documents, Charles Kinslow">
  <meta name="author" content="Charles W. Kinslow IV, J.D., C.P.A.">
  
  <!-- Open Graph Tags for Social & LinkedIn Preview -->
  <meta property="og:title" content="Affirm BNPL Dispute Failure & Primary Evidence Vault">
  <meta property="og:description" content="Public evidence repository: Police report, CFPB filings, Louisiana AG submission, liability clearance letters, and Morgan Lewis correspondence in Kinslow v. Affirm, Inc.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/">
  
  <!-- Schema.org JSON-LD Structured Data for Search Crawlers -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Report",
    "name": "Affirm BNPL Fraud Dispute & Regulatory Primary Evidence Vault",
    "url": "https://chasekn43.github.io/Kinslow-Affirm-Dispute-Case-Study/",
    "description": "Public evidentiary repository containing police reports, CFPB complaints, Louisiana AG dispute filings, liability clearance letters, and legal directives.",
    "author": {
      "@type": "Person",
      "name": "Charles W. Kinslow IV",
      "jobTitle": "J.D., C.P.A.",
      "sameAs": "https://www.linkedin.com/in/chasekn/"
    }
  }
  </script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 900px; margin: 0 auto; padding: 25px; }
    .hero-card { background: #f0f7ff; border-left: 5px solid #0a66c2; padding: 22px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .btn-linkedin { display: inline-block; background: #0a66c2; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; margin-top: 12px; font-size: 15px; }
    .btn-linkedin:hover { background: #004182; }
    h1, h2, h3 { color: #0a192f; }
    code { background: #f4f4f4; padding: 3px 6px; border-radius: 4px; font-family: monospace; font-size: 14px; }
    hr { border: 0; height: 1px; background: #e0e0e0; margin: 30px 0; }
    .badge { background: #eef3f8; color: #0a66c2; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    
    /* Evidence Vault Grid */
    .doc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 15px; margin-top: 20px; }
    .doc-card { background: #ffffff; border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); transition: transform 0.2s; }
    .doc-card:hover { border-color: #0a66c2; transform: translateY(-2px); }
    .doc-title { font-weight: bold; font-size: 15px; color: #0a192f; margin-bottom: 6px; }
    .doc-meta { font-size: 12px; color: #586069; margin-bottom: 12px; }
    .btn-doc { display: inline-block; background: #24292e; color: #ffffff; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    .btn-doc:hover { background: #0366d6; }
  </style>
</head>
<body>

  <div class="hero-card">
    <span class="badge">OFFICIAL CASE STUDY & LINKEDIN HUB</span>
    <h2>Kinslow v. Affirm, Inc. | Case Study & Evidence Vault</h2>
    <p>Read the primary evidence documents and case chronology below. For ongoing discussion, media inquiries, and real-time updates, visit Chase Kinslow's official LinkedIn profile:</p>
    <a href="https://www.linkedin.com/in/chasekn/" class="btn-linkedin">View Live Case Updates on LinkedIn &rarr;</a>
  </div>

  <h1>Kinslow v. Affirm, Inc. | Public Regulatory Case Record & Evidentiary Vault</h1>
  <p><strong>Author:</strong> Charles W. Kinslow IV, J.D., C.P.A. | Monroe, LA 71201</p>
  <p><strong>Primary Identifiers:</strong> CFPB Complaint <code>#260717-35668593</code> | Fraud Loan ID <code>XQ8M-YX19</code> | Monroe Police Dept Report <code>#26-29572</code></p>

  <hr>

  <h2>Primary Evidence & Public Document Vault</h2>
  <p>Direct download and viewable PDF primary evidence documents establishing the complete paper trail in <em>Kinslow v. Affirm, Inc.</em>:</p>

  <div class="doc-grid">
    <div class="doc-card">
      <div class="doc-title">📋 Monroe Police Department Incident Report</div>
      <div class="doc-meta">Official Law Enforcement Filing | Case #26-29572 (July 9, 2026)</div>
      <a href="documents/Monroe_Police_Report_26-29572.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">✅ Affirm Written Liability Clearance Letter</div>
      <div class="doc-meta">Formal Investigation Resolution | July 16, 2026</div>
      <a href="documents/Affirm_Liability_Clearance_July16.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">🔒 Affirm Managing Counsel Hostile Directives, Countersuit Threats & Account Lockdown</div>
      <div class="doc-meta">Andy Chen Cease & Desist Orders (#1, #2, #3), Countersuit Warnings & UI Lockdown Compilation (July 17–22)</div>
      <a href="documents/Affirm_Managing_Counsel_Directive_July17.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">⚖️ CFPB Master Complaint Compilation</div>
      <div class="doc-meta">Initial Complaint, Affirm Reply, Rebuttal & Supplemental Filing</div>
      <a href="documents/CFPB_Complaint_and_Affirm_False_Response.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">✉️ Morgan Lewis Representation Correspondence</div>
      <div class="doc-meta">Madison Marshall Email, False Disclosure Notice & Aug 6 Rule 4.2 Ethics Notice</div>
      <a href="documents/Morgan_Lewis_Correspondence.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">🏛️ Louisiana Attorney General Executive Submission</div>
      <div class="doc-meta">Formal LUTPA Submission to AG Liz Murrill (murrille@ag.louisiana.gov)</div>
      <a href="documents/Louisiana_AG_Dispute_Submission.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">🏛️ California Attorney General Notice</div>
      <div class="doc-meta">Rob Bonta / Assistant AG Nicklas Akers Submission</div>
      <a href="documents/California_AG_Dispute_Notice.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>

    <div class="doc-card">
      <div class="doc-title">🚚 Merchant Fulfillment & OnTrac Carrier Tracking Evidence</div>
      <div class="doc-meta">Order PE270138 Emails, OnTrac Tracking #1LSDCR10011QF38 & 2hr 45min Loading Dock Analysis</div>
      <a href="documents/Fraudulent_Vendor_Emails_and_Tracking.pdf" class="btn-doc" target="_blank">View / Download PDF &rarr;</a>
    </div>
  </div>

  <hr>

  <h2>Executive Case Summary</h2>
  <p>This repository serves as a permanent, public evidentiary record documenting systemic compliance failures, account lockdowns, and false regulatory disclosures by <strong>Affirm, Inc. (NYSE: AFRM)</strong>. Prepared by a dual-credentialed Attorney and CPA, this case study details how an automated BNPL credit engine processed an unauthorized fraud loan, locked out user interface payment controls for performing loans, and submitted material false statements to federal regulators claiming a non-existent consumer chargeback.</p>

  <h2>Phase II: The Intrusion, Geographic Anomaly & Logistics Mitigation Analysis</h2>
  <ul>
    <li><strong>July 7, 2026 (11:53 AM CDT):</strong> Unauthorized intrusion into Shop account. Malicious actor initiated Order PE270138 via Affirm credit facility ($104.63).</li>
    <li><strong>Geographic Discrepancy:</strong> Consumer's verified billing profile is anchored exclusively to Monroe, Louisiana (71201). The fraudulent order was routed to 81 Keever Court, San Jose, California 95127 (over 1,800 miles away).</li>
    <li><strong>July 7, 2026 (12:55 PM CDT) — Emergency Call & "Rest Assured" Assurance:</strong> Consumer placed emergency call to Affirm Customer Support immediately after the fraud hit. Frontline agents told the consumer to "rest assured" they would not be charged, refused an administrative freeze due to "pending" transaction status, and instructed the consumer to call back after the status changed.</li>
    <li><strong>July 7, 2026 (1:27 PM CDT) — Label Generation (Farmers Branch, TX 75234):</strong> Perfume Empire generated a digital shipping label (EDI data) at its Farmers Branch warehouse. No physical package had been scanned or tendered to any carrier.</li>
    <li><strong>July 7, 2026 (2:19 PM CDT) — Consumer Fraud Alert Window:</strong> Consumer reported fraud to Affirm within 86 minutes. At 2:19 PM, the physical item remained un-scanned in a bulk staging bin on Perfume Empire's loading dock in Farmers Branch, TX.</li>
    <li><strong>July 7, 2026 (3:36 PM & 4:38 PM CDT):</strong> Formal written cancellation demands sent to merchant (Perfume Empire) via email and portal hours before physical carrier dispatch.</li>
    <li><strong>July 7, 2026 (4:12 PM CDT) — OnTrac Origin Scan (DeSoto, TX 75115):</strong> OnTrac carrier registered the first physical laser scan 36.5 miles away at its DeSoto regional hub — <strong>2 hours and 45 minutes after label generation</strong> and nearly 2 hours after Affirm received fraud notice.</li>
    <li><strong>July 8, 2026 (3:23 AM CDT):</strong> Perfume Empire issued an automated refusal to cancel or intercept the shipment (OnTrac Tracking <code>#1LSDCR10011QF38</code>), claiming it had "already processed."</li>
  </ul>

  <hr>

  <p><em>For real-time updates, press inquiries, and public discussion, visit <a href="https://www.linkedin.com/in/chasekn/">Chase Kinslow's LinkedIn Profile</a>.</em></p>

</body>
</html>
"""

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Update Phase II Logistics Mitigation Analysis and add Document Card #8 for Fraudulent Vendor Emails and OnTrac Tracking Evidence'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
