
#%%
# STEP 1 - INPUT AUGMENTATION
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Improve the provided textual descriptions of BPMN process models within the delimiters {delimiter}, making them easier to understand and identify BPMN elements. Output a Python list of JSON objects with keys: Original and Augmented. Ensure the output is strictly in JSON format without any additional text.

Instructions:
1. Specify the domain or industry related to the process (e.g., logistics, manufacturing, service, finance, government services).
2. Clearly state the main goal of the process.
3. Identify the main activities or events involved in the "Original" process description. Identify the main activities or events involved in the "Augmented" process description. Ensure that the keywords or important related terms are used exactly as provided (Original and Augmented), without rephrasing or rewriting them.
4. Identify any loops or cycles within the process, explaining how they operate. For similar tasks with similar meanings (e.g., re-work, re-check, check again), do not mention them separately; instead, use loop structure sentences to indicate these repeated actions. Here are some sample sentence structure:
        - Documents can enter the review loop from various departments (HR, Finance, Operations). Regardless of the entry point, the loop continues with document revisions until final approval is granted.
        - Submissions can enter the review loop from different sources (students, faculty, external researchers). After reviews, papers can exit the loop as accepted, needing minor revisions, or rejected.
        - Tasks can enter the loop from different team members. After processing, tasks can be marked as completed, delegated to another member, or flagged for further review.
        -  New hires enter the training loop. They undergo training sessions and assessments, repeating as necessary, until they pass all required evaluations and exit the loop.
        - Software builds enter the testing loop. Each build is tested, debugged, and retested until it is bug-free, then exits as ready for deployment.
        - Customer complaints enter the handling loop. Each complaint is processed, with exits for resolution, escalation, or requiring more details from the customer.
5. Highlight the decision points (gateways) and the conditions that lead to different paths in the process.
6. Clearly mention the participants and their roles involved in the process.
7. Ensure the flow of activities, events, and gateways is clear and logical.
8. Strictly adhere to the original content and main ideas of the input textual description. Inferences based on the original content are allowed.
9. Output the improved textual description in a similar format to the input textual description.

Examples:

Input:
The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.

Output:
[
    {
        "Original": "The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.",
        "Augmented": "In the HR context, the employee onboarding process starts when a new hire submits their completed paperwork. Initially, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction, creating a loop that repeats until all documents are complete and correct. Once the documentation is in order, the new hire is scheduled for an orientation session. After attending the orientation, the new hire is assigned to their respective department, marking the completion of the onboarding process. The sequence flows include loops for document correction without duplicating tasks and gateways for document verification and scheduling orientation, with roles such as HR personnel and new hire."
    }
]

Input:
The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.

Output:
[
    {
        "Original": "The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.",
        "Augmented": "In the manufacturing context, the product development process begins with identifying market needs. Once the needs are identified, a product concept is created. Following this, the product design phase is initiated. After designing the product, a prototype is developed. The prototype undergoes testing, and if it meets the required standards, the product is finalized and launched into the market, completing the development process. The sequence flows are linear, progressing from market need identification to concept creation, design, prototype development, testing, and final product launch, involving roles such as market analysts, designers, developers, and testers."
    }
]

"""

text_description_1st = """
    A company has two warehouses that store different products: Amsterdam and Hamburg. When an order is received, it is distributed across these warehouses: if some of the relevant products are maintained in Amsterdam, a sub-order is sent there; likewise, if some relevant products are maintained in Hamburg, a sub-order is sent there. Afterwards, the order is registered and the process completes. 
    """

text_description_2nd = """
    Relevant Process Description information:
    In the treasury minister’s office, once a ministerial inquiry has been received, it is first registered into the system. Then the inquiry is investigated so that a ministerial response can be prepared. The finalization of a response includes the preparation of the response itself by the cabinet officer and the review of the response by the principal registrar. If the registrar does not approve the response, the latter needs to be prepared again by the cabinet officer for review. The process finishes only once the response has been approved. 
    """

SYSTEM_MESSAGE_TEMPLATE_NEW_8_12_2024 = """"
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2). 

Task:
Please create a process description based on the guidelines provided below. Use the template format as a reference, and develop the process description using the input text enclosed within the delimiters ####. Ensure the output is strictly in the string format (plaintext) without any additional text.

Process Name: {{process_name}}
Process Owner: {{process_owner}}
Objective: {{objective}}
Scope: {{scope}}
Inputs: {{inputs}}
Outputs: {{outputs}}
Steps: #  Each step resembles an action, typically beginning with a verb. Avoid creating sub-steps; if they exist, break them down and place them at the same level as other main steps.
  1.0 {{step1_name}} - {{step1_description}}
    Responsible: {{step1_responsible}}
    Tools/System: {{step1_tools}}
  2.0 {{step2_name}} - {step2_description}}
    Responsible: {{step2_responsible}}
    Tools/System: {{step2_tools}}
  ...
Decisions Points:
  4.0 {{X_decision1}}  # X_decision can be inclusive, exclusive, or parallel.
    From Step: … # Step number
    4.1 {{optionA}}: # Outcome_of_Option_A
    4.2 {{optionB}}  # Outcome_of_Option_B
    To Steps: … # Steps numbers
    Reason for X_decision1: ..
Merge Points:
  5.0 {{merge_description_1}} # This step consolidates multiple process flows, whether from one or many decision points, ensuring synchronization before continuing.
Exceptions: {exceptions}}  # Optional: Specific exceptions and how they're handled.
KPIs: {{kpis}}  # Optional: Metrics for evaluating process performance.
Roles: {{roles}}  # Optional: Roles and their responsibilities in the process.
Version: {{version}}  # Optional: Document version for change tracking.
References: {{references}}  # Optional: Relevant documents or resources.
Approval: {{approval}  # Optional: Approval details.

"""

# GIVE SOME FEW SHOT EXAMPLE COULD BE NICE

OUTPUT_TEMPLATE_NEW_8_12_2024_1st = """
Process Name: Order Distribution and Fulfillment
Process Owner: Warehouse Manager
Objective: To efficiently distribute and fulfill orders across multiple warehouses.
Scope: This process covers the distribution of incoming orders to the appropriate warehouses and the registration of the order in the system.
Inputs: Customer order details
Outputs: Registered order and distributed sub-orders to respective warehouses
Steps:
  1.0 Receive Order - Capture customer order details.
    Responsible: Sales Department
    Tools/System: Order Management System (OMS)
  2.0 Distribute Order to Amsterdam Warehouse - Send a sub-order to the Amsterdam warehouse if it contains relevant products.
    Responsible: Order Processing Team
    Tools/System: OMS, Warehouse Management System (WMS)
  3.0 Distribute Order to Hamburg Warehouse - Send a sub-order to the Hamburg warehouse if it contains relevant products.
    Responsible: Order Processing Team
    Tools/System: OMS, WMS
  4.0 Register Order - Record the completed order in the system.
    Responsible: Order Processing Team
    Tools/System: OMS
Decisions Points:
  4.0 Inclusive Decision - Determine which warehouses the order should be distributed to.
    From Step: 1.0
    4.1 Amsterdam: If the order contains products stored in the Amsterdam warehouse.
    4.2 Hamburg: If the order contains products stored in the Hamburg warehouse.
    To Steps: 2.0, 3.0
    Reason for X_decision1: Efficiently manage inventory and reduce delivery times by utilizing multiple warehouses.
Merge Points:
  5.0 Consolidate Order Distribution - Ensure all sub-orders have been sent to the relevant warehouses before registering the order.
Exceptions: None
KPIs: Order fulfillment time, accuracy of order distribution
Roles: Sales Department, Order Processing Team, Warehouse Manager
Version: 1.0
References: Warehouse Management Guidelines, Order Processing Manual
Approval: Warehouse Manager
"""

OUTPUT_TEMPLATE_NEW_8_12_2024_2nd = """
Process Name: Ministerial Inquiry Response
Process Owner: Treasury Minister’s Office
Objective: To effectively process and respond to ministerial inquiries with an approved response.
Scope: This process encompasses the receipt, investigation, preparation, review, and finalization of responses to ministerial inquiries.
Inputs: Ministerial inquiry details
Outputs: Approved ministerial response
Steps:
  1.0 Register Inquiry - Record the received ministerial inquiry in the system.
    Responsible: Administrative Staff
    Tools/System: Inquiry Management System (IMS)
  2.0 Investigate Inquiry - Conduct an investigation to gather necessary information for the response.
    Responsible: Cabinet Officer
    Tools/System: IMS, Internal Databases
  3.0 Prepare Response - Draft the ministerial response based on the investigation.
    Responsible: Cabinet Officer
    Tools/System: IMS, Document Editing Software
  4.0 Review Response - Evaluate the prepared response for accuracy and completeness.
    Responsible: Principal Registrar
    Tools/System: IMS, Document Editing Software
Decisions Points:
  4.0 Exclusive Decision - Determine whether the prepared response meets approval standards.
    From Step: 4.0
    4.1 Approve Response: If the response meets the required standards.
    4.2 Reject Response: If the response does not meet the required standards and needs revision.
    To Steps: 5.0 (for approval), 3.0 (for rejection and re-preparation)
    Reason for X_decision1: Ensure the response is accurate and complies with ministerial standards.
Merge Points:
  5.0 Finalize and Approve Response - Once the response is approved, finalize it for official release.
Exceptions: None
KPIs: Response turnaround time, approval rate of initial drafts
Roles: Administrative Staff, Cabinet Officer, Principal Registrar
Version: 1.0
References: Ministerial Inquiry Response Guidelines, Treasury Office Manual
Approval: Treasury Minister

"""

SYSTEM_MESSAGE_TEMPLATE_OLD = """
You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

Task:
Improve the provided textual descriptions of BPMN process models within the delimiters {delimiter}, make them easier to understand and identify BPMN elements. Output a Python list of JSON objects with keys: Original and Augmented. Ensure the output is strictly in JSON format without any additional text.


Instructions:
1. Specify the domain or industry related to the process (e.g., logistics, manufacturing, service, finance, government services).
2. Clearly state the main goal of the process.
3. Describe the sequence of main activities or events involved in the process.
4. Identify any loops or cycles within the process and how they operate.
5. Highlight the decision points (gateways) and the conditions that lead to different paths in the process.
6. Clearly mention the participants and their roles involved in the process.
7. Ensure the flow of activities, events, and gateways is clear and logical.
8. Strictly adhere to the original content and main ideas of the input textual description. Inference based on the original content are allowed.
9. Output the improved textual description with similar format of the input textual description.

Examples:

Input:
The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.

Output:
[
    {
        "Original": "The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.",
        "Augmented": "In the HR context, the employee onboarding process starts when a new hire submits their completed paperwork. Initially, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction, creating a loop that repeats until all documents are complete and correct. Once the documentation is in order, the new hire is scheduled for an orientation session. After attending the orientation, the new hire is assigned to their respective department, marking the completion of the onboarding process. The sequence flows include loops for document correction and gateways for document verification and scheduling orientation, with roles such as HR personnel and new hire."
    }
]

Output:
[
    {
        "Original": "The employee onboarding process begins when a new hire submits their completed paperwork. First, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction. This process repeats until all documents are complete and correct. Once the documents are in order, the new hire is scheduled for orientation. After attending the orientation, the new hire is assigned to their department, completing the onboarding process.",
        "Augmented": "In the HR context, the employee onboarding process starts when a new hire submits their completed paperwork. Initially, the HR department reviews the submitted documents. If any documents are missing or incorrect, they are returned to the new hire for correction, creating a loop that repeats until all documents are complete and correct. Once the documentation is in order, the new hire is scheduled for an orientation session. After attending the orientation, the new hire is assigned to their respective department, marking the completion of the onboarding process. The sequence flows include loops for document correction without duplicating tasks and gateways for document verification and scheduling orientation, with roles such as HR personnel and new hire."
    }
]

Input:
The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.

Output:
[
    {
        "Original": "The product development process begins with the identification of market needs. Once the needs are identified, a product concept is created. The next step is to design the product, followed by developing a prototype. The prototype is then tested, and if it meets the requirements, the product is finalized and launched into the market, completing the process.",
        "Augmented": "In the manufacturing context, the product development process begins with identifying market needs. Once the needs are identified, a product concept is created. Following this, the product design phase is initiated. After designing the product, a prototype is developed. The prototype undergoes testing, and if it meets the required standards, the product is finalized and launched into the market, completing the development process. The sequence flows are linear, progressing from market need identification to concept creation, design, prototype development, testing, and final product launch, involving roles such as market analysts, designers, developers, and testers."
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
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        dict: A dictionary containing identified gateways and related metadata.
    """
    system_message = SYSTEM_MESSAGE_TEMPLATE_NEW_8_12_2024
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
