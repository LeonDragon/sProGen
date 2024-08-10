# FLASK WEB UI
import json
from flask import Flask, render_template, request, url_for, jsonify
from main_pipeline import pipeline as bpm_genenration # Import the pipeline function
from bp_logic_visualizer import visualize_bpmn, generate_dot_from_sequence # Import graphviz visualizer function
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    description = request.form['description']
    result, sequenceFlows = bpm_genenration(description)
    
    # Save bpm SVG file to ./static
    try:
        data = json.loads(sequenceFlows)
        sequence_flows = data[0]["SequenceFlows"]
        bp_dot = generate_dot_from_sequence(sequence_flows)
        visualize_bpmn(bp_dot, file_name='web_view_bpm_model', directory='./static', file_format='svg')
        print(" ===> DONE \n")
    except Exception as e:
        print(" ===> Error in visualization")
        print(f"Error: {e}")
    
    # Assuming your visualization function saves an SVG in a predictable location
    svg_url = url_for('static', filename='web_view_bpm_model.svg')
    return jsonify({'svg_url': svg_url})

if __name__ == '__main__':
    app.run(debug=True)

# SAMPLE DESCRIPTION
# In the treasury minister’s office, once a ministerial inquiry has been received, it is first registered into the system. Then the inquiry is investigated so that a ministerial response can be prepared. The finalization of a response includes the preparation of the response itself by the cabinet officer and the review of the response by the principal registrar. If the registrar does not approve the response, the latter needs to be prepared again by the cabinet officer for review. The process finishes only once the response has been approved. 