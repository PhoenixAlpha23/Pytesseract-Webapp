import fitz
from PIL import Image
import numpy as np
from .image_processing import preprocess_image
from .text_extraction import extract_text

def process_pdf(uploaded_file, options):
    """
    Processes an uploaded PDF file:
    1. Read PDF
    2. Converts each page to an image
    3. Preprocesses each image
    4. Extracts text from each preprocessed image
    5. Combines text from all pages
    """
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    texts = []
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_np = np.array(img)
        processed_image = preprocess_image(img_np, options)
        texts.append(extract_text(processed_image, options))
    return "\n\n".join(texts)
