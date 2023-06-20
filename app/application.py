import os
import sys

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from flask import Flask, render_template, request, send_file, send_from_directory
from app.textract.document_analysis import DocumentAnalysis
from app.textract.comprehend import TextComprehender, TextExtractor
from app.textract.db import DB, DBs  
import tempfile
import json

application = Flask(__name__)

dbs = DBs(
    memory=DB('app/dbs/memory', cleanup_on_exit=False),
    inputs=DB('app/dbs/inputs', cleanup_on_exit=False),
          )

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

            # save the file to the inputs database and get the hash_key
            hash_key = dbs.inputs.add(temp_file.name)
            temp_file.close()

            # run the analysis and draw the bounding boxes
            doc = DocumentAnalysis(dbs, 'pdf-to-text-aws', hash_key)
            bb_hash_key, csv_hash_key, json_hash_key = doc.draw_bounding_boxes(testing=True)

            json_data = json.loads(dbs.memory.get(json_hash_key))
            json_path = f"dbs/memory/{json_hash_key}"
            csv_path = f"dbs/memory/{csv_hash_key}"
            pdf_path = f"dbs/memory/{bb_hash_key}"

            # extarct text from the document
            text_extractor = TextExtractor(json_path="app/"+json_path)
            text = text_extractor.extract_text()
            # use your TextComprehender here to generate the response
            response = text_comprehender.comprehend_text(text, init=True)

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
