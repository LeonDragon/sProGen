# FLASK WEB UI
from flask import Flask, render_template, request, url_for, jsonify
import os

app = Flask(__name__)

# Import the pipeline function
from main_pipeline import pipeline

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    # description = request.form['description']
    # result, sequenceFlows = pipeline(description)
    
    # Assuming your visualization function saves an SVG in a predictable location
    svg_url = url_for('static', filename='my_bpmn_model.svg')
    return jsonify({'svg_url': svg_url})

if __name__ == '__main__':
    app.run(debug=True)
