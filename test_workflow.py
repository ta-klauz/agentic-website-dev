"""
Test script for the extended langgraph workflow.
This script runs the complete workflow using a user-provided description.
"""
import sys
from main import graph

def run_workflow(description):
    """
    Run the workflow with a user-provided description
    
    Args:
        description: A short description of the 1-page website to generate
    """
    print(f"Starting workflow with description: '{description}'")
    
    # Initial state
    initial_state = {
        "test_results": [],
        "messages": [],
        "requirements": [],
        "acceptance_criteria": [],
        "description": description,
        "script_filename": "",
        "script_comments": ""
    }
    
    # Run the workflow
    events = graph.stream(initial_state, stream_mode="values")
    
    # Process the events
    final_state = None
    for i, event in enumerate(events):
        print(f"\n------ Event {i} ------")
        if "requirements" in event and event["requirements"]:
            print("\nGenerated Requirements:")
            for req in event["requirements"]:
                print(f"- {req}")
        
        if "acceptance_criteria" in event and event["acceptance_criteria"]:
            print("\nAcceptance Criteria:")
            for crit in event["acceptance_criteria"]:
                print(f"- {crit}")
        
        if "script_filename" in event and event["script_filename"]:
            print(f"\nGenerated script saved to: {event['script_filename']}")
            
        if "script_comments" in event and event["script_comments"]:
            print("\nScript Generator Comments:")
            print(event["script_comments"])
        
        final_state = event
    
    print("\n------ Workflow Complete ------")
    return final_state

if __name__ == "__main__":
    # Get the description from command line arguments or use a default
    description = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Create a simple portfolio website with a header, about section, skills section, and contact form."
    
    # Run the workflow
    final_state = run_workflow(description)
    
    # Print the final script filename
    if final_state and "script_filename" in final_state and final_state["script_filename"]:
        print(f"\nFinal script is available at: {final_state['script_filename']}")
        print(f"Run it with: python {final_state['script_filename']}") 