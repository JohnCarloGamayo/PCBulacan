"""
PDF Receipt Generator for Orders
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import io


def generate_order_receipt_pdf(order):
    """
    Generate a beautiful PDF receipt for an order
    """
    # Create a BytesIO buffer
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#475569'),
        spaceAfter=6,
    )
    
    # Add company header
    company_name = Paragraph("<b>PCBulacan</b>", title_style)
    elements.append(company_name)
    
    tagline = Paragraph("Your Premium PC Components Store", normal_style)
    elements.append(tagline)
    elements.append(Spacer(1, 0.3*inch))
    
    # Add receipt title with order number
    receipt_title = Paragraph(f"<b>ORDER RECEIPT</b><br/><font size=12>#{order.order_number}</font>", 
                             ParagraphStyle('ReceiptTitle', parent=title_style, fontSize=18))
    elements.append(receipt_title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Order information section
    order_info = [
        ["Order Date:", order.created_at.strftime("%B %d, %Y %I:%M %p")],
        ["Status:", order.get_status_display().upper()],
        ["Payment Method:", order.payment_method.upper()],
    ]
    
    order_info_table = Table(order_info, colWidths=[2*inch, 4*inch])
    order_info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(order_info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Customer information
    elements.append(Paragraph("Customer Information", heading_style))
    
    customer_info = [
        ["Name:", order.full_name],
        ["Email:", order.email],
        ["Phone:", order.phone or "Not provided"],
    ]
    
    customer_table = Table(customer_info, colWidths=[2*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Shipping address
    elements.append(Paragraph("Shipping Address", heading_style))
    
    address_data = [
        [order.address],
        [f"{order.city}, {order.state} {order.zip_code}"],
    ]
    
    address_table = Table(address_data, colWidths=[6*inch])
    address_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(address_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Order items
    elements.append(Paragraph("Order Items", heading_style))
    
    # Items table header
    items_data = [['Product', 'Price', 'Qty', 'Total']]
    
    # Add order items
    for item in order.items.all():
        items_data.append([
            item.product.name,
            f"₱{item.price:,.2f}",
            str(item.quantity),
            f"₱{item.item_total:,.2f}"
        ])
    
    items_table = Table(items_data, colWidths=[3.5*inch, 1*inch, 0.7*inch, 1.3*inch])
    items_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2563eb')),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Order summary
    summary_data = [
        ['Subtotal:', f"₱{order.total - (order.shipping_cost or 0):,.2f}"],
        ['Shipping Fee:', f"₱{order.shipping_cost or 0:,.2f}"],
        ['', ''],  # Spacer row
        ['TOTAL:', f"₱{order.total:,.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        # Regular rows
        ('FONTNAME', (0, 0), (0, 1), 'Helvetica'),
        ('FONTNAME', (1, 0), (1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 1), 10),
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.HexColor('#64748b')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        
        # Total row
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 3), (-1, 3), 14),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.HexColor('#2563eb')),
        ('LINEABOVE', (0, 3), (-1, 3), 2, colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 3), (-1, 3), 12),
        
        # Padding
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, 2), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=normal_style,
        fontSize=9,
        textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER,
    )
    
    footer_text = """
    <b>Thank you for your order!</b><br/>
    For questions or concerns, please contact us at support@pcbulacan.com<br/>
    <br/>
    <i>This is a computer-generated receipt and does not require a signature.</i>
    """
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
