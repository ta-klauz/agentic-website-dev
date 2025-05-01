from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import json
import os

from pydantic import BaseModel, Field


class Output(BaseModel):
    edited_code: str = Field(description="The edited code that fixes the bug")
    comments: str = Field(description="Any additional comments about the code")
	



def read_file_to_string(filename):
    try:
        with open(filename, "r") as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def write_string_to_file(content, output_filename):
    try:
        with open(output_filename, "w") as file:
            file.write(content)
        print(f"Content successfully written to {output_filename}")
        return True
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False



system_prompt = """You are an expert coder who helps to fix bugs in code.

You will be provided with a code snippet and the results of user testing, where the code has failed to meet the acceptance criteria.

You will need to fix the code so that it meets the acceptance criteria.

You will also be provided with the expected acceptance criterion.

You will be provided with pairs of <Expected Acceptance Criterion, Feedback>, one pair at a time.

"""


llm = ChatOpenAI(model="o3-mini")
structured_llm  = llm.with_structured_output(Output)

def get_messages_info(messages):
    return [SystemMessage(content=system_prompt)] + messages

debug_value = None


def execute(state):
    # Get the script filename from the state
    script_filename = state.get("script_filename", "generated_website.py")
    
    # Generate output filename by adding "_fixed" before the extension
    base_name, ext = os.path.splitext(script_filename)
    output_filename = f"{base_name}_fixed{ext}"

    code_as_string = read_file_to_string(script_filename)

    all_feedback = state["test_results"][-1]

    messages = get_messages_info([])

    messages.append(HumanMessage(content=f"Code: {code_as_string}"))

    edited_code = code_as_string

    for feedback in all_feedback:
        result = feedback["result"]
                
        if not result["isCriterionMet"]:
        
            messages.append(HumanMessage(content=feedback["feedback_message"]))

            llm_response = structured_llm.invoke(messages)

            print(llm_response)

            response = AIMessage(content=f"Here's the latest code:{llm_response.edited_code}")

            edited_code = llm_response.edited_code

            messages.append(response)

    write_string_to_file(edited_code, output_filename)

    # Update the script_filename in the state to use the fixed version
    return {"script_filename": output_filename}