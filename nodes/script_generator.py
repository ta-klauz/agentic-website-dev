from langchain_openai import ChatOpenAI
import os
from pydantic import BaseModel, Field

class WebsiteScript(BaseModel):
    """Model for structured output from the script generator"""
    script_code: str = Field(description="The complete Python script code for the website")
    comments: str = Field(description="Any additional comments or explanations about the generated script")

def execute(state):
    """
    This node generates a Python script to fulfill the requirements and 
    acceptance criteria produced by the requirements_generator.
    
    Args:
        state: The current state containing requirements and acceptance criteria
        
    Returns:
        Updated state with the filename of the generated script and any comments
    """
    # Get the requirements and acceptance criteria from the state
    requirements = state.get("requirements", [])
    acceptance_criteria = state.get("acceptance_criteria", [])
    
    if not requirements and not acceptance_criteria:
        return {"script_filename": None, "script_comments": ""}
    
    # Initialize the LLM with structured output
    llm = ChatOpenAI(model="gpt-4o")
    structured_llm = llm.with_structured_output(WebsiteScript)
    
    # Create the prompt for generating the script
    system_prompt = """
    You are an expert Python web developer. Your task is to write a complete Python script 
    that fulfills the given requirements and acceptance criteria for a 1-page website.
    
    The script should:
    1. Use Flask as the web framework
    2. Include all HTML/CSS needed directly in the script
    3. Be completely self-contained in a single file
    4. Be ready to run immediately without any additional setup
    5. Listen on port 5000
    6. Include clear comments in the code
    
    Put ONLY the complete executable Python code in the script_code field.
    
    If you have any explanations, observations, or additional information about your implementation,
    put them in the comments field, NOT in the script_code. The script_code field should only contain
    valid Python code that can be executed without modification.
    """
    
    # Generate the script
    requirements_text = "\n".join([f"- {req}" for req in requirements])
    criteria_text = "\n".join([f"- {crit}" for crit in acceptance_criteria])
    
    user_prompt = f"""
    Generate a complete Python Flask script for a 1-page website based on the following:
    
    Requirements:
    {requirements_text}
    
    Acceptance Criteria:
    {criteria_text}
    
    The entire application must be in a single Python file that can be run directly.
    """
    
    result = structured_llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Save only the script code to a file
    script_filename = "generated_website.py"
    with open(script_filename, "w") as file:
        file.write(result.script_code)
    
    # Return the updated state with the script filename and any comments
    return {
        "script_filename": script_filename,
        "script_comments": result.comments
    } 