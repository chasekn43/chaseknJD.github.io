import os
import re
import subprocess
from pypdf import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

repo_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Kinslow-Affirm-Repo'
desktop_dir = r'C:\Users\Charwiz43\OneDrive\Desktop\Affirm'
index_path = os.path.join(repo_dir, 'index.html')
orig_pdf = os.path.join(desktop_dir, 'Frraudulent Vendor Emails with New Tracking Info.pdf')
dst_pdf = os.path.join(repo_dir, 'documents', 'Fraudulent_Vendor_Emails_and_Tracking.pdf')

# 1. Update index.html to 100% First-Person Voice (I / me / my)
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('Consumer alerted Affirm Customer Support within 86 minutes. Frontline agents refused an administrative freeze on pending transactions, telling consumer to "rest assured."', 'I alerted Affirm Customer Support within 86 minutes. Frontline agents refused an administrative freeze on pending transactions, telling me to "rest assured."')
html = html.replace('Consumer placed two follow-up calls to Affirm CS providing tracking data, police report numbers, and evidence for the active investigation file.', 'I placed two follow-up calls to Affirm CS providing tracking data, police report numbers, and evidence for the active investigation file.')
html = html.replace('demanding full consumer liability without human review.', 'demanding full liability from me without human review.')
html = html.replace('confirming consumer is "NOT responsible" for fraud loan XQ8M-YX19.', 'confirming I am "NOT responsible" for fraud loan XQ8M-YX19.')
html = html.replace('Consumer dispatched urgent cancellation email to sales@perfume-empire.com at 4:36 PM CDT on July 7 (3 days before delivery); merchant issued automated refusal July 8.', 'I dispatched an urgent cancellation email to sales@perfume-empire.com at 4:36 PM CDT on July 7 (3 days before delivery); merchant issued automated refusal July 8.')
html = html.replace('failing to respond to consumer\'s August 3 notice', 'failing to respond to my August 3 notice')
html = html.replace('traps a consumer who can neither pay performing debts nor get straight answers', 'traps me when I can neither pay performing debts nor get straight answers')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Converted index.html to 100% first-person (I / me / my)!")

# 2. Rebuild Document #2 PDF with 100% First-Person Voice (I / me / my)
def create_summary_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    NAVY = colors.HexColor('#0F2C59')
    DARK = colors.HexColor('#333333')

    t_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=15, leading=19, textColor=NAVY, fontName='Helvetica-Bold')
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=9.5, leading=12.5, textColor=DARK, fontName='Helvetica-Oblique')
    b_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8.5, leading=11.5, textColor=DARK, fontName='Helvetica', spaceAfter=4)

    story = []
    story.append(Paragraph('MASTER EXECUTIVE SUMMARY & FAULT AUDIT: ORDER #PE270138', t_style))
    story.append(Paragraph('Comprehensive Merchant Fulfillment, Carrier Logistics & Delivery Photo Audit', sub_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY, spaceBefore=2, spaceAfter=6))

    points = [
        ('1. Order Origination & Geographic Anomaly:', 'Order PE270138 (104.63 USD Total: 95.55 merchandise + 9.08 tax) was initiated July 7 at 12:53 PM CDT via Affirm without my knowledge or authorization. My billing profile is anchored exclusively to Monroe, LA 71201. The fraudulent shipment was routed to 81 Keever Ct, San Jose, CA 95127 (1,800 miles away).'),
        ('2. Fulfillment Origin (Farmers Branch DC 75234):', 'Perfume Empire fulfills from 3402 Garden Brook Dr, Farmers Branch, TX 75234. At 1:27 PM CDT, only a digital shipping label (EDI data) was created. No physical parcel was handed to any carrier.'),
        ('3. The 36.5-Mile Staging Window & Carrier Scan (DeSoto Hub 75115):', 'I reported the fraud to Affirm at 2:19 PM CDT. OnTrac registered its first laser scan at 4:12 PM CDT at its regional hub (802 E Centre Park Blvd, DeSoto, TX 75115)—36.5 miles down I-35E South from Farmers Branch. When I notified Affirm at 2:19 PM, the physical box was static on Perfume Empire\'s loading dock in Farmers Branch, nearly 2 hours before reaching DeSoto.'),
        ('4. Immediate Fraud Notice & Merchant Refusal:', 'I dispatched an urgent cancellation email to sales@perfume-empire.com at 4:36 PM CDT on July 7 (3 days before delivery). Perfume Empire issued an automated refusal at 4:23 AM on July 8 claiming processing.'),
        ('5. Physical Delivery Photo Audit (Overhead Camera, Security Bars & Abandoned Boxes):', 'The OnTrac delivery photo reveals key physical features: (a) A prominent overhead surveillance camera mounted above the door; (b) Heavy security bars/reinforced gate covering the entrance door; (c) Multiple uncollected boxes thrown about the doorstep as if nobody resides there / abandoned porch drop; and (d) A stark physical contrast to the neighboring door which has zero security bars or cameras.')
    ]

    for title, desc in points:
        story.append(Paragraph(f'<b>{title}</b> {desc}', b_style))

    doc.build(story)

sec0 = os.path.join(repo_dir, 'sec0.pdf')
create_summary_pdf(sec0)

sec1 = os.path.join(repo_dir, 'sec1.pdf')
sec2 = os.path.join(repo_dir, 'sec2.pdf')
sec3 = os.path.join(repo_dir, 'sec3.pdf')
sec4 = os.path.join(repo_dir, 'sec4.pdf')

def create_section_pdf(title, sub, text_bullets, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    NAVY = colors.HexColor('#0F2C59')
    DARK = colors.HexColor('#333333')

    t_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=14, leading=18, textColor=NAVY, fontName='Helvetica-Bold')
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=9.5, leading=12.5, textColor=DARK, fontName='Helvetica-Oblique')
    b_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=12, textColor=DARK, fontName='Helvetica', spaceAfter=5)

    story = []
    story.append(Paragraph(title, t_style))
    story.append(Paragraph(sub, sub_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY, spaceBefore=2, spaceAfter=6))

    for b in text_bullets:
        story.append(Paragraph(b, b_style))

    doc.build(story)

create_section_pdf(
    'SECTION 1: ORDER ORIGINATION & GEOGRAPHIC DISCREPANCY',
    'Order #PE270138 | July 7, 2026 at 12:53 PM CDT',
    [
        '<b>Geographic Anomaly:</b> My billing profile is anchored to Monroe, LA 71201. The fraudulent order was routed to 81 Keever Ct, San Jose, CA 95127.',
        '<b>Financial Facility:</b> Initiated via Affirm Pay-in-4 facility for 104.63 USD Total (95.55 merchandise + 9.08 tax).',
        '<i>Underlying order confirmation document displayed below:</i>'
    ],
    sec1
)

create_section_pdf(
    'SECTION 2: FARMERS BRANCH DC vs. PHYSICAL TENDER AUDIT',
    'Label Generated: July 7 at 1:27 PM CDT | Farmers Branch, TX 75234',
    [
        '<b>Fulfillment Origin:</b> Perfume Empire central warehouse at 3402 Garden Brook Dr, Farmers Branch, TX 75234.',
        '<b>Digital Manifest vs. Physical Tender:</b> Label generated at 1:27 PM was digital EDI data only. When I reported fraud to Affirm at 2:19 PM, the box was sitting static on the loading dock in Farmers Branch.',
        '<i>Underlying shipping label confirmation document displayed below:</i>'
    ],
    sec2
)

create_section_pdf(
    'SECTION 3: DESOTO ONTRAC HUB SCAN & 36.5-MILE TRANSIT DISTANCE AUDIT',
    'OnTrac Origin Scan: July 7 at 4:12 PM CDT | DeSoto, TX 75115',
    [
        '<b>Carrier Hub Location:</b> OnTrac regional hub at 802 E Centre Park Blvd, DeSoto, TX 75115.',
        '<b>36.5-Mile Highway Distance:</b> 36.5 miles via I-35E South between Farmers Branch DC (75234) and DeSoto Hub (75115).',
        '<b>165-Minute Staging Window:</b> I notified Affirm at 2:19 PM—nearly 2 hours before the box was driven 36.5 miles to DeSoto.',
        '<i>Underlying OnTrac tracking logs displayed below:</i>'
    ],
    sec3
)

create_section_pdf(
    'SECTION 4: PHYSICAL DELIVERY PHOTO AUDIT & MERCHANT REFUSAL',
    'Delivery: July 10 at 12:22 PM | San Jose, CA 95127',
    [
        '<b>Overhead Security Camera:</b> Prominent surveillance camera mounted directly above the doorway.',
        '<b>Security Bars on Door:</b> Heavy security bars/reinforced gate covering door, sharply contrasting with neighbor\'s unprotected door.',
        '<b>Multiple Abandoned Boxes:</b> Multiple boxes thrown about doorstep as if nobody resides there.',
        '<b>Merchant Non-Action:</b> I sent an urgent cancellation email July 7 at 4:36 PM; merchant issued an automated refusal July 8.',
        '<i>Underlying OnTrac delivery photo and email thread displayed below:</i>'
    ],
    sec4
)

reader_orig = PdfReader(orig_pdf)
merger = PdfWriter()

# Page 1: Master Summary in First-Person
for p in PdfReader(sec0).pages: merger.add_page(p)

# Section 1 + Order Email
for p in PdfReader(sec1).pages: merger.add_page(p)
merger.add_page(reader_orig.pages[0])

# Section 2 + Shipping Email
for p in PdfReader(sec2).pages: merger.add_page(p)
merger.add_page(reader_orig.pages[1])

# Section 3 + Tracking Logs
for p in PdfReader(sec3).pages: merger.add_page(p)
for i in [2, 3]: merger.add_page(reader_orig.pages[i])

# Section 4 + Delivery Photo & Email Thread
for p in PdfReader(sec4).pages: merger.add_page(p)
for i in [4, 5, 6, 7, 8]: merger.add_page(reader_orig.pages[i])

with open(dst_pdf, 'wb') as out:
    merger.write(out)

print("Rebuilt Document #2 in 100% first-person voice (I / me / my)!")

for f in [sec0, sec1, sec2, sec3, sec4]:
    if os.path.exists(f): os.remove(f)

subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Convert website narrative, timeline, and Document #2 PDF from third-person (consumer) to 100% first-person (I / me / my)'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
