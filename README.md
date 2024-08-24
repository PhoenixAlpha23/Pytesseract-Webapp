# OCR Text Extraction App

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Pytesseract](#pytesseract)
5. [Image Processing Techniques](#image-processing-techniques)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

This Streamlit application leverages Optical Character Recognition (OCR) technology to extract text from images and PDF files. It employs advanced image processing techniques to enhance OCR accuracy, making it a powerful tool for digitizing printed or handwritten text.

## Features

- Upload multiple images (PNG, JPG, JPEG) or PDF files
- Advanced image preprocessing to improve OCR accuracy
- Text extraction using Tesseract OCR
- Display of extracted text within the app
- Downloadable extracted text as a .txt file

## Technologies Used

- Python 3.7+
- Streamlit
- OpenCV
- Pytesseract
- PyMuPDF
- NumPy
- Pillow

## Pytesseract

Pytesseract is the core OCR engine used in this project. It's a Python wrapper for Google's Tesseract-OCR Engine. Here's why we chose Pytesseract:

- **Open-source**: Freely available and continually improved by the community
- **Multi-language support**: Capable of recognizing a wide array of languages
- **Accuracy**: High accuracy rates, especially when combined with preprocessing techniques
- **Integration**: Easily integrates with other Python libraries

In our application, Pytesseract is used to convert preprocessed images into text. We've configured it to use the following options:

```python
config = r'--oem 3 --psm 6 preserve_interword_spaces=1'
```

- `--oem 3`: Uses the LSTM neural network mode
- `--psm 6`: Assumes a single uniform block of text
- `preserve_interword_spaces=1`: Maintains spacing between words

## Image Processing Techniques

To enhance OCR accuracy, we've implemented several image processing techniques:

### 1. Deskewing
```python
def deskew_hough(image):
    # Implementation details...
```
This function uses the Hough Line Transform to detect and correct skew in the image. It's crucial for ensuring that text lines are horizontal, which significantly improves OCR accuracy.

### 2. Binarization
```python
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
```
We use Otsu's method for binarization, which automatically determines the optimal threshold value. This helps separate text from the background effectively.

### 3. Noise Removal
```python
denoised = cv2.fastNlMeansDenoising(resized, None, 10, 7, 21)
```
The fastNlMeansDenoising function is used to remove noise from the image, which can otherwise be mistaken for text by the OCR engine.

### 4. Resizing
```python
resized = cv2.resize(inverted, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
```
Slightly enlarging the image can help in recognizing smaller text. We use cubic interpolation for better quality.

### 5. Contrast Enhancement
While not explicitly implemented in the current version, contrast enhancement can be added to further improve text visibility:

```python
# Example of contrast enhancement
def enhance_contrast(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(image)
```

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ocr-text-extraction-app.git
   cd ocr-text-extraction-app
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:
   - On Ubuntu: `sudo apt-get install tesseract-ocr`
   - On macOS: `brew install tesseract`
   - On Windows: Download the installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Upload image or PDF files using the file uploader.

4. The app will process the files and display the extracted text.

5. Download the extracted text as a .txt file using the "Download Extracted Text" button.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
