from flask import Flask, render_template, request, send_file
from textract.document_analysis import draw_bounding_boxes  # adjust this import as necessary
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # save the file to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            file.save(temp_file.name)
            # create paths for the output files
            json_path = os.path.join('app', 'textract_results', 'output.json')
            output_path = os.path.join('app', 'bounding_box_results', 'output.pdf')
            # run the analysis and draw the bounding boxes
            draw_bounding_boxes(temp_file.name, 'your-bucket', file.filename, output_path, json_path)
            # close and delete the temporary file
            temp_file.close()
            os.unlink(temp_file.name)
            # read the JSON data and send it to the user
            with open(json_path, 'r') as f:
                json_data = f.read()
            return render_template('results.html', json_data=json_data, pdf_filename=output_path)
    return render_template('upload.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
