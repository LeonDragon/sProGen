import graphviz

# import os
# os.environ["PATH"] += os.pathsep + 'D:\ProgramFiles\Graphviz-12.0.0-win64'

def visualize_bpmn(dot_string):
    """
    Visualizes a BPMN model using Graphviz.

    Parameters:
        dot_string (str): The DOT language representation of the BPMN model.
    """
    try:
        graph = graphviz.Source(dot_string)  # Create Graphviz Source object
        graph.render('bpmn_model', format='jpg', view=True)  # Render and view the graph
        print("Graphviz visualization generated successfully.")
    except Exception as e:
        print("Error in generating visualization:", e)  # Print error message if any

# Example DOT string for a simple BPMN model
dot_string = """
digraph BPMN {
    rankdir=LR;
    node [shape=circle, style=filled, color=lightblue];

    // Start and End nodes
    start [label="Start", color=green];
    end [label="End", color=red, penwidth=3];

    // Activities
    node [shape=box, style=rounded, color=lightgreen];
    activity1 [label="Activity 1"];
    activity2 [label="Activity 2"];
    activity3 [label="Activity 3"];

    // Gateways
    node [shape=diamond, style=filled, color="#FFD700"];
    xor_gateway [label="XOR Gateway"];
    and_gateway [label="AND Gateway"];

    // Edges
    start -> activity1;
    activity1 -> xor_gateway;
    xor_gateway -> activity2 [label="Condition A"];
    xor_gateway -> activity3 [label="Condition B"];
    activity2 -> and_gateway;
    activity3 -> and_gateway;
    and_gateway -> end;

    // Labels positioned below the nodes
    start_label [shape=plaintext, label="Start", color=white];
    end_label [shape=plaintext, label="End", color=white];

    { rank=same; start; start_label; }
    { rank=same; end; end_label; }

    // Invisible edges for proper label positioning
    start -> start_label [style=invis];
    end -> end_label [style=invis];
}
"""

# Visualize the example BPMN model
visualize_bpmn(dot_string)
