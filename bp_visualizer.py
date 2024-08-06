#%%
# STEP 7 - VISUALIZE BPM MODEL
import json
from llm_completion import get_completion

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

Example:

Input:
"SequenceFlows": [
    {
        "from": "Start",
        "to": "Activity 1"
    },
    {
        "from": "Activity 1",
        "to": "Split Gateway"
    },
    {
        "from": "Split Gateway",
        "to": "Activity 2",
        "condition": "Condition A"
    },
    {
        "from": "Split Gateway",
        "to": "Activity 3",
        "condition": "Condition B"
    },
    {
        "from": "Activity 2",
        "to": "Join Gateway 1"
    },
    {
        "from": "Activity 3",
        "to": "Join Gateway 1"
    },
    {
        "from": "Join Gateway 1",
        "to": "Activity 4"
    },
    {
        "from": "Activity 4",
        "to": "Split Gateway 2"
    },
    {
        "from": "Split Gateway 2",
        "to": "Activity 5",
        "condition": "Condition C"
    },
    {
        "from": "Split Gateway 2",
        "to": "Join Gateway 2",
        "condition": "Condition D"
    },
    {
        "from": "Activity 5",
        "to": "Join Gateway 2"
    },
    {
        "from": "Join Gateway 2",
        "to": "Loop Gateway"
    },
    {
        "from": "Loop Gateway",
        "to": "Activity 1",
        "condition": "Loop Condition"
    },
    {
        "from": "Loop Gateway",
        "to": "End",
        "condition": "Exit Loop"
    }
]


Output:
digraph BPMN {
    rankdir=LR;
    node [shape=circle, style=filled, color=lightblue];

    // Start and End nodes
    start [label="", color=green];
    end [label="", color=red, penwidth=3];

    // Activities
    node [shape=box, style=rounded, color=lightgreen];
    activity1 [label="Activity 1"];
    activity2 [label="Activity 2"];
    activity3 [label="Activity 3"];
    activity4 [label="Activity 4"];
    activity5 [label="Activity 5"];

    // Gateways
    node [shape=diamond, style=filled, color="#FFD700"];
    split_gateway [label="Split Gateway"];
    join_gateway1 [label="Join Gateway 1"];
    split_gateway2 [label="Split Gateway 2"];
    join_gateway2 [label="Join Gateway 2"];
    loop_gateway [label="Loop Gateway"];

    // Edges
    start -> activity1;
    activity1 -> split_gateway;
    split_gateway -> activity2 [label="Condition A"];
    split_gateway -> activity3 [label="Condition B"];
    activity2 -> join_gateway1;
    activity3 -> join_gateway1;
    join_gateway1 -> activity4;
    activity4 -> split_gateway2;
    split_gateway2 -> activity5 [label="Condition C"];
    split_gateway2 -> join_gateway2 [label="Condition D"];
    activity5 -> join_gateway2;
    join_gateway2 -> loop_gateway;
    loop_gateway -> activity1 [label="Loop Condition"];
    loop_gateway -> end [label="Exit Loop"];

    // Labels positioned below the nodes
    start_label [shape=plaintext, label="Start_ ...", color=white];
    end_label [shape=plaintext, label="End_ ...", color=white];

    { rank=same; start; start_label; }
    { rank=same; end; end_label; }

    // Invisible edges for proper label positioning
    start -> start_label [style=invis];
    end -> end_label [style=invis];
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
    result = identify_from_message(text_description, api="openai", model="gpt-4o-mini", temperature=0.7)
    print(result)

# %%
