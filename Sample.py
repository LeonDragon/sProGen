#%%
from openai import OpenAI
from config import OPENAI_API_KEY
import os
import json


client = OpenAI(
    api_key=OPENAI_API_KEY
)

def get_completion(messages, model="gpt-4o", temperature=0, max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

def summarize_context(text):
    """
    Step 1: Understand the Textual Description, Identify context and overall Process Goal:
    - Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details.
    - Context: Describe the context of the process model in the given textual description, e.g., logistics, manufacturing, service, finance, etc.
    - Clarify Scope: Determine the boundaries of the process (start and end points).
    - Set Objectives: Understand the purpose of the process and its desired outcomes.

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        dict: A dictionary containing the context, scope, and objectives of the process.
    """
    system_message = """
    Follow these steps to analyze the business process.
    The process description will be delimited with four hashtags, i.e. ####.
    
    Step 1: Understand the Textual Description, Identify context and overall Process Goal:
    - Read Thoroughly: Carefully read the textual description of the business process to grasp the overall objective, scope, and details.
    - Context: Describe the context of the process model in the given textual description, e.g., logistics, manufacturing, service, finance, etc.
    - Clarify Scope: Determine the boundaries of the process (start and end points).
    - Set Objectives: Understand the purpose of the process and its desired outcomes.

    Return the output in a JSON format:
    {
    "Context": "{{context_placeholder}}",
    "Scope": {
        "Start": "{{start_placeholder}}",
        "End": "{{end_placeholder}}"
    },
    "Objectives": "{{objectives_placeholder}}"
    }


    """
    user_message = f"####{text}####"
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = get_completion(messages)
    return response

def identify_events(text):
    """
    Step 2: Identify Start and End event
    - Start Event: Define the starting point of the process that initiates the workflow.
    - End Event: Define the endpoint of the process, describing the completion of the process flow.

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        dict: A dictionary containing the start and end events.
    """
    system_message = """
    Follow these steps to analyze the business process.
    The process description will be delimited with four hashtags, i.e. ####.
    
    Step 2: Identify Start and End event
    - Start Event: Define the starting point of the process that initiates the workflow. Provide a brief label or description to clarify what triggers the process (e.g., Start_ReceiveOrder).
    - End Event: Define the endpoint of the process, describing the completion of the process flow. Provide a brief label or description to clarify the end condition (e.g., "End_OrderFulfilled," "End_InvoiceSent", End_ShipmentComplete).

    Return the output in a JSON format:
    {
        "StartEvent": "{{start_event_placeholder}}",
        "EndEvent": "{{end_event_placeholder}}"
    }

    """
    user_message = f"####{text}####"
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = get_completion(messages)
    return response

def identify_activities(text):
    """
    Step 3: Identify Main Activities (Tasks) or Intermediate Events:
    - Activities/Events: Identify specific actions or tasks described in the text and event usually in verb forms, assigning a variable to each (e.g., A_RecieveOrder, A_CheckCredit, E_RecieveEmail).

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        dict: A dictionary containing the identified activities and events.
    """
    system_message = """
    Follow these steps to analyze the business process.
    The process description will be delimited with four hashtags, i.e. ####.
    
    Step 3: Identify Main Activities (Tasks) or Intermediate Events:
    - Activities/Events: Identify specific actions or tasks described in the text and event usually in verb forms, assigning a variable to each (e.g., A_RecieveOrder, A_CheckCredit, E_RecieveEmail).

    Return the output in a JSON format:
    {
        "total_number_activities": "{{number_of_activities}}",
        "total_number_events": "{{number_of_events}}",
        "activities_or_events": [
            "{{activity_or_event_key_1}}": "{{activity_or_event_value_1}}",
            "{{activity_or_event_key_2}}": "{{activity_or_event_value_2}}",
            ...
        ]
    }

    """
    user_message = f"####{text}####"
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = get_completion(messages)
    return response

def identify_loops(text):
    """
    Step 4: Identify Loops or Cycles:
    - Identify Loops: Look for any repeated actions or instructions that indicate a task or set of tasks is performed more than once under certain conditions.

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        dict: A dictionary containing the identified loops and their activities or events.
    """
    system_message = """
    Follow these steps to analyze the business process.
    The process description will be delimited with four hashtags, i.e. ####.
    
    Step 4: Identify Loops or Cycles:
    - Identify Loops: Look for any repeated actions or instructions that indicate a task or set of tasks is performed more than once under certain conditions.

    Return the output in a JSON format:
    {
       "loop_name": "{{loop_name_placeholder}}",
       "activities_or_events": "{{activities_or_events_placeholder}}"
    }

    """
    user_message = f"####{text}####"
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = get_completion(messages)
    return response

def identify_gateways(text):
    """
    Step 5: Determine Gateways for Decision Points and Parallelism:
    - Identify Gateways (Decision Points): Exclusive (XOR), Inclusive (OR), and Parallel (AND).

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        dict: A dictionary containing identified gateways with keys id, name, type, classification, from_node/from_nodes, to_node/to_nodes.
    """
    system_message = """
    Follow these steps to analyze the business process.
    The process description will be delimited with four hashtags, i.e. ####.
    
    Step 5: Determine Gateways for Decision Points and Parallelism:
    - Identify Gateways (Decision Points): Exclusive (XOR), Inclusive (OR), and Parallel (AND).

    Return the output in a JSON format
    {
        "total_number_gateways": "{{number_of_gateways}}",
        "total_number_XOR_split": "{{number_of_XOR_split}}",
        "total_number_XOR_join": "{{number_of_XOR_join}}",
        "total_number_AND_split": "{{number_of_AND_split}}",
        "total_number_AND_join": "{{number_of_AND_join}}",
        "total_number_OR_split": "{{number_of_OR_split}}",
        "total_number_OR_join": "{{number_of_OR_join}}",
        "gateways": [
            {
                "id": "{{gateway_id_1}}",
                "name": "{{gateway_name_1}}",
                "type": "{{gateway_type_1}}",
                "classification": "{{gateway_classification_1}}",
                "from_node": "{{from_node_1}}",
                "to_nodes": ["{{to_node_1a}}", "{{to_node_1b}}"]
            },
            {
                "id": "{{gateway_id_2}}",
                "name": "{{gateway_name_2}}",
                "type": "{{gateway_type_2}}",
                "classification": "{{gateway_classification_2}}",
                "from_node": "{{from_node_2}}",
                "to_nodes": ["{{to_node_2a}}"]
            },
            ...
        ]
    }
    Detail the keys meaning:
    id: A unique identifier for the gateway.
    name: A placeholder name for the gateway.
    type: The type of gateway (XOR, AND, OR).
    classification: Indicates whether the gateway is a "split" or "join".
    from_node/from_nodes: The node(s) preceding the gateway.
    to_node/to_nodes: The node(s) following the gateway.

    """
    user_message = f"####{text}####"
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = get_completion(messages)
    return response

def identify_roles(text):
    """
    Step 6: Identify Participants and Roles:
    - Roles and Responsibilities: Identify different roles or participants involved in the process.

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        dict: A dictionary containing the identified participants and roles.
    """
    system_message = """
    Follow these steps to analyze the business process.
    The process description will be delimited with four hashtags, i.e. ####.
    
    Step 6: Identify Participants and Roles:
    - Roles and Responsibilities: Identify different roles or participants involved in the process.

    Return the output in a JSON format: 
    {
        "total_number_participants": "{{number_of_participants}}",
        "total_number_roles": "{{number_of_roles}}",
        "Participants": [
            "{{participant_1}}",
            "{{participant_2}}",
            "{{participant_3}}",
            "{{participant_4}}"
        ],
        "Roles": {
            "{{participant_1}}": "{{role_1}}",
            "{{participant_2}}": "{{role_2}}",
            "{{participant_3}}": "{{role_3}}",
            "{{participant_4}}": "{{role_4}}"
        }
    }

    """
    user_message = f"####{text}####"
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = get_completion(messages)
    return response

def determine_sequence_flows(text):
    """
    Step 7: Determine Sequence Flows:
    - Establish the order of activities, events, and gateways, detailing the sequence flow with variables.

    Parameters:
        text (str): The textual description of the business process.

    Returns:
        dict: A dictionary containing the sequence flows with attributes like id, source_node, and target_node.
    """
    system_message = """
    Follow these steps to analyze the business process.
    The process description will be delimited with four hashtags, i.e. ####.
    
    Step 7: Determine Sequence Flows:
    - Establish the order of activities, events, and gateways, detailing the sequence flow with variables.

    Return the output in a JSON format 
    {
    {
        "total_number_flows": "{{number_of_flows}}",
        "sequence_flows": [
            {
                "id": "{{sequence_flow_id_1}}",
                "source_node": "{{source_node_1}}",
                "target_node": "{{target_node_1}}"
            },
            {
                "id": "{{sequence_flow_id_2}}",
                "source_node": "{{source_node_2}}",
                "target_node": "{{target_node_2}}"
            },
            {
                "id": "{{sequence_flow_id_3}}",
                "source_node": "{{source_node_3}}",
                "target_node": "{{target_node_3}}",
                "condition": "{{condition_3}}"
            },
            ...
        ]
    }

    """
    user_message = f"####{text}####"
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    
    response = get_completion(messages)
    return response

#%%
# Example usage
if __name__ == "__main__":
    text = """
    Order-to-cash process starts whenever a purchase order has been received from a customer. The first activity that is carried out is confirming the order. Next, the shipment address is received so that the product can be shipped to the customer. Afterwards, the invoice is emitted and once the payment is received the order is archived, thus completing the process. Please note that a purchase order is only confirmed if the product is in stock, otherwise the process completes by rejecting the order. If the order is confirmed, the shipment address is received and the requested product is shipped while the invoice is emitted and the payment is received. Afterwards, the order is archived and the process completes
    """
    import json
    import pandas as pd
    from IPython.display import display

    context_response = summarize_context(text)
    print("Step 1:", context_response)

    #===================
    
    events_response = identify_events(text)
    print("Step 2:", events_response)
    
    activities_response = identify_activities(text)
    print("Step 3:", activities_response)
    
    loops_response = identify_loops(text)
    print("Step 4:", loops_response)
    
    gateways_response = identify_gateways(text)
    print("Step 5:", gateways_response)
    
    roles_response = identify_roles(text)
    print("Step 6:", roles_response)
    
    flows_response = determine_sequence_flows(text)
    print("Step 7:", flows_response)

# %%
