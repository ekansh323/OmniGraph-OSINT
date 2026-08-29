"""
PDF Evidence Generation

Generates 6 PDF files using reportlab:
1. Financial statement (TechVentures Q1 2026)
2. Service contract (CryptoHoldings/OffshoreConsult)
3. Bank statement (Chen personal, June 2026)
4. Corporate filing (CryptoHoldings incorporation)
5. Invoice (PharmaCorp to Morgan Medical)
6. Email screenshot (Chen to Rodriguez)
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


def generate_financial_statement(output_dir: str, scenario):
    """Generate TechVentures LLC Q1 2026 Financial Statement"""
    filename = os.path.join(output_dir, "financial_statement_techventures_2026q1.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Header
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16)
    story.append(Paragraph("TechVentures LLC", title_style))
    story.append(Paragraph("Financial Statement - Q1 2026", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))

    # Company info
    story.append(Paragraph("<b>Registration:</b> DE-2024-887654", styles['Normal']))
    story.append(Paragraph("<b>Address:</b> 1500 Market St, Suite 2000, San Francisco, CA 94102", styles['Normal']))
    story.append(Paragraph("<b>CEO:</b> Marcus Chen", styles['Normal']))
    story.append(Paragraph("<b>CFO:</b> Sarah Rodriguez", styles['Normal']))
    story.append(Paragraph("<b>Period:</b> January 1 - March 31, 2026", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Revenue & Expenses Table
    data = [
        ['Revenue', '', 'Amount'],
        ['Product Sales', '', '$1,250,000'],
        ['Consulting Services', '', '$300,000'],
        ['Service Contracts', '', '$450,000'],
        ['<b>Total Revenue</b>', '', '<b>$2,000,000</b>'],
        ['', '', ''],
        ['Expenses', '', ''],
        ['Salaries & Benefits', '', '$650,000'],
        ['Office & Operations', '', '$180,000'],
        ['Consulting Services (Paid)', '', '$300,000'],
        ['Marketing', '', '$120,000'],
        ['Legal & Professional', '', '$85,000'],
        ['<b>Total Expenses</b>', '', '<b>$1,335,000</b>'],
        ['', '', ''],
        ['<b>Net Income</b>', '', '<b>$665,000</b>'],
    ]

    t = Table(data, colWidths=[3*inch, 1*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),
        ('LINEBELOW', (0, 11), (-1, 11), 1, colors.black),
        ('LINEBELOW', (0, 13), (-1, 13), 2, colors.black),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*inch))

    # Notes
    story.append(Paragraph("<b>Notes:</b>", styles['Heading3']))
    story.append(Paragraph("1. Consulting Services revenue reflects payments from CryptoHoldings Inc ($250,000) and other clients.", styles['Normal']))
    story.append(Paragraph("2. Consulting Services expense includes payments to offshore consultants.", styles['Normal']))
    story.append(Paragraph("3. CEO Marcus Chen holds 85% ownership, remaining 15% held by early investors.", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Signatures
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("_________________________", styles['Normal']))
    story.append(Paragraph("Marcus Chen, CEO", styles['Normal']))
    story.append(Paragraph("Date: April 15, 2026", styles['Normal']))

    doc.build(story)
    print(f"  ✓ Generated: {filename}")


def generate_contract(output_dir: str, scenario):
    """Generate Service Agreement between CryptoHoldings and OffshoreConsult"""
    filename = os.path.join(output_dir, "contract_cryptoholdings_offshore.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=14)
    story.append(Paragraph("SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Parties
    story.append(Paragraph("<b>PARTIES:</b>", styles['Heading3']))
    story.append(Paragraph("This Service Agreement (\"Agreement\") is entered into as of March 1, 2026, by and between:", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>CryptoHoldings Inc</b> (\"Client\")", styles['Normal']))
    story.append(Paragraph("450 Sutter St, Suite 1200, San Francisco, CA 94108", styles['Normal']))
    story.append(Paragraph("Registration: DE-2025-991234", styles['Normal']))
    story.append(Paragraph("Represented by: David Kim, Director", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("AND", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>OffshoreConsult Ltd</b> (\"Service Provider\")", styles['Normal']))
    story.append(Paragraph("789 Delaware Ave, Wilmington, DE 19801", styles['Normal']))
    story.append(Paragraph("Registration: DE-2025-003456", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Terms
    story.append(Paragraph("<b>1. SERVICES</b>", styles['Heading3']))
    story.append(Paragraph("Service Provider agrees to provide financial advisory and consulting services to Client for the management and optimization of digital asset portfolios.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>2. COMPENSATION</b>", styles['Heading3']))
    story.append(Paragraph("Client agrees to pay Service Provider a total fee of $280,000 USD for services rendered during the contract period.", styles['Normal']))
    story.append(Paragraph("Payment schedule: 50% upon signing ($140,000), 50% upon completion ($140,000).", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>3. TERM</b>", styles['Heading3']))
    story.append(Paragraph("This Agreement shall commence on March 1, 2026 and continue through August 31, 2026, unless terminated earlier in accordance with this Agreement.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>4. CONFIDENTIALITY</b>", styles['Normal']))
    story.append(Paragraph("Both parties agree to maintain confidentiality of all proprietary information shared during the term of this Agreement.", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Signatures
    story.append(Paragraph("<b>SIGNATURES:</b>", styles['Heading3']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("_________________________", styles['Normal']))
    story.append(Paragraph("David Kim, Director", styles['Normal']))
    story.append(Paragraph("CryptoHoldings Inc", styles['Normal']))
    story.append(Paragraph("Date: March 1, 2026", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("_________________________", styles['Normal']))
    story.append(Paragraph("Authorized Representative", styles['Normal']))
    story.append(Paragraph("OffshoreConsult Ltd", styles['Normal']))
    story.append(Paragraph("Date: March 1, 2026", styles['Normal']))

    doc.build(story)
    print(f"  ✓ Generated: {filename}")


def generate_bank_statement(output_dir: str, scenario):
    """Generate Marcus Chen personal bank statement for June 2026"""
    filename = os.path.join(output_dir, "bank_statement_chen_personal_202606.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Bank header
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=14, textColor=colors.HexColor('#003366'))
    story.append(Paragraph("FIRST NATIONAL BANK", title_style))
    story.append(Paragraph("1 Montgomery St, San Francisco, CA 94104", ParagraphStyle('Center', alignment=TA_CENTER, fontSize=10)))
    story.append(Spacer(1, 0.2*inch))

    # Account info
    story.append(Paragraph("<b>ACCOUNT STATEMENT</b>", styles['Heading2']))
    story.append(Paragraph("<b>Account Holder:</b> Marcus Chen", styles['Normal']))
    story.append(Paragraph("<b>Account Number:</b> ****1234", styles['Normal']))
    story.append(Paragraph("<b>Statement Period:</b> June 1 - June 30, 2026", styles['Normal']))
    story.append(Paragraph("<b>Address:</b> 2847 Pacific Ave, San Francisco, CA 94115", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Summary
    summary_data = [
        ['Opening Balance (June 1):', '$125,450.00'],
        ['Total Deposits:', '$285,000.00'],
        ['Total Withdrawals:', '$178,500.00'],
        ['<b>Closing Balance (June 30):</b>', '<b>$231,950.00</b>'],
    ]
    t = Table(summary_data, colWidths=[3*inch, 2*inch])
    t.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 2), (-1, 2), 1, colors.black),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))

    # Transactions
    story.append(Paragraph("<b>TRANSACTIONS:</b>", styles['Heading3']))
    trans_data = [
        ['Date', 'Description', 'Amount', 'Balance'],
        ['06/02', 'Deposit - Wire Transfer', '$9,500.00', '$134,950.00'],
        ['06/03', 'Transfer to S. Rodriguez', '-$9,500.00', '$125,450.00'],
        ['06/05', 'Deposit - Business', '$9,800.00', '$135,250.00'],
        ['06/06', 'Transfer to Account ***5678', '-$9,700.00', '$125,550.00'],
        ['06/08', 'Deposit - Wire Transfer', '$9,900.00', '$135,450.00'],
        ['06/10', 'Transfer to D. Kim', '-$9,200.00', '$126,250.00'],
        ['06/12', 'Deposit - Crypto Conversion', '$50,000.00', '$176,250.00'],
        ['06/15', 'Large Transfer In', '$260,000.00', '$436,250.00'],
        ['06/16', 'Transfer Out', '-$180,000.00', '$256,250.00'],
        ['06/18', 'Deposit', '$9,500.00', '$265,750.00'],
        ['06/20', 'Transfer to J. White', '-$9,600.00', '$256,150.00'],
        ['06/22', 'Transfer Out', '-$15,000.00', '$241,150.00'],
        ['06/25', 'Deposit', '$9,300.00', '$250,450.00'],
        ['06/28', 'Transfer to Rodriguez', '-$9,500.00', '$240,950.00'],
        ['06/30', 'Deposit', '$9,000.00', '$231,950.00'],
    ]

    t = Table(trans_data, colWidths=[0.8*inch, 3.2*inch, 1.2*inch, 1.3*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<i>For questions about your account, contact us at 1-800-555-BANK</i>", styles['Normal']))

    doc.build(story)
    print(f"  ✓ Generated: {filename}")


def generate_corporate_filing(output_dir: str, scenario):
    """Generate Delaware Certificate of Incorporation for CryptoHoldings Inc"""
    filename = os.path.join(output_dir, "corporate_filing_cryptoholdings.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # State seal placeholder
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16, textColor=colors.HexColor('#003366'))
    story.append(Paragraph("STATE OF DELAWARE", title_style))
    story.append(Paragraph("OFFICE OF THE SECRETARY OF STATE", ParagraphStyle('Center', alignment=TA_CENTER, fontSize=12)))
    story.append(Spacer(1, 0.3*inch))

    # Certificate title
    story.append(Paragraph("CERTIFICATE OF INCORPORATION", ParagraphStyle('CertTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=14)))
    story.append(Spacer(1, 0.2*inch))

    # Filing info
    story.append(Paragraph("<b>Filing Number:</b> DE-2025-991234", styles['Normal']))
    story.append(Paragraph("<b>Date Filed:</b> February 10, 2025", styles['Normal']))
    story.append(Paragraph("<b>Status:</b> Active - Good Standing", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Company details
    story.append(Paragraph("<b>1. NAME OF CORPORATION</b>", styles['Heading3']))
    story.append(Paragraph("The name of the corporation is CryptoHoldings Inc.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>2. REGISTERED OFFICE</b>", styles['Heading3']))
    story.append(Paragraph("The address of the registered office in the State of Delaware is:", styles['Normal']))
    story.append(Paragraph("450 Sutter St, Suite 1200", styles['Normal']))
    story.append(Paragraph("San Francisco, CA 94108", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>3. REGISTERED AGENT</b>", styles['Heading3']))
    story.append(Paragraph("The name of the registered agent at such address is:", styles['Normal']))
    story.append(Paragraph("<b>David Kim</b>", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>4. PURPOSE</b>", styles['Heading3']))
    story.append(Paragraph("The purpose of the corporation is to engage in cryptocurrency trading, digital asset management, and blockchain consulting services.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>5. AUTHORIZED SHARES</b>", styles['Heading3']))
    story.append(Paragraph("Total authorized shares: 10,000,000 shares of Common Stock, $0.001 par value per share.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>6. INCORPORATOR</b>", styles['Heading3']))
    story.append(Paragraph("The name and address of the incorporator is:", styles['Normal']))
    story.append(Paragraph("David Kim", styles['Normal']))
    story.append(Paragraph("450 Sutter St, Suite 1200, San Francisco, CA 94108", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Official stamp
    story.append(Paragraph("<b>FILED AND EFFECTIVE:</b> February 10, 2025", styles['Normal']))
    story.append(Paragraph("<i>This is a certified copy of the original Certificate of Incorporation filed with the Delaware Secretary of State.</i>", styles['Normal']))

    doc.build(story)
    print(f"  ✓ Generated: {filename}")


def generate_invoice(output_dir: str, scenario):
    """Generate PharmaCorp invoice to Morgan Medical"""
    filename = os.path.join(output_dir, "invoice_pharma_001234.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Invoice header
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0066cc'))
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 0.2*inch))

    # From/To
    from_to_data = [
        ['<b>FROM:</b>', '', '<b>INVOICE TO:</b>'],
        ['PharmaCorp Distributors', '', 'Morgan Medical Clinic'],
        ['1200 Industrial Pkwy', '', '789 Health Way'],
        ['San Jose, CA 95112', '', 'San Jose, CA 95110'],
        ['Phone: +1-408-555-0299', '', 'Attn: James Parker'],
        ['Tax ID: 94-1234567', '', 'Account: MED-45678'],
    ]
    t = Table(from_to_data, colWidths=[2.5*inch, 0.5*inch, 3*inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))

    # Invoice details
    invoice_info = [
        ['<b>Invoice Number:</b>', '001234'],
        ['<b>Date:</b>', 'May 15, 2026'],
        ['<b>Due Date:</b>', 'June 14, 2026'],
        ['<b>Payment Terms:</b>', 'Net 30'],
    ]
    t = Table(invoice_info, colWidths=[2*inch, 3*inch])
    story.append(t)
    story.append(Spacer(1, 0.2*inch))

    # Line items
    items_data = [
        ['Item Code', 'Description', 'Qty', 'Unit Price', 'Total'],
        ['MED-5501', 'Prescription Drug A (500mg)', '500', '$45.00', '$22,500.00'],
        ['MED-5502', 'Prescription Drug B (250mg)', '300', '$62.00', '$18,600.00'],
        ['MED-5503', 'Generic Antibiotic', '1000', '$12.50', '$12,500.00'],
        ['MED-5504', 'Pain Management Med', '250', '$78.00', '$19,500.00'],
        ['', '', '', '<b>Subtotal:</b>', '<b>$73,100.00</b>'],
        ['', '', '', 'Tax (8.25%):', '$6,030.75'],
        ['', '', '', '<b>TOTAL DUE:</b>', '<b>$79,130.75</b>'],
    ]
    t = Table(items_data, colWidths=[1.2*inch, 2.5*inch, 0.7*inch, 1.2*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('ALIGN', (2, 0), (4, -1), 'RIGHT'),
        ('LINEABOVE', (3, 4), (4, 4), 1, colors.black),
        ('LINEABOVE', (3, 6), (4, 6), 2, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*inch))

    # Payment instructions
    story.append(Paragraph("<b>PAYMENT INSTRUCTIONS:</b>", styles['Heading3']))
    story.append(Paragraph("Wire Transfer: Account ***6666, Chase Business Bank", styles['Normal']))
    story.append(Paragraph("Checks payable to: PharmaCorp Distributors", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<i>Thank you for your business!</i>", styles['Normal']))

    doc.build(story)
    print(f"  ✓ Generated: {filename}")


def generate_email_screenshot(output_dir: str, scenario):
    """Generate email screenshot from Chen to Rodriguez"""
    filename = os.path.join(output_dir, "email_screenshot_chen_rodriguez.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Email header (styled like email client)
    email_header_style = ParagraphStyle('EmailHeader', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#666666'))
    story.append(Paragraph("From: Marcus Chen &lt;mchen@techventures.com&gt;", email_header_style))
    story.append(Paragraph("To: Sarah Rodriguez &lt;srodriguez@techventures.com&gt;", email_header_style))
    story.append(Paragraph("Date: March 15, 2026 10:42 AM", email_header_style))
    story.append(Paragraph("Subject: Q1 Financial Arrangements", email_header_style))
    story.append(Spacer(1, 0.2*inch))

    # Email body
    story.append(Paragraph("Sarah,", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("We need to move the $850,000 through the CryptoHoldings account before end of quarter as discussed. The offshore arrangement with OffshoreConsult is now finalized.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Here's the sequence:", styles['Normal']))
    story.append(Paragraph("1. Transfer $300K from my personal account to TechVentures", styles['Normal']))
    story.append(Paragraph("2. TechVentures pays CryptoHoldings $300K as \"consulting fees\"", styles['Normal']))
    story.append(Paragraph("3. CryptoHoldings converts to crypto and sends to OffshoreConsult", styles['Normal']))
    story.append(Paragraph("4. Final conversion back through Pacific Trust", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("David Kim has the paperwork ready. Please coordinate with Jennifer White on the accounting treatment - it should show as normal business expenses.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Keep this confidential. The fewer people who know the full picture, the better.", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("- M. Chen", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Screenshot metadata
    story.append(Paragraph("<i>-- Email screenshot captured from investigation records --</i>", ParagraphStyle('Italic', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))

    doc.build(story)
    print(f"  ✓ Generated: {filename}")


def generate_all_documents(scenarios: dict):
    """Generate all PDF evidence files"""
    output_dir = "evidence/pdfs"
    os.makedirs(output_dir, exist_ok=True)

    scenario_1 = scenarios['scenario_1']
    scenario_2 = scenarios['scenario_2']

    print("Generating PDF evidence files...")
    generate_financial_statement(output_dir, scenario_1)
    generate_contract(output_dir, scenario_1)
    generate_bank_statement(output_dir, scenario_1)
    generate_corporate_filing(output_dir, scenario_1)
    generate_invoice(output_dir, scenario_2)
    generate_email_screenshot(output_dir, scenario_1)

    return [
        "financial_statement_techventures_2026q1.pdf",
        "contract_cryptoholdings_offshore.pdf",
        "bank_statement_chen_personal_202606.pdf",
        "corporate_filing_cryptoholdings.pdf",
        "invoice_pharma_001234.pdf",
        "email_screenshot_chen_rodriguez.pdf"
    ]


if __name__ == "__main__":
    from scenarios import load_scenarios
    scenarios = load_scenarios()
    generate_all_documents(scenarios)
