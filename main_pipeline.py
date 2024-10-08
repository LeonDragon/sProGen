#%%
# MAIN PIPELINE FOR BUSINESS PROCESS GENERATION FROM TEXT
import json
import time
from input_preprocess import identify_from_message as preprocess_identify_from_message
from context_understanding import identify_from_message as context_identify_from_message
from actions_identifier import identify_from_message as actions_identify_from_message
from actionInstances_identifier import identify_from_message as actionInstances_identify_from_message # Action Instance
from gateways_identifier import identify_from_message as gateways_identify_from_message
from loops_identifier import identify_from_message as loops_identify_from_message
from sequenceFlows_identifier import identify_from_message as sequenceFlow_identify_from_message
#from bp_logic_visualizer import identify_from_message as bpm_visualization_from_message
from bp_logic_visualizer import visualize_bpmn, generate_dot_from_sequence

import json

def combine_results(previous_result, current_result, input_text=""):
    """
    Combines the results from two steps, including the input text and JSON format for each step.
    Parameters:
        previous_result (str): JSON string from the previous step.
        current_result (str): JSON string from the current step.
        input_text (str): The input text used for the current step.
    Returns:
        str: Combined string containing input text and combined JSON data.
    """
    if previous_result:
        previous_json_data = json.loads(previous_result)
        if isinstance(previous_json_data, list):
            previous_json_data = previous_json_data[0]
    else:
        previous_json_data = {}

    try:
        current_json_data = json.loads(current_result)
    except json.JSONDecodeError:
        print("Error: current_result is not a valid JSON.")
        print("current_result:", current_result)
        return "Error: current_result is not a valid JSON."

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

def calculate_cost(prompt_tokens, completion_tokens, price_per_1m_prompt_tokens, price_per_1m_completion_tokens):
    """
    Calculate the cost for given prompt and completion tokens based on the pricing per 1 million tokens.

    Parameters:
    prompt_tokens (int): Number of prompt tokens
    completion_tokens (int): Number of completion tokens
    price_per_1m_prompt_tokens (float): Price per 1 million prompt tokens
    price_per_1m_completion_tokens (float): Price per 1 million completion tokens

    Returns:
    dict: A dictionary containing the cost for prompt tokens, completion tokens, and total cost
    """
    cost_prompt_tokens = (prompt_tokens / 1_000_000) * price_per_1m_prompt_tokens
    cost_completion_tokens = (completion_tokens / 1_000_000) * price_per_1m_completion_tokens
    total_cost = cost_prompt_tokens + cost_completion_tokens

    return {
        "cost_prompt_tokens": cost_prompt_tokens,
        "cost_completion_tokens": cost_completion_tokens,
        "total_cost": total_cost
    }

def update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens):
    total_prompt_tokens += prompt_tokens
    total_completion_tokens += completion_tokens
    return total_prompt_tokens, total_completion_tokens

def pipeline(process_description):
    """
    Processes the input text through a pipeline of identifying business process models from text.
    Parameters:
        text (str): The textual description of the business process.
    Returns:
        str: The combined output from all steps.
    """
    total_start_time = time.time()
    total_prompt_tokens = 0
    total_completion_tokens = 0
    delay_time = 0

    previous_json_result=""

    # Step 1: Preprocessing to improve the textual description
    print("Step 1: Preprocessing to improve the textual description", end=' ', flush=True)
    #preprocess_result, prompt_tokens, completion_tokens = preprocess_identify_from_message(process_description, api="vertexai", model="meta/llama3-405b-instruct-maas", temperature=0.0)
    
    preprocess_result, prompt_tokens, completion_tokens = preprocess_identify_from_message(process_description, api="openai", model="gpt-4o", temperature=0.7)
    # total_prompt_tokens, total_completion_tokens = update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens)
    # new_process_description = json.loads(preprocess_result)[0]["Original"] #Original or Augmented
    #new_process_description = process_description
    new_process_description = preprocess_result
    
    #print(preprocess_result)
    print(" ===> DONE \n")
    print(new_process_description)
    time.sleep(delay_time) # For vertex AI Llama3.1 405b
    
    # Step 2: Context understanding to identify context and objectives
    print("Step 2: Context understanding to identify context and objectives", end=' ', flush=True)
    #context_json_result, prompt_tokens, completion_tokens = context_identify_from_message(new_process_description, api="vertexai", model="meta/llama3-405b-instruct-maas", temperature=0.0)
    #context_json_result, prompt_tokens, completion_tokens = context_identify_from_message(new_process_description, api="ollama", model="phi3", temperature=0.7)
    context_json_result, prompt_tokens, completion_tokens = context_identify_from_message(new_process_description, api="openai", model="gpt-4o-mini", temperature=0.7)
    total_prompt_tokens, total_completion_tokens = update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens)
    previous_json_result = context_json_result
    combined_prompt = combine_results("", context_json_result, new_process_description)
    print(" ===> DONE \n")
    print(previous_json_result)
    #print(combined_prompt)
    time.sleep(delay_time) # For vertex AI Llama3.1 405b
    
    # Step 3: Identifying actions
    print("Step 3: Identifying actions", end=' ', flush=True) 
    #actions_json_result, prompt_tokens, completion_tokens = actions_identify_from_message(combined_prompt, api="vertexai", model="meta/llama3-405b-instruct-maas", temperature=0.0)
    #actions_json_result, prompt_tokens, completion_tokens = actions_identify_from_message(combined_prompt, api="ollama", model="phi3", temperature=0.0)
    actions_json_result, prompt_tokens, completion_tokens = actions_identify_from_message(combined_prompt, api="openai", model="gpt-4o-mini", temperature=0.7)
    total_prompt_tokens, total_completion_tokens = update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens)
    previous_json_result = combine_results(previous_json_result, actions_json_result)
    combined_prompt = combine_results(previous_json_result, actions_json_result, new_process_description)
    print(" ===> DONE \n")
    print(actions_json_result)
    #print(combined_prompt)
    time.sleep(delay_time) # For vertex AI Llama3.1 405b

    # Step 3-1: Identifying Action Instance (Ordering relation between activities and events) actionInstance_identify_from_message
    print("Step 3-1: Identifying action instances", end=' ', flush=True) 
    #actionsInstance_json_result, prompt_tokens, completion_tokens = actions_identify_from_message(combined_prompt, api="vertexai", model="meta/llama3-405b-instruct-maas", temperature=0.0)
    #actions_json_result, prompt_tokens, completion_tokens = actions_identify_from_message(combined_prompt, api="ollama", model="phi3", temperature=0.0)
    actionsInstances_json_result, prompt_tokens, completion_tokens = actionInstances_identify_from_message(combined_prompt, api="openai", model="gpt-4o-mini", temperature=0.7)
    total_prompt_tokens, total_completion_tokens = update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens)
    previous_json_result = combine_results(previous_json_result, actionsInstances_json_result)
    combined_prompt = combine_results(previous_json_result, actionsInstances_json_result, new_process_description)
    print(" ===> DONE \n")
    print(actionsInstances_json_result)
    #print(combined_prompt)
    time.sleep(delay_time) # For vertex AI Llama3.1 405b
    
    # Step 4: Identifying gateways
    print("Step 4: Identifying gateways", end=' ', flush=True)
    #gateways_json_result, prompt_tokens, completion_tokens = gateways_identify_from_message(combined_prompt, api="vertexai", model="meta/llama3-405b-instruct-maas", temperature=0.0)
    #gateways_json_result, prompt_tokens, completion_tokens = gateways_identify_from_message(combined_prompt, api="ollama", model="phi3", temperature=0.0)
    gateways_json_result, prompt_tokens, completion_tokens = gateways_identify_from_message(combined_prompt, api="openai", model="gpt-4o-mini", temperature=0.7)
    total_prompt_tokens, total_completion_tokens = update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens)
    previous_json_result = combine_results(previous_json_result, gateways_json_result)
    combined_prompt = combine_results(previous_json_result, gateways_json_result, new_process_description)
    print(" ===> DONE \n") 
    print(gateways_json_result)
    
    #print(gateways_json_result)
    #print(combined_prompt)
    time.sleep(delay_time) # For vertex AI Llama3.1 405b
    
    # Step 5: Identifying loops
    print("Step 5: Identifying loops", end=' ', flush=True)
    #loops_json_result, prompt_tokens, completion_tokens = loops_identify_from_message(combined_prompt, api="vertexai", model="meta/llama3-405b-instruct-maas", temperature=0.0)
    #loops_json_result, prompt_tokens, completion_tokens = loops_identify_from_message(combined_prompt, api="ollama", model="phi3", temperature=0.0)
    loops_json_result, prompt_tokens, completion_tokens = loops_identify_from_message(combined_prompt, api="openai", model="gpt-4o-mini", temperature=0.7)
    total_prompt_tokens, total_completion_tokens = update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens)
    previous_json_result = combine_results(previous_json_result, loops_json_result)
    combined_prompt = combine_results(previous_json_result, loops_json_result, new_process_description)
    print(" ===> DONE \n")
    print(loops_json_result)
    #print(combined_prompt)
    time.sleep(delay_time) # For vertex AI Llama3.1 405b
    
    # Step 6: Identifying sequence flows
    print("Step 6: Identifying sequence flows", end=' ', flush=True)
    #sequence_flow_result, prompt_tokens, completion_tokens = sequenceFlow_identify_from_message(combined_prompt, api="vertexai", model="meta/llama3-405b-instruct-maas", temperature=0.7)
    #sequence_flow_result, prompt_tokens, completion_tokens = sequenceFlow_identify_from_message(combined_prompt, api="ollama", model="phi3", temperature=0.7)
    sequence_flow_result, prompt_tokens, completion_tokens = sequenceFlow_identify_from_message(combined_prompt, api="openai", model="gpt-4o-mini", temperature=0.7)
    total_prompt_tokens, total_completion_tokens = update_total_tokens(prompt_tokens, completion_tokens, total_prompt_tokens, total_completion_tokens)
    previous_json_result = combine_results(previous_json_result, sequence_flow_result)
    combined_prompt = combine_results(previous_json_result, sequence_flow_result, new_process_description)
    print(" ===> DONE \n")
    print(sequence_flow_result)
    #print(combined_prompt)

    # Step 7: Visualize Business Process with Graphviz
    #print("Step 7: Visualize Business Process with Graphviz")
    # try:
    #     data = json.loads(sequence_flow_result)
    #     sequence_flows = data[0]["SequenceFlows"]
    #     bp_dot = generate_dot_from_sequence(sequence_flows)
    #     visualize_bpmn(bp_dot, file_name='my_bpmn_model', directory='./output', file_format='svg')
    #     print(" ===> DONE \n")
    # except Exception as e:
    #     print(" ===> Error in visualization")
    #     print(f"Error: {e}")
    

    # Print out stats
    total_end_time = time.time()
    total_tokens = total_prompt_tokens + total_completion_tokens
    print(f"Total Computation time: {total_end_time - total_start_time:.4f} seconds")
    # print(f"Total Tokens Used: {total_tokens}")
    # print(f"Total Prompt Tokens: {total_prompt_tokens}")
    # print(f"Total Completion Tokens: {total_completion_tokens} \n")

    # Constants
    PROMPT_TOKENS = total_prompt_tokens
    COMPLETION_TOKENS = total_completion_tokens
    PRICE_PER_1M_PROMPT_TOKENS = 0.150  # USD
    PRICE_PER_1M_COMPLETION_TOKENS = 0.600  # USD
    costs = calculate_cost(PROMPT_TOKENS, COMPLETION_TOKENS, PRICE_PER_1M_PROMPT_TOKENS, PRICE_PER_1M_COMPLETION_TOKENS)
    # Output the results
    print(f"Cost for {total_prompt_tokens} Prompt Tokens: ${costs['cost_prompt_tokens']:.8f}")
    print(f"Cost for {total_completion_tokens} Completion Tokens: ${costs['cost_completion_tokens']:.8f}")
    print(f"Total Cost for {total_tokens} Tokens: ${costs['total_cost']:.8f}")
    
    return previous_json_result, sequence_flow_result

# Example usage
if __name__ == "__main__":
    text_description_2 = """
    A company has two warehouses that store different products: Amsterdam and Hamburg. When an order is received, it is distributed across these warehouses: if some of the relevant products are maintained in Amsterdam, a sub-order is sent there; likewise, if some relevant products are maintained in Hamburg, a sub-order is sent there. Afterwards, the order is registered and the process completes. 
    """

    text_description = """
    Relevant Process Description information:
    In the treasury minister’s office, once a ministerial inquiry has been received, it is first registered into the system. Then the inquiry is investigated so that a ministerial response can be prepared. The finalization of a response includes the preparation of the response itself by the cabinet officer and the review of the response by the principal registrar. If the registrar does not approve the response, the latter needs to be prepared again by the cabinet officer for review. The process finishes only once the response has been approved. 
    """
    result, sequenceFlows = pipeline(text_description)
    #print(result)
    #print(json.dumps(result, indent=4))

#%%
#print(sequenceFlows)
# %%
#print(result)
# Step 7: Visualize Business Process with Graphviz
#print("Step 7: AGAIN \n")
#bp_dot = bp_llm_visualization_from_message(sequenceFlows, api="openai", model="gpt-4o-mini", temperature=0)
# print(bp_dot)
# visualize_bpmn(bp_dot, file_name='my_bpmn_model_temp', directory='./output', file_format='svg')
# %%
