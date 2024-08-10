
#%%
# STEP 3 - ACTIONS (EVENTS/ACTIVITIES) IDENTIFICATION
import json
from llm_completion_v2 import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Analyze the following textual description of a business process within the delimiters {####} and identify distinct activities. Ensure that each activity is unique and avoid listing any duplicate activities or events that may occur due to loops within the process. Provide a clear and concise list of these activities, explicitly handling any repetitive actions due to loops without duplicating them. Output a Python list of JSON objects with keys: StartEvent, EndEvent, Activities, and Participants. Ensure the output is strictly in JSON format without any additional text.

Instructions:
- Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details.
- Identify Start Event: Define the starting point of the process that initiates the workflow. Provide a brief label or description to clarify what triggers the process (e.g., Start_ReceiveOrder).
    - Textual Clues: Phrases indicating the initiation of the process, such as "The process begins when...", "Start by...", "Initially...", "Upon receiving...", or "As soon as...".
- Identify End Event: Define the endpoint of the process, describing the completion of the process flow. Provide a brief label or description to clarify the end condition (e.g., "End_OrderFulfilled", "End_InvoiceSent", End_ShipmentComplete).
    - Textual Clues: Phrases indicating the conclusion of the process, such as "The process ends when...", "Completion of...", "Finally...", "Once finished...", or "At the end...".
- Ensure Uniqueness: Ensure that each activity is unique and avoid listing any duplicate activities or events that may occur due to loops within the process. If you find similar activities or events, remove the duplicates and retain only the first instance.
    - Textual Clues for Removing Duplicates: Look for phrases indicating repetition or loops such as "re-...", "re-submit", "if not approved, return to...", "... again" or "repeat until...".
- Identify Activities/Events: Identify specific actions or tasks described in the text and event usually in verb forms, assigning a variable to each (e.g., A_RecieveOrder, A_CheckCredit, E_RecieveEmail) (note that A for activities or tasks, E for Events). List of distinct activities without any redundancy.
    - Textual Clues: These are the core actions that drive the process forward. Look for verbs or action phrases like "register", "investigate", "prepare", "review", "approve", "admit", "examine", "process", "schedule", or "conduct".
- Identify Participants: Identify the single participant involved in each activity or event and include them in the output.
- DO NOT output additional text except the JSON format. Do not output ```json or ```. Do not output comment "//"


"""


SYSTEM_MESSAGE_TEMPLATE_OLD = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Analyze the following textual description of a business process within the delimiters {delimiter} and identify distinct activities. Ensure that each activity is unique and avoid listing any duplicate activities or events that may occur due to loops within the process. Provide a clear and concise list of these activities, explicitly handling any repetitive actions due to loops without duplicating them.. Output a Python list of JSON objects with keys: StartEvent, EndEvent, Activities. Ensure the output is strictly in JSON format without any additional text.

Instructions:
- Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details.
- Identify Start Event: Define the starting point of the process that initiates the workflow. Provide a brief label or description to clarify what triggers the process (e.g., Start_ReceiveOrder).
    - Textual Clues: Phrases indicating the initiation of the process, such as "The process begins when...", "Start by...", "Initially...", "Upon receiving...", or "As soon as...".
- Identify End Event: Define the endpoint of the process, describing the completion of the process flow. Provide a brief label or description to clarify the end condition (e.g., "End_OrderFulfilled", "End_InvoiceSent", End_ShipmentComplete).
    - Textual Clues: Phrases indicating the conclusion of the process, such as "The process ends when...", "Completion of...", "Finally...", "Once finished...", or "At the end...".
- Ensure Uniqueness: Ensure that each activity is unique and avoid listing any duplicate activities or events that may occur due to loops within the process. If you find similar activities or events, remove the duplicates and retain only the first instance.
    - Textual Clues for Removing Duplicates: Look for phrases indicating repetition or loops such as "re-...", "re-submit", "if not approved, return to...", "... again"or "repeat until...".
- Identify Activities/Events: Identify specific actions or tasks described in the text and event usually in verb forms, assigning a variable to each (e.g., A_RecieveOrder, A_CheckCredit, E_RecieveEmail) (note that A for activities or tasks, E for Events). List of distinct activities without any redundancy.
    - Textual Clues:These are the core actions that drive the process forward. Look for verbs or action phrases like "register", "investigate", "prepare", "review", "approve", "admit", "examine", "process", "schedule", or "conduct".


Examples:

Input:
The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.

[
    {
        "Context": "Human Resources",
        "Scope": "Starts with the submission of completed paperwork by the new hire and ends with the assignment of the new hire to their department.",
        "Objectives": "To ensure new hires complete all necessary paperwork, attend orientation, and are successfully integrated into their departments.",
        "Participants": [
            {"HR_Department": "Responsible for reviewing documents, scheduling orientation, and assigning new hire to the department"},
            {"New_Hire": "Responsible for submitting paperwork and attending orientation"}
        ]
    }
]

Output:
[
    {
        "ModelName": "Onboarding process",
        "StartEvent": "Start_SubmitPaperwork",
        "EndEvent": "End_AssignDepartment",
        "ActivitiesEvent": [
            {"A_ReviewDocuments": "The HR department reviews the submitted documents"},
            {"A_ReturnForCorrection": "If any documents are missing or incorrect, they are returned to the new hire for correction"},
            {"A_ScheduleOrientation": "Once the documents are in order, the new hire is scheduled for orientation"},
            {"E_AttendOrientation": "After attending the orientation"},
            {"A_AssignToDepartment": "the new hire is assigned to their department"}
        ]
    }
]

Input:
The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.

[
    {
        "ModelName": "Product development process",
        "Context": "Manufacturing",
        "Scope": "Starts with the identification of market needs and ends with the launch of the product into the market.",
        "Objectives": "To develop a new product that meets market needs, from concept to market launch.",
        "Participants": [
            {"Market_Analysts": "Responsible for identifying market needs"},
            {"Designers": "Responsible for creating the product concept and designing the product"},
            {"Developers": "Responsible for developing the product prototype"},
            {"Testers": "Responsible for testing the prototype"}
        ]
    }
]

Output:
[
    {
        "StartEvent": "Start_IdentifyMarketNeeds",
        "EndEvent": "End_LaunchProduct",
        "ActivitiesEvent": [
            {"A_CreateConcept": "Once the needs are identified, a product concept is created"},
            {"A_DesignProduct": "The next step is to design the product"},
            {"A_DevelopPrototype": "followed by developing a prototype"},
            {"A_TestPrototype": "The prototype is then tested"},
            {"A_FinalizeProduct": "if it meets the requirements, the product is finalized"},
            {"A_LaunchProduct": "and launched into the market"}
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

def json_format():
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "process_flow",
            "schema": {
                "type": "object",
                "properties": {
                    "StartEvent": {"type": "string"},
                    "EndEvent": {"type": "string"},
                    "ActivitiesEvents": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "activity": {"type": "string"},
                                "description": {"type": "string"},
                                "participant": {"type": "string"}
                            },
                            "required": ["activity", "description", "participant"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["StartEvent", "EndEvent", "ActivitiesEvents"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
    return response_format

def identify_from_message(text, api="openai", model="gpt-4o-mini", json_format="", temperature=0.0,):
    """
    Identifies activities or events in a business process description.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        dict: A dictionary containing identified  activities or events.
    """
    system_message = SYSTEM_MESSAGE_TEMPLATE
    user_message = construct_user_message(text)
    messages = construct_messages(system_message, user_message)

    
    #response = get_completion(messages, api="ollama", model="llama3.1", max_tokens=1000, temperature=0.0)
    response, prompt_tokens, completion_tokens = get_completion(
        messages=messages,
        api=api,
        model=model,
        temperature=temperature,
        json_format=json_format
    )
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
            ]
        }
    ]
    """
    result, prompt_tokens, completion_tokens = identify_from_message(text_description, api="openai", model="gpt-4o-mini",json_format=json_format(), temperature=0.0,)
    print(result)

# %%
