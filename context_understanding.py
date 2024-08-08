
#%%
# STEP 2 - CONTEXT UNDERSTANDING
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Understand the textual description, identify the context, and overall process goal of textual descriptions of BPMN process models within the delimiters {delimiter}. Output a Python list of JSON objects with keys: ModelName, Context, Scope, Objectives, Participants. Ensure the output is strictly in JSON format without any additional text.

Instructions:
- Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details.
- Context: Describe the context of the process model in the given textual description, e.g., logistics, manufacturing, service, finance, etc.
- Clarify Scope: Determine the boundaries of the process (start and end points).
- Set Objectives: Understand the purpose of the process and its desired outcomes.
- Identify Participants and Roles: Identify different Participants and Roles involved in the process. These are typically represented as pools or lanes in BPMN. Textual Clues: Look for specific roles or departments mentioned, such as "cabinet officer", "principal registrar", "customer service", or "logistics team".
- DO NOT output additional text except the JSON format. Do not output ```json or ``` or \n

Examples:

Example 1: Simple Business Process: Ordering a Book Online
Input:
The process begins with a customer browsing an online bookstore and selecting a book to purchase. After adding the book to the cart, the customer proceeds to checkout. The system then prompts the customer to enter shipping and payment details. Once the payment is successfully processed, the system generates an order confirmation. The warehouse receives the order and prepares the book for shipment. The final step is shipping the book to the customer's address. The process concludes when the customer receives the book.

Output:
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
        ]
    }
]


Example 2: Moderate Business Process: Employee Onboarding
Input:
The employee onboarding process starts when a new hire accepts a job offer. The HR department sends an offer letter and a welcome packet containing essential forms and information about the company. The new hire fills out the required forms and submits them back to HR. Meanwhile, the IT department sets up the new employee's workstation and creates necessary accounts. The process includes a loop where HR reviews the submitted forms and may request additional information if anything is missing or incorrect. Once all forms are verified, HR schedules an orientation session, and the new employee attends this session. After orientation, the new employee meets with their manager to discuss job responsibilities and expectations, concluding the onboarding process.

Output:
[
    {
        "ModelName": "Employee Onboarding Process",
        "Context": "Human Resources",
        "Scope": "Starts with a new hire accepting a job offer and ends with the new employee meeting with their manager to discuss job responsibilities and expectations.",
        "Objectives": "To ensure a smooth transition for new hires by completing necessary paperwork, setting up workstations, providing orientation, and meeting with managers.",
        "Participants": [
            {
                "HR_Department": "Responsible for sending offer letters, reviewing submitted forms, requesting additional information if needed, and scheduling orientation sessions."
            },
            {
                "New_Hire": "Responsible for filling out and submitting required forms, attending orientation, and meeting with their manager."
            },
            {
                "IT_Department": "Responsible for setting up the new employee's workstation and creating necessary accounts."
            },
            {
                "Manager": "Responsible for discussing job responsibilities and expectations with the new employee."
            }
        ]
    }
]


Example 3: Complex Business Process: Loan Application Processing
Input:
A customer initiates the loan application process by filling out an online application form. The system performs an initial check to ensure all required fields are completed. If any fields are missing, the system loops back, prompting the customer to provide the missing information. Once the application is complete, it is forwarded to a loan officer for review. The loan officer evaluates the application and checks the applicant's credit history. If the credit check fails, the application is rejected, and the process ends. If the credit check passes, the loan officer assesses the loan terms and may request additional documentation from the applicant. The applicant submits the required documents, and the loan officer re-evaluates the application. Once all criteria are met, the loan officer approves the loan, and the system generates a loan agreement for the customer to sign. After signing, the loan amount is disbursed to the customer, completing the process.

Output:
[
    {
        "ModelName": "Loan Application Process",
        "Context": "Finance",
        "Scope": "Starts with the customer filling out an online application form and ends with the disbursement of the loan amount to the customer.",
        "Objectives": "To process loan applications from initial submission to final disbursement, ensuring all criteria are met and required documentation is provided.",
        "Participants": [
            {
                "Customer": "Responsible for filling out the application form and submitting additional documentation if requested"
            },
            {
                "System": "Performs initial checks on the application form for completeness"
            },
            {
                "Loan_Officer": "Responsible for reviewing the application, performing credit checks, evaluating loan terms, requesting additional documentation, and approving the loan"
            }
        ]
    }
]


Example 4: Complex Business Process with Inclusive Behavior: University Course Enrollment
Input:
The course enrollment process begins when students log into the university's enrollment system at the start of the semester. Students select courses they wish to enroll in. If a selected course has prerequisites, the system checks if the student meets these requirements. If prerequisites are not met, the system provides alternatives or suggestions for courses that can be taken instead. Students may choose to enroll in multiple courses, making this an inclusive process. The system checks for schedule conflicts, and if any are found, it prompts the student to adjust their course selections. Once the schedule is confirmed, the system calculates tuition fees based on the selected courses. Students are then directed to the payment gateway to pay their tuition fees. After payment confirmation, the enrollment is finalized, and students receive their class schedules.

Output:
[
    {
        "ModelName": "Course Enrollment Process",
        "Context": "Education",
        "Scope": "Starts with students logging into the university's enrollment system and ends with students receiving their class schedules after payment confirmation.",
        "Objectives": "To facilitate student enrollment in courses, ensure prerequisites and schedule conflicts are addressed, and finalize enrollment upon payment.",
        "Participants": [
            {
                "Students": "Responsible for selecting courses, adjusting selections based on prerequisites and schedule conflicts, and completing tuition payment."
            },
            {
                "Enrollment_System": "Responsible for checking prerequisites, providing course alternatives, detecting schedule conflicts, calculating tuition fees, and confirming payment."
            }
        ]
    }
]


Example 5: Advanced Business Process with Loops and Inclusive Behavior: Supply Chain Management
Input:
The supply chain management process starts with forecasting demand based on historical sales data and market analysis. The procurement team then creates purchase orders for raw materials from suppliers. If a supplier cannot fulfill the order, the system loops back to select an alternative supplier. Once the materials are ordered, the inventory management system tracks their arrival. Upon arrival, materials are inspected for quality. If materials fail the inspection, the process loops back to request replacements from the supplier. Concurrently, the production planning team schedules manufacturing runs, considering the availability of materials and production capacity. During production, there is an inclusive behavior where different production lines can operate simultaneously to manufacture various products. Finished products are sent to the warehouse, where the system manages inventory levels and prepares shipments. The logistics team arranges transportation to distribute products to retail outlets or customers. Throughout the process, data is continuously monitored and analyzed to optimize efficiency and address any issues promptly, concluding the supply chain management process.

Output:
[
    {
        "ModelName": "Supply Chain Management Process",
        "Context": "Logistics",
        "Scope": "Starts with forecasting demand and ends with distributing products to retail outlets or customers.",
        "Objectives": "To manage the end-to-end supply chain process efficiently, ensuring timely procurement, quality inspection, production, inventory management, and distribution of products.",
        "Participants": [
            {"Forecasting_Team": "Responsible for forecasting demand based on historical sales data and market analysis"},
            {"Procurement_Team": "Responsible for creating purchase orders and managing supplier relationships"},
            {"Suppliers": "Responsible for fulfilling orders for raw materials"},
            {"Inventory_Management_System": "Tracks the arrival and inspection of materials"},
            {"Quality_Inspectors": "Inspect the quality of received materials"},
            {"Production_Planning_Team": "Schedules manufacturing runs"},
            {"Production_Lines": "Operate simultaneously to manufacture various products"},
            {"Warehouse_Management_System": "Manages inventory levels and prepares shipments"},
            {"Logistics_Team": "Arranges transportation for distribution"}
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
    Identifies context in a business process description.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        dict: A dictionary containing identified context and related metadata.
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
    Relevant Process Description information:
    Once a loan application is received by the loan provider, and before proceeding with its assessment, the application itself needs to be checked for completeness. If the application is incomplete, it is returned to the applicant, so that they can fill out the missing information and send it back to the loan provider. This process is repeated until the application is found complete.
    """
    result, prompt_tokens, completion_tokens = identify_from_message(text_description, api="openai", model="gpt-4o-mini", temperature=0.0)
    print(result)

# %%
