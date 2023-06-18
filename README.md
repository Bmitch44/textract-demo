# AWS Textract Project

https://github.com/Bmitch44/textract-demo/assets/87099534/0b5a20c3-73d0-4c15-b866-32479afd6ba5

This project aims to create a robust application that utilizes AWS Textract to extract information from structured and semi-structured PDF documents, and OpenAI's ChatGPT to interact with the application and analyze the results. These documents may contain both handwritten and printed text.

## About AWS Textract
AWS Textract is a service that automatically extracts text and data from scanned documents. It goes beyond simple optical character recognition (OCR) to identify, understand, and extract data from forms and tables.

## About ChatGPT
ChatGPT is a language model developed by OpenAI. In this application, we use it to interact with users and analyze the results of AWS Textract.

## Getting Started
To use this application, follow the steps below:

### Prerequisites
You will need an AWS account, OpenAI account, the AWS CLI (Command Line Interface) installed on your local machine, and setup your OpenAI and AWS credentials to authenticate with their services. [Here](https://aws.amazon.com/getting-started/guides/setup-environment/) is a guide to set up AWS. For OpenAI setup, please refer to the OpenAI API documentation.

### Installing

1. Install Anaconda on your machine. Visit the [Anaconda website](https://www.anaconda.com/products/individual) for installation instructions.

2. Create a new conda environment and install the required dependencies by running the following commands:

```
$ conda env create -f environment.yml
$ conda activate aws-text
```

### Running the Application

1. Make sure you have activated the `aws-text` conda environment.

2. Run the `application.py` file to start the application. This file sets up a local server that accepts PDF uploads, runs AWS Textract on the uploaded PDFs, then uses ChatGPT to interact with the application and analyze the results.

```
$ python application.py
```

3. Access the application by opening your web browser and navigating to `http://localhost:5000`.

4. Upload your PDF files through the web interface. The results of AWS Textract will be displayed on the page, and you can also interact with ChatGPT to analyze the results. You can download the results in JSON, PDF (with bounding boxes), and CSV formats.

## View results

The outputs are located in `app/results/textract_results`, `app/results/bounding_box_results`, and `app/results/table_results`.

## Built With

* [AWS Textract](https://aws.amazon.com/textract/) - Text extraction service
* [ChatGPT](https://openai.com/) - A interactive LLM
* [Flask](https://flask.palletsprojects.com/) - Web framework

## Author

* **Brady Mitchelmore** - *Initial work* - [bradymitchelmore](mailto:bradymitchelmore@gmail.com)