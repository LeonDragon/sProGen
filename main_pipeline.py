#%%
# MAIN PIPELINE FOR BUSINESS PROCESS GENERATION FROM TEXT
import json
from input_preprocess import identify_from_message as preprocess_identify_from_message
from context_understanding import identify_from_message as context_identify_from_message
from actions_identifier import identify_from_message as actions_identify_from_message
from gateways_identifier import identify_from_message as gateways_identify_from_message
from loops_identifier import identify_from_message as loops_identify_from_message
from sequenceFlows_identifier import identify_from_message as sequenceFlow_identify_from_message

def combine_results(previous_result, current_result, input_text=""):
    """
    Combines the results from two steps, including the input text and JSON format for each step.
    Parameters:
        previous_result (str): JSON string from the previous step.
        current_result (str): JSON string from the current step.
        input_text (str): The input text used for the current step.
        step_name (str): The name of the current step.
    Returns:
        str: Combined string containing input text and combined JSON data.
    """
    if previous_result:
        previous_json_data = json.loads(previous_result)
        if isinstance(previous_json_data, list):
            previous_json_data = previous_json_data[0]
    else:
        previous_json_data = {}
    current_json_data = json.loads(current_result)

    # Combine both JSON results
    if isinstance(previous_json_data, list):
        previous_json_data = previous_json_data[0]
    if isinstance(current_json_data, list):
        current_json_data = current_json_data[0]
    
    # Combine both JSON results
    combined_json_data = previous_json_data
    combined_json_data.update(current_json_data)
    
    # Create the final combined result string
    if input_text != "":
        final_result = input_text + "\n" + json.dumps(combined_json_data, indent=4)
    else:
        final_result = json.dumps(combined_json_data, indent=4)
    
    return final_result

def pipeline(process_description):
    """
    Processes the input text through a pipeline of identifying business process models from text.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        str: The combined output from all steps.
    """

    previous_json_result=""

    # Step 1: Preprocessing to improve the textual description
    print("Step 1: ======================= \n")
    preprocess_result = preprocess_identify_from_message(process_description)
    print(preprocess_result)
    new_process_description = json.loads(preprocess_result)[0]["Augmentation"]
    print(new_process_description)
    
    # Step 2: Context understanding to identify context and objectives
    print("Step 2: ======================= \n")
    context_json_result = context_identify_from_message(new_process_description)
    previous_json_result = context_json_result
    combined_prompt = combine_results("", context_json_result, new_process_description)
    print(combined_prompt)
    
    # Step 3: Identifying actions
    print("Step 3: ======================= \n")
    actions_json_result = actions_identify_from_message(combined_prompt)
    previous_json_result = combine_results(previous_json_result, actions_json_result)
    combined_prompt = combine_results(previous_json_result, actions_json_result, new_process_description)
    print(combined_prompt)
    
    # Step 4: Identifying gateways
    print("Step 4: ======================= \n")
    gateways_json_result = gateways_identify_from_message(combined_prompt)
    previous_json_result = combine_results(previous_json_result, gateways_json_result)
    combined_prompt = combine_results(previous_json_result, gateways_json_result, new_process_description)
    print(combined_prompt)
    
    # Step 5: Identifying loops
    print("Step 5: ======================= \n")
    loops_json_result = loops_identify_from_message(combined_prompt)
    previous_json_result = combine_results(previous_json_result, loops_json_result)
    combined_prompt = combine_results(previous_json_result, loops_json_result, new_process_description)
    print(combined_prompt)
    
    # Step 6: Identifying sequence flows
    print("Step 6: ======================= \n")
    sequence_flow_result = sequenceFlow_identify_from_message(combined_prompt)
    previous_json_result = combine_results(previous_json_result, sequence_flow_result)
    combined_prompt = combine_results(previous_json_result, sequence_flow_result, new_process_description)
    print(combined_prompt)
    
    return previous_json_result

# Example usage
if __name__ == "__main__":
    text_description = """
    Relevant Process Description information:
    In the treasury minister’s office, once a ministerial inquiry has been received, it is first registered into the system. Then the inquiry is investigated so that a ministerial response can be prepared. The finalization of a response includes the preparation of the response itself by the cabinet officer and the review of the response by the principal registrar. If the registrar does not approve the response, the latter needs to be prepared again by the cabinet officer for review. The process finishes only once the response has been approved. 
    """
    result = pipeline(text_description)
    print(result)
    #print(json.dumps(result, indent=4))

# %%
print(result)
# %%
