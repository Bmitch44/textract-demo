from PIL import ImageDraw, Image
from pdf2image.pdf2image import convert_from_path
import json


def draw_boxes(file, output_path, blocks_path, line_width=4):
    """Draws bounding boxes on a PDF file."""
    if file.lower().endswith('.pdf'):
        image = convert_from_path(file, dpi=500)[0]
    else:
        image = Image.open(file)

    img_width = image.width
    img_height = image.height

    with open(blocks_path, 'r') as f:
        blocks = json.load(f)['Blocks']

    draw = ImageDraw.Draw(image)
    for block in blocks:
        points = []
        for p in block['Geometry']['Polygon']:
            points.append((int(p['X'] * img_width), int(p['Y'] * img_height)))

        if 'BoundingBox' in block['Geometry']:
            box = block['Geometry']['BoundingBox']
            left = int(img_width * box['Left'])
            top = int(img_height * box['Top'])
            width = int(img_width * box['Width'])
            height = int(img_height * box['Height'])

            points.append((left, top))
            points.append((left + width, top))
            points.append((left + width, top + height))
            points.append((left, top + height))

        draw.line(points, fill='Red', width=line_width)

    # save image to output path
    image.save(output_path, 'PDF', resolution=100.0)

# Example usage
draw_boxes('documents/test2.pdf', 'app/textract_results/output2_bb.pdf', 'app/textract_results/output2.json')