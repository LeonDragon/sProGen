#%%
# STEP 7 - VISUALIZE BPM MODEL
import json
from llm_completion import get_completion
import graphviz

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Generate Graphviz DOT language for a given sequence flow of BPMN elements within the delimiter {delimiter}. Ensure the output is strictly in DOT language without any additional text.

Instructions:
- Use a round rectangle to represent activities or events.
- Use a diamond to represent gateways, with specific labels for each type:
    - Use "X" to denote XOR gateways. Remember to put related description near this element
    - Use "+" to denote AND gateways. Remember to put related description near this element
    - Use "O" to denote OR gateways. Remember to put related description near this element
- Use a circle to represent the Start Event.
- Use a thick bold circle to represent the End Event.
- Follow all best practices in BPMN modeling to ensure clarity and accuracy.
- Please use "\n" to break up labels (e.g., label=) if they are lengthy.
- DO NOT output additional text except the DOT language. Do not output ```dot or ```

Example:

Input:
"SequenceFlows": [
            {"from": "Start_SubmitPaperwork", "to": "A_ReviewDocuments"},
            {"from": "A_ReviewDocuments", "to": "XOR_ReviewDocuments"},
            {"from": "XOR_ReviewDocuments", "to": "A_ReturnForCorrection", "condition": "if documents are missing or incorrect"},
            {"from": "XOR_ReviewDocuments", "to": "A_ScheduleOrientation", "condition": "if documents are complete and correct"},
            {"from": "A_ReturnForCorrection", "to": "A_ReviewDocuments"},
            {"from": "A_ScheduleOrientation", "to": "E_AttendOrientation"},
            {"from": "E_AttendOrientation", "to": "XOR_OnboardingComplete"},
            {"from": "XOR_OnboardingComplete", "to": "A_AssignToDepartment"},
            {"from": "A_AssignToDepartment", "to": "End_AssignDepartment"}
        ]


Output:
digraph BPMN {
    rankdir=LR;
    node [shape=circle, style=filled, color=lightblue, penwidth=2];

    // Start and End nodes
    Start_SubmitPaperwork [label="", color=forestgreen];
    End_AssignDepartment [label="", color=firebrick, penwidth=3];

    // Activities
    node [
        shape=box, 
        style="rounded,filled", 
        fillcolor=lightgoldenrodyellow, 
        color=black,
        penwidth=1, 
        fontcolor=black];
    A_ReviewDocuments [label="Review \n Documents"];
    A_ReturnForCorrection [label="Return For \n Correction"];
    A_ScheduleOrientation [label="Schedule \n Orientation"];
    E_AttendOrientation [label="Attend \n Orientation"];
    A_AssignToDepartment [label="Assign To \n Department"];

    // Gateways
    node [
        shape=diamond, 
        style=filled, 
        fillcolor=gold, 
        color=black, 
        penwidth=1];
    XOR_ReviewDocuments [label="X"];
    XOR_OnboardingComplete [label="X"];

    // Edges
    Start_SubmitPaperwork -> A_ReviewDocuments;
    A_ReviewDocuments -> XOR_ReviewDocuments;

    XOR_ReviewDocuments -> A_ReturnForCorrection [label="if documents are \n missing or incorrect"];
    XOR_ReviewDocuments -> A_ScheduleOrientation [label="if documents are \n complete and correct"];
    A_ReturnForCorrection -> A_ReviewDocuments;
    A_ScheduleOrientation -> E_AttendOrientation;
    E_AttendOrientation -> XOR_OnboardingComplete;
    XOR_OnboardingComplete -> A_AssignToDepartment;
    A_AssignToDepartment -> End_AssignDepartment;

    // Labels positioned below the nodes
    start_label [shape=plaintext, label="Start: Submit Paperwork", fillcolor=white];
    end_label [shape=plaintext, label="End: Assign Department", fillcolor=white];

    { rank=same; Start_SubmitPaperwork; start_label; }
    { rank=same; End_AssignDepartment; end_label; }

    // Invisible edges for proper label positioning
    Start_SubmitPaperwork -> start_label [style=invis];
    End_AssignDepartment -> end_label [style=invis];
}

"""

def construct_user_message(text):
    """
    Constructs the user message by wrapping the text with delimiters.

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        str: The user message wrapped with delimiters.
    """
    return f"####{text}####"

def construct_messages(system_message, user_message):
    """
    Constructs the message payload for the API request.

    Parameters:
        system_message (str): The system message containing instructions.
        user_message (str): The user message containing the process description.

    Returns:
        list: A list of message dictionaries.
    """
    return [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

def visualize_bpmn(dot_string):
    """
    Visualizes a BPMN model using Graphviz.

    Parameters:
        dot_string (str): The DOT language representation of the BPMN model.
    """
    try:
        graph = graphviz.Source(dot_string)  # Create Graphviz Source object
        graph.render('bpmn_model', format='svg', view=True)  # Render and view the graph
        print("Graphviz visualization generated successfully.")
    except Exception as e:
        print("Error in generating visualization:", e)  # Print error message if any


def identify_from_message(text, api="openai", model="gpt-4o-mini", temperature=0.0):
    """
    Identifies sequence flows in a business process description.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        dict: A dictionary containing identified sequence flows.
    """
    system_message = SYSTEM_MESSAGE_TEMPLATE
    user_message = construct_user_message(text)
    messages = construct_messages(system_message, user_message)

    #response = get_completion(messages, api="ollama", model="llama3.1", max_tokens=1000, temperature=0.0)
    response = get_completion(messages, api, model, temperature)
    return response
    # try:
    #     return json.loads(response)
    # except json.JSONDecodeError:
    #     return {"error": "Failed to decode JSON response"}

# Example usage
if __name__ == "__main__":
    text_description = """
    [
        {
            "SequenceFlows": [
                {"from": "Start_SubmitPaperwork", "to": "A_ReviewDocuments"},
                {"from": "A_ReviewDocuments", "to": "XOR_ReviewDocuments"},
                {"from": "XOR_ReviewDocuments", "to": "A_ReturnForCorrection", "condition": "if documents are missing or incorrect"},
                {"from": "XOR_ReviewDocuments", "to": "A_ScheduleOrientation", "condition": "if documents are complete and correct"},
                {"from": "A_ReturnForCorrection", "to": "A_ReviewDocuments"},
                {"from": "A_ScheduleOrientation", "to": "E_AttendOrientation"},
                {"from": "E_AttendOrientation", "to": "XOR_OnboardingComplete"},
                {"from": "XOR_OnboardingComplete", "to": "A_AssignToDepartment"},
                {"from": "A_AssignToDepartment", "to": "End_AssignDepartment"}
            ]
        }
    ]
    """
    result = identify_from_message(text_description, api="openai", model="gpt-4o", temperature=0)
    print(result)
    # Visualize the result
    visualize_bpmn(result)

# %%
