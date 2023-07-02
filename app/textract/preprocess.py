"""
This module is used to preprocess the pdf documents before running them through AWS Textract.

This includes deskewing the document, and converting it to a png file.
"""

import os
import logging
import numpy as np
import tempfile
from PIL import Image
from pdf2image.pdf2image import convert_from_path
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate


def deskew_pdf(dbs, hash_key):
    # try to get the pdf from memory
    try:
        path = f"{dbs.inputs.path}/{hash_key}"
        image = convert_from_path(path)[0]
    except Exception as e:
        logging.error(f"Error converting pdf to images: {e}")
        return None

    # try to deskew the image
    try:
        image = np.array(image)
        angle = get_angle(image)
        rotated = rotate(image, angle)
        rotated = Image.fromarray(rotated)
        image = rotated
    except Exception as e:
        logging.error(f"Error deskewing image: {e}")
        return None
    
    # try to save the image
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=".pdf")
        image.save(temp_file.name)
        new_hash_key = dbs.memory.add(temp_file.name)
        # close and delete the temporary file
        temp_file.close()
        return new_hash_key
    except Exception as e:
        logging.error(f"Error saving corrected image: {e}")
        return None


if __name__ == "__main__":
    from db import DBs, DB
    dbs = DBs(
        memory=DB('dbs/memory'),
        inputs=DB('dbs/inputs'),
    )
    hash_key = dbs.inputs.add('documents/tests/pdf_tests/test.pdf')
    deskew_pdf(dbs, hash_key)
    # deskew_pdf('documents/tests/pdf_tests/test.pdf', 'test.pdf', 'tests/expected_output')
