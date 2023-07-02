"""
A fucntion to draw bounding boxes on a PDF file given textract results and save the result.
"""

from PIL import ImageDraw, Image, ImageFont
from pdf2image.pdf2image import convert_from_path
import tempfile
import app.textract.ctrp as ctrp
import json

        
def draw_boxes(dbs, hash_key, blocks, testing=False, line_width=4):
    if testing:
        path = f"app/dbs/inputs/{hash_key}"
    else:
        path = f"app/dbs/memory/{hash_key}"
    try:
        if path.lower().endswith('.pdf'):
            image = convert_from_path(path, dpi=300)[0]
        else:
            image = Image.open(path)
    
        img_width = image.width

        img_height = image.height

        doc = ctrp.Document(blocks)

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('documents/fonts/OpenSans-Regular.ttf', line_width*6)

        color_dict = {"LINE": "Red", "TABLE": "Blue", "SELECTION_ELEMENT": "Green", "KEY_VALUE_SET": "Orange", "WORD": "Purple"}

        for page in doc.pages:
            for line in page.content:
                box = line.geometry.boundingBox
                left = int(img_width * box.left)
                top = int(img_height * box.top)
                width = int(img_width * box.width)
                height = int(img_height * box.height)

                points = [(left, top), (left + width, top), (left + width, top + height), (left, top + height)]

                draw.polygon(points, outline=color_dict[line.blockType], width=line_width)
                
                text_bbox = draw.textbbox((left, top), line.blockType, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                draw.rectangle((left+2, top+2, left + text_width, top + text_height), fill="Blue")
                draw.text((left, top), line.blockType, fill='White', font=font)

        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf')
        image.save(temp_file.name, 'PDF', resolution=200.0)
        new_hash_key = dbs.memory.add(temp_file.name)
        temp_file.close()
        return new_hash_key
    
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")


if __name__ == '__main__':
    from db import DB, DBs
    dbs = DBs(
        memory=DB('dbs/memory'),
        inputs=DB('dbs/inputs'),
    )
    hash_key = dbs.memory.add('documents/tests/pdf_tests/test2.pdf')
    with open('app/results/textract_results/output2.json', 'r') as json_file:
        blocks = json.load(json_file)
    draw_boxes(dbs, hash_key, blocks)
