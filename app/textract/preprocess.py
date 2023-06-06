"""
This file is used to preprocess the pdf documents before running them through AWS Textract.

This includes deskewing the document, and converting it to a png file.

"""

from pdf2image import convert_from_path
from PIL import Image
import pytesseract as pt
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


def get_image_info(png_path):
    """
    gets information about image for preprocessing
    """
    image = Image.open(png_path)
    image_info = pt.image_to_osd(image)
    return image_info


print(get_image_info('app/png_results/test/page_1.png'))


    


    