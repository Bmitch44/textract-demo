import boto3
import time
import json

# Store PDF in documents/test.pdf in the S3 bucket
s3 = boto3.client('s3')
s3.upload_file('documents/test.pdf', 'pdf-to-text-aws', 'test.pdf')

# Call AWS Textract API
textract = boto3.client('textract')
response = textract.start_document_analysis(
    DocumentLocation={
        'S3Object': {
            'Bucket': 'pdf-to-text-aws',
            'Name': 'test.pdf'
        }
    },
    FeatureTypes=["FORMS"]
)

# Wait for the document analysis job to complete
while True:
    job_status = textract.get_document_analysis(JobId=response['JobId'])
    status = job_status['JobStatus']
    if status in ['SUCCEEDED', 'FAILED']:
        break
    time.sleep(5)

# Retrieve the extracted text or data from the response
if status == 'SUCCEEDED':
    result = job_status['Blocks']

    # Store raw json response in output.txt
    with open('output.txt', 'w') as f:
        json.dump(result, f, indent=4)
else:
    print("Document analysis job failed.")




