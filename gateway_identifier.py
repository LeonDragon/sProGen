
#%%
# Gateways Identification
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
Task: You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

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

Instruction: Given the process description and the list of Activities/Events (also called "Nodes") identified from this description within the delimiters {delimiter}, please Identify as many gateways as you can by performing the following steps:

Steps to Perform
    - Step 1: List all identified gateways along with textual clues that led to the decision. Identify as many gateways as you can, whether they are for divergence (such as XOR-split, OR-split, or AND-split) or convergence (such as XOR-join, OR-join, or AND-join). Generally, if a process has a split gateway (e.g., XOR-split, OR-split, or AND-split), it will be followed by a corresponding join gateway (e.g., XOR-join, OR-join, or AND-join) to converge the paths. However, this is not always the case; several split gateways could converge into a single join gateway. Do not print out this step.
    - Step 2: Output a Python list of JSON objects, detailing the gateways identified in Step 1. Ensure the output is strictly in JSON format without any additional text. Do not print out Step 1.

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
    -- from_node: Node(s) preceding the gateway.
    -- to_nodes: Node(s) following the gateway.
    -- reason: This is a description explaining (clues) why you can make that inference.
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
    Order-to-cash process starts whenever a purchase order has been received from a customer. The first activity that is carried out is confirming the order. Next, the shipment address is received so that the product can be shipped to the customer. Afterwards, the invoice is emitted and once the payment is received the order is archived, thus completing the process. Please note that a purchase order is only confirmed if the product is in stock, otherwise the process completes by rejecting the order. If the order is confirmed, the shipment address is received and the requested product is shipped while the invoice is emitted and the payment is received. Afterwards, the order is archived and the process completes.

    Relevant activities/event information:
    {
    "StartEvent": {
        "Label": "Start_ReceiveOrder",
        "Description": "The process begins when a purchase order is received from a customer."
    },
    "EndEvents": [
        {
        "Label": "End_OrderArchived",
        "Description": "The process completes with the order archived after payment is received."
        },
        {
        "Label": "End_OrderRejected",
        "Description": "The process completes with the order rejected if the product is not in stock."
        }
    ],
    "MainActivitiesOrIntermediateEvents": [
        {
        "Label": "A_ConfirmOrder",
        "Description": "Confirm the order."
        },
        {
        "Label": "A_ReceiveShipmentAddress",
        "Description": "Receive the shipment address."
        },
        {
        "Label": "A_ShipProduct",
        "Description": "Ship the product to the customer."
        },
        {
        "Label": "A_EmitInvoice",
        "Description": "Emit the invoice."
        },
        {
        "Label": "A_ReceivePayment",
        "Description": "Receive the payment."
        },
        {
        "Label": "A_ArchiveOrder",
        "Description": "Archive the order."
        },
        {
        "Label": "A_RejectOrder",
        "Description": "Reject the order if the product is not in stock."
        }
    ]
    }

    """
    result = identify_gateways(text_description)
    print(result)

# %%
