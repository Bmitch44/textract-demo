"""
An interface to process documents using AWS Textract service.
"""

import json
import logging
import time
import tempfile

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

    def store_analysis_result(self, db, job_status):
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
                temp_file = tempfile.NamedTemporaryFile(suffix=".json")

                with open(temp_file.name, 'w') as f:
                    json.dump(result, f, indent=4)

                new_hash_key = db.add(temp_file.name)
                temp_file.close()
                return new_hash_key
            except Exception as e:
                logging.error(f"Error storing analysis result: {e}")
        else:
            logging.error("Document analysis job failed.")

    
    def process_pdf(self, dbs, hash_key):

        path = f"{dbs.memory.path}/{hash_key}"

        self.upload_to_s3(path, hash_key)

        job_id = self.start_document_analysis(hash_key)
        if not job_id:
            return

        job_status = self.wait_for_analysis(job_id)
        if not job_status:
            return

        return self.store_analysis_result(dbs.memory, job_status)


if __name__ == '__main__':
    from db import DB, DBs
    dbs = DBs(
        memory=DB('dbs/memory'),
        inputs=DB('dbs/inputs')
    )
    hash_key = dbs.memory.add('documents/tests/pdf_tests/corrected_test_cropped.pdf')
    processor = TextractProcessor('pdf-to-text-aws')
    processor.process_pdf(dbs, hash_key)
