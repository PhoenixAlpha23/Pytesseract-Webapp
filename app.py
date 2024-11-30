import streamlit as st
import io
import zipfile
import numpy as np
import opencv as cv2
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
    """Create user-friendly OCR processing options."""
    st.sidebar.header("Image Enhancement Options")
    return {
        'apply_threshold': st.sidebar.checkbox(
            "Sharpen Text", 
            value=True,
            help="Improves text clarity by increasing contrast between text and background. Helps with faded or low-quality scans."
        ),
        'apply_deskew': st.sidebar.checkbox(
            "Straighten Document", 
            value=True,
            help="Corrects tilted or skewed documents. Fixes images where text is not perfectly horizontal, making text easier to read."
        ),
        'apply_denoise': st.sidebar.checkbox(
            "Remove Background Noise", 
            value=True,
            help="Removes specks, graininess, and background interference. Makes text clearer in scanned documents with imperfect backgrounds."
        ),
        'apply_contrast': st.sidebar.checkbox(
            "Enhance Text Visibility", 
            value=False,
            help="Boosts text brightness and contrast. Useful for documents with poor lighting or faded print."
        ),
        'psm': st.sidebar.selectbox(
            "Text Layout Detection",
            options=[3, 4, 6, 11, 12],
            format_func=lambda x: {
                3: "Automatic Detection",
                4: "Single Column Layout",
                6: "Single Text Block",
                11: "Line by Line",
                12: "Word by Word"
            }[x],
            help="Choose how the system should read your document's layout. Automatic[3] is best for most documents."
        )
    }

def display_processed_image(original_image, processed_image):
    """
    Display original and processed images side by side
    
    Args:
        original_image (numpy.ndarray): Original input image
        processed_image (numpy.ndarray): Preprocessed image
    """
    # Create two columns for display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        # Convert OpenCV image (BGR) to RGB for correct color display
        st.image(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), 
                 use_column_width=True)
    
    with col2:
        st.subheader("Processed Image")
        st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), 
                 use_column_width=True)


def process_uploaded_files(uploaded_files, options):
    """
    Modified function to show processed images
    
    Args:
        uploaded_files (list): List of uploaded files
        options (dict): OCR processing options
    
    Returns:
        tuple: Lists of all text and individual texts
    """
    all_text = []
    individual_texts = {}
    
    # Progress bar for multiple file processing
    progress_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        try:
            # Update progress bar
            progress_bar.progress((i + 1) / len(uploaded_files))
            
            if uploaded_file.type == "application/pdf":
                # Handle PDF processing
                text = process_pdf(uploaded_file, options)
                st.warning("PDF preview not supported. Text extracted.")
            else:
                # Image processing
                image = Image.open(uploaded_file)
                image_np = np.array(image)
                
                # Show original image before processing
                st.subheader(f"Processing: {uploaded_file.name}")
                
                # Display original image
                st.image(image, caption="Original Image", use_column_width=True)
                
                # Preprocess image
                processed_image = preprocess_image(image_np, options)
                
                # Display original and processed images side by side
                display_processed_image(image_np, processed_image)
                
                # Extract text
                text = extract_text(processed_image, options)
            
            all_text.append(f"File: {uploaded_file.name}\n\n{text}\n\n{'='*50}\n")
            individual_texts[uploaded_file.name] = text
        
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    # Clear progress bar
    progress_bar.empty()
    
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
