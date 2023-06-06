"""
A User interface where you input a pdf and get the json results and a pdf with bounding boxes drawn on it
"""

from .textract import process_pdf
from .bounding_box import draw_boxes
from .preprocess import deskew_pdf
from .ctrp import Document

import pandas as pd


def run_document_analysis(filepath, bucket, filename, json_path):
    """Runs AWS Textract analysis on a PDF file."""
    pp_filepath = deskew_pdf(filepath, filename)
    return process_pdf(pp_filepath, bucket, filename, json_path)

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


def draw_bounding_boxes(filepath, bucket, filename, output_path, json_path, csv_path):
    """Draws bounding boxes on a PDF file."""
    blocks = run_document_analysis(filepath, bucket, filename, json_path)
    table_to_csv(blocks, csv_path)
    draw_boxes(filepath, output_path, blocks)
    


# Example usage
if __name__ == '__main__':
    draw_bounding_boxes('documents/tests/test2.pdf',
                        'pdf-to-text-aws',
                        'test2.pdf',
                        'app/results/bounding_box_results/output2.pdf',
                        'app/results/textract_results/output2.json',
                        'app/results/table_results/output2.csv')

    