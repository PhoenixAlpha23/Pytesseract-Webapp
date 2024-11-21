# OCR Text Extraction Using Streamlit

## Overview

A powerful Streamlit application that uses Optical Character Recognition (OCR) to extract text from images and PDF files. The app employs advanced image processing techniques to enhance OCR accuracy and provide a user-friendly text extraction experience.

## Key Features

- Multi-file upload support (PNG, JPG, JPEG, PDF)
- Advanced image preprocessing techniques
- Configurable OCR options
- Real-time text extraction
- Downloadable extracted text files

## Technologies

- Python 3.7+
- Streamlit
- OpenCV
- Pytesseract
- PyMuPDF
- NumPy
- Pillow

## OCR Processing Techniques

### Image Preprocessing
- Deskewing
- Binarization (Otsu's method)
- Noise removal
- Contrast enhancement
- Page segmentation mode selection

### Pytesseract Configuration
- LSTM neural network mode
- Uniform text block assumption
- Interword space preservation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ocr-text-extraction-app.git
   cd ocr-text-extraction-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:
   - Ubuntu: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`
   - Windows: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open `http://localhost:8501` in your web browser

3. Upload images or PDF files

4. Configure OCR options in the sidebar

5. Download extracted text files

## Deployment

Deploy using Streamlit Cloud:
1. Push code to GitHub
2. Connect Streamlit Cloud to your repository
3. Configure build settings

## Contributing

Contributions are welcome! Please submit pull requests to the main repository.

## License

MIT License - see [LICENSE](LICENSE) file for details.
