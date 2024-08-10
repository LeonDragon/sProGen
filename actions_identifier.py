
#%%
# STEP 3 - ACTIONS (EVENTS/ACTIVITIES) IDENTIFICATION
from llm_completion import get_completion

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
        ]
    }
]

Output:
[
    {
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


Example 2:
Input:
The employee onboarding process starts when a new hire accepts a job offer. The HR department sends an offer letter and a welcome packet containing essential forms and information about the company. The new hire fills out the required forms and submits them back to HR. Meanwhile, the IT department sets up the new employee's workstation and creates necessary accounts. The process includes a loop where HR reviews the submitted forms and may request additional information if anything is missing or incorrect. Once all forms are verified, HR schedules an orientation session, and the new employee attends this session. After orientation, the new employee meets with their manager to discuss job responsibilities and expectations, concluding the onboarding process.

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

Output:
[
    {
        "StartEvent": "Start_AcceptJobOffer",
        "EndEvent": "End_MeetWithManager",
        "ActivitiesEvents": [
            {
                "A_SendOfferLetterAndWelcomePacket": "The HR department sends an offer letter and a welcome packet containing essential forms and information about the company",
                "Participant": "HR_Department"
            },
            {
                "A_FillOutAndSubmitForms": "The new hire fills out the required forms and submits them back to HR",
                "Participant": "New_Hire"
            },
            {
                "A_SetupWorkstationAndCreateAccounts": "The IT department sets up the new employee's workstation and creates necessary accounts",
                "Participant": "IT_Department"
            },
            {
                "A_ReviewForms": "HR reviews the submitted forms and may request additional information if anything is missing or incorrect",
                "Participant": "HR_Department"
            },
            {
                "A_ScheduleOrientation": "Once all forms are verified, HR schedules an orientation session",
                "Participant": "HR_Department"
            },
            {
                "E_AttendOrientation": "The new employee attends the orientation session",
                "Participant": "New_Hire"
            },
            {
                "A_MeetWithManager": "The new employee meets with their manager to discuss job responsibilities and expectations",
                "Participant": "Manager"
            }
        ]
    }
]


Example 3:
Input:
A customer initiates the loan application process by filling out an online application form. The system performs an initial check to ensure all required fields are completed. If any fields are missing, the system loops back, prompting the customer to provide the missing information. Once the application is complete, it is forwarded to a loan officer for review. The loan officer evaluates the application and checks the applicant's credit history. If the credit check fails, the application is rejected, and the process ends. If the credit check passes, the loan officer assesses the loan terms and may request additional documentation from the applicant. The applicant submits the required documents, and the loan officer re-evaluates the application. Once all criteria are met, the loan officer approves the loan, and the system generates a loan agreement for the customer to sign. After signing, the loan amount is disbursed to the customer, completing the process.

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

Output:
[
    {
        "StartEvent": "Start_FillOnlineApplication",
        "EndEvent": "End_DisburseLoan",
        "ActivitiesEvents": [
            {
                "A_PerformInitialCheck": "The system performs an initial check to ensure all required fields are completed",
                "Participant": "System"
            },
            {
                "A_PromptForMissingInfo": "If any fields are missing, the system loops back, prompting the customer to provide the missing information",
                "Participant": "System"
            },
            {
                "A_ForwardApplication": "Once the application is complete, it is forwarded to a loan officer for review",
                "Participant": "System"
            },
            {
                "A_ReviewApplication": "The loan officer evaluates the application and checks the applicant's credit history",
                "Participant": "Loan_Officer"
            },
            {
                "A_RejectApplication": "If the credit check fails, the application is rejected, and the process ends",
                "Participant": "Loan_Officer"
            },
            {
                "A_AssessLoanTerms": "If the credit check passes, the loan officer assesses the loan terms and may request additional documentation from the applicant",
                "Participant": "Loan_Officer"
            },
            {
                "A_SubmitDocuments": "The applicant submits the required documents",
                "Participant": "Customer"
            },
            {
                "A_ReEvaluateApplication": "The loan officer re-evaluates the application",
                "Participant": "Loan_Officer"
            },
            {
                "A_ApproveLoan": "Once all criteria are met, the loan officer approves the loan",
                "Participant": "Loan_Officer"
            },
            {
                "A_GenerateLoanAgreement": "The system generates a loan agreement for the customer to sign",
                "Participant": "System"
            },
            {
                "E_SignLoanAgreement": "After signing, the loan amount is disbursed to the customer",
                "Participant": "Customer"
            }
        ]
    }
]


Example 4:
Input:
The course enrollment process begins when students log into the university's enrollment system at the start of the semester. Students select courses they wish to enroll in. If a selected course has prerequisites, the system checks if the student meets these requirements. If prerequisites are not met, the system provides alternatives or suggestions for courses that can be taken instead. Students may choose to enroll in multiple courses, making this an inclusive process. The system checks for schedule conflicts, and if any are found, it prompts the student to adjust their course selections. Once the schedule is confirmed, the system calculates tuition fees based on the selected courses. Students are then directed to the payment gateway to pay their tuition fees. After payment confirmation, the enrollment is finalized, and students receive their class schedules.

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

Output:
[
    {
        "StartEvent": "Start_LogIntoEnrollmentSystem",
        "EndEvent": "End_ReceiveClassSchedules",
        "ActivitiesEvents": [
            {"A_SelectCourses": "Students select courses they wish to enroll in", "Participant": "Students"},
            {"A_CheckPrerequisites": "The system checks if the student meets course prerequisites", "Participant": "Enrollment_System"},
            {"A_ProvideAlternatives": "If prerequisites are not met, the system provides alternatives or suggestions for courses", "Participant": "Enrollment_System"},
            {"A_CheckScheduleConflicts": "The system checks for schedule conflicts", "Participant": "Enrollment_System"},
            {"A_AdjustCourseSelections": "If any schedule conflicts are found, the system prompts the student to adjust their course selections", "Participant": "Students"},
            {"A_CalculateTuitionFees": "The system calculates tuition fees based on the selected courses", "Participant": "Enrollment_System"},
            {"A_DirectToPaymentGateway": "Students are directed to the payment gateway to pay their tuition fees", "Participant": "Enrollment_System"},
            {"A_ConfirmPayment": "After payment confirmation", "Participant": "Enrollment_System"},
            {"A_FinalizeEnrollment": "the enrollment is finalized", "Participant": "Enrollment_System"}
        ]
    }
]


Example 5:
Input:
The supply chain management process starts with forecasting demand based on historical sales data and market analysis. The procurement team then creates purchase orders for raw materials from suppliers. If a supplier cannot fulfill the order, the system loops back to select an alternative supplier. Once the materials are ordered, the inventory management system tracks their arrival. Upon arrival, materials are inspected for quality. If materials fail the inspection, the process loops back to request replacements from the supplier. Concurrently, the production planning team schedules manufacturing runs, considering the availability of materials and production capacity. During production, there is an inclusive behavior where different production lines can operate simultaneously to manufacture various products. Finished products are sent to the warehouse, where the system manages inventory levels and prepares shipments. The logistics team arranges transportation to distribute products to retail outlets or customers. Throughout the process, data is continuously monitored and analyzed to optimize efficiency and address any issues promptly, concluding the supply chain management process.

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

Output:
[
    {
        "StartEvent": "Start_ForecastDemand",
        "EndEvent": "End_DistributeProducts",
        "ActivitiesEvents": [
            {"A_ForecastDemand": "Forecasting demand based on historical sales data and market analysis", "Participant": "Forecasting_Team"},
            {"A_CreatePurchaseOrders": "The procurement team creates purchase orders for raw materials from suppliers", "Participant": "Procurement_Team"},
            {"A_SelectAlternativeSupplier": "If a supplier cannot fulfill the order, the system loops back to select an alternative supplier", "Participant": "Procurement_Team"},
            {"A_TrackArrival": "The inventory management system tracks the arrival of materials", "Participant": "Inventory_Management_System"},
            {"A_InspectMaterials": "Upon arrival, materials are inspected for quality", "Participant": "Quality_Inspectors"},
            {"A_RequestReplacements": "If materials fail the inspection, the process loops back to request replacements from the supplier", "Participant": "Procurement_Team"},
            {"A_ScheduleManufacturingRuns": "The production planning team schedules manufacturing runs", "Participant": "Production_Planning_Team"},
            {"A_ManufactureProducts": "Different production lines operate simultaneously to manufacture various products", "Participant": "Production_Lines"},
            {"A_ManageInventory": "Finished products are sent to the warehouse, where the system manages inventory levels and prepares shipments", "Participant": "Warehouse_Management_System"},
            {"A_ArrangeTransportation": "The logistics team arranges transportation to distribute products to retail outlets or customers", "Participant": "Logistics_Team"},
            {"A_MonitorAndAnalyzeData": "Throughout the process, data is continuously monitored and analyzed to optimize efficiency and address any issues promptly", "Participant": "Forecasting_Team"}
        ]
    }
]

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
            ]
        }
    ]
    """
    result, prompt_tokens, completion_tokens = identify_from_message(text_description, api="openai", model="gpt-4o-mini", temperature=0.0)
    print(result)

# %%
