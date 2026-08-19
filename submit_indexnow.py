import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request as AuthRequest

HOST = "kinslow-regulatory-archive.org"
SCOPES = ["https://googleapis.com"]
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "google_credentials.json")

# Cleaned array path layouts containing core backslashes
TARGET_URLS = [
    "https://kinslow-regulatory-archive.org",
    "https://kinslow-regulatory-archive.orgDear%20Penny.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/monroe-police-report-26-29572.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/fraudulent-vendor-emails-and-tracking.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/mobile-call-history-screenshots.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/affirm-liability-clearance-july16.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/affirm-managing-counsel-directive-july17.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/cfpb-complaint-and-affirm-false-response.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/morgan-lewis-correspondence.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/louisiana-ag-dispute-submission.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/california-ag-dispute-notice.pdf",
    "https://kinslow-regulatory-archive.orgdocuments/Silence_Amidst_Reporters_Inquiry_Perfect_Fall_Detail.pdf",
    "https://kinslow-regulatory-archive.orgtopics/regulation-z-apa-compliance",
    "https://kinslow-regulatory-archive.orgtopics/fintech-bnpl-merchant-dispute-resolution",
    "https://kinslow-regulatory-archive.orgtopics/udaap-customer-service-failures",
    "https://kinslow-regulatory-archive.orgtopics/california-ag-regulatory-rebuttal",
    "https://kinslow-regulatory-archive.orgtopics/bnpl-billing-disputes-regulation-z",
    "https://kinslow-regulatory-archive.orgtopics/apa-fintech-rulemaking-exemptions",
    "https://kinslow-regulatory-archive.orgtopics/pos-chargeback-payment-friction",
    "https://kinslow-regulatory-archive.orgtopics/udaap-merchant-refund-friction",
    "https://kinslow-regulatory-archive.orgdocuments/ca-ag-reply-1553638.pdf",
    "https://kinslow-regulatory-archive.orgtopics/verity-je-status-429",
    "https://kinslow-regulatory-archive.orgtopics/tila-12cfr1026-closed-end-dispute-mechanics",
    "https://kinslow-regulatory-archive.orgtopics/apa-notice-and-comment-reliance-defenses",
    "https://kinslow-regulatory-archive.orgtopics/fintech-sox-ledger-friction-chargebacks",
    "https://kinslow-regulatory-archive.orgguides/affirm-bank-billpay-workaround",
    "https://kinslow-regulatory-archive.orgguides/affirm-dispute-denied-returned-item",
    "https://kinslow-regulatory-archive.orgguides/affirm-automated-customer-service-escalation",
    "https://kinslow-regulatory-archive.orgguides/affirm-ceo-executive-contacts-escalation",
    "https://kinslow-regulatory-archive.orgguides/affirm-credit-bureau-dispute-letters",
    "https://kinslow-regulatory-archive.orgguides/affirm-merchant-return-tracking-proof",
    "https://kinslow-regulatory-archive.orgpress-release",
    "https://kinslow-regulatory-archive.orgtopics/affirm-capital-stack-abs-warehouse-facility-risks",
    "https://kinslow-regulatory-archive.orgtopics/affirm-institutional-whistleblower-memorandum",
    "https://kinslow-regulatory-archive.orgdocuments/california-state-bar-misconduct-complaint-morgan-lewis.pdf",
    "https://kinslow-regulatory-archive.orgtopics/affirm-dispute-denied-automated-bot-guide",
    "https://kinslow-regulatory-archive.orgtopics/affirm-account-locked-during-dispute-solution",
    "https://kinslow-regulatory-archive.orgtopics/affirm-frozen-account-communication-paradox",
    "https://kinslow-regulatory-archive.orgtopics/behind-the-portal-fintech-executive-aliases-disputes",
    "https://kinslow-regulatory-archive.orgtopics/affirm-cfpb-complaint-database-bbb-case-logs",
    "https://kinslow-regulatory-archive.orgtools/affirm-dispute-demand-generator",
    "https://kinslow-regulatory-archive.orgtopics/affirm-merchant-settlement-holding-refund-delays",
    "https://kinslow-regulatory-archive.orgtopics/morgan-lewis-amlaw10-collections-protocol",
    "https://kinslow-regulatory-archive.orgtopics/single-use-virtual-cards-reconciliation-loops",
    "https://kinslow-regulatory-archive.orgtools/interactive-docket-timeline",
    "https://kinslow-regulatory-archive.orgtools/dispute-readiness-checklist",
    "https://kinslow-regulatory-archive.orgpress-kit"
]

def run_google_pipeline():
    if not os.path.exists(KEY_PATH):
        print(f"[-] Missing credentials file! Place 'google_credentials.json' in: {KEY_PATH}")
        return
        
    print("[+] Authorizing secure credentials channel with Google API...")
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    
    # Request token ONCE up front to handle the bulk job run safely
    credentials.refresh(AuthRequest())
    
    session = requests.Session()
    print(f"[+] Processing {len(TARGET_URLS)} targets inside network memory...")
    endpoint = "https://googleapis.com"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials.token}"
    }

    for target_url in TARGET_URLS:
        payload = {"url": target_url, "type": "URL_UPDATED"}
        try:
            response = session.post(endpoint, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f" [SUCCESS] Google Index Queue Accepted -> {target_url}")
            else:
                print(f" [-] Failed Status {response.status_code} for {target_url}: {response.text}")
        except Exception as e:
            print(f" [-] Network Execution Error on {target_url}: {e}")

if __name__ == '__main__':
    print('=== Google Indexing API Automation Dashboard ===')
    run_google_pipeline()
