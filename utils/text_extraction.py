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
        'Marathi':'mar',
        'Gujrati':'guj',
        'Punjabi':'pan'
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

def detect_script(image: Union[str, bytes]) -> str:
    """
    Detects the script of the text in the image using Tesseract OCR.
    
    Args:
        image: Preprocessed image
    
    Returns:
        str: Detected script code (e.g., 'Latin', 'Devanagari', etc.)
    """
    try:
        # Use Tesseract's script detection feature
        script_config = "--psm 3 -l script"
        script_info = pytesseract.image_to_osd(image, config=script_config)
        
        # Extract script name from the OSD output
        script_line = [line for line in script_info.split('\n') if "Script" in line][0]
        script_name = script_line.split(":")[1].strip()
        
        return script_name
    except Exception as e:
        logger.error(f"Error detecting script: {str(e)}")
        return "Latin"  # Fallback to Latin script (English)

def map_script_to_language(script: str) -> str:
    """
    Maps a detected script to the corresponding Tesseract language code.
    
    Args:
        script: Detected script name (e.g., 'Latin', 'Devanagari')
    
    Returns:
        str: Tesseract language code (e.g., 'eng', 'hin')
    """
    script_to_lang = {
        'Latin': 'eng',          # English
        'Devanagari': 'hin',     # Hindi
        'Gujarati': 'guj',       # Gujarati
        'Gurmukhi': 'pan',       # Punjabi
        'Devanagari': 'mar'      # Marathi (same script as Hindi)
    }
    return script_to_lang.get(script, 'eng')  # Fallback to English
def extract_text(image: Union[str, bytes], options: Dict) -> str:
    """
    Extracts text from the preprocessed image using pytesseract OCR.
    Automatically detects the script and adjusts the language configuration.
    
    Args:
        image: Preprocessed image
        options: Dictionary containing OCR options including:
            - psm: Page segmentation mode
            - language: Language code(s) for OCR (optional)
    """
    try:
        # Detect script and map to language
        detected_script = detect_script(image)
        detected_lang = map_script_to_language(detected_script)
        
        # Override the language setting if script detection is successful
        options['language'] = detected_lang
        
        # Configure OCR settings
        config = f"--oem 3 --psm {options['psm']} preserve_interword_spaces=1"
        
        # Perform OCR
        text = pytesseract.image_to_string(
            image,
            config=config,
            lang=options['language']
        )
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error during text extraction: {str(e)}")
        raise Exception(f"Text extraction failed: {str(e)}")
