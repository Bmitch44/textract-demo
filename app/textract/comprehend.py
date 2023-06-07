"""
In this file I will begin trying to comprehend the output of the textract, I will experiemnt with multiple 
tools including GPT-3 and GPT-4, and any other tools that I can find.
"""

import json
from ctrp import Document

def extract_text(json_path):
    """Extracts the text from the json file using Document class"""
    try:
        with open(json_path) as f:
            data = json.load(f)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return None

    doc = Document(data)
    text = ""

    for page in doc.pages:
        for content in page.content:
            text += process_content(content)
    return text

def process_content(content):
    """Processes the content based on its type"""
    text = ""
    if content.blockType == "SELECTION_ELEMENT":
        text += process_selection_element(content)
    elif content.blockType == "KEY_VALUE_SET":
        text += process_key_value_set(content)
    elif content.blockType == "TABLE":
        text += process_table(content)
    elif content.blockType == "LINE":
        text += process_line(content)
    return text

def process_selection_element(content):
    """Processes SELECTION_ELEMENT"""
    return f"\nSELECTION_ELEMENT:\n" + content.selectionStatus + " "

def process_key_value_set(content):
    """Processes KEY_VALUE_SET"""
    text = f"\nKEY_VALUE_SET:\n"
    text += "KEY: " + (content.key.text + " " if content.key is not None else "")
    text += "\nVALUE: " + (content.value.text + " " if content.value is not None else "")
    return text

def process_table(content):
    """Processes TABLE"""
    text = f"\nTABLE:\n"
    for i, row in enumerate(content.rows):
        for j, cell in enumerate(row.cells):
            text += f"Row {str(i)} - Column {str(j)}: " + cell.text + " "
        text += "\n"
    return text

def process_line(content):
    """Processes LINE"""
    return f"\nLINE:\n" + content.text + " "

if __name__ == '__main__':
    text = extract_text('app/results/textract_results/output3.json')
    print(text)

