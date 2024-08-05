
#%%
import json
from llm_completion import get_completion

# Constants for system and user messages
delimiter = "####"
SYSTEM_MESSAGE_TEMPLATE = """
Task: You are an expert in business process modeling, specializing in Business Process Management (BPM) and Business Process Model and Notation (BPMN 2.0.2).

To accurately identify gateways for decision points and parallelism in BPMN, you need to understand the following concepts:
- There are three types of gateways: Exclusive (XOR), Inclusive (OR), and Parallel (AND). Each gateway type can function as either a split or a join.
- Exclusive Gateways (XOR):
    - Definition: Exclusive Gateways are used to model decision points where only one of the available paths can be taken. This is akin to a simple "either/or" decision.
    - Textual Clues: Look for words and phrases like "if", "only if", "either", "exclusive", "else", "depending on", "in case of", "should", "must", "when", etc.
    - XOR can be split (divergence) or join (convergence):
        - Split Behavior (Choosing Multiple Paths): When you reach this gateway, it checks all the conditions for each path. All paths with true conditions are taken simultaneously. Example: Imagine you are ordering food, and you can choose to get a drink, a side dish, or both. Depending on what you choose, you might get one, both, or none.
        - Join Behavior (Synchronizing Paths): When paths come together at this gateway, it waits for all active paths to arrive before moving forward. It ensures all conditions are met before proceeding. Example: In the process where a customer places an order that can either be approved or rejected, the process proceeds to notify the customer after either outcome, making it an XOR join as it does not require synchronization.
    - Modeling Instructions: Provide a question that describes the decision point. Example: XOR_CreditOK? If the condition is met, the flow follows one path; otherwise, it follows a different path.
    - Example:
        - Text: "If the credit is approved, process the payment. Else, send a rejection notice."
        - Model: 
            - Gateway: XOR_CreditApproved?
            - Path 1: Yes → Task: Process payment
            - Path 2: No → Task: Send rejection notice

- Inclusive Gateways (OR):
    - Definition: Inclusive Gateways allow for multiple paths to be taken simultaneously. This means that one or more of the available paths can be chosen based on the conditions.
    - Textual Clues: Look for words and phrases like "optionally", "can", "might", "inclusive", "and/or", "one or more", "any of", "possibly", "choose", "elect", etc.
    - OR can be split (divergence) or join (convergence)::
        - Split Behavior (Choosing Multiple Paths): When you reach this gateway, it checks all the conditions for each path. All paths with true conditions are taken simultaneously. Example: Imagine you are ordering food, and you can choose to get a drink, a side dish, or both. Depending on what you choose, you might get one, both, or none.
        - Join Behavior (Synchronizing Paths):When paths come together at this gateway, it waits for all active paths to arrive before moving forward. It ensures all conditions are met before proceeding. Example: In a marketing campaign running through email, social media, and direct mail, the process moves to analyze results once any of these channels complete, requiring synchronization of all active channels, thus making it an OR join.
    - Modeling Instructions: Provide a question that describes the decision point and clearly describe the conditions for each path. All applicable paths can be activated simultaneously.
    - Example:
        - Text: "A customer can choose to receive email notifications, SMS notifications, or both."
        - Model: 
            - Gateway: OR_NotificationPreferences?
            - Path 1: Email → Task: Send email notification
            - Path 2: SMS → Task: Send SMS notification

- Parallel Gateways (AND):
    - Definition: Parallel Gateways are used to model situations where multiple tasks occur concurrently. This means that all paths are taken simultaneously without any conditions.
    - Textual Clues: Look for words and phrases like "and", "both", "concurrently", "simultaneously", "parallel", "at the same time", "in tandem", "jointly", "while", etc.
    - AND can be split (divergence) or join (convergence)::
        - Split Behavior (Starting Multiple Tasks):When you reach this gateway, all paths are started at the same time, allowing tasks to be done concurrently. Example: Imagine you need to bake a cake and also make a salad. You start both tasks at the same time and continue with the next step only when both are done.
        - Join Behavior (Waiting for All Tasks): When paths come together at this gateway, it waits for all paths to be completed before moving forward. It ensures that all tasks are done before proceeding. Example: For a project needing approvals from both the technical and financial departments, the process proceeds only after both departments have approved, necessitating synchronization of both flows, identifying it as an AND join.
    - Modeling Instructions: State explicitly that tasks are to be performed in parallel.
    - Example:
        - Text: "The system will package and label the order at the same time."
        - Model: 
            - Gateway: AND_PackageAndLabel
            - Path 1: Task: Package order
            - Path 2: Task: Label order

Given the process description and the list of Activities/Events (also called "Nodes")identified from this description within the delimiters {delimiter}, please perform the following steps:

Steps to Perform
Step 1: List all identified gateways along with textual clues that led to the decision.
Step 2: Output a Python list of JSON objects, detailing the gateways identified in Step 1.

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

Keys Explanation
- id: Unique identifier for each gateway.
- name: Placeholder name for each gateway.
- type: Type of gateway (XOR, AND, OR), determined from textual clues.
- classification: Indicates whether the gateway splits into multiple paths or joins multiple paths.
- from_node/from_nodes: Element(s) immediately before the gateway.
- to_node/to_nodes: Element(s) immediately after the gateway.

Final Notes
- Split gateways are typically accompanied by join gateways but not always.
- Ensure output is strictly in the JSON format without any additional text.
"""

# {
#     "total_number_gateways": "{{number_of_gateways}}",
#     "total_number_XOR_split": "{{number_of_XOR_split}}",
#     "total_number_XOR_join": "{{number_of_XOR_join}}",
#     "total_number_AND_split": "{{number_of_AND_split}}",
#     "total_number_AND_join": "{{number_of_AND_join}}",
#     "total_number_OR_split": "{{number_of_OR_split}}",
#     "total_number_OR_join": "{{number_of_OR_join}}",
#     "gateways": [
#         {
#             "id": "{{gateway_id_1}}",
#             "name": "{{gateway_name_1}}",
#             "type": "{{gateway_type_1}}",
#             "classification": "{{gateway_classification_1}}",
#             "from_node": "{{from_node_1}}",
#             "to_nodes": ["{{to_node_1a}}", "{{to_node_1b}}"]
#         },
#         {
#             "id": "{{gateway_id_2}}",
#             "name": "{{gateway_name_2}}",
#             "type": "{{gateway_type_2}}",
#             "classification": "{{gateway_classification_2}}",
#             "from_node": "{{from_node_2}}",
#             "to_nodes": ["{{to_node_2a}}"]
#         },
#         ...
#     ]
# }

# Detail the keys' meaning:
# id: A unique identifier for the gateway.
# name: A placeholder name for the gateway.
# type: The type of gateway (XOR, AND, OR). Identify based on the textual clues provided above.
# classification: Indicates whether the gateway is a "split" or "join". Determine from the context where the gateway either splits into multiple paths or joins multiple paths.
# from_node/from_nodes: The node(s) preceding the gateway. Identify the element immediately before the gateway.
# to_node/to_nodes: The node(s) following the gateway. Identify the element(s) immediately after the gateway.

# REMEMBER:
# - Typically, a split gateway is accompanied by a join gateway, though this is not always the case. 
# - Do not include any additional text outside of the JSON format. 
# - Refrain from providing any explanatory text after the requested JSON output.



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

    #response = get_completion(messages, api="ollama", model="llama3.1")
    response = get_completion(messages, api="openai", model="gpt-4o")
    return response
    # try:
    #     return json.loads(response)
    # except json.JSONDecodeError:
    #     return {"error": "Failed to decode JSON response"}

# Example usage
if __name__ == "__main__":
    text_description = """Order-to-cash process starts whenever a purchase order has been received from a customer. The first activity that is carried out is confirming the order. Next, the shipment address is received so that the product can be shipped to the customer. Afterwards, the invoice is emitted and once the payment is received the order is archived, thus completing the process. Please note that a purchase order is only confirmed if the product is in stock, otherwise the process completes by rejecting the order. If the order is confirmed, the shipment address is received and the requested product is shipped while the invoice is emitted and the payment is received. Afterwards, the order is archived and the process completes.

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
