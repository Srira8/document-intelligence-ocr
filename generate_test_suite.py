
"""
Generate multiple test invoices with different scenarios
Tests various edge cases and formats
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from datetime import datetime, timedelta
import random
import os

def generate_simple_invoice(filename):
    """Simple invoice with minimal formatting"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("TechCo Solutions", styles['Heading1']))
    story.append(Paragraph("456 Tech Drive, Seattle, WA 98101", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph(f"Invoice: INV-{random.randint(1000, 9999)}", styles['Heading2']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Bill To: Customer ABC Inc", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Simple items
    items_data = [
        ['Item', 'Quantity', 'Price', 'Total'],
        ['Web Development', '1', '$5,000.00', '$5,000.00'],
        ['Hosting (Annual)', '1', '$1,200.00', '$1,200.00'],
    ]
    
    items_table = Table(items_data)
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Total: $6,200.00", styles['Heading2']))
    
    doc.build(story)
    print(f"✅ Generated: {filename}")


def generate_complex_invoice(filename):
    """Complex invoice with many line items"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("Global Services Ltd", styles['Heading1']))
    story.append(Paragraph("789 Enterprise Blvd, Boston, MA 02101", styles['Normal']))
    story.append(Paragraph("Tax ID: 12-3456789", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph(f"INVOICE #{random.randint(10000, 99999)}", styles['Heading2']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Many line items
    items_data = [
        ['#', 'Description', 'Qty', 'Rate', 'Amount'],
        ['1', 'Consulting Hours - Senior', '120', '$200', '$24,000'],
        ['2', 'Consulting Hours - Junior', '80', '$100', '$8,000'],
        ['3', 'Software License', '5', '$500', '$2,500'],
        ['4', 'Training Sessions', '3', '$1,500', '$4,500'],
        ['5', 'Support Contract (6 months)', '1', '$3,000', '$3,000'],
        ['6', 'Travel Expenses', '1', '$2,400', '$2,400'],
        ['7', 'Equipment Rental', '2', '$800', '$1,600'],
    ]
    
    items_table = Table(items_data, colWidths=[0.4*inch, 3*inch, 0.6*inch, 0.8*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.2*inch))
    
    totals_data = [
        ['', 'Subtotal:', '$46,000.00'],
        ['', 'Tax (10%):', '$4,600.00'],
        ['', 'TOTAL:', '$50,600.00'],
    ]
    
    totals_table = Table(totals_data, colWidths=[3*inch, 1*inch, 1*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONT', (1, 2), (-1, 2), 'Helvetica-Bold'),
        ('LINEABOVE', (1, 2), (-1, 2), 2, colors.black),
    ]))
    story.append(totals_table)
    
    doc.build(story)
    print(f"✅ Generated: {filename}")


def generate_receipt_style(filename):
    """Receipt-style invoice (like from a store)"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    center_style = ParagraphStyle('Center', parent=styles['Normal'], alignment=TA_CENTER)
    
    story.append(Paragraph("QuickMart Store #42", center_style))
    story.append(Paragraph("123 Main Street", center_style))
    story.append(Paragraph("Anytown, ST 12345", center_style))
    story.append(Paragraph("Tel: (555) 987-6543", center_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("=" * 50, center_style))
    story.append(Paragraph("RECEIPT", center_style))
    story.append(Paragraph("=" * 50, center_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(f"Date: {datetime.now().strftime('%m/%d/%Y %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"Receipt #: {random.randint(100000, 999999)}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    items_data = [
        ['Item', 'Qty', 'Price'],
        ['Office Supplies - Paper', '3', '$45.00'],
        ['Pens (Box)', '2', '$12.00'],
        ['Stapler', '1', '$8.99'],
        ['Filing Cabinet', '1', '$159.99'],
        ['Desk Lamp', '1', '$34.99'],
    ]
    
    items_table = Table(items_data, colWidths=[3*inch, 0.8*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Subtotal: $260.97", styles['Normal']))
    story.append(Paragraph("Tax: $20.88", styles['Normal']))
    story.append(Paragraph("TOTAL: $281.85", styles['Heading3']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Payment Method: VISA ****1234", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Thank you for shopping with us!", center_style))
    
    doc.build(story)
    print(f"✅ Generated: {filename}")


def generate_international_invoice(filename):
    """Invoice with international format (EUR)"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("EuroTech GmbH", styles['Heading1']))
    story.append(Paragraph("Hauptstraße 123, 10115 Berlin, Germany", styles['Normal']))
    story.append(Paragraph("VAT: DE123456789", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph(f"Invoice No: EU-{random.randint(1000, 9999)}", styles['Heading2']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%d.%m.%Y')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    items_data = [
        ['Position', 'Description', 'Quantity', 'Price', 'Total'],
        ['1', 'Software Development', '40h', '€80.00', '€3,200.00'],
        ['2', 'Project Management', '10h', '€100.00', '€1,000.00'],
        ['3', 'Server Hosting', '1', '€500.00', '€500.00'],
    ]
    
    items_table = Table(items_data)
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Netto: €4,700.00", styles['Normal']))
    story.append(Paragraph("MwSt (19%): €893.00", styles['Normal']))
    story.append(Paragraph("Brutto: €5,593.00", styles['Heading2']))
    
    doc.build(story)
    print(f"✅ Generated: {filename}")


def generate_minimal_invoice(filename):
    """Very minimal invoice - tests basic extraction"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("SimpleServe", styles['Title']))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph(f"Invoice: {random.randint(1, 999)}", styles['Heading1']))
    story.append(Paragraph(f"{datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("Service: Web Design", styles['Normal']))
    story.append(Paragraph("Amount: $2,500.00", styles['Heading2']))
    
    doc.build(story)
    print(f"✅ Generated: {filename}")


def main():
    """Generate all test invoices"""
    print("=" * 60)
    print("🧪 Generating Test Invoice Suite")
    print("=" * 60)
    print()
    
    # Create test_invoices directory
    os.makedirs("test_invoices", exist_ok=True)
    
    # Generate different invoice types
    generate_simple_invoice("test_invoices/01_simple_invoice.pdf")
    generate_complex_invoice("test_invoices/02_complex_invoice.pdf")
    generate_receipt_style("test_invoices/03_receipt_style.pdf")
    generate_international_invoice("test_invoices/04_international_eur.pdf")
    generate_minimal_invoice("test_invoices/05_minimal_invoice.pdf")
    
    print()
    print("=" * 60)
    print("✅ Generated 5 test invoices in 'test_invoices/' folder")
    print("=" * 60)
    print()
    print("📝 Test these with your API:")
    print("   1. Simple invoice - Basic fields")
    print("   2. Complex invoice - Many line items")
    print("   3. Receipt style - Store format")
    print("   4. International - EUR currency")
    print("   5. Minimal - Very basic")
    print()
    print("💡 Upload them at: http://localhost:8000")
    print("   Or test via CLI: python test_api.py test_invoices/01_simple_invoice.pdf")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Error: reportlab not installed")
        print("   Install it with: pip install reportlab")
    except Exception as e:
        print(f"❌ Error: {e}")
