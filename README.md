# Text Extraction Application 
The [Website](https://ocr-project-msvaqi6mtvblxm3d3bigxn.streamlit.app/)
## Overview

A powerful Streamlit application that uses Optical Character Recognition (OCR) to extract text from images and PDF files. The app employs custom image preprocessing techniques to enhance OCR accuracy and provide a user-friendly text extraction experience for multiple files.

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
- Binarization 
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
   git clone https://github.com/PhoenixAlpha23/Pytesseract-Webapp/main
   cd main
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Tesseract for OCR functionalities:
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
2. Connect Streamlit Cloud to the repository
3. Configure build settings

## Contributing

Contributions are welcome! Please submit pull requests to this main repository.

## License

MIT License - see [LICENSE](LICENSE) file for details.
