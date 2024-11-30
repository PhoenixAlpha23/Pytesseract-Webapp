import streamlit as st
import io
import zipfile
import numpy as np
from PIL import Image

from utils.image_processing import preprocess_image
from utils.pdf_processing import process_pdf
from utils.text_extraction import extract_text

def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Text Extraction Using Pytesseract",
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
    st.sidebar.header("OCR enhancement options Options")
        psm_modes = {
        3: "Automatic Page Segmentation",
        4: "Single Column of Text",
        6: "Single Block of Text",
        11: "Single Text Line",
        12: "Single Word"
    }
    return {
        'apply_threshold': st.sidebar.checkbox("Apply Thresholding", value=True),
        'apply_deskew': st.sidebar.checkbox("Apply Deskewing", value=True),
        'apply_denoise': st.sidebar.checkbox("Apply Denoising", value=True),
        'apply_contrast': st.sidebar.checkbox("Apply Contrast Enhancement", value=False),
        'psm': st.sidebar.selectbox(
            "Page Segmentation Mode",
            options=list(psm_modes.keys()),
            format_func=lambda x: psm_modes[x],
            help="Select how Tesseract should analyze the document layout"
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
    st.title("OCR Text Extraction from Images and PDFs using Tesseract OCR")
    st.write("""Upload multiple images or PDF files to extract text. 
    Tesseract Page Segmentation Modes (PSM) control how Tesseract analyzes and interprets document layouts:

PSM 3: Automatic page segmentation with orientation and script detection.\n
PSM 4: Assumes single column of text.\n
PSM 6: Assumes single uniform block of text.\n
PSM 11: Treats each line as a single text line.\n
PSM 12: Considers each word as a separate entity.\n

Choose based on your document's structure:

Complex layouts: PSM 3
Simple, single-column documents: PSM 4 or 6
Need line-by-line extraction: PSM 11
Word-level processing: PSM 12.""")
    
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
