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
  </div>

  <hr>

  <h2>Executive Case Summary</h2>
  <p>This repository serves as a permanent, public evidentiary record documenting systemic compliance failures, account lockdowns, and false regulatory disclosures by <strong>Affirm, Inc. (NYSE: AFRM)</strong>. Prepared by a dual-credentialed Attorney and CPA, this case study details how an automated BNPL credit engine processed an unauthorized fraud loan, locked out user interface payment controls for performing loans, and submitted material false statements to federal regulators claiming a non-existent consumer chargeback.</p>

  <h2>Key Case Milestones & Complete Paper Trail</h2>
  <ul>
    <li><strong>July 7, 2026:</strong> Unauthorized fraudulent transaction <code>PE270138</code> ($104.63) originated on Shop Pay / Affirm, shipping perfume to San Jose, CA. Immediately reported to Affirm within 86 minutes.</li>
    <li><strong>July 9, 2026:</strong> Formal identity theft report filed with Monroe Police Department (Case <code>#26-29572</code>).</li>
    <li><strong>July 16, 2026:</strong> Affirm issued formal written investigation resolution clearing consumer of all liability for loan <code>XQ8M-YX19</code>.</li>
    <li><strong>July 17, 2026 (Andy Chen Initial C&D & UI Lock):</strong> Affirm Managing Counsel Andy Chen issued initial Cease & Desist directive barring direct employee contact, demanding phone-only communication, and locking out in-app UI payment tools for performing accounts.</li>
    <li><strong>July 18–20, 2026 (Andy Chen Follow-Up C&D Orders #2 & #3):</strong> Andy Chen issued repeated, escalating Cease & Desist directives (Emails #2 and #3) prohibiting written dispute resolution and reiterating full account UI lockdown.</li>
    <li><strong>July 22, 2026 (Andy Chen Countersuit Threats):</strong> Andy Chen transmitted explicit legal threats of corporate countersuit litigation against the consumer while maintaining the active account payment lockout.</li>
    <li><strong>July 28, 2026:</strong> Affirm submitted a formal response to CFPB Complaint <code>#260717-35668593</code> containing material false statements, fabricating a claim that a "$26.16 consumer bank chargeback" occurred.</li>
    <li><strong>August 4, 2026:</strong> Outside defense counsel Madison Marshall (Morgan Lewis & Bockius LLP) asserted representation, then went radio-silent while Affirm continued automated collection texts.</li>
    <li><strong>August 5, 2026:</strong> Supplemental CFPB Complaint filed for material regulatory misrepresentations; formal LUTPA dispute submitted to Louisiana AG Liz Murrill (<code>murrille@ag.louisiana.gov</code>).</li>
    <li><strong>August 6, 2026:</strong> Formal Rule 4.2 Bar Ethics & Representation Scope Notice served on Morgan Lewis (Madison Marshall & Arjun Rao) calling out representation obstruction and the UDAAP payment Catch-22.</li>
  </ul>

  <hr>

  <p><em>For real-time updates, press inquiries, and public discussion, visit <a href="https://www.linkedin.com/in/chasekn/">Chase Kinslow's LinkedIn Profile</a>.</em></p>

</body>
</html>
"""

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Expand Key Case Milestones paper trail to document all Andy Chen C&D orders (#1, #2, #3), countersuit threats, and Aug 6 Morgan Lewis Rule 4.2 notice'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
