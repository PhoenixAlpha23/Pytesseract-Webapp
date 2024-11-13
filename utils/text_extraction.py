import pytesseract

def extract_text(image, options):
    """
    Extracts text from the preprocessed image using pytesseract OCR.
    """
    config = f"--oem 3 --psm {options['psm']} preserve_interword_spaces=1"
    return pytesseract.image_to_string(image, config=config, lang="eng")
