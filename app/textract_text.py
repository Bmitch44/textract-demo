"""
Uses AWS Textract text detection to extract text from a PDF file.
"""
import boto3
import time
import json

def upload_to_s3(filepath, bucket, filename):
    """Uploads a file to an S3 bucket."""
    s3 = boto3.client('s3')
    s3.upload_file(filepath, bucket, filename)


def start_text_detection(bucket, filename):
    """Starts AWS Textract text detection on a document in an S3 bucket."""
    textract = boto3.client('textract')
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': filename
            }
        }
    )

    return response


def store_text_detection_result(response, filepath):
    """Stores the result of AWS Textract text detection."""
    with open(filepath, 'w') as f:
        json.dump(response, f, indent=4)


def process_pdf(filepath, bucket, filename, output_path):
    """Processes a PDF file with AWS Textract text detection and stores the result."""
    upload_to_s3(filepath, bucket, filename)
    response = start_text_detection(bucket, filename)
    store_text_detection_result(response, output_path)


# Example usage
process_pdf('documents/test.pdf', 'pdf-to-text-aws', 'test.pdf', 'app/output_text.json')