"""
This file is used to preprocess the pdf documents before running them through AWS Textract.

This includes deskewing the document, and converting it to a png file.

"""

from pdf2image import convert_from_path
import math
from typing import Tuple, Union
import cv2
import numpy as np
from deskew import determine_skew
from PIL import Image
import os

def pdf_to_png(pdf_path, png_path='app/png_results'):
    """
    Converts a pdf file to a png file.
    """

    if not os.path.exists(png_path):
        os.makedirs(png_path)

    
    # This will return a list of PIL Image objects, one for each page of the pdf
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        # We are going to save each page as a separate png image
        # png_path should be a directory, not a file path
        image_path = f"{png_path}/page_{i+1}.png"
        image.save(image_path, 'PNG')

    print(f"Converted {len(images)} pages.")

def rotate(
        image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2

    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

def deskew_pdf(pdf_path, filename, skew_path='app/results/skew_correction'):
    """
    Converts a pdf file to a png file, and then deskews the png file.
    """

    if not os.path.exists(skew_path):
        os.makedirs(skew_path)

    # This will return a list of PIL Image objects, one for each page of the pdf
    images = convert_from_path(pdf_path)

    corrected_images = []

    for image in images:
        # deskew each image
        grayscale = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)
        rotated = rotate(np.array(image), angle, (255, 255, 255))

        corrected_image = Image.fromarray(rotated)
        corrected_images.append(corrected_image)
    
    # now we will combine each image into a single pdf
    corrected_images[0].save(f"{skew_path}/corrected_{filename}", save_all=True, append_images=corrected_images[1:])

if __name__ == "__main__":
    deskew_pdf('documents/tests/test.pdf', 'test.pdf')