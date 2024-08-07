
#%%
# STEP 4 - GATEWAYS IDENTIFICATION
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Explanation:
To accurately identify gateways for decision points and parallelism in BPMN, you need to understand the following concepts:
    1) XOR Split (Exclusive Gateway)
        - Definition: Used to model decision points where only one of the available paths can be taken (either/or decision).
        - Textual Clues: "if", "only if", "either", "exclusive", "else", "depending on", "in case of", "should", "must", "when".
        - Behavior: Checks all conditions for each path. Only one path is taken based on the condition.
        - Example:
            Text: "If the credit is approved, process the payment. Else, send a rejection notice."
            Model:
                Gateway: XOR_CreditApproved?
                Path 1: Yes → Task: Process payment
                Path 2: No → Task: Send rejection notice
    2) XOR Join (Exclusive Gateway)
        - Definition: Waits for one active path to arrive before moving forward. No synchronization required.
        - Contextual Clues: Actions taken after multiple alternative paths, concluding decisions where one of several conditions is met.
        - Behavior: Sometimes inferred from context if explicit clues are not present.
        - Example:
            Text: "Notify the customer after the order is either approved or rejected."
            Model:
                Gateway: XOR_OrderOutcome?
                Path 1: Approved → Task: Notify customer
                Path 2: Rejected → Task: Notify customer
    3) OR Split (Inclusive Gateway)
        - Definition: Allows multiple paths to be taken simultaneously (one or more paths can be chosen based on conditions).
        - Textual Clues: "optionally", "can", "might", "inclusive", "and/or", "one or more", "any of", "possibly", "choose", "elect".
        - Behavior: Checks conditions for each path. Multiple paths with true conditions are taken simultaneously.
        - Example:
            Text: "A customer can choose to receive email notifications, SMS notifications, or both."
            Model:
                Gateway: OR_NotificationPreferences?
                Path 1: Email → Task: Send email notification
                Path 2: SMS → Task: Send SMS notification
    4) OR Join (Inclusive Gateway)
        - Definition: Waits for all active paths to arrive before moving forward. Synchronizes all active paths.
        - Contextual Clues: Need to wait for multiple tasks or conditions to be completed before proceeding.
        - Behavior: Sometimes inferred from context if explicit clues are not present.
        - Example:
            Text: "After completing email, social media, and direct mail campaigns, analyze the results."
            Model:
                Gateway: OR_AnalyzeResults?
                Path 1: Email → Task: Analyze email results
                Path 2: Social Media → Task: Analyze social media results
                Path 3: Direct Mail → Task: Analyze direct mail results
    5) AND Split (Parallel Gateway)
        - Definition: Models situations where multiple tasks occur concurrently (all paths are taken simultaneously without conditions).
        - Textual Clues: "and", "both", "concurrently", "simultaneously", "parallel", "at the same time", "in tandem", "jointly", "while".
        - Behavior: Starts all paths at the same time, allowing tasks to be done concurrently.
        - Example:
            Text: "The system will package and label the order at the same time."
            Model:
                Gateway: AND_PackageAndLabel
                Path 1: Task: Package order
                Path 2: Task: Label order
    6) AND Join (Parallel Gateway)
        - Definition: Waits for all paths to be completed before moving forward. Ensures all tasks are done before proceeding.
        - Contextual Clues: Multiple parallel tasks or conditions need to be completed before a subsequent action can be taken.
        - Behavior: Sometimes inferred from context if explicit clues are not present.
        - Example:
            Text: "Proceed after receiving approvals from both the technical and financial departments."
            Model:
                Gateway: AND_Approvals
                Path 1: Task: Technical approval
                Path 2: Task: Financial approval

TASK: Given the process description and the list of Activities/Events (also called "Nodes") identified from this description within the delimiters {delimiter}. Output a Python list of JSON objects. Ensure the output is strictly in JSON format without any additional text. Please Identify as many gateways as you can by performing the following steps:

Instructions:
- Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details. Try to identify gateways.
- Using the list of provided "ActivitiesEvent", identify gateways along with textual clues that led to the decision. 
- Identify as many gateways as you can, whether they are for divergence (such as XOR-split, OR-split, or AND-split) or convergence (such as XOR-join, OR-join, or AND-join). Generally, if a process has a split gateway (e.g., XOR-split, OR-split, or AND-split), it will be followed by a corresponding join gateway (e.g., XOR-join, OR-join, or AND-join) to converge the paths. However, this is not always the case; several split gateways could converge into a single join gateway.
- Output a Python list of JSON objects, detailing the gateways identified in Step 1. Ensure the output is strictly in JSON format without any additional text. Do not print out Step 1.
- DO NOT output additional text except the JSON format. Do not output ```json or ```

JSON Object Structure
- total_gateways: Total number of gateways identified. total_gateways = total_XOR_split + total_XOR_join + total_AND_split + total_AND_join + total_OR_split + total_OR_join
- total_XOR_split: Number of XOR split gateways.
- total_XOR_join: Number of XOR join gateways.
- total_AND_split: Number of AND split gateways.
- total_AND_join: Number of AND join gateways.
- total_OR_split: Number of OR split gateways.
- total_OR_join: Number of OR join gateways.
- gateways: A list of gateway objects, each containing:
    -- id: Unique identifier for the gateway.
    -- name: Placeholder name for the gateway.
    -- type: Type of gateway (XOR, AND, OR).
    -- classification: Indicates whether the gateway is a "split" or "join".
    -- conditions: Specify the splitting condition for divergence gateways and the merging (joining) condition for convergence gateways.
    -- from_node: Node(s) preceding the gateway.
    -- to_nodes: Node(s) following the gateway.
    -- reason: This is a description explaining (clues) why you can make that inference.

    

Examples:

Example 1:
Input:

Output:

Example 2:
Input:

Output:

Example 3:
Input:

Output:

Example 4:
Input:

Output:

Example 5:
Input:

Output:


=====================================================
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
        ]
    }
]

Output:
[
    {
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
                "conditions": [
                    {
                        "condition": "If any documents are missing or incorrect, return to new hire for correction",
                        "to_node": "A_ReturnForCorrection"
                    },
                    {
                        "condition": "If all documents are complete and correct, schedule orientation",
                        "to_node": "A_ScheduleOrientation"
                    }
                ],
                "from_node": ["A_ReviewDocuments"],
                "to_nodes": ["A_ReturnForCorrection", "A_ScheduleOrientation"],
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
                "from_node": ["A_ReturnForCorrection", "A_ScheduleOrientation"],
                "to_nodes": ["A_AssignToDepartment"],
                "reason": "After attending the orientation and completing all necessary steps, the new hire is assigned to their department."
            }
        ]
    }
]

"""
# Final Notes
# - Generally, if a process has a split gateway (e.g., XOR-split, OR-split, or AND-split), it will be followed by a corresponding join gateway (e.g., XOR-join, OR-join, or AND-join) to converge the paths. However, this is not always the case, as some processes may diverge without needing an explicit convergence.
# - Ensure the output is strictly in JSON format without any additional text.

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
    Identifies gateways in a business process description.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        dict: A dictionary containing identified gateways and related metadata.
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
            ]
        }
    ]

    """
    result, prompt_tokens, completion_tokens = identify_from_message(text_description, api="openai", model="gpt-4o-mini", temperature=0.0)
    print(result)

# %%
