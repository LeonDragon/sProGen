
#%%
# CHECK DUPLICATION OF IDENTIFIED ACTIONS (EVENTS/ACTIVITIES) - AFTER STEP 3
# Input from STEP 3 - Actions identification
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Analyze the following textual description of a business process within the delimiters {delimiter} and identify distinct activities. Ensure that each activity is unique and avoid listing any duplicate activities or events that may occur due to loops within the process. Provide a clear and concise list of these activities, explicitly handling any repetitive actions due to loops without duplicating them. Output a Python list of JSON objects. Ensure the output is strictly in JSON format without any additional text.

Instructions:
- Identify a list of activities or events from the description.
- Validate if there are any duplicated activities. Specifically, check if any activities can be referred to as the same task and are performed by the same participant.
- Answer with "Yes" or "No" regarding the presence of duplicated activities.
- List the duplicated activities and events as a JSON object.

Examples:

Input:
The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.

[
    {
        "ModelName": "Onboarding process",
        "StartEvent": "Start_SubmitPaperwork",
        "EndEvent": "End_AssignDepartment",
        "ActivitiesEvent": [
            {"A_ReviewDocuments": "The HR department reviews the submitted documents", "Participant": "HR_Department"},
            {"A_ReturnForCorrection": "If any documents are missing or incorrect, they are returned to the new hire for correction", "Participant": "HR_Department"},
            {"A_ScheduleOrientation": "Once the documents are in order, the new hire is scheduled for orientation", "Participant": "HR_Department"},
            {"E_AttendOrientation": "After attending the orientation", "Participant": "New_Hire"},
            {"A_AssignToDepartment": "The new hire is assigned to their department", "Participant": "HR_Department"}
        ]
    }
]

Output:
[
    {
        "DuplicatedActions": "Yes",
        "ActionsDuplication": [
            {"A_ReviewDocuments": "The HR department reviews the submitted documents", "A_ReturnForCorrection": "If any documents are missing or incorrect, they are returned to the new hire for correction"}
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
    Identifies activities or events in a business process description.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        dict: A dictionary containing identified  activities or events.
    """
    system_message = SYSTEM_MESSAGE_TEMPLATE
    user_message = construct_user_message(text)
    messages = construct_messages(system_message, user_message)

    #response = get_completion(messages, api, model, temperature) #api="ollama", model="llama3.1", max_tokens=1000, temperature=0.0)
    response = get_completion(messages, api, model, temperature)
    return response
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
    result = identify_from_message(text_description, api="openai", model="gpt-4o-mini", temperature=0.0)
    print(result)

# %%
