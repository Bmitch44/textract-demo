from trp import Document
import json

def process_document_analysis_result(filepath):
    """Processes the result of AWS Textract analysis."""
    with open(filepath, 'r') as f:
        result = json.load(f)

    doc = Document(result)
    in_order = doc.pages[0].getLinesInReadingOrder()
    return in_order

print(process_document_analysis_result('app/output_text.json'))