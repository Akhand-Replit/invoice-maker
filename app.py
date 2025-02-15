import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Function to generate PDF
def generate_invoice_pdf(invoice_data, items):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Invoice")
    
    # Business details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Business: {invoice_data['business_name']}")
    c.drawString(50, height - 120, f"Address: {invoice_data['business_address']}")
    c.drawString(50, height - 140, f"Email: {invoice_data['business_email']}")
    
    # Client details
    c.drawString(50, height - 180, f"Bill To: {invoice_data['client_name']}")
    c.drawString(50, height - 200, f"Client Address: {invoice_data['client_address']}")
    c.drawString(50, height - 220, f"Client Email: {invoice_data['client_email']}")
    
    # Invoice details
    c.drawString(400, height - 100, f"Invoice No: {invoice_data['invoice_number']}")
    c.drawString(400, height - 120, f"Date: {invoice_data['invoice_date']}")
    
    # Table header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 260, "Description")
    c.drawString(250, height - 260, "Quantity")
    c.drawString(350, height - 260, "Unit Price")
    c.drawString(450, height - 260, "Total")
    
    y = height - 280
    c.setFont("Helvetica", 12)
    total_amount = 0
    for index, row in items.iterrows():
        c.drawString(50, y, row["Description"])
        c.drawString(250, y, str(row["Quantity"]))
        c.drawString(350, y, f"${row["Unit Price"]:.2f}")
        c.drawString(450, y, f"${row["Total"]:.2f}")
        total_amount += row["Total"]
        y -= 20
    
    # Total amount
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y - 30, "Grand Total:")
    c.drawString(450, y - 30, f"${total_amount:.2f}")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title("Invoice Generator")

st.sidebar.header("Business Details")
business_name = st.sidebar.text_input("Business Name")
business_address = st.sidebar.text_area("Business Address")
business_email = st.sidebar.text_input("Business Email")

st.sidebar.header("Client Details")
client_name = st.sidebar.text_input("Client Name")
client_address = st.sidebar.text_area("Client Address")
client_email = st.sidebar.text_input("Client Email")

invoice_number = st.text_input("Invoice Number")
invoice_date = st.date_input("Invoice Date")

st.subheader("Invoice Items")
items = st.data_editor(pd.DataFrame(columns=["Description", "Quantity", "Unit Price", "Total"]))

if st.button("Generate Invoice PDF"):
    items["Quantity"] = items["Quantity"].astype(float)
    items["Unit Price"] = items["Unit Price"].astype(float)
    items["Total"] = items["Quantity"] * items["Unit Price"]
    
    invoice_data = {
        "business_name": business_name,
        "business_address": business_address,
        "business_email": business_email,
        "client_name": client_name,
        "client_address": client_address,
        "client_email": client_email,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
    }
    pdf_buffer = generate_invoice_pdf(invoice_data, items)
    st.download_button("Download Invoice PDF", pdf_buffer, f"invoice_{invoice_number}.pdf", "application/pdf")
