import pytest
import boto3
import json
import os
from unittest.mock import MagicMock
from moto import mock_s3, mock_textract
from unittest.mock import patch
from app.textract.textract import TextractProcessor  # replace "your_module" with the name of the module containing the TextractProcessor class

# Set the test fixtures

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@pytest.fixture
def mock_start_response():
    return {'JobId': 'test_job_id'}

@pytest.fixture
def mock_get_response():
    with open('tests/json_tests/bb_test.json') as json_file:
        data = json.load(json_file)
    return data

@pytest.fixture
def processor(aws_credentials):
    with mock_s3(), mock_textract():
        boto3.setup_default_session()
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='pdf-to-text-aws')
        yield TextractProcessor('pdf-to-text-aws')

def test_process_pdf(processor: TextractProcessor, mock_get_response, mock_start_response):
    with patch.object(processor, 'upload_to_s3', return_value=None):
        processor.textract.get_document_analysis = MagicMock(return_value=mock_get_response)
        processor.textract.start_document_analysis = MagicMock(return_value=mock_start_response)

        # Call the method under test.
        result = processor.process_pdf('input.pdf', 'input.pdf', 'output.json')

        # Verify the result.
        assert result == mock_get_response


# Run the tests
if __name__ == '__main__':
    pytest.main([__file__])
