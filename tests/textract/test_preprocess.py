import os
import pytest
from PIL import ImageChops
from app.textract.preprocess import deskew_pdf
from pdf2image import convert_from_path


@pytest.fixture
def pdf_path():
    return 'tests/pdf_tests/deskew_test.pdf'

@pytest.fixture
def filename():
    return 'deskew_test.pdf'

@pytest.fixture
def skew_path():
    return 'tests'

@pytest.fixture
def output_path(pdf_path, filename, skew_path):

    output_path = deskew_pdf(pdf_path, filename, skew_path)
    yield output_path
    # Clean up the output file
    if os.path.exists(output_path):
        os.remove(output_path)

def test_deskew_pdf(output_path):
    # Check that the output file exists
    assert os.path.exists(output_path)

    # Check that the output file is a PDF
    assert output_path.endswith('.pdf')

    # Convert the output PDF to image
    output_images = convert_from_path(output_path)

    # Convert the expected output PDF to image
    expected_output_path = 'tests/expected_output/expected_deskew_test.pdf'
    expected_images = convert_from_path(expected_output_path)

    # Compare the images (assumes that the PDFs have the same number of pages)
    for output_image, expected_image in zip(output_images, expected_images):
        diff = ImageChops.difference(output_image, expected_image)
        assert diff.getbbox() is None

# This will automatically run the test if the script is run directly
if __name__ == '__main__':
    pytest.main([__file__])