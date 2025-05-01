"""
Main entry point for the agentic website development system.
"""
from typing import Annotated, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from operator import add

# Import components from our package
from nodes import requirements_generator
from nodes import script_generator
from nodes import node_tester
from nodes import node_coder

#************************************************************************************

description = "Create an attractive landing page for a business that sells IoT products and services"

#************************************************************************************

class State(TypedDict):
    messages: Annotated[list, add_messages]
    test_results: Annotated[list[Any], add]
    requirements: Any
    acceptance_criteria: Any
    description: str
    script_filename: str
    script_comments: str
    iteration_count: int  # Track iterations of the coder-tester loop

def create_workflow(description: str):
    """Create a workflow graph for website generation."""
    graph_builder = StateGraph(State)
    graph_builder.add_node("requirements_generator", requirements_generator.execute)
    graph_builder.add_node("script_generator", script_generator.execute)
    graph_builder.add_node("code_tester", node_tester.execute)
    graph_builder.add_node("code_editor", node_coder.execute)

    # Update the workflow edges
    graph_builder.add_edge(START, "requirements_generator")
    graph_builder.add_edge("requirements_generator", "script_generator")
    graph_builder.add_edge("script_generator", "code_tester")
    # No conditional edge needed, as node_tester now uses Command to direct flow
    # Add edge from code_editor back to code_tester to create the loop
    graph_builder.add_edge("code_editor", "code_tester")

    return graph_builder.compile()

def main(description: str = None):
    """Run the website generation workflow."""
    if description is None:
        description = "Create an attractive landing page for a business that sells IoT products and services"
    
    # Create workflow
    graph = create_workflow(description)
    
    # Starting state
    initial_state = {
        "test_results": [],
        "messages": [],
        "requirements": [],
        "acceptance_criteria": [],
        "description": description,
        "script_filename": "",
        "script_comments": "",
        "iteration_count": 0  # Initialize iteration counter
    }

    # Run workflow
    events = graph.stream(initial_state, stream_mode="values",)

    final_state = None
    for event in events:
        final_state = event
        print(event,"-------------------------------------------------------------------------------")
    
    return final_state

if __name__ == "__main__":
    import argparse
    
    # Setup command line arguments
    parser = argparse.ArgumentParser(description='Generate a website based on a description')
    parser.add_argument('--description', type=str, default=description,
                        help='Description of the website to generate')
    
    args = parser.parse_args()
    main(args.description)
