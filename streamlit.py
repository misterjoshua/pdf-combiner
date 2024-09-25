import os
import tempfile
import streamlit as st
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from PIL import Image

def combine_pdfs(files):
    output = PyPDF2.PdfMerger()
    for file in files:
        output.append(file)
    return output

def create_pdf_from_image(image_file):
    # Open the image using PIL
    with Image.open(image_file) as img:
        # Convert to RGB if it's not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        img_width, img_height = img.size
        
        # Save as JPEG to a BytesIO object
        img_jpg = io.BytesIO()
        img.save(img_jpg, format='JPEG')
        img_jpg.seek(0)
    
    # Use the BytesIO object to create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_file.write(img_jpg.getvalue())
        temp_file_path = temp_file.name

    # Create a PDF with the same size as the image
    img_buffer = io.BytesIO()
    c = canvas.Canvas(img_buffer, pagesize=(img_width, img_height))
    
    # Draw the image on the canvas using the temporary file
    c.drawImage(temp_file_path, 0, 0, width=img_width, height=img_height)
    c.showPage()
    c.save()
    img_buffer.seek(0)

    os.unlink(temp_file_path)  # Remove the temporary file
    return PyPDF2.PdfReader(img_buffer)

st.title("PDF Combiner")

uploaded_files = st.file_uploader("Choose files to combine", accept_multiple_files=True, type=['pdf', 'jpg', 'jpeg', 'png'])

if uploaded_files:
    st.write("Drag and drop to reorder:")
    ordered_files = st.multiselect("Order files:", [file.name for file in uploaded_files], [file.name for file in uploaded_files])
    
    if st.button("Combine PDFs"):
        pdf_merger = PyPDF2.PdfMerger()
        
        for filename in ordered_files:
            file = next(f for f in uploaded_files if f.name == filename)
            if file.type == "application/pdf":
                pdf_merger.append(file)
            else:  # It's an image
                pdf_page = create_pdf_from_image(file)
                pdf_merger.append(pdf_page)
        
        output_buffer = io.BytesIO()
        pdf_merger.write(output_buffer)
        pdf_merger.close()
        
        st.download_button(
            label="Download combined PDF",
            data=output_buffer.getvalue(),
            file_name="combined.pdf",
            mime="application/pdf"
        )
