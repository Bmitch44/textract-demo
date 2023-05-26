# AWS Textract Project

This project aims to create a working product that utilizes AWS Textract to extract information from structured and semi-structured PDF documents. These documents may contain both handwritten and printed text.

## About AWS Textract

AWS Textract is a service that automatically extracts text and data from scanned documents. It goes beyond simple optical character recognition (OCR) to identify, understand, and extract data from forms and tables.

## Getting Started

To use this application, follow the steps below:

### Prerequisites

You will need an AWS account and the AWS CLI (Command Line Interface) installed on your local machine. Set up your AWS credentials to authenticate with AWS services. [Here](https://aws.amazon.com/getting-started/guides/setup-environment/) is a nice guide to set it all up.

### Installing

1. Install Anaconda on your machine. Visit the [Anaconda website](https://www.anaconda.com/products/individual) for installation instructions.

2. Create a new conda environment and install the required dependencies by running the following commands:

```
$ conda create --name aws-text --file requirements.txt
$ conda activate aws-text
```

## Running the Application

1. Make sure you have activated the `aws-text` conda environment.

2. Run the `textract.py` file to start the application. This file demonstrates the usage of AWS Textract to extract information from PDF documents and stores the data extracted using textract in a json file.

```
$ python textract.py
```


3. The output will be saved in the `output.json` file. You can review the extracted information there.

## Built With

* [AWS Textract](https://aws.amazon.com/textract/) - Text extraction service

## Author

* **Brady Mitchelmore** - *Initial work* - [bradymitchelmore](mailto:bradymitchelmore@gmail.com)
