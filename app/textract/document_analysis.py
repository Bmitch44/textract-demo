"""
A User interface where you input a pdf and get the json results and a pdf with bounding boxes drawn on it
"""

from .textract import process_pdf
from .textract_text import process_pdf as process_pdf_text
from .bounding_box import draw_boxes


def run_document_analysis(filepath, bucket, filename, json_path):
    """Runs AWS Textract analysis on a PDF file."""
    return process_pdf(filepath, bucket, filename, json_path)

def run_text_detection(filepath, bucket, filename, json_path):
    """Runs AWS Textract text detection on a PDF file."""
    return process_pdf_text(filepath, bucket, filename, json_path)

def draw_bounding_boxes(filepath, bucket, filename, output_path, json_path, analysis=True):
    """Draws bounding boxes on a PDF file."""
    if analysis:
        run_document_analysis(filepath, bucket, filename, json_path)
        draw_boxes(filepath, output_path, json_path)
    else:
        run_text_detection(filepath, bucket, filename, json_path)
        draw_boxes(filepath, output_path, json_path)

# Example usage
if __name__ == '__main__':
    draw_bounding_boxes('documents/test2.pdf', 'pdf-to-text-aws', 'test2.pdf', 'app/bounding_box_results/output2.pdf', 'app/textract_results/output2.json')

    