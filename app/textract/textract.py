"""
Uses AWS Textract document analysis to extract text, forms, and tables from a PDF file.
"""
import boto3
import time
import json

def upload_to_s3(filepath, bucket, filename):
    """Uploads a file to an S3 bucket."""
    s3 = boto3.client('s3')
    s3.upload_file(filepath, bucket, filename)


def start_document_analysis(bucket, filename):
    """Starts AWS Textract analysis on a document in an S3 bucket."""
    textract = boto3.client('textract')
    response = textract.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': filename
            }
        },
        FeatureTypes=['TABLES', 'FORMS']
    )

    return response['JobId']


def wait_for_analysis(job_id):
    """Waits for AWS Textract analysis to complete."""
    textract = boto3.client('textract')

    while True:
        job_status = textract.get_document_analysis(JobId=job_id)
        status = job_status['JobStatus']

        if status in ['SUCCEEDED', 'FAILED']:
            break

        time.sleep(5)

    return job_status


def store_analysis_result(job_status, filepath):
    """Stores the result of AWS Textract analysis."""
    if job_status['JobStatus'] == 'SUCCEEDED':
        result = job_status

        with open(filepath, 'w') as f:
            json.dump(result, f, indent=4)
            return result
    else:
        print("Document analysis job failed.")
        return None


def process_pdf(filepath, bucket, filename, output_path):
    """Processes a PDF file with AWS Textract and stores the result."""
    upload_to_s3(filepath, bucket, filename)
    job_id = start_document_analysis(bucket, filename)
    job_status = wait_for_analysis(job_id)
    return store_analysis_result(job_status, output_path)
        



# Example usage
if __name__ == '__main__':
    process_pdf('documents/test2.pdf', 'pdf-to-text-aws', 'test2.pdf', 'app/textract_results/output2.json')

