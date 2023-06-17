# AWS Textract Project

https://github.com/Bmitch44/textract-demo/assets/87099534/0b5a20c3-73d0-4c15-b866-32479afd6ba5


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

2. Run the `application.py` file to start the application. This file sets up a local server that accepts PDF uploads, runs AWS Textract on the uploaded PDFs, and then displays the results.

```
$ python application.py
```

3. Access the application by opening your web browser and navigating to `http://localhost:5000`.

4. Upload your PDF files through the web interface. The results of AWS Textract will be displayed on the page, and you can also download the results in JSON, PDF (with bounding boxes), and CSV formats.

## View results

The outputs are located in `app/results/textract_results`, `app/results/bounding_box_results`, and `app/results/table_results`.

## Built With

* [AWS Textract](https://aws.amazon.com/textract/) - Text extraction service
* [Flask](https://flask.palletsprojects.com/) - Web framework

## Author

* **Brady Mitchelmore** - *Initial work* - [bradymitchelmore](mailto:bradymitchelmore@gmail.com)
