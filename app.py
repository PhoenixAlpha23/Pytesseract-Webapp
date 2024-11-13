import streamlit as st
import io
import zipfile
from utils.image_processing import preprocess_image
from utils.pdf_processing import process_pdf
from utils.text_extraction import extract_text

def main():
    st.title("Enhanced OCR Text Extraction from Images and PDFs")
    st.write("Upload multiple images or a PDF file to extract text.")

    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["png", "jpg", "jpeg", "pdf"])

    st.sidebar.header("OCR Options")
    options = {
        'apply_threshold': st.sidebar.checkbox("Apply Thresholding", value=True),
        'apply_deskew': st.sidebar.checkbox("Apply Deskewing", value=True),
        'apply_denoise': st.sidebar.checkbox("Apply Denoising", value=True),
        'apply_contrast': st.sidebar.checkbox("Apply Contrast Enhancement", value=False),
        'psm': st.sidebar.selectbox("Page Segmentation Mode",
                                   options=[3, 4, 6, 11, 12],
                                   format_func=lambda x: f"PSM {x}",
                                   help="3: Full auto, 4: Single column, 6: Single block of text, 11: Single text line, 12: Single word")
    }

    if uploaded_files:
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

        combined_text = "\n".join(all_text)
        st.text_area("Extracted Text", value=combined_text, height=300)

        # Create a download button for the combined extracted text
        combined_text_io = io.BytesIO(combined_text.encode('utf-8'))
        st.download_button(
            label="Download Combined Extracted Text",
            data=combined_text_io,
            file_name="combined_extracted_text.txt",
            mime="text/plain"
        )

        # Create a download button for individual text files
        if len(individual_texts) > 0:
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

if __name__ == "__main__":
    main()
