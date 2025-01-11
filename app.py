import streamlit as st
import io
import zipfile
import numpy as np
import cv2
from PIL import Image

from utils.image_processing import preprocess_image
from utils.pdf_processing import process_pdf
from utils.text_extraction import extract_text, get_supported_languages

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
    st.sidebar.header("OCR Settings")
    
    # Language Selection
    st.sidebar.subheader("Language Settings")
    available_languages = get_supported_languages()
    default_lang = 'English'
    
    # Primary language selection
    primary_lang = st.sidebar.selectbox(
        "Primary Language",
        options=list(available_languages.keys()),
        index=list(available_languages.keys()).index(default_lang),
        help="Select the main language of your document"
    )
    
    # Additional languages selection
    additional_langs = st.sidebar.multiselect(
        "Additional Languages (Optional)",
        options=[lang for lang in available_languages.keys() if lang != primary_lang],
        help="Select additional languages if your document contains multiple languages"
    )
    
    # Combine selected languages
    selected_langs = [primary_lang] + additional_langs
    lang_codes = '+'.join([available_languages[lang] for lang in selected_langs])

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
        ),
        'language': lang_codes  
    }

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
                st.image(image, caption="Original Image", use_container_width=True)
                              
                # Extract text
                text = extract_text(image, options)
            
            all_text.append(f"File: {uploaded_file.name}\nLanguage: {options['language']}\n\n{text}\n\n{'='*50}\n")
            individual_texts[uploaded_file.name] = text
        
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")

    def display_results(all_text):
        """Display the extracted text results"""
        st.subheader("Extracted Text")

        # Display tabs for each processed file
        if st.session_state.processed_files:
            tabs = st.tabs(list(st.session_state.processed_files.keys()))
            for tab, (filename, file_info) in zip(tabs, st.session_state.processed_files.items()):
                with tab:
                    st.text_area("Extracted Content",value=fileinfo['text'],height=300,key=f"text{filename}")
                    st.info(f"File Type: {file_info['type']}\nFile Size: {file_info['size']} bytes")
    
    # Clear progress bar
    progress_bar.empty()
    
    return all_text, individual_texts

def main():
    """Main Streamlit application function."""
    # Setup page configuration
    setup_page_config()
    
    # Initialize session state
    initialize_session_state()
    
    # App title and description
    st.title("Text Extraction using Tesseract OCR")
    st.markdown('## Upload multiple images or PDF files to extract text from.')
    
    # Display supported languages
    available_languages = get_supported_languages()
    st.write('Supported Languages:', ', '.join(available_languages.keys()))
    
    st.write('From the list of Tesseract Page Segmentation Modes (PSM) on the left,\n you control how Tesseract analyzes and interprets document with varying layouts:')
    st.write(""" Automatic detection works fine for most documents,\n
    You can also Choose a different one based on your document's structure from the list.\n""")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files", 
        accept_multiple_files=True, 
        type=["png", "jpg", "jpeg", "pdf"]
    )
    
    #OCR options
    options = create_sidebar_options()
    
    # Process files when uploaded
    if uploaded_files:
        # Process uploaded files
        all_text, individual_texts = process_uploaded_files(uploaded_files, options)
        
        # Display extracted text
        if all_text:
            st.text_area("Extracted Text", value="\n".join(all_text), height=300)
            
            # download buttons
            create_text_downloads(all_text, individual_texts)

if __name__ == "__main__":
    main()
