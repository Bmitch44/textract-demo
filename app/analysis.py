from trp import Document
import json

def process_document_analysis_result(filepath):
    """Processes the result of AWS Textract analysis. Returns analysis of the document."""
    with open(filepath, 'r') as f:
        result = json.load(f)

    doc = Document(result)
    page = doc.pages[0]
    for table in page.tables:
        print(table.get_header_field_names())
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                print("Table[{}][{}] = {}".format(r, c, cell.text))
    for field in page.form.fields:
        print("Field Key: {}, Value: {}".format(field.key, field.value))

# Example usage
process_document_analysis_result('app/textract_results/output2.json')