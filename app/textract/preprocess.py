"""
This file is used to preprocess the pdf documents before running them through AWS Textract.

This includes deskewing the document, and converting it to a png file.

"""

from pdf2image import convert_from_path
import numpy as np
from PIL import Image
import os
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate

def deskew_pdf(pdf_path, filename, skew_path='app/results/skew_correction'):
    """
    Converts pdf to png, and then deskews the png file.
    """
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting pdf to images: {e}")
        return None

    if not os.path.exists(skew_path):
        os.makedirs(skew_path)

    corrected_images = []

    for image in images:
        try:
            image = np.array(image)
            angle = get_angle(image)
            rotated = rotate(image, angle, (255, 255, 255))
            rotated = Image.fromarray(rotated)
            corrected_images.append(rotated)
        except Exception as e:
            print(f"Error deskewing image: {e}")
            return None
    
    try:
        corrected_images[0].save(f"{skew_path}/corrected_{filename}", save_all=True, append_images=corrected_images[1:])
        return f"{skew_path}/corrected_{filename}"
    except Exception as e:
        print(f"Error saving corrected image: {e}")
        return None


if __name__ == "__main__":
    deskew_pdf('documents/tests/pdf_tests/test.pdf', 'test.pdf', 'tests/expected_output')