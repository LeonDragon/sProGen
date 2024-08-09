
#%%
# STEP 6 - SEQUENCE FLOWS IDENTIFICATION
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Understand the textual description, identify context, and overall process goal of textual descriptions of BPMN process models within the delimiters {delimiter}. Output a Python list of JSON objects with keys: SequenceFlows. Each object must include "from" and "to" keys that strictly follow the naming format: {"from": "Start_<ActivityName>", "to": "A_<ActivityName>"}, {"from": "E_<EventName>", "to": "OR_<GatewayName>"}, where:Start: Indicates the start of a sequence. A: Represents activities. XOR/OR/AND: Represents conditional or parallel gateways. E: Represents events. End: Indicates the end of a sequence.

Instructions:
1. Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details. Try to identify or infer the sequence flows of (events, activities, or gateways).
2. Using the list of provided "ActivitiesEvent," list of provided "Gateways", list of provided "Loops" (if any), and list of provided "ActionFlows", define the sequence flows ("SequenceFlows"). Ensure that each element is correctly categorized. Remember that the "SequenceFlows" are the extended version of "ActionFlows" with "gateways".
3. Establish Sequence Flows: Establish the order of activities, events, and gateways, detailing the sequence flow with variables. Ensure the sequence logically follows the process goals identified in Step 1. Strictly follow the "from" and "to" of each gateways to correctly identify the sequence flow.
4. Distinguish Gateways: Clearly distinguish between the types of gateways and represent the conditional (XOR, OR) and parallel (AND) flows accurately. Double-check that the gateways are correctly categorized and represent the process logic before moving to the validation steps.
5. Validation with Negative Prompts:
    - Check the final results against the "Negative Prompts."
    - If errors are detected, identify the specific part of the sequence flow where the error occurred, correct it based on the provided instructions, and then revalidate that part before continuing.
    - If no errors are found, proceed to Step 6.
6. Validation with BPMN-Specific Negative Prompts:
    - Check the final results against the "BPMN-Specific Negative Prompts."
    - If errors are detected, identify the specific part of the sequence flow where the error occurred, correct it based on the provided instructions, and then revalidate that part before continuing.
    - If no errors are found, produce the output.

Negative Prompts:
- No Additional Text: DO NOT include any additional text or metadata in the output, such as code comments, explanations, or formatting markers (e.g., ```json, ```, #, //).
- No Non-JSON Data: DO NOT output any non-JSON data, such as headers, footers, or any descriptive text that is not part of the JSON structure.
- No Empty or Null Values: DO NOT include empty or null values in the JSON output unless they are explicitly required by the context of the sequence flow.
- No Inconsistent Formatting: DO NOT use inconsistent formatting in the JSON structure, such as unnecessary white spaces, line breaks, or indentation that does not adhere to standard JSON formatting practices.
- No Incorrect Keys or Fields: DO NOT use incorrect or additional keys or fields in the JSON objects that are not specified in the task (e.g., avoid adding extra fields like "Notes" or "Description" unless explicitly instructed).

BPMN-Specific Negative Prompts:
- Gateway Split and Join: DO NOT allow a gateway to have multiple incoming flows with multiple outgoing flows simultaneously. Ensure that a gateway either splits (one incoming flow with multiple outgoing flows) or joins (multiple incoming flows with one outgoing flow) but not both at the same time.
- Prevent Single Flow Gateways: DO NOT allow gateways to have a single incoming flow and a single outgoing flow. Gateways must represent decision points or parallel processing and should always have multiple outgoing or incoming flows.
- Nodes Connection: DO NOT allow any nodes (activities, events, or gateways) to be unconnected. Every node must be connected to at least one other node via a sequence flow, ensuring continuity in the process flow.
- Dangling Sequence Flows: DO NOT create sequence flows that do not have a proper start or end point. All sequence flows must begin and end at defined nodes, ensuring a logical and continuous path through the process.
- Avoid Cyclic Loops (unless specified): DO NOT create cyclic loops unless explicitly indicated in the textual description and in the given JSON key of "Loops". Loops should be clearly defined and intentional, not a result of misinterpreted sequence flows.
- Misalignment of Events and Activities: DO NOT allow sequence flows that improperly align events and activities, such as flows that incorrectly connect a start event directly to an activity or skip necessary steps in the process.
- Inconsistent Use of Parallel and Conditional Flows: DO NOT mix parallel (AND) and conditional (XOR/OR) flows inappropriately. Ensure that the correct gateway type is used and that the flow logic is consistent and accurate.


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
        "ActionFlows": [
            {"from": "Start_SubmitPaperwork", "to": "A_ReviewDocuments"},
            {"from": "A_ReviewDocuments", "to": "A_ReturnForCorrection"},
            {"from": "A_ReturnForCorrection", "to": "A_ReviewDocuments"},
            {"from": "A_ReviewDocuments", "to": "A_ScheduleOrientation"},
            {"from": "A_ScheduleOrientation", "to": "E_AttendOrientation"},
            {"from": "E_AttendOrientation", "to": "A_AssignToDepartment"},
            {"from": "A_AssignToDepartment", "to": "End_AssignDepartment"}
        ],
        "Gateways": [
            {
                "id": "G1",
                "name": "XOR_ReviewDocuments",
                "type": "XOR",
                "classification": "split",
                "conditions": [
                    {
                        "condition": "If any documents are missing or incorrect, return to new hire for correction",
                        "to": "A_ReturnForCorrection"
                    },
                    {
                        "condition": "If all documents are complete and correct, schedule orientation",
                        "to": "A_ScheduleOrientation"
                    }
                ],
                "from": ["A_ReviewDocuments"],
                "to": ["A_ReturnForCorrection", "A_ScheduleOrientation"],
                "reason": "If any documents are missing or incorrect, they are returned to the new hire for correction. Otherwise, the new hire is scheduled for orientation."
            },
            {
                "id": "G2",
                "name": "XOR_OnboardingComplete",
                "type": "XOR",
                "classification": "join",
                "conditions": [
                    {
                        "condition": "All necessary steps are completed, assign to department",
                        "to_node": "A_AssignToDepartment"
                    }
                ],
                "from": ["A_ReturnForCorrection", "A_ScheduleOrientation"],
                "to": ["A_AssignToDepartment"],
                "reason": "After attending the orientation and completing all necessary steps, the new hire is assigned to their department."
            }
        ],
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

Output:
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
            ],
            "Loops": [
                {
                    "LoopID": "L1",
                    "LoopDescription": "Application completeness check loop",
                    "Conditions": "If the application is incomplete",
                    "GatewaysForLoopEntries": [],
                    "GatewaysForLoopExits": [
                        {
                            "LoopExit1": "XOR_CheckCompleteness"
                        }
                    ],
                    "ActivitiesInLoop": [
                        "A_CheckApplicationCompleteness",
                        "A_ReturnIncompleteApplication",
                        "A_ResubmitApplication"
                    ]
                }
            ]
        }
    ]
    """
    result = identify_from_message(text_descriptionapi="openai", model="gpt-4o-mini", temperature=0.0)
    print(result)

# %%
Final_output = """
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
                    "reason": "The process is repeated until the application is found complete."
                }
            ],
            "Loops": [
                {
                    "LoopID": "L1",
                    "LoopDescription": "Application completeness check loop",
                    "Conditions": "If the application is incomplete",
                    "GatewaysForLoopEntries": [],
                    "GatewaysForLoopExits": [
                        {
                            "LoopExit1": "XOR_CheckCompleteness"
                        }
                    ],
                    "ActivitiesInLoop": [
                        "A_CheckApplicationCompleteness",
                        "A_ReturnIncompleteApplication",
                        "A_ResubmitApplication"
                    ]
                }
            ],
            "SequenceFlows": [
                {"from": "Start_ReceiveLoanApplication", "to": "A_CheckApplicationCompleteness"},
                {"from": "A_CheckApplicationCompleteness", "to": "XOR_CheckCompleteness"},
                {"from": "XOR_CheckCompleteness", "to": "A_ReturnIncompleteApplication", "condition": "if application is incomplete"},
                {"from": "XOR_CheckCompleteness", "to": "End_ApplicationComplete", "condition": "if application is complete"},
                {"from": "A_ReturnIncompleteApplication", "to": "A_ResubmitApplication"},
                {"from": "A_ResubmitApplication", "to": "XOR_ResubmitOrComplete"},
                {"from": "XOR_ResubmitOrComplete", "to": "A_CheckApplicationCompleteness"}
            ]
        }
    ]
"""