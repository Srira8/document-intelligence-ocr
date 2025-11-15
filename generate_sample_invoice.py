"""
Generate a sample invoice PDF for testing
Requires: pip install reportlab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from datetime import datetime, timedelta
import random

def generate_sample_invoice(filename="sample_invoice.pdf"):
    """Generate a realistic sample invoice PDF"""
    
    # Create PDF
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    right_align = ParagraphStyle(
        'RightAlign',
        parent=styles['Normal'],
        alignment=TA_RIGHT
    )
    
    # Company Header
    story.append(Paragraph("ACME Corporation", title_style))
    story.append(Paragraph("123 Business Street", styles['Normal']))
    story.append(Paragraph("New York, NY 10001", styles['Normal']))
    story.append(Paragraph("Phone: (555) 123-4567", styles['Normal']))
    story.append(Paragraph("Email: billing@acmecorp.com", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Invoice title
    invoice_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#e74c3c')
    )
    story.append(Paragraph("INVOICE", invoice_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Invoice details
    invoice_num = f"INV-2024-{random.randint(1000, 9999)}"
    invoice_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    details_data = [
        ['Invoice Number:', invoice_num],
        ['Invoice Date:', invoice_date],
        ['Due Date:', due_date],
        ['Payment Terms:', 'Net 30'],
    ]
    
    details_table = Table(details_data, colWidths=[2*inch, 2*inch])
    details_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONT', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Bill To
    story.append(Paragraph("<b>Bill To:</b>", styles['Normal']))
    story.append(Paragraph("Tech Innovations LLC", styles['Normal']))
    story.append(Paragraph("456 Client Avenue", styles['Normal']))
    story.append(Paragraph("San Francisco, CA 94102", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Line Items
    items_data = [
        ['Item', 'Description', 'Qty', 'Unit Price', 'Total'],
        ['1', 'Professional Services - Consulting', '40', '$150.00', '$6,000.00'],
        ['2', 'Software Development', '80', '$125.00', '$10,000.00'],
        ['3', 'Project Management', '20', '$100.00', '$2,000.00'],
        ['4', 'Technical Support (Monthly)', '1', '$500.00', '$500.00'],
    ]
    
    items_table = Table(items_data, colWidths=[0.5*inch, 3*inch, 0.7*inch, 1.2*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Body
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Totals
    totals_data = [
        ['', '', 'Subtotal:', '$18,500.00'],
        ['', '', 'Tax (8.5%):', '$1,572.50'],
        ['', '', '<b>Total Due:</b>', '<b>$20,072.50</b>'],
    ]
    
    totals_table = Table(totals_data, colWidths=[0.5*inch, 3*inch, 1.9*inch, 1.2*inch])
    totals_table.setStyle(TableStyle([
        ('FONT', (2, 0), (2, 1), 'Helvetica'),
        ('FONT', (2, 2), (2, 2), 'Helvetica-Bold'),
        ('FONT', (3, 0), (3, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (2, 0), (-1, -1), 10),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('LINEABOVE', (2, 2), (-1, 2), 2, colors.black),
        ('BACKGROUND', (2, 2), (-1, 2), colors.HexColor('#ecf0f1')),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Payment info
    story.append(Paragraph("<b>Payment Information:</b>", styles['Normal']))
    story.append(Paragraph("Bank: First National Bank", styles['Normal']))
    story.append(Paragraph("Account Number: 123456789", styles['Normal']))
    story.append(Paragraph("Routing Number: 987654321", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Paragraph("Thank you for your business!", styles['Normal']))
    story.append(Paragraph("For questions, contact: billing@acmecorp.com", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Sample invoice generated: {filename}")
    return filename


if __name__ == "__main__":
    try:
        filename = generate_sample_invoice()
        print(f"\n📄 You can now test the API with this invoice:")
        print(f"   Upload it via the web UI at http://localhost:8000")
        print(f"   Or use: python test_api.py {filename}")
    except ImportError:
        print("❌ Error: reportlab not installed")
        print("   Install it with: pip install reportlab")
    except Exception as e:
        print(f"❌ Error generating invoice: {e}")