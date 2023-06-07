"""
A User interface where you input a pdf and get the json results and a pdf with bounding boxes drawn on it
"""

from .textract import process_pdf
from .bounding_box import draw_boxes
from .preprocess import deskew_pdf
from .ctrp import Document

import pandas as pd


class DocumentAnalysis:
    def __init__(self, filepath, bucket, filename, json_path, csv_path, output_path):
        self.filepath = filepath
        self.bucket = bucket
        self.filename = filename
        self.json_path = json_path
        self.csv_path = csv_path
        self.output_path = output_path

    def run_document_analysis(self):
        """Runs AWS Textract analysis on a PDF file."""
        pp_filepath = deskew_pdf(self.filepath, self.filename)
        return process_pdf(pp_filepath, self.bucket, self.filename, self.json_path)

    def table_to_csv(self, blocks):
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
        df.to_csv(self.csv_path, index=False)

    def draw_bounding_boxes(self):
        """Draws bounding boxes on a PDF file."""
        blocks = self.run_document_analysis()
        self.table_to_csv(blocks)
        draw_boxes(self.filepath, self.output_path, blocks)
    

# Example usage
if __name__ == '__main__':
    doc = DocumentAnalysis('documents/tests/test6.pdf',
                        'pdf-to-text-aws',
                        'test6.pdf',
                        'app/results/bounding_box_results/output6.pdf',
                        'app/results/textract_results/output6.json',
                        'app/results/table_results/output6.csv')
    doc.draw_bounding_boxes()

    