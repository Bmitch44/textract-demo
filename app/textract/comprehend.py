"""
In this file I will begin trying to comprehend the output of the textract, I will experiemnt with multiple 
tools including GPT-3 and GPT-4, and any other tools that I can find.
"""

import json
import openai
from ctrp import Document

def extarct_text(json_path):
    """extracts the text from the json file using Document class"""
    with open(json_path) as f:
        data = json.load(f)

    doc = Document(data)
    text = ""

    for page in doc.pages:
        for content in page.content:
            location = content.geometry.boundingBox
            if content.blockType == "SELECTION_ELEMENT":
                text += f"\nSELECTION_ELEMENT: located -> {location}\n"
                text += content.selectionStatus + " "
            elif content.blockType == "KEY_VALUE_SET":
                text += f"KEY_VALUE_SET: located -> {location}"
                text += "\nKEY: "
                if content.key is not None:
                    text += content.key.text + " "
                text += "\nVALUE: "
                if content.value is not None:
                    text += content.value.text + " "
            elif content.blockType == "TABLE":
                text += f"TABLE: located -> {location}\n"
                for i, row in enumerate(content.rows):
                    for j, cell in enumerate(row.cells):
                        text += f"\nRow {str(i)} - Column {str(j)}: "
                        text += cell.text + " "
                    text += "\n"
            elif content.blockType == "LINE":
                text += f"\nLINE: located -> {location}\n"
                text += content.text + " "
    
    return text





if __name__ == '__main__':
    text = extarct_text('app/results/textract_results/output2.json')
    print(text)

