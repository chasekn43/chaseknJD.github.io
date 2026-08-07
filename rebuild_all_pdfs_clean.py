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
docs_dir = os.path.join(repo_dir, 'documents')

NAVY = colors.HexColor('#0F2C59')
DARK = colors.HexColor('#333333')
styles = getSampleStyleSheet()
t_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=14, leading=18, textColor=NAVY, fontName='Helvetica-Bold')
sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=9.5, leading=12.5, textColor=DARK, fontName='Helvetica-Oblique')
b_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=12, textColor=DARK, fontName='Helvetica', spaceAfter=5)

def create_section_pdf(title, sub, text_bullets, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []
    story.append(Paragraph(title, t_style))
    story.append(Paragraph(sub, sub_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY, spaceBefore=2, spaceAfter=6))
    for b in text_bullets:
        story.append(Paragraph(b, b_style))
    doc.build(story)

# 1. Rebuild CFPB_Complaint_and_Affirm_False_Response.pdf
cfpb_orig = os.path.join(desktop_dir, 'Initial CFPB Complaint_Affirm Reply_My Feedback_Follow-up CFPB Complaint.pdf')

sec1_cfpb = os.path.join(repo_dir, 'sec1_cfpb.pdf')
sec2_cfpb = os.path.join(repo_dir, 'sec2_cfpb.pdf')

create_section_pdf(
    'SECTION 1: FORMAL CFPB COMPLAINT FILING',
    'CFPB Complaint Case #260717-35668593 | Filed July 17, 2026',
    [
        '<b>Factual Allegations:</b> Submitted formal dispute detailing identity theft loan XQ8M-YX19, merchant refusal, front-line support negligence, and managing counsel directives.',
        '<b>Relief Sought:</b> Complete credit bureau reporting block, written liability discharge, and administrative account audit.',
        '<i>Underlying CFPB Complaint Detail report displayed below:</i>'
    ],
    sec1_cfpb
)

create_section_pdf(
    'SECTION 2: AFFIRM FALSE WRITTEN RESPONSE & EXECUTIVE OUTREACH',
    'Response Date: July 20, 2026 | Submitted to Federal Database',
    [
        '<b>False Material Disclosures:</b> Affirm falsely claimed to federal regulators that I was "in direct communication with merchant" and falsely implied merchant resolution.',
        '<b>Contradictory Legal Demands:</b> Submitted 3.5 hours after Andy Chen threatened a corporate countersuit and demanded phone-only communication.',
        '<i>Underlying Affirm CFPB Response and executive emails displayed below:</i>'
    ],
    sec2_cfpb
)

reader_cfpb = PdfReader(cfpb_orig)
merger_cfpb = PdfWriter()

# Section 1 + Complaint Detail pages (pages 0..5)
merger_cfpb.add_page(PdfReader(sec1_cfpb).pages[0])
for i in range(0, 6): merger_cfpb.add_page(reader_cfpb.pages[i])

# Section 2 + Response pages (pages 6..end)
merger_cfpb.add_page(PdfReader(sec2_cfpb).pages[0])
for i in range(6, len(reader_cfpb.pages)): merger_cfpb.add_page(reader_cfpb.pages[i])

dst_cfpb = os.path.join(docs_dir, 'CFPB_Complaint_and_Affirm_False_Response.pdf')
with open(dst_cfpb, 'wb') as out: merger_cfpb.write(out)

# 2. Rebuild Louisiana_AG_Dispute_Submission.pdf
la_orig = os.path.join(desktop_dir, 'Email to Louisiana AG.pdf')
sec1_la = os.path.join(repo_dir, 'sec1_la.pdf')

create_section_pdf(
    'LOUISIANA ATTORNEY GENERAL DISPUTE SUBMISSION',
    'State Filing | Protection Division | AG Liz Murrill',
    [
        '<b>State Jurisdiction:</b> Submitted formal complaint to LA Attorney General Liz Murrill regarding unfair credit reporting and identity theft handling affecting Louisiana residents.',
        '<b>Executive Notice:</b> Executive outreach transmitted to Affirm C-suite and Managing Counsel.',
        '<i>Underlying Louisiana AG dispute submission document displayed below:</i>'
    ],
    sec1_la
)

reader_la = PdfReader(la_orig)
merger_la = PdfWriter()
merger_la.add_page(PdfReader(sec1_la).pages[0])
for p in reader_la.pages: merger_la.add_page(p)

dst_la = os.path.join(docs_dir, 'Louisiana_AG_Dispute_Submission.pdf')
with open(dst_la, 'wb') as out: merger_la.write(out)

# 3. Rebuild Morgan_Lewis_Correspondence.pdf
ml_orig = os.path.join(desktop_dir, 'Gmail - Re_ Affirm Account _ Payments & Representation Clarification.pdf')
sec1_ml = os.path.join(repo_dir, 'sec1_ml.pdf')

create_section_pdf(
    'MORGAN, LEWIS & BOCKIUS LLP LEGAL CORRESPONDENCE',
    'Outside Legal Counsel for Affirm, Inc. | Madison Marshall Outreach (July 24, 2026 at 4:34 PM CDT)',
    [
        '<b>Initial Outreach (July 24 at 4:34 PM CDT):</b> Outreach from Madison Marshall of Morgan Lewis on behalf of Affirm, Inc. (her one and only email before going radio-silent).',
        '<b>Rule 4.2 Ethics Notice (Aug 6):</b> Formal ethics notice sent to outside counsel directing all future communications through designated legal channels.',
        '<i>Underlying legal correspondence displayed below:</i>'
    ],
    sec1_ml
)

reader_ml = PdfReader(ml_orig)
merger_ml = PdfWriter()
merger_ml.add_page(PdfReader(sec1_ml).pages[0])
for p in reader_ml.pages: merger_ml.add_page(p)

dst_ml = os.path.join(docs_dir, 'Morgan_Lewis_Correspondence.pdf')
with open(dst_ml, 'wb') as out: merger_ml.write(out)

# Clean up temp files
for f in [sec1_cfpb, sec2_cfpb, sec1_la, sec1_ml]:
    if os.path.exists(f): os.remove(f)

# Git add, commit, push
subprocess.run(['git', 'add', '-A'], cwd=repo_dir)
subprocess.run(['git', 'commit', '-m', 'Rebuild all generated PDF cover and section pages to enforce 100% first-person voice (I / me / my) with zero third-person consumer references'], cwd=repo_dir)
p = subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_dir, capture_output=True, text=True)
print("Git push stdout:", p.stdout)
print("Git push stderr:", p.stderr)
