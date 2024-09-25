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
        
        # Save as high quality JPEG to a BytesIO object
        img_jpg = io.BytesIO()
        img.save(img_jpg, format='JPEG', quality=95)  # Increased quality to 95
        img_jpg.seek(0)
    
    # Use the BytesIO object to create a temporary file and process the image
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_file:
        temp_file.write(img_jpg.getvalue())
        
        # Create a PDF with the same size as the image
        img_buffer = io.BytesIO()
        c = canvas.Canvas(img_buffer, pagesize=(img_width, img_height))
        
        # Draw the high quality image on the canvas using the temporary file
        c.drawImage(temp_file.name, 0, 0, width=img_width, height=img_height, preserveAspectRatio=True, anchor='c')
        c.showPage()
        c.save()
        img_buffer.seek(0)
        return PyPDF2.PdfReader(img_buffer)


st.title("PDF Combiner")
st.markdown("*App built by Josh Kellendonk*")

# Add instructions for use
st.markdown("""
## How to Use:

- Drag and drop all files (PDF, JPEG, PNG) onto the box below in the order you want to combine them.
- Click Combine Files then click Download PDF

**Note:** Images will be converted to PDF pages automatically.
""")

# Add a horizontal line for visual separation
st.markdown("---")


uploaded_files = st.file_uploader("Choose files to combine", accept_multiple_files=True, type=['pdf', 'jpg', 'jpeg', 'png'])

if uploaded_files:
    st.write("Files to be combined in order:")
    for index, file in enumerate(uploaded_files, start=1):
        st.write(f"{index}. {file.name}")
    
    if st.button("Combine Files"):
        pdf_merger = PyPDF2.PdfMerger()
        
        for file in uploaded_files:
            if file.type == "application/pdf":
                pdf_merger.append(file)
            else:  # It's an image
                pdf_page = create_pdf_from_image(file)
                pdf_merger.append(pdf_page)
        
        output_buffer = io.BytesIO()
        pdf_merger.write(output_buffer)
        pdf_merger.close()
        
        st.download_button(
            label="Download PDF",
            data=output_buffer.getvalue(),
            file_name="combined.pdf",
            mime="application/pdf"
        )
