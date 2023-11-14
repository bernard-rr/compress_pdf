import streamlit as st
import PyPDF2
import os
import tempfile
import shutil
from io import BytesIO

# Function to compress PDF
def compress_pdf(input_pdf_path, output_pdf_path):
    reader = PyPDF2.PdfFileReader(input_pdf_path)
    writer = PyPDF2.PdfFileWriter()

    for i in range(reader.getNumPages()):
        writer.addPage(reader.getPage(i))

    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

# Streamlit app
st.title("PDF Compressor App")

uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")
compression_button = st.button("Compress PDFs")

if compression_button and uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Compress and save PDFs to temporary directory
        for uploaded_file in uploaded_files:
            input_path = os.path.join(temp_dir, uploaded_file.name)
            output_path = os.path.join(temp_dir, f"compressed_{uploaded_file.name}")
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            compress_pdf(input_path, output_path)

        # Zip compressed files
        zip_path = os.path.join(temp_dir, "compressed_pdfs.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.startswith("compressed_"):
                        zipf.write(os.path.join(root, file), file)

        # Let user download the zipped file
        with open(zip_path, "rb") as f:
            st.download_button(label="Download Compressed PDFs",
                               data=f,
                               file_name="compressed_pdfs.zip",
                               mime="application/zip")
