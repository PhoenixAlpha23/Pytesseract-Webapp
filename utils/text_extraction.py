import pytesseract
from typing import Dict, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_installed_languages() -> list:
    """Get list of installed Tesseract language packs"""
    try:
        return pytesseract.get_languages()
    except Exception as e:
        logger.error(f"Error getting installed languages: {str(e)}")
        return ['eng']

def get_supported_languages() -> Dict[str, str]:
    """Returns a dictionary of supported languages and their codes"""
    all_languages = {
        'English': 'eng',
        'Hindi': 'hin',
        'Gujrati':'guj',
        'Punjabi':'pan',
        'Marathi': 'mar',
        
    }
    
    installed_langs = get_installed_languages()
    return {name: code for name, code in all_languages.items() 
            if code in installed_langs}

def validate_language(lang: str) -> str:
    """Validate if the requested language is installed"""
    installed_langs = get_installed_languages()
    requested_langs = lang.split('+')
    valid_langs = [l for l in requested_langs if l in installed_langs]
    return '+'.join(valid_langs) if valid_langs else 'eng'

def extract_text(image: Union[str, bytes], options: Dict) -> str:
    """
    Extracts text from the preprocessed image using pytesseract OCR.
    
    Args:
        image: Preprocessed image
        options: Dictionary containing OCR options including:
            - psm: Page segmentation mode
            - language: Language code(s) for OCR
    """
    try:
        # Get and validate language
        lang = validate_language(options.get('language', 'eng'))
        
        # Configure OCR settings
        config = f"--oem 3 --psm {options['psm']} preserve_interword_spaces=1"
        
        # Perform OCR
        text = pytesseract.image_to_string(
            image,
            config=config,
            lang=lang
        )
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error during text extraction: {str(e)}")
        raise Exception(f"Text extraction failed: {str(e)}")
