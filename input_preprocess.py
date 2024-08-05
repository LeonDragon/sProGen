
#%%
# STEP 1 - INPUT AUGMENTATION
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Improve the provided textual descriptions of BPMN process models within the delimiters {delimiter}, make them easier to understand and identify BPMN elements. Output a Python list of JSON objects with keys: Original and Augmentation. Ensure the output is strictly in JSON format without any additional text.


Instructions:
1. Specify the domain or industry related to the process (e.g., logistics, manufacturing, service, finance, government services).
2. Clearly state the main goal of the process.
3. Describe the sequence of main activities or events involved in the process.
4. Identify any loops or cycles within the process and how they operate.
5. Highlight the decision points (gateways) and the conditions that lead to different paths in the process.
6. Clearly mention the participants and their roles involved in the process.
7. Ensure the flow of activities, events, and gateways is clear and logical.
8. Strictly adhere to the original content and main ideas of the input textual description. Inference based on the original content are allowed.
8. Output the improved textual description with similar format of the input textual description.

Examples:

Input:
The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.

Output:
[
    {
        "Original": "The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.",
        "Augmentation": "In the HR context, the employee onboarding process starts when a new hire submits their completed paperwork. Initially, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction, creating a loop that repeats until all documents are complete and correct. Once the documentation is in order, the new hire is scheduled for an orientation session. After attending the orientation, the new hire is assigned to their respective department, marking the completion of the onboarding process. The sequence flows include loops for document correction and gateways for document verification and scheduling orientation, with roles such as HR personnel and new hire."
    }
]

Input:
The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.

Output:
[
    {
        "Original": "The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.",
        "Augmentation": "In the manufacturing context, the product development process begins with identifying market needs. Once the needs are identified, a product concept is created. Following this, the product design phase is initiated. After designing the product, a prototype is developed. The prototype undergoes testing, and if it meets the required standards, the product is finalized and launched into the market, completing the development process. The sequence flows are linear, progressing from market need identification to concept creation, design, prototype development, testing, and final product launch, involving roles such as market analysts, designers, developers, and testers."
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

def identify_from_message(text):
    """
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
    result = identify_from_message(text_description)
    print(result)

# %%
