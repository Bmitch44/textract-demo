"""
This file is used to preprocess the pdf documents before running them through AWS Textract.

This includes deskewing the document, and converting it to a png file.
"""

from pdf2image.pdf2image import convert_from_path

def convert_pdf_to_png(pdf_path, output_path):
    """Converts a PDF file to a PNG file."""
    pages = convert_from_path(pdf_path, 500)
    pages[0].save(output_path, 'PNG')

convert_pdf_to_png('documents/test.pdf', 'documents/test.png')
