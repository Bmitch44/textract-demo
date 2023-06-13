# BEGIN: 8f3d4a5g6h7j
import boto3
import time
import json

class TextractProcessor:
    def __init__(self, bucket):
        self.bucket = bucket
        self.s3 = boto3.client('s3')
        self.textract = boto3.client('textract')

    def upload_to_s3(self, filepath, filename):
        """Uploads a file to an S3 bucket."""
        self.s3.upload_file(filepath, self.bucket, filename)

    def start_document_analysis(self, filename):
        """Starts AWS Textract analysis on a document in an S3 bucket."""
        response = self.textract.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': self.bucket,
                    'Name': filename
                }
            },
            FeatureTypes=['TABLES', 'FORMS']
        )

        return response['JobId']

    def wait_for_analysis(self, job_id):
        """Waits for AWS Textract analysis to complete."""
        while True:
            job_status = self.textract.get_document_analysis(JobId=job_id)
            status = job_status['JobStatus']

            if status in ['SUCCEEDED', 'FAILED']:
                break

            time.sleep(5)

        return job_status

    def store_analysis_result(self, job_status, filepath):
        """Stores the result of AWS Textract analysis."""
        if job_status['JobStatus'] == 'SUCCEEDED':
            result = job_status

            with open(filepath, 'w') as f:
                json.dump(result, f, indent=4)
                return result
        else:
            print("Document analysis job failed.")
            return None

    def process_pdf(self, filepath, filename, output_path):
        """Processes a PDF file with AWS Textract and stores the result."""
        self.upload_to_s3(filepath, filename)
        job_id = self.start_document_analysis(filename)
        job_status = self.wait_for_analysis(job_id)
        return self.store_analysis_result(job_status, output_path)

if __name__ == '__main__':
    processor = TextractProcessor('pdf-to-text-aws')
    processor.process_pdf('documents/tests/pdf_tests/corrected_test_cropped.pdf', 'corrected_test_cropped.pdf', 'app/results/textract_results/corrected_test_cropped_output.json')

