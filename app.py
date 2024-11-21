import streamlit as st
import io
import zipfile
import numpy as np
from PIL import Image
import pytesseract
import cv2

from utils.image_processing import preprocess_image
from utils.pdf_processing import process_pdf
from utils.text_extraction import extract_text

def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Text Extraction tool using Pytesseract",
        page_icon=":page_facing_up:",
        layout="wide"
    )

def initialize_session_state():
    """Initialize or reset session state variables."""
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = None
    if 'all_text' not in st.session_state:
        st.session_state.all_text = []
    if 'individual_texts' not in st.session_state:
        st.session_state.individual_texts = {}

def create_sidebar_options():
    """Create sidebar options for OCR processing."""
    st.sidebar.header("OCR Options")
    return {
        'apply_threshold': st.sidebar.checkbox("Apply Thresholding", value=True),
        'apply_deskew': st.sidebar.checkbox("Apply Deskewing", value=True),
        'apply_denoise': st.sidebar.checkbox("Apply Denoising", value=True),
        'apply_contrast': st.sidebar.checkbox("Apply Contrast Enhancement", value=False),
        'psm': st.sidebar.selectbox(
            "Page Segmentation Mode",
            options=[3, 4, 6, 11, 12],
            format_func=lambda x: f"PSM {x}",
            help="3: Full auto, 4: Single column, 6: Single block of text, 11: Single text line, 12: Single word"
        )
    }

def process_uploaded_files(uploaded_files, options):
    """
    Process uploaded files and extract text.
    
    Args:
        uploaded_files (list): List of uploaded files
        options (dict): OCR processing options
    
    Returns:
        tuple: Lists of all text and individual texts
    """
    all_text = []
    individual_texts = {}
    
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.type == "application/pdf":
                text = process_pdf(uploaded_file, options)
            else:
                image = Image.open(uploaded_file)
                image_np = np.array(image)
                processed_image = preprocess_image(image_np, options)
                text = extract_text(processed_image, options)
            
            all_text.append(f"File: {uploaded_file.name}\n\n{text}\n\n{'='*50}\n")
            individual_texts[uploaded_file.name] = text
        
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    return all_text, individual_texts

def create_text_downloads(all_text, individual_texts):
    """
    Create download buttons for extracted texts.
    
    Args:
        all_text (list): Combined extracted texts
        individual_texts (dict): Individual file texts
    """
    # Combined text download
    combined_text = "\n".join(all_text)
    combined_text_io = io.BytesIO(combined_text.encode('utf-8'))
    st.download_button(
        label="Download Combined Extracted Text",
        data=combined_text_io,
        file_name="combined_extracted_text.txt",
        mime="text/plain"
    )
    
    # Individual texts download
    if individual_texts:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, text in individual_texts.items():
                zip_file.writestr(f"{file_name}_extracted.txt", text)
        
        st.download_button(
            label="Download Individual Extracted Texts",
            data=zip_buffer.getvalue(),
            file_name="individual_extracted_texts.zip",
            mime="application/zip"
        )

def main():
    """Main Streamlit application function."""
    # Setup page configuration
    setup_page_config()
    
    # Initialize session state
    initialize_session_state()
    
    # App title and description
    st.title("Enhanced OCR Text Extraction from Images and PDFs")
    st.write("Upload multiple images or a PDF file to extract text.")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files", 
        accept_multiple_files=True, 
        type=["png", "jpg", "jpeg", "pdf"]
    )
    
    # Create OCR options
    options = create_sidebar_options()
    
    # Process files when uploaded
    if uploaded_files:
        # Process uploaded files
        all_text, individual_texts = process_uploaded_files(uploaded_files, options)
        
        # Display extracted text
        if all_text:
            st.text_area("Extracted Text", value="\n".join(all_text), height=300)
            
            # Create download buttons
            create_text_downloads(all_text, individual_texts)

# This ensures the app runs automatically when accessed
if __name__ == "__main__":
    main()
