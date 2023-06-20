"""
A User interface where you input a pdf and get the json results and a pdf with bounding boxes drawn on it
"""

from app.textract.textract import TextractProcessor
from app.textract.bounding_box import draw_boxes
from app.textract.preprocess import deskew_pdf
from app.textract.ctrp import Document

import pandas as pd
import json
import tempfile


class DocumentAnalysis:
    """
    Analyzes a document using AWS Textract, converts detected tables to CSV format, 
    and draws bounding boxes on identified features.
    """

    def __init__(self, dbs, bucket, hash_key):
        self.dbs = dbs
        self.bucket = bucket
        self.hash_key = hash_key
        self.new_hash_key = None


    def run_document_analysis(self):
        """
        Analyzes the document using AWS Textract.

        Returns:
            dict: The result of the Textract analysis or None if an error occurred.
        """
        try:
            
            # pp_filepath = deskew_pdf(self.filepath, self.filename)
            self.new_hash_key = deskew_pdf(self.dbs, self.hash_key)
            textract = TextractProcessor(self.bucket)
            return textract.process_pdf(self.dbs, self.new_hash_key)
        except Exception as e:
            print(f"Error running document analysis: {e}")
            return None

    def table_to_csv(self, dbs, blocks):
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
            temp_file = tempfile.NamedTemporaryFile(suffix=".csv")
            df.to_csv(temp_file.name, index=False)
            csv_hash_key = dbs.memory.add(temp_file.name)
            temp_file.close()
            return csv_hash_key
        except Exception as e:
            print(f"Error converting table to CSV: {e}")
            return None

    def draw_bounding_boxes(self, testing=False, testing_blocks_path="app/results/textract_results/output3.json"):
        """
        Draws bounding boxes around the features identified by Textract on the document, extarcts tables, and converts them to CSV format.
        """
   
        if testing:
            json_hash_key = self.dbs.memory.add(testing_blocks_path)
            blocks = json.loads(self.dbs.memory.get(hash_key=json_hash_key))
        else:
            json_hash_key = self.run_document_analysis()
            blocks = json.loads(self.dbs.memory.get(hash_key=json_hash_key))


        
        if self.new_hash_key is not None:
            hash_key = self.new_hash_key
        else:
            hash_key = self.hash_key
        csv_hash_key = self.table_to_csv(self.dbs, blocks)
        bb_hash_key = draw_boxes(self.dbs, hash_key, blocks, testing=testing)
        keys = (bb_hash_key, csv_hash_key, json_hash_key)
        return keys
            

# Example usage
if __name__ == '__main__':
    from db import DBs, DB
    dbs = DBs(
        memory=DB('dbs/memory'),
        inputs=DB('dbs/inputs'),
    )
    hash_key = dbs.inputs.add('documents/tests/pdf_tests/test3.pdf')
    doc = DocumentAnalysis(
        dbs,
        'pdf-to-text-aws',
        hash_key
    )
    doc.draw_bounding_boxes()


    