import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Set Streamlit page layout
st.set_page_config(page_title="Invoice Generator", layout="wide")

st.title("Invoice Generator 📜")

# Initialize session state for invoice items
if "items" not in st.session_state:
    st.session_state.items = pd.DataFrame(columns=["Description", "Quantity", "Unit Price", "Total"])

# Business Details
st.sidebar.header("Business Details")
business_name = st.sidebar.text_input("Business Name", "Akhand & Associates")
business_address = st.sidebar.text_area("Business Address", "20/21, Garden Road, Karwan Bazar Lane, Tejgaon, Dhaka - 1215, Bangladesh")
business_email = st.sidebar.text_input("Business Email", "akhand.law@gmail.com")

# Client Details
st.sidebar.header("Client Details")
client_name = st.sidebar.text_input("Client Name", "")
client_address = st.sidebar.text_area("Client Address", "")
client_email = st.sidebar.text_input("Client Email", "")

# Invoice Details
col1, col2 = st.columns(2)
with col1:
    invoice_number = st.text_input("Invoice Number", "1001")
with col2:
    invoice_date = st.date_input("Invoice Date")

# Invoice Items
st.subheader("Invoice Items")

# Editable DataFrame for items
edited_items = st.data_editor(st.session_state.items.copy(), num_rows="dynamic")

# Update session state only if changes occur
if not edited_items.equals(st.session_state.items):
    st.session_state.items = edited_items

# Function to generate PDF invoice
def generate_pdf():
    if st.session_state.items.empty:
        st.warning("⚠️ Please add at least one item before generating the invoice!")
        return
    
    pdf_path = "invoice.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    
    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, f"Invoice No: {invoice_number}")
    c.drawString(100, 780, f"Invoice Date: {invoice_date}")

    # Business & Client Info
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Business: {business_name}")
    c.drawString(100, 730, f"Address: {business_address}")
    c.drawString(100, 710, f"Email: {business_email}")

    c.drawString(100, 680, f"Client: {client_name}")
    c.drawString(100, 660, f"Address: {client_address}")
    c.drawString(100, 640, f"Email: {client_email}")

    # Table Header
    y_position = 600
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "Description")
    c.drawString(300, y_position, "Quantity")
    c.drawString(400, y_position, "Unit Price")
    c.drawString(500, y_position, "Total")

    # Invoice Items
    c.setFont("Helvetica", 12)
    for _, row in st.session_state.items.iterrows():
        y_position -= 20
        c.drawString(100, y_position, str(row["Description"]))
        c.drawString(300, y_position, str(row["Quantity"]))
        c.drawString(400, y_position, str(row["Unit Price"]))
        c.drawString(500, y_position, str(row["Total"]))

    c.save()
    st.session_state.pdf_generated = True
    st.success("✅ Invoice PDF generated successfully!")

# Button to generate PDF
if st.button("Generate Invoice PDF"):
    generate_pdf()

# Show download button if PDF is generated
if "pdf_generated" in st.session_state and st.session_state.pdf_generated:
    with open("invoice.pdf", "rb") as pdf_file:
        st.download_button("📥 Download Invoice PDF", pdf_file, file_name="invoice.pdf", mime="application/pdf")
