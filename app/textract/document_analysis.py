"""
A User interface where you input a pdf and get the json results and a pdf with bounding boxes drawn on it
"""

from .textract import process_pdf
from .textract_text import process_pdf as process_pdf_text
from .bounding_box import draw_boxes
from .ctrp import Document

import pandas as pd


def run_document_analysis(filepath, bucket, filename, json_path):
    """Runs AWS Textract analysis on a PDF file."""
    return process_pdf(filepath, bucket, filename, json_path)

def run_text_detection(filepath, bucket, filename, json_path):
    """Runs AWS Textract text detection on a PDF file."""
    return process_pdf_text(filepath, bucket, filename, json_path)

def table_to_csv(blocks, output_path):
    """Converts a table in a PDF file to a CSV file."""
    matricies = []

    doc = Document(blocks)
    for page in doc.pages:
        if page.tables:
            for table in page.tables:
                for row in table.rows:
                    cells = [cell for cell in row.cells]
                    matricies.append(cells)
                
    df = pd.DataFrame(matricies)
    df.to_csv(output_path, index=False)


def draw_bounding_boxes(filepath, bucket, filename, output_path, json_path, analysis=True):
    """Draws bounding boxes on a PDF file."""
    if analysis:
        blocks = run_document_analysis(filepath, bucket, filename, json_path)
        table_to_csv(blocks, 'app/table_results/output.csv')
        draw_boxes(filepath, output_path, blocks)
    else:
        blocks = run_text_detection(filepath, bucket, filename, json_path)
        table_to_csv(blocks, 'app/table_results/output.csv')
        draw_boxes(filepath, output_path, blocks)


# Example usage
if __name__ == '__main__':
    draw_bounding_boxes('documents/tests/test3.pdf', 'pdf-to-text-aws', 'test3.pdf', 'app/bounding_box_results/output3.pdf', 'app/textract_results/output3.json')
    table_to_csv('app/textract_results/output3.json', 'app/table_results/output3.csv')
    