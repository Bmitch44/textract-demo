import os
import pytest
from PIL import Image, ImageChops
import json
from app.textract.bounding_box import draw_boxes 
from pdf2image import convert_from_path



@pytest.fixture
def filepath():
    return 'tests/pdf_tests/bb_test.pdf'

@pytest.fixture
def output_path():
    return 'tests/output_bb_test.pdf'

@pytest.fixture
def blocks():
    with open('tests/json_tests/bb_test.json') as json_file:
        blocks = json.load(json_file)
    return blocks

@pytest.fixture
def setup_draw_boxes(filepath, output_path, blocks):
    draw_boxes(filepath, output_path, blocks)
    yield output_path
    # Clean up the output file
    if os.path.exists(output_path):
        os.remove(output_path)

def test_draw_boxes(setup_draw_boxes):
    output_path = setup_draw_boxes

    # Check that the output file exists
    assert os.path.exists(output_path)

    # Check that the output file is a PDF
    assert output_path.endswith('.pdf')

    # Convert the output PDF to image

    output_image = convert_from_path(output_path)[0]

    # Convert the expected output PDF to image
    expected_output_path = 'tests/expected_output/expected_bb_test.pdf'
    expected_image = convert_from_path(expected_output_path)[0]

    # Compare the images
    diff = ImageChops.difference(expected_image, output_image)
    assert diff.getbbox() is None

# This will automatically run the test if the script is run directly
if __name__ == '__main__':
    pytest.main([__file__])
