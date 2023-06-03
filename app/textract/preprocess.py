"""
This file is used to preprocess the pdf documents before running them through AWS Textract.

This includes deskewing the document, and converting it to a png file.
"""

from pdf2image.pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract

def convert_pdf_to_png(pdf_path, output_path):
    """Converts a PDF file to a PNG file."""
    pages = convert_from_path(pdf_path, 500)
    pages[0].save(output_path, 'PNG')

def rotate_image(image, angle):
    """Rotates an image by a given angle."""
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def deskew_image(pdf_path, output_path):
    """Deskews an image and saves output as a PNG file in the app folder."""
    app_output_path = f'{output_path}.png'
    convert_pdf_to_png(pdf_path, app_output_path)
    image = cv2.imread(app_output_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    # angle = cv2.minAreaRect(coords)[-1]
    # if angle < -45:
    #     angle = -(90 + angle)
    # else:
    #     angle = -angle
    angle = -1
    rotated = rotate_image(image, angle)
    cv2.imwrite(app_output_path, rotated)
    

# Example usage
deskew_image('documents/test.pdf', 'documents/test_deskewed')