#%%
import graphviz
import json
import os

def generate_dot_from_sequence(sequence_flows):
    """
    Generates DOT language from a sequence flow of BPMN elements.
    
    Parameters:
        sequence_flows (list): A list of sequence flow dictionaries containing 'from', 'to', and optionally 'condition'.
    
    Returns:
        str: The DOT language representation of the BPMN model.
    """
    dot_lines = [
        "digraph BPMN {",
        "    rankdir=LR;",
        "    node [shape=circle, style=filled, color=lightblue, penwidth=2];"
    ]

    nodes = set()
    for flow in sequence_flows:
        nodes.add(flow["from"])
        nodes.add(flow["to"])

    start_nodes = [node for node in nodes if node.startswith("Start_")]
    end_nodes = [node for node in nodes if node.startswith("End_")]
    activity_nodes = [node for node in nodes if node.startswith("A_") or node.startswith("E_")]
    gateway_nodes = [node for node in nodes if node.startswith("XOR_") or node.startswith("AND_") or node.startswith("OR_")]

    # Start and End nodes
    for start_node in start_nodes:
        dot_lines.append(f'    {start_node} [label="", color=forestgreen];')
    for end_node in end_nodes:
        dot_lines.append(f'    {end_node} [label="", color=firebrick, penwidth=3];')

    # Activities
    dot_lines.append("""
    node [
        shape=box, 
        style="rounded,filled", 
        fillcolor=lightgoldenrodyellow, 
        color=black,
        penwidth=1, 
        fontcolor=black
    ];""")
    for activity_node in activity_nodes:
        label = activity_node.split("_")[1].replace(" ", "\n")
        dot_lines.append(f'    {activity_node} [label="{label}"];')

    # Gateways
    dot_lines.append("""
    node [
        shape=diamond, 
        style=filled, 
        fillcolor=gold, 
        color=black, 
        penwidth=1
    ];""")
    for gateway_node in gateway_nodes:
        label = gateway_node.split("_")[0]
        dot_lines.append(f'    {gateway_node} [label="{label}"];')

    # Edges
    for flow in sequence_flows:
        condition = flow.get("condition", "")
        label = f' [label="{condition}"]' if condition else ""
        dot_lines.append(f'    {flow["from"]} -> {flow["to"]}{label};')

    dot_lines.append("}")

    return "\n".join(dot_lines)

def visualize_bpmn(dot_string, file_name='bpmn_model', directory='.', file_format='svg'):
    """
    Visualizes a BPMN model using Graphviz.
    
    Parameters:
        dot_string (str): The DOT language representation of the BPMN model.
        file_name (str): The name of the output file (without extension).
        directory (str): The directory where the output file will be saved.
        file_format (str): The format of the output file (e.g., 'svg', 'png', 'pdf').
    """
    try:
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create the full file path
        file_path = os.path.join(directory, file_name)
        
        # Create Graphviz Source object
        graph = graphviz.Source(dot_string)
        
        # Render and view the graph
        graph.render(file_path, format=file_format, view=True)
        
        print(f"Graphviz visualization generated successfully at {file_path}.{file_format}.")
    except Exception as e:
        print("Error in generating visualization:", e)  # Print error message if any

# Example usage
if __name__ == "__main__":
     # JSON string input
    json_string = '''
     [
        {
            "SequenceFlows": [
                {"from": "Start_ReceiveInquiry", "to": "A_RegisterInquiry"},
                {"from": "A_RegisterInquiry", "to": "A_InvestigateInquiry"},
                {"from": "A_InvestigateInquiry", "to": "A_PrepareResponse"},
                {"from": "A_PrepareResponse", "to": "A_ReviewResponse"},
                {"from": "A_ReviewResponse", "to": "XOR_ResponseApproval"},
                {"from": "XOR_ResponseApproval", "to": "A_ResubmitResponse", "condition": "if the response is not approved"},
                {"from": "XOR_ResponseApproval", "to": "End_ApproveResponse", "condition": "if the response is approved"},
                {"from": "A_ResubmitResponse", "to": "A_PrepareResponse"}
            ]
        }
    ]
    '''

    json_string_new = '''
    [
        {
            "SequenceFlows": [
                {"from": "Start_ReceiveInquiry", "to": "XOR_RegisterInquiry"},
                {"from": "XOR_RegisterInquiry", "to": "A_RegisterInquiry"},
                {"from": "XOR_RegisterInquiry", "to": "A_InvestigateInquiry"},
                {"from": "A_RegisterInquiry", "to": "A_InvestigateInquiry"},
                {"from": "A_InvestigateInquiry", "to": "A_PrepareResponse"},
                {"from": "A_PrepareResponse", "to": "E_ReviewResponse"},
                {"from": "E_ReviewResponse", "to": "XOR_ApproveResponse"},
                {"from": "XOR_ApproveResponse", "to": "End_ApproveResponse", "condition": "if approved"},
                {"from": "A_PrepareForRevision", "to": "A_InvestigateInquiry"},
                {"from": "A_PrepareForRevision", "to": "E_ReviewResponse"},
                {"from": "XOR_ApproveResponse", "to": "A_PrepareForRevision", "condition": "if not approved"}
            ]
        }
    ]
    '''

    # Parse the JSON string
    data = json.loads(json_string)
    sequence_flows = data[0]["SequenceFlows"]

    dot_result = generate_dot_from_sequence(sequence_flows)
    print(dot_result)
    # Visualize the result
    visualize_bpmn(dot_result, file_name='logic_tested_bpmn_model', directory='./output', file_format='svg')

# %%
