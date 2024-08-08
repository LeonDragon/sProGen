
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
- Determine Flow: Establish the flow between identified nodes, ensuring each transition is clear and follows the logical sequence of the business process.
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
        ],
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

Output:
[
    {
        "ActionFlows": [
            {"from": "Start_AcceptJobOffer", "to": "A_SendOfferLetterAndWelcomePacket"},
            {"from": "A_SendOfferLetterAndWelcomePacket", "to": "A_FillOutAndSubmitForms"},
            {"from": "A_FillOutAndSubmitForms", "to": "A_ReviewForms"},
            {"from": "A_ReviewForms", "to": "A_SetupWorkstationAndCreateAccounts"},
            {"from": "A_SetupWorkstationAndCreateAccounts", "to": "A_ScheduleOrientation"},
            {"from": "A_ScheduleOrientation", "to": "E_AttendOrientation"},
            {"from": "E_AttendOrientation", "to": "A_MeetWithManager"},
            {"from": "A_MeetWithManager", "to": "End_MeetWithManager"}
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
        ],
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

Output:
[
    {
        "ActionFlows": [
            {"from": "Start_FillOnlineApplication", "to": "A_PerformInitialCheck"},
            {"from": "A_PerformInitialCheck", "to": "A_PromptForMissingInfo"},
            {"from": "A_PromptForMissingInfo", "to": "A_PerformInitialCheck"},
            {"from": "A_PerformInitialCheck", "to": "A_ForwardApplication"},
            {"from": "A_ForwardApplication", "to": "A_ReviewApplication"},
            {"from": "A_ReviewApplication", "to": "A_RejectApplication"},
            {"from": "A_RejectApplication", "to": "End_DisburseLoan"},
            {"from": "A_ReviewApplication", "to": "A_AssessLoanTerms"},
            {"from": "A_AssessLoanTerms", "to": "A_SubmitDocuments"},
            {"from": "A_SubmitDocuments", "to": "A_ReEvaluateApplication"},
            {"from": "A_ReEvaluateApplication", "to": "A_ApproveLoan"},
            {"from": "A_ApproveLoan", "to": "A_GenerateLoanAgreement"},
            {"from": "A_GenerateLoanAgreement", "to": "E_SignLoanAgreement"},
            {"from": "E_SignLoanAgreement", "to": "End_DisburseLoan"}
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
        ],
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

Output:
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
        ],
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
        ],
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

Output:
[
    {
        "ActionFlows": [
            {"from": "Start_ForecastDemand", "to": "A_ForecastDemand"},
            {"from": "A_ForecastDemand", "to": "A_CreatePurchaseOrders"},
            {"from": "A_CreatePurchaseOrders", "to": "A_SelectAlternativeSupplier"},
            {"from": "A_SelectAlternativeSupplier", "to": "A_TrackArrival"},
            {"from": "A_TrackArrival", "to": "A_InspectMaterials"},
            {"from": "A_InspectMaterials", "to": "A_RequestReplacements"},
            {"from": "A_RequestReplacements", "to": "A_SelectAlternativeSupplier"},
            {"from": "A_InspectMaterials", "to": "A_ScheduleManufacturingRuns"},
            {"from": "A_ScheduleManufacturingRuns", "to": "A_ManufactureProducts"},
            {"from": "A_ManufactureProducts", "to": "A_ManageInventory"},
            {"from": "A_ManageInventory", "to": "A_ArrangeTransportation"},
            {"from": "A_ArrangeTransportation", "to": "End_DistributeProducts"}
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
