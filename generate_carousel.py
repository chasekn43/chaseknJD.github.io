import os, shutil
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350

# Colors
BG_DARK = (11, 15, 25)
BG_CARD = (20, 29, 46)
BG_CARD_ALT = (26, 38, 59)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (203, 213, 225)
ACCENT_BLUE = (56, 189, 248)
ACCENT_CYAN = (14, 165, 233)
ACCENT_AMBER = (251, 191, 36)
ACCENT_RED = (248, 113, 113)
BORDER_COLOR = (51, 65, 85)

def get_font(size, bold=False):
    font_names = ['segoeuib.ttf' if bold else 'segoeui.ttf', 'arialbd.ttf' if bold else 'arial.ttf']
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except:
            pass
    return ImageFont.load_default()

def draw_header_footer(draw, slide_num, total_slides=6):
    draw.rounded_rectangle([60, 45, 430, 90], radius=8, fill=(26, 38, 57), outline=(56, 189, 248), width=1)
    draw.text((75, 56), 'FINTECH CASE STUDY', font=get_font(20, bold=True), fill=ACCENT_BLUE)
    
    page_str = f'{slide_num} / {total_slides}'
    draw.text((W - 140, 56), page_str, font=get_font(22, bold=True), fill=TEXT_MUTED)
    
    draw.line([(60, H - 85), (W - 60, H - 85)], fill=BORDER_COLOR, width=1)
    draw.text((60, H - 60), 'kinslow-regulatory-archive.org', font=get_font(22, bold=True), fill=ACCENT_BLUE)
    draw.text((W - 380, H - 60), 'Charles W. Kinslow IV, JD, CPA', font=get_font(20), fill=TEXT_MUTED)

slides = []

# ==================== SLIDE 1: COVER ====================
img1 = Image.new('RGB', (W, H), BG_DARK)
d1 = ImageDraw.Draw(img1)

d1.rounded_rectangle([60, 140, W - 60, H - 120], radius=24, fill=BG_CARD, outline=BORDER_COLOR, width=2)
d1.rounded_rectangle([100, 190, 420, 240], radius=8, fill=(14, 165, 233, 40), outline=ACCENT_BLUE, width=1)
d1.text((120, 202), 'REAL-WORLD CASE STUDY', font=get_font(18, bold=True), fill=ACCENT_BLUE)

d1.text((100, 280), 'How an 86-Minute\nBot Denial Exposed\na $214M Glitch', font=get_font(60, bold=True), fill=TEXT_WHITE, spacing=14)
d1.text((100, 500), 'What really happens when a $10B fintech\'s\nautomated plumbing breaks down.', font=get_font(30, bold=True), fill=ACCENT_AMBER, spacing=10)

d1.line([(100, 610), (W - 100, 610)], fill=BORDER_COLOR, width=2)

bullets1 = [
    '• Step 1: Criminal fraud reported with police report',
    '• Step 2: Automated bot denies dispute in 86 minutes',
    '• Step 3: Execs admit fraud in writing... then lock the app',
    '• Step 4: How we bypassed the lockout with Federal ACH'
]
y = 650
for b in bullets1:
    d1.text((100, y), b, font=get_font(25), fill=TEXT_MUTED)
    y += 65

d1.rounded_rectangle([100, H - 260, W - 100, H - 160], radius=16, fill=BG_CARD_ALT, outline=ACCENT_BLUE, width=2)
d1.text((160, H - 225), 'Swipe to see the evidence & paper trail  →', font=get_font(26, bold=True), fill=TEXT_WHITE)

draw_header_footer(d1, 1)
slides.append(img1)

# ==================== SLIDE 2: THE BOT DENIAL ====================
img2 = Image.new('RGB', (W, H), BG_DARK)
d2 = ImageDraw.Draw(img2)
d2.text((60, 130), '01 / The 86-Minute Investigation', font=get_font(38, bold=True), fill=TEXT_WHITE)

d2.rounded_rectangle([60, 200, W - 60, 420], radius=20, fill=BG_CARD, outline=ACCENT_RED, width=2)
d2.text((100, 230), '86 MINUTES', font=get_font(72, bold=True), fill=ACCENT_RED)
d2.text((100, 325), 'From Police Report Submission to Automated Bot Denial', font=get_font(26, bold=True), fill=TEXT_WHITE)
d2.text((100, 365), 'Monroe Police Incident Report #26-29572 + OnTrac Carrier Tracking', font=get_font(21), fill=TEXT_MUTED)

d2.rounded_rectangle([60, 455, W - 60, 725], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d2.text((90, 480), 'The Obvious Fraud', font=get_font(28, bold=True), fill=ACCENT_BLUE)
b2_a = (
    'Carrier tracking showed the package was delivered to an address\n'
    'in California—over 2,000 miles away from Monroe, Louisiana.\n'
    'A human would have caught this in 10 seconds.'
)
d2.text((90, 535), b2_a, font=get_font(23), fill=TEXT_MUTED, spacing=8)

d2.rounded_rectangle([60, 755, W - 60, 1025], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d2.text((90, 780), 'The Bot Reality', font=get_font(28, bold=True), fill=ACCENT_AMBER)
b2_b = (
    'No human investigator opened the police PDF.\n'
    'The dispute was run through an automated filter designed\n'
    'to close claims instantly and protect merchant transaction fees.'
)
d2.text((90, 835), b2_b, font=get_font(23), fill=TEXT_MUTED, spacing=8)

draw_header_footer(d2, 2)
slides.append(img2)

# ==================== SLIDE 3: THE LOCKOUT PARADOX ====================
img3 = Image.new('RGB', (W, H), BG_DARK)
d3 = ImageDraw.Draw(img3)
d3.text((60, 130), '02 / Winning The Dispute, Losing The App', font=get_font(38, bold=True), fill=TEXT_WHITE)

d3.rounded_rectangle([60, 200, W - 60, 430], radius=20, fill=BG_CARD, outline=ACCENT_AMBER, width=2)
d3.text((100, 230), 'THE PARADOX', font=get_font(36, bold=True), fill=ACCENT_AMBER)
d3.text((100, 285), 'July 16: Execs admit fraud in writing ($0 balance)\nJuly 17: Legal directs staff to LOCK the account', font=get_font(26, bold=True), fill=TEXT_WHITE, spacing=8)
d3.text((100, 365), 'Directive issued by Managing Counsel Andy Chen.', font=get_font(21), fill=TEXT_MUTED)

d3.rounded_rectangle([60, 465, W - 60, 735], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d3.text((90, 490), 'Why Did They Lock It?', font=get_font(28, bold=True), fill=ACCENT_BLUE)
b3_a = (
    'Because the charge was on a single-use virtual card, their backend\n'
    'ledger couldn\'t route the refund properly. Instead of fixing their\n'
    'accounting glitch, they froze the entire user account.'
)
d3.text((90, 545), b3_a, font=get_font(23), fill=TEXT_MUTED, spacing=8)

d3.rounded_rectangle([60, 765, W - 60, 1035], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d3.text((90, 790), 'The Trap', font=get_font(28, bold=True), fill=ACCENT_RED)
b3_b = (
    'Locking the app disabled payment buttons for OTHER active, on-time\n'
    'loans. Meanwhile, automated collection emails fired daily\n'
    'threatening late fees on loans they wouldn\'t let me pay!'
)
d3.text((90, 845), b3_b, font=get_font(23), fill=TEXT_MUTED, spacing=8)

draw_header_footer(d3, 3)
slides.append(img3)

# ==================== SLIDE 4: THE MACRO TRUTH ====================
img4 = Image.new('RGB', (W, H), BG_DARK)
d4 = ImageDraw.Draw(img4)
d4.text((60, 130), '03 / What BNPL Pitch Decks Don\'t Show', font=get_font(38, bold=True), fill=TEXT_WHITE)

d4.rounded_rectangle([60, 200, 520, 410], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d4.text((90, 225), '$13.8 Billion', font=get_font(42, bold=True), fill=ACCENT_BLUE)
d4.text((90, 285), 'Q2 2026 Gross Volume\n(+35% Expansion)', font=get_font(21), fill=TEXT_MUTED, spacing=6)

d4.rounded_rectangle([560, 200, W - 60, 410], radius=16, fill=BG_CARD, outline=ACCENT_RED, width=1)
d4.text((590, 225), '$214 Million', font=get_font(42, bold=True), fill=ACCENT_RED)
d4.text((590, 285), 'Credit Loss Provisions\n(+40% YoY Spike)', font=get_font(21), fill=TEXT_MUTED, spacing=6)

d4.rounded_rectangle([60, 445, W - 60, 725], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d4.text((90, 470), 'The 71% Interest Reality', font=get_font(28, bold=True), fill=ACCENT_AMBER)
b4_a = (
    '• BNPL is marketed as "interest-free 0% Pay-in-4".\n'
    '• In reality, 71% of Affirm\'s loan volume carries interest.\n'
    '• Only 13% of installment volume is actually 0% interest.\n'
    '• APRs reach up to 36.99%—higher than most credit cards.'
)
d4.text((90, 525), b4_a, font=get_font(23), fill=TEXT_MUTED, spacing=8)

d4.rounded_rectangle([60, 755, W - 60, 1035], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d4.text((90, 780), 'Why The CFPB Is Stepping In', font=get_font(28, bold=True), fill=TEXT_WHITE)
b4_b = (
    'Federal regulators are closing the loophole: BNPL lenders are\n'
    'being classified under Regulation Z rules—forcing them to provide\n'
    'the same 60-day billing dispute rights as traditional credit cards.'
)
d4.text((90, 835), b4_b, font=get_font(23), fill=TEXT_MUTED, spacing=8)

draw_header_footer(d4, 4)
slides.append(img4)

# ==================== SLIDE 5: CONSUMER SURVIVAL PLAYBOOK ====================
img5 = Image.new('RGB', (W, H), BG_DARK)
d5 = ImageDraw.Draw(img5)
d5.text((60, 130), '04 / How To Protect Yourself (3 Steps)', font=get_font(38, bold=True), fill=TEXT_WHITE)

d5.rounded_rectangle([60, 200, W - 60, 440], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d5.text((90, 225), '1. Bypass App Lockouts with External Bank BillPay', font=get_font(26, bold=True), fill=ACCENT_BLUE)
b5_a = (
    'If an app locks you out, route payments directly from your bank\'s\n'
    'Online BillPay to Affirm\'s corporate ACH Lockbox. This creates an\n'
    'airtight Federal Reserve payment record they cannot dispute.'
)
d5.text((90, 275), b5_a, font=get_font(21), fill=TEXT_MUTED, spacing=5)

d5.rounded_rectangle([60, 470, W - 60, 710], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d5.text((90, 495), '2. Get Sworn Police & Carrier Proof (POD)', font=get_font(26, bold=True), fill=ACCENT_AMBER)
b5_b = (
    'Chatbots ignore chat logs. They cannot legally ignore official\n'
    'police reports and certified delivery affidavits from UPS/FedEx/OnTrac.\n'
    'Always get the physical paper trail.'
)
d5.text((90, 545), b5_b, font=get_font(21), fill=TEXT_MUTED, spacing=5)

d5.rounded_rectangle([60, 740, W - 60, 980], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
d5.text((90, 765), '3. File a CFPB Complaint with Receipts', font=get_font(26, bold=True), fill=(56, 189, 248))
b5_c = (
    'When lenders give misleading responses to federal regulators,\n'
    'rebut them directly with your evidence. False statements to federal\n'
    'agencies carry severe penalties under 18 U.S.C. § 1001.'
)
d5.text((90, 815), b5_c, font=get_font(21), fill=TEXT_MUTED, spacing=5)

draw_header_footer(d5, 5)
slides.append(img5)

# ==================== SLIDE 6: CTA ====================
img6 = Image.new('RGB', (W, H), BG_DARK)
d6 = ImageDraw.Draw(img6)
d6.text((60, 130), '05 / Read The Full Investigation', font=get_font(38, bold=True), fill=TEXT_WHITE)

d6.rounded_rectangle([60, 200, W - 60, 760], radius=24, fill=BG_CARD, outline=ACCENT_BLUE, width=2)
d6.text((100, 240), 'Open-Source Regulatory Archive', font=get_font(34, bold=True), fill=ACCENT_BLUE)

docs = [
    '✓ Certified Monroe Police Incident Report #26-29572',
    '✓ Internal Affirm Managing Counsel Directives & Emails',
    '✓ California Dept of Justice Determination Letters',
    '✓ SEC Form TCR Whistleblower Intake #17867-223-108-883',
    '✓ Interactive Dispute Readiness & Legal Demand Generators'
]
y = 310
for doc in docs:
    d6.text((100, y), doc, font=get_font(23), fill=TEXT_MUTED)
    y += 62

d6.rounded_rectangle([100, 790, W - 100, 980], radius=20, fill=BG_CARD_ALT, outline=ACCENT_AMBER, width=2)
d6.text((140, 820), 'Read the full case study & evidence vault at:', font=get_font(22), fill=TEXT_MUTED)
d6.text((140, 865), 'kinslow-regulatory-archive.org', font=get_font(42, bold=True), fill=ACCENT_AMBER)

d6.text((100, 1030), 'Charles W. Kinslow IV, J.D., C.P.A. | ORCID: 0009-0002-8851-7890', font=get_font(21), fill=TEXT_MUTED)

draw_header_footer(d6, 6)
slides.append(img6)

pdf_path = 'Anatomy_of_a_Fintech_Dispute_Carousel.pdf'
slides[0].save(pdf_path, 'PDF', resolution=100.0, save_all=True, append_images=slides[1:])
print(f'Successfully re-generated {pdf_path} ({os.path.getsize(pdf_path)/1024:.1f} KB)')

for target in [os.path.expanduser('~/Desktop'), os.path.expanduser('~/Downloads')]:
    shutil.copy(pdf_path, target)
print('Updated PDF copied to Desktop and Downloads!')
