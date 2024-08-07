
#%%
# STEP 5 - LOOPS/CYCLES IDENTIFICATION
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Understand the textual description, identify context, and overall process goal of textual descriptions of BPMN process models within the delimiters {delimiter}. Output a Python list of JSON objects with keys: Loop. Ensure the output is strictly in JSON format without any additional text.

Instructions:
- Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details. Try to identify loops.
- Using the list of provided "ActivitiesEvent" and list of provided "Gateways", identify loops.
- Identify Loops: Look for any repeated actions or instructions that indicate a task or set of tasks is performed more than once under certain conditions.
- Read the Process Description Thoroughly: Look for any repeated actions or instructions that indicate a task or set of tasks is performed more than once under certain conditions.
- Identify Key Phrases and Conditions: Phrases like "if not approved, then...", "repeat until...", "loop back to...", "revisit...", or "perform again" are indicators of loops or cycles in the process.
- Trace the Sequence of Activities: Identify the sequence flow of activities. If an activity leads back to a previous activity, forming a closed path, this indicates a loop or cycle. 
    - Textual Clues: Look for actions or events that repeat based on certain conditions.
- Look for Decision Points: Decision points (gateways) in the process often control the looping behavior. Exclusive gateways (XOR) are commonly used to determine whether to repeat a set of activities or proceed to the next step.
    - Textual Clues: Words like "if", "else", "otherwise", or "depending on".
- Examine Feedback Mechanisms: Check for feedback loops where the output or result of a process step is evaluated, and based on the evaluation, the process may loop back to an earlier step for rework or further action.
- Identify Loop Control Conditions: Understand the conditions under which the loop continues and the conditions under which the loop terminates. This helps to accurately model the loop in BPMN.
    - Textual Clues: Conditions or criteria for repetition, such as "until approved", "while not complete", or "as long as".
- DO NOT output additional text except the JSON format. Do not output ```json or ```



Examples:

Input:
The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.

[
    {
        "ModelName": "Onboarding process",
        "Context": "Human Resources",
        "Scope": "Starts with the submission of completed paperwork by the new hire and ends with the assignment of the new hire to their department.",
        "Objectives": "To ensure new hires complete all necessary paperwork, attend orientation, and are successfully integrated into their departments.",
        "Participants": [
            {"HR_Department": "Responsible for reviewing documents, scheduling orientation, and assigning new hire to the department"},
            {"New_Hire": "Responsible for submitting paperwork and attending orientation"}
        ],
        "StartEvent": "Start_SubmitPaperwork",
        "EndEvent": "End_AssignDepartment",
        "ActivitiesEvents": [
            {"A_ReviewDocuments": "The HR department reviews the submitted documents"},
            {"A_ReturnForCorrection": "If any documents are missing or incorrect, they are returned to the new hire for correction"},
            {"A_ScheduleOrientation": "Once the documents are in order, the new hire is scheduled for orientation"},
            {"E_AttendOrientation": "After attending the orientation"},
            {"A_AssignToDepartment": "the new hire is assigned to their department"}
        ],
        "total_gateways": 2,
        "total_XOR_split": 1,
        "total_XOR_join": 1,
        "total_AND_split": 0,
        "total_AND_join": 0,
        "total_OR_split": 0,
        "total_OR_join": 0,
        "Gateways": [
            {
                "id": "G1",
                "name": "XOR_ReviewDocuments",
                "type": "XOR",
                "classification": "split",
                "from_node": ["A_ReviewDocuments"],
                "to_nodes": ["A_ReturnForCorrection", "A_ScheduleOrientation"],
                "reason": "If any documents are missing or incorrect, they are returned to the new hire for correction. Otherwise, the new hire is scheduled for orientation."
            },
            {
                "id": "G2",
                "name": "XOR_OnboardingComplete",
                "type": "XOR",
                "classification": "join",
                "from_node": ["A_ReturnForCorrection", "A_ScheduleOrientation"],
                "to_nodes": ["A_AssignToDepartment"],
                "reason": "After attending the orientation, the new hire is assigned to their department."
            }
        ]
    }
]

Output:
[
    {
        "Loops": [
            {
                "LoopID": "L1",
                "LoopDescription": "Document correction loop",
                "Conditions": "If any documents are missing or incorrect",
                "GatewaysForLoopEntries":[],
                "GatewaysForLoopExits":[
                    {
                        "LoopExit1": "XOR_ReviewDocuments"
                    }
                ],
                "ActivitiesInLoop": [
                    "A_ReviewDocuments",
                    "A_ReturnForCorrection"
                ]
            }
        ]
    }
]

Input:
The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.

Output:
[
    {
        "Loops": []
    }
]
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
    Identifies loops in a business process description.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        dict: A dictionary containing identified loops.
    """
    system_message = SYSTEM_MESSAGE_TEMPLATE
    user_message = construct_user_message(text)
    messages = construct_messages(system_message, user_message)

    #response = get_completion(messages, api="ollama", model="llama3.1", max_tokens=1000, temperature=0.0)
    response, prompt_tokens, completion_tokens = get_completion(messages, api, model, temperature)
    return response, prompt_tokens, completion_tokens
    # try:
    #     return json.loads(response)
    # except json.JSONDecodeError:
    #     return {"error": "Failed to decode JSON response"}

# Example usage
if __name__ == "__main__":
    text_description = """
    Relevant Process Description information and JSON format of Context:
    Once a loan application is received by the loan provider, and before proceeding with its assessment, the application itself needs to be checked for completeness. If the application is incomplete, it is returned to the applicant, so that they can fill out the missing information and send it back to the loan provider. This process is repeated until the application is found complete.

    [
        {
            "ModelName": "Loan Application Completeness Check",
            "Context": "Finance",
            "Scope": "Starts with the receipt of a loan application by the loan provider and ends with the application being found complete.",
            "Objectives": "To ensure that loan applications are complete before proceeding with their assessment.",
            "Participants": [
                {"Loan_Provider": "Responsible for checking the completeness of the loan application and returning incomplete applications to the applicant"},
                {"Applicant": "Responsible for filling out missing information and resubmitting the loan application"}
            ],
            "StartEvent": "Start_ReceiveLoanApplication",
            "EndEvent": "End_ApplicationComplete",
            "ActivitiesEvent": [
                {"A_CheckApplicationCompleteness": "The application itself needs to be checked for completeness"},
                {"A_ReturnIncompleteApplication": "If the application is incomplete, it is returned to the applicant"},
                {"A_ResubmitApplication": "Applicant fills out the missing information and sends it back to the loan provider"}
            ],
            "Gateways": [
                {
                    "id": "G1",
                    "name": "XOR_CheckCompleteness",
                    "type": "XOR",
                    "classification": "split",
                    "from_node": ["A_CheckApplicationCompleteness"],
                    "to_nodes": ["A_ReturnIncompleteApplication", "End_ApplicationComplete"],
                    "reason": "If the application is incomplete, it is returned to the applicant. Otherwise, the application is found complete."
                },
                {
                    "id": "G2",
                    "name": "XOR_ResubmitOrComplete",
                    "type": "XOR",
                    "classification": "join",
                    "from_node": ["A_ReturnIncompleteApplication", "A_ResubmitApplication"],
                    "to_nodes": ["A_CheckApplicationCompleteness"],
                    "reason": "The process is repeated until the application is found complete, indicating a loop where the application is resubmitted and checked again."
                }
            ]
        }
    ]
    """
    result, prompt_tokens, completion_tokens = identify_from_message(text_description, api="openai", model="gpt-4o-mini", temperature=0.0)
    print(result)

# %%
