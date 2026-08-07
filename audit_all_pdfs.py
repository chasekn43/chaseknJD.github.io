import os
import re
from pypdf import PdfReader

repo = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
docs_dir = os.path.join(repo, 'documents')

print("Starting full audit of all 9 PDF documents...\n")

for file in sorted(os.listdir(docs_dir)):
    if file.endswith('.pdf'):
        p = os.path.join(docs_dir, file)
        reader = PdfReader(p)
        print(f"=== AUDITING: {file} ({len(reader.pages)} Pages) ===")
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            
            # Check for third-person 'consumer'
            consumer_matches = re.findall(r'\bconsumer\b|\bconsumer\'s\b', text, re.IGNORECASE)
            if consumer_matches:
                print(f"  - Page {i+1}: Found {len(consumer_matches)} 'consumer' reference(s)")
            
            # Check for old/incorrect timestamps or amounts
            if '2:19' in text:
                print(f"  - Page {i+1}: Found '2:19' timestamp")
            if '104.65' in text:
                print(f"  - Page {i+1}: Found '104.65' amount")
            if '104.63' in text and i == 0 and file == 'Fraudulent_Vendor_Emails_and_Tracking.pdf':
                print(f"  - Page {i+1}: Verified correct '104.63 USD Total'")

print("\nAudit script complete!")
