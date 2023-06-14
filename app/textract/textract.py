import json
import logging
import time

import boto3


class TextractProcessor:
    """
    A class used to process documents using AWS Textract service.

    Attributes:
        bucket (str): The name of the S3 bucket to use.
        s3 (boto3.client): The S3 client.
        textract (boto3.client): The Textract client.
    """

    def __init__(self, bucket):
        """
        Constructs all the necessary attributes for the TextractProcessor object.

        Parameters:
            bucket (str): The name of the S3 bucket to use.
        """
        self.bucket = bucket
        self.s3 = boto3.client('s3')
        self.textract = boto3.client('textract')

    def upload_to_s3(self, filepath, filename):
        """
        Uploads a file to an S3 bucket.

        Parameters:
            filepath (str): The path of the file to upload.
            filename (str): The name of the file.

        Returns:
            None
        """
        try:
            self.s3.upload_file(filepath, self.bucket, filename)
        except Exception as e:
            logging.error(f"Error uploading file to S3: {e}")

    def start_document_analysis(self, filename):
        """
        Starts AWS Textract analysis on a document in an S3 bucket.

        Parameters:
            filename (str): The name of the file.

        Returns:
            str: The job ID for the analysis or None if an error occurred.
        """
        try:
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
        except Exception as e:
            logging.error(f"Error starting document analysis: {e}")

    def wait_for_analysis(self, job_id):
        """
        Waits for AWS Textract analysis to complete.

        Parameters:
            job_id (str): The job ID for the analysis.

        Returns:
            dict: The job status or None if an error occurred.
        """
        while True:
            try:
                job_status = self.textract.get_document_analysis(JobId=job_id)
                status = job_status['JobStatus']

                if status in ['SUCCEEDED', 'FAILED']:
                    break

                time.sleep(5)
            except Exception as e:
                logging.error(f"Error getting document analysis: {e}")

        return job_status

    def store_analysis_result(self, job_status, filepath):
        """
        Stores the result of AWS Textract analysis.

        Parameters:
            job_status (dict): The job status.
            filepath (str): The path to store the result.

        Returns:
            dict: The result of the analysis or None if an error occurred.
        """
        if job_status and job_status['JobStatus'] == 'SUCCEEDED':
            result = job_status
            try:
                with open(filepath, 'w') as f:
                    json.dump(result, f, indent=4)
                return result
            except Exception as e:
                logging.error(f"Error storing analysis result: {e}")
        else:
            logging.error("Document analysis job failed.")

    def process_pdf(self, filepath, filename, output_path):
        """
        Processes a PDF file with AWS Textract and stores the result.

        Parameters:
            filepath (str): The path of the PDF file to process.
            filename (str): The name of the file.
            output_path (str): The path to store the result.

        Returns:
            dict: The result of the analysis or None if an error occurred.
        """
        self.upload_to_s3(filepath, filename)

        job_id = self.start_document_analysis(filename)
        if not job_id:
            return

        job_status = self.wait_for_analysis(job_id)
        if not job_status:
            return

        return self.store_analysis_result(job_status, output_path)


if __name__ == '__main__':
    processor = TextractProcessor('pdf-to-text-aws')
    processor.process_pdf(
        'documents/tests/pdf_tests/corrected_test_cropped.pdf', 
        'corrected_test_cropped.pdf', 
        'app/results/textract_results/corrected_test_cropped_output.json'
    )
