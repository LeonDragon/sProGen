
#%%
# STEP 3-1 - (OPTIONAL) IDENTIFY EXECUTION INSTANCE (FLOW OF ACTIONS)
# It will make easier to identify gateways, loops, and sequence flows latter.
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """"
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Explanation: In a business process, the flow of actions refers to the sequence in which activities and events (collectively called nodes) are executed. Identifying the flow involves understanding how one activity leads to another and how events trigger transitions between activities. This can include various types of flows such as sequential flows, conditional flows, and parallel flows.

TASK: Given the process description and the list of Activities/Events (also called "Nodes") identified from this description within the delimiters {delimiter}, output a Python list of JSON objects. Ensure the output is strictly in JSON format without any additional text. Please identify the flow of actions (Activities/Events) by performing the following steps:

Instructions:
- Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details.
- Identify Nodes: Using the list of provided "Activities/Events," identify the sequence of actions and their flow in the process.
- Determine Flow: Establish the flow between identified nodes, such as flow_1, flow_2, etc., ensuring each transition is clear and follows the logical sequence of the business process.
- Construct JSON Objects: For each flow, create a JSON object that includes the list of nodes in the flow, in the correct sequence.
- Output Format: Output a Python list of JSON objects detailing the flows identified in the previous steps. Ensure the output is strictly in JSON format without any additional text.

Examples:

Example 1:
Input:
The process begins with a customer browsing an online bookstore and selecting a book to purchase. After adding the book to the cart, the customer proceeds to checkout. The system then prompts the customer to enter shipping and payment details. Once the payment is successfully processed, the system generates an order confirmation. The warehouse receives the order and prepares the book for shipment. The final step is shipping the book to the customer's address. The process concludes when the customer receives the book.

[
    {
        "ModelName": "Online Bookstore Purchase Process",
        "Context": "E-commerce",
        "Scope": "Starts with the customer browsing the online bookstore and ends with the customer receiving the book.",
        "Objectives": "To facilitate the purchase and delivery of a book from an online bookstore to the customer.",
        "Participants": [
            {"Customer": "Responsible for browsing, selecting a book, entering shipping and payment details, and receiving the book"},
            {"System": "Responsible for prompting shipping and payment details, processing payment, and generating order confirmation"},
            {"Warehouse": "Responsible for receiving the order and preparing the book for shipment"},
            {"Shipping_Company": "Responsible for delivering the book to the customer's address"}
        ],
        "StartEvent": "Start_BrowseBookstore",
        "EndEvent": "End_ReceiveBook",
        "ActivitiesEvents": [
            {"A_SelectBook": "Customer selects a book to purchase", "Participant": "Customer"},
            {"A_AddToCart": "Customer adds the book to the cart", "Participant": "Customer"},
            {"A_ProceedToCheckout": "Customer proceeds to checkout", "Participant": "Customer"},
            {"A_EnterShippingPaymentDetails": "System prompts the customer to enter shipping and payment details", "Participant": "System"},
            {"A_ProcessPayment": "System processes the payment", "Participant": "System"},
            {"A_GenerateOrderConfirmation": "System generates an order confirmation", "Participant": "System"},
            {"A_ReceiveOrder": "Warehouse receives the order", "Participant": "Warehouse"},
            {"A_PrepareShipment": "Warehouse prepares the book for shipment", "Participant": "Warehouse"},
            {"A_ShipBook": "Shipping company ships the book to the customer", "Participant": "Shipping_Company"}
        ]
    }
]

Output:
[
    {
        "ActionFlows": [
            {"from": "Start_SubmitPaperwork", "to": "A_ReviewDocuments"},
            {"from": "A_ReviewDocuments", "to": "A_ReturnForCorrection"},
            {"from": "A_ReturnForCorrection", "to": "A_ReviewDocuments"},
            {"from": "A_ReviewDocuments", "to": "A_ScheduleOrientation"},
            {"from": "A_ScheduleOrientation", "to": "E_AttendOrientation"},
            {"from": "E_AttendOrientation", "to": "A_AssignToDepartment"},
            {"from": "A_AssignToDepartment", "to": "End_AssignDepartment"}
        ]
    }
]


"""

SYSTEM_MESSAGE_TEMPLATE_OLD = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Explanation: 
- Decision Point: A moment within a process where a choice must be made between two or more paths based on specific conditions or criteria. Decision points are crucial for managing process flow and ensuring scenarios are handled appropriately.
    - Examples: If the payment is successful, the order confirmation is generated. Once the user logs in, they can access their dashboard. When the temperature drops below freezing, the heating system activates.
    - Textual Clues: Look for conditional phrases that indicate decision points such as "If", "Once", "When", "Depending on", "In case of", "Should", "Must", "Can", "Might", "Choose", "Either", "Else", "Only if", "Provided that", "Assuming that", "Unless", "As long as", "Given that", "Otherwise", "In the event that", "In the case that", "Provided", "On condition that", "As soon as", "Supposing that", "Considering that", "In the scenario where", "Assuming", "In the circumstance that", "Contingent upon", "So long as", "Whenever", "Wherever", "Where", "Even if", "Just in case", "On the assumption that", "With the understanding that", etc.
- Execution Instance: A single occurrence of a process from Start Event to End Event, covering all possible paths through decision points.

TASK: Given the process description and the list of Activities/Events (also called "nodes") identified from this description within the delimiters {delimiter}, output a Python list of JSON objects. Ensure the output is strictly in JSON format without any additional text. Please identify the execution instance (Activities/Events) by performing the following steps:
- Read Thoroughly: Understand the process description, objectives, and scope.
- Identify Decision Points: List all decision points and their conditions.
- Determine Execution Instances:
    -- If there are no decision points, create a single execution instance.
    -- If there are decision points, create multiple execution instances based on each possible path through the decision points.
- Construct JSON Objects: For each execution instance, include a list of nodes in the correct sequence from Start Event to End Event.
- Output Format: Provide a Python list of JSON objects in strict JSON format, detailing each execution instance.

Detailed Instructions:
1. Identify Decision Points:
    - Clearly describe each decision point.
    - Specify the conditions and possible outcomes for each decision point.
2. Specify Activities/Events:
    - List all activities and events involved.
    - Indicate which activities or events are linked to specific decision points.
Describe Each Path:
    - For each decision point, describe all potential paths and how they impact the process flow

Examples:

Example 1:
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
        "ActionFlows": [
            {"from": "Start_SubmitPaperwork", "to": "A_ReviewDocuments"},
            {"from": "A_ReviewDocuments", "to": "A_ReturnForCorrection"},
            {"from": "A_ReturnForCorrection", "to": "A_ReviewDocuments"},
            {"from": "A_ReviewDocuments", "to": "A_ScheduleOrientation"},
            {"from": "A_ScheduleOrientation", "to": "E_AttendOrientation"},
            {"from": "E_AttendOrientation", "to": "A_AssignToDepartment"},
            {"from": "A_AssignToDepartment", "to": "End_AssignDepartment"}
        ]
    }
]




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
