import os
import sys

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from flask import Flask, render_template, request, send_file, jsonify
from app.textract.document_analysis import DocumentAnalysis
from app.textract.comprehend import TextComprehender, TextExtractor  # adjust this import as necessary
import tempfile
import json

application = Flask(__name__)

text_comprehender = TextComprehender()

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # save the file to a temporary file with .pdf extension
            temp_file = tempfile.NamedTemporaryFile(suffix='.pdf')
            file.save(temp_file.name)
            # create paths for the output files
            json_path = os.path.join('app', 'results', 'textract_results', 'output.json')
            pdf_path = os.path.join('app', 'output.pdf')
            csv_path = os.path.join('app', 'results', 'table_results', 'output.csv')
            # run the analysis and draw the bounding boxes
            doc = DocumentAnalysis(temp_file.name, 'pdf-to-text-aws', file.filename, json_path, csv_path, pdf_path)
            doc.draw_bounding_boxes(testing=True)
            # close and delete the temporary file
            temp_file.close()
            # read the JSON data and send it to the user
            with open(json_path, 'r') as f:
                json_data = json.load(f)

            # extarct text from the document
            text_extractor = TextExtractor(json_path=json_path)
            text = text_extractor.extract_text()
            # use your TextComprehender here to generate the response
            response = text_comprehender.comprehend_text(text, init=True)

            # remove /app from the path so that the file can be downloaded
            pdf_path = pdf_path[4:]
            csv_path = csv_path[4:]
            return render_template('results.html', json_data=json_data, pdf_filename=pdf_path, csv_filename=csv_path, gpt_response=response)
    return render_template('upload.html')

@application.route('/download/<path:filename>')
def download_file(filename):
    print(f"download_file - {filename}")
    return send_file(filename, as_attachment=True)

@application.route('/chat')
def chat():
    return render_template('chat.html')

@application.route('/get', methods=['GET', 'POST'])
def get_bot_response():
    userText = request.args.get('msg')
    return text_comprehender.comprehend_text(userText)

if __name__ == '__main__':
    application.run(debug=True)
