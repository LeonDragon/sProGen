
#%%
# Gateways Identification
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Understand the textual description, identify context, and overall process goal of textual descriptions of BPMN process models within the delimiters {delimiter}. Output a Python list of JSON objects with keys: Context, Scope, Objectives. Ensure the output is strictly in JSON format without any additional text.

Instructions:
- Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details.
- Context: Describe the context of the process model in the given textual description, e.g., logistics, manufacturing, service, finance, etc.
- Clarify Scope: Determine the boundaries of the process (start and end points).
- Set Objectives: Understand the purpose of the process and its desired outcomes.

Examples:

Input:
The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.

Output:
[
    {
        "Context": "Human Resources",
        "Scope": "Starts with the submission of completed paperwork by the new hire and ends with the assignment of the new hire to their department.",
        "Objectives": "To ensure new hires complete all necessary paperwork, attend orientation, and are successfully integrated into their departments."
    }
]

Input:
The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.

Output:
[
    {
        "Context": "Manufacturing",
        "Scope": "Starts with the identification of market needs and ends with the launch of the product into the market.",
        "Objectives": "To develop a new product that meets market needs, from concept to market launch."
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

def identify_gateways(text):
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
    response = get_completion(messages, api="openai", model="gpt-4o", temperature=0.0)
    return response
    # try:
    #     return json.loads(response)
    # except json.JSONDecodeError:
    #     return {"error": "Failed to decode JSON response"}

# Example usage
if __name__ == "__main__":
    text_description = """
    Relevant Process Description information:
    Once a loan application is received by the loan provider, and before proceeding with its assessment, the application itself needs to be checked for completeness. If the application is incomplete, it is returned to the applicant, so that they can fill out the missing information and send it back to the loan provider. This process is repeated until the application is found complete.
    """
    result = identify_gateways(text_description)
    print(result)

# %%
