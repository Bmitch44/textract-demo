from PIL import ImageDraw, Image, ImageFont
from pdf2image.pdf2image import convert_from_path
import json
import trp

def draw_boxes(file, output_path, blocks_path, line_width=4):
    """Draws bounding boxes on a PDF file."""
    if file.lower().endswith('.pdf'):
        image = convert_from_path(file, dpi=500)[0]
    else:
        image = Image.open(file)

    img_width = image.width
    img_height = image.height

    with open(blocks_path, 'r') as f:
        doc = trp.Document(json.load(f))

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

            # Using different color for different type of blocks
            draw.polygon(points, outline=color_dict[line.blockType], width=line_width)
            
            # Measure the size of the text using textbbox
            text_bbox = draw.textbbox((left, top), line.blockType, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Draw a rectangle as a background for the text
            draw.rectangle((left+2, top+2, left + text_width, top + text_height), fill="Blue")
            
            # Draw the text itself
            draw.text((left, top), line.blockType, fill='White', font=font)

    # save image to output path
    image.save(output_path, 'PDF', resolution=100.0)

# Example usage
draw_boxes('documents/test2.pdf', 'app/bounding_box_results/output2_bb.pdf', 'app/textract_results/output2.json')


