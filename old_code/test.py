#%%
import json

def combine_results(previous_result, current_result, input_text, step_name):
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
    previous_json_data = json.loads(previous_result)
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
    final_result = input_text + "\n" + json.dumps(combined_json_data, indent=4)
    
    return final_result

# Example usage
if __name__ == "__main__":
    text_description = """
    Relevant Process Description information:
    Once a loan application is received by the loan provider, and before proceeding with its assessment, the application itself needs to be checked for completeness. If the application is incomplete, it is returned to the applicant, so that they can fill out the missing information and send it back to the loan provider. This process is repeated until the application is found complete.
    """

    json_data1 = [
        {
            "SequenceFlows": [
                {"from": "Start_ReceiveLoanApplication", "to": "A_CheckApplicationCompleteness"},
                {"from": "A_CheckApplicationCompleteness", "to": "XOR_CheckCompleteness"},
                {"from": "XOR_CheckCompleteness", "to": "A_ReturnIncompleteApplication", "condition": "if application is incomplete"},
                {"from": "XOR_CheckCompleteness", "to": "End_ApplicationComplete", "condition": "if application is complete"},
                {"from": "A_ReturnIncompleteApplication", "to": "A_ResubmitApplication"},
                {"from": "A_ResubmitApplication", "to": "XOR_ResubmitOrComplete"},
                {"from": "XOR_ResubmitOrComplete", "to": "A_CheckApplicationCompleteness"}
            ]
        }
    ]

    json_data2 = {
        "StartEvent": "Start_ReceiveLoanApplication",
        "EndEvent": "End_ApplicationComplete",
        "ActivitiesEvent": [
            {"A_CheckApplicationCompleteness": "The application itself needs to be checked for completeness"},
            {"A_ReturnIncompleteApplication": "If the application is incomplete, it is returned to the applicant"},
            {"A_ResubmitApplication": "Applicant fills out the missing information and sends it back to the loan provider"}
        ]
    }

    # Convert JSON data to strings
    previous_result = json.dumps(json_data1, indent=4)
    current_result = json.dumps(json_data2, indent=4)
    
    # Combine results
    combined_result = combine_results(previous_result, current_result, text_description, "Step1")
    print(combined_result)

# %%
