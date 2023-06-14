"""
A User interface where you input a pdf and get the json results and a pdf with bounding boxes drawn on it
"""

from .textract import TextractProcessor
from .bounding_box import draw_boxes
from .preprocess import deskew_pdf
from .ctrp import Document

import pandas as pd


class DocumentAnalysis:
    """
    Analyzes a document using AWS Textract, converts detected tables to CSV format, 
    and draws bounding boxes on identified features.

    Attributes:
        filepath (str): Path to the document to be analyzed.
        bucket (str): Name of the AWS S3 bucket where document is stored.
        filename (str): Name of the document file.
        json_path (str): Path where the JSON output of the analysis will be stored.
        csv_path (str): Path where the converted CSV file will be stored.
        output_path (str): Path where the document with drawn bounding boxes will be stored.
    """
    
    def __init__(self, filepath, bucket, filename, json_path, csv_path, output_path):
        self.filepath = filepath
        self.bucket = bucket
        self.filename = filename
        self.json_path = json_path
        self.csv_path = csv_path
        self.output_path = output_path

    def run_document_analysis(self):
        """
        Analyzes the document using AWS Textract.

        Returns:
            dict: The result of the Textract analysis or None if an error occurred.
        """
        try:
            pp_filepath = deskew_pdf(self.filepath, self.filename)
            textract = TextractProcessor(self.bucket)
            return textract.process_pdf(pp_filepath, self.filename, self.json_path)
        except Exception as e:
            print(f"Error running document analysis: {e}")
            return None

    def table_to_csv(self, blocks):
        """
        Converts tables found in the document into CSV format.

        Parameters:
            blocks (dict): A dictionary containing the block structure of the Textract output.
        """
        try:
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
        except Exception as e:
            print(f"Error converting table to CSV: {e}")
            return None

    def draw_bounding_boxes(self):
        """
        Draws bounding boxes around the features identified by Textract on the document.
        """
        try:
            blocks = self.run_document_analysis()
            if blocks is not None:
                self.table_to_csv(blocks)
                draw_boxes(self.filepath, self.output_path, blocks)
        except Exception as e:
            print(f"Error drawing bounding boxes: {e}")
            return None
    

# Example usage
if __name__ == '__main__':
    doc = DocumentAnalysis(
        'documents/tests/test6.pdf',
        'pdf-to-text-aws',
        'test6.pdf',
        'app/results/bounding_box_results/output6.pdf',
        'app/results/textract_results/output6.json',
        'app/results/table_results/output6.csv'
    )
    doc.draw_bounding_boxes()


    