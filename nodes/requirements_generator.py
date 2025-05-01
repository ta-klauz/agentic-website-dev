from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

class WebsiteRequirements(BaseModel):
    requirements: List[str] = Field(description="List of specific, testable requirements for the website")
    acceptance_criteria: List[str] = Field(description="List of clear acceptance criteria for the website")

def execute(state):
    """
    This node accepts a short description for a 1-page website and generates
    requirements and acceptance criteria.
    
    Args:
        state: The current state containing a "description" field
        
    Returns:
        Updated state with requirements and acceptance criteria
    """
    # Get the website description from the state
    description = state.get("description", "")
    
    if not description:
        return {"requirements": [], "acceptance_criteria": []}
    
    # Initialize the LLM with structured output
    llm = ChatOpenAI(model="gpt-4o")
    structured_llm = llm.with_structured_output(WebsiteRequirements)
    
    # Generate requirements and acceptance criteria based on the description
    system_prompt = """
    You are an expert web developer and product manager. Your task is to convert a brief website 
    description into clear, specific requirements and acceptance criteria.
    
    Requirements should be specific, measurable, and focused on what the website must do.
    Acceptance criteria should be testable conditions that verify the website meets the requirements.
    
    Provide 5-10 requirements and corresponding acceptance criteria.
    """
    
    result = structured_llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create detailed requirements and acceptance criteria for a 1-page website with the following description: {description}"}
        ]
    )
    
    # Update the state with the generated requirements and acceptance criteria
    return {
        "requirements": result.requirements,
        "acceptance_criteria": result.acceptance_criteria
    } 