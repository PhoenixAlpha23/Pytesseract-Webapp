import cv2
import numpy as np

def ensure_gray(image):
    """
    Ensures the input image is in grayscale format.
    If the image is already grayscale, it's returned as-is.
    If it's in color, it's converted to grayscale.
    """
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def deskew_hough(image):
    """
    Applies Hough Line Transform to detect and correct skew in the image.
    """
    gray = ensure_gray(image)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

    if lines is not None:
        angle = 0
        for rho, theta in lines[0]:
            if theta < np.pi/4 or theta > 3*np.pi/4:
                angle = theta
                break

        if angle != 0:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle * 180 / np.pi - 90, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return rotated

    return image

def preprocess_image(image, options):
    """
    Applies various preprocessing techniques to improve OCR accuracy:
    1. Converts to grayscale
    2. Applies thresholding
    3. Deskews the image
    4. Inverts colors
    5. Resizes
    6. Applies denoising
    """
    gray = ensure_gray(image)

    if options['apply_threshold']:
        _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if options['apply_deskew']:
        gray = deskew_hough(gray)

    if options['apply_denoise']:
        gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    if options['apply_contrast']:
        gray = cv2.equalizeHist(gray)

    return gray
