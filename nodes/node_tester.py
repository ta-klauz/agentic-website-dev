from langchain_openai import ChatOpenAI
from langsmith import tracing_context
from browser_use import Agent, BrowserConfig, Browser
from browser_use import Controller
from pydantic import BaseModel, Field
import asyncio
import json
import subprocess
import time
import socket
import traceback
from typing import Literal
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END


class AcceptanceCriterion(BaseModel):
	isCriterionMet: bool = Field(description="True if the acceptance criterion was met. False if it was not met")
	comments: str = Field(description="Any additional comments about the test results")
	isTestBlocked: bool = Field(description="True if the test was blocked from completing. For example, if a website/browser was not available, stuck on a CAPTCHA, the test was blocked by a firewall etc..")


browser = Browser(
    config=BrowserConfig(
        headless=True,
    )
)

def wait_for_server(port, process, timeout=10.0):
    """Waits for a server to become available at localhost:port within 'timeout' seconds.
    Also checks if the process has exited with an error."""
    endtime = time.time() + timeout
    error_output = None
    
    while time.time() < endtime:
        # Check if process has exited with an error
        if process.poll() is not None:
            # Process ended - get error output
            stdout, stderr = process.communicate()
            error_output = stderr.decode('utf-8') if stderr else (stdout.decode('utf-8') if stdout else "Unknown error")
            return False, error_output
            
        try:
            # Try to establish a connection to the server
            s = socket.create_connection(('localhost', port), timeout=1)
            s.close()
            return True, None
        except OSError:
            time.sleep(0.1) # wait a bit before trying again
    
    # Timeout reached, check if process is still running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        error_output = stderr.decode('utf-8') if stderr else (stdout.decode('utf-8') if stdout else "Unknown error")
    
    return False, error_output or "Server did not respond within timeout period"

def terminate_process(process, timeout=3):
    """Safely terminates a process with timeout."""
    if process.poll() is None:  # Process is still running
        process.terminate()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

async def main(state):

    async with await browser.new_context() as context:
        
        try:

            with tracing_context(enable=False):

                controller = Controller(output_model=AcceptanceCriterion)

                agent_output = []

                for i, criterion in enumerate(state["acceptance_criteria"]):
                    agent = Agent(
                        # browser=browser,
                        browser_context=context,
                        task= f'Go to localhost:5000 and check the following acceptance criterion for the website - "{criterion}"',
                        llm=ChatOpenAI(model="gpt-4o"),
                        controller=controller,
                        use_vision=False,
                    )

                    agent_result = await agent.run(max_steps=5)

                  
                    # Only store the final result of the agent run
                    agent_output.append({
                        "result": json.loads(agent_result.final_result()),
                        "feedback_message": f'Expected acceptance criterion: "{criterion}"\n\nFeedback: "{json.loads(agent_result.final_result())["comments"]}"'
                    })


        finally:
            await browser.close()

        return agent_output


def execute(state):
    # Get the script filename from the state, default to "generated_website.py" if not found
    script_filename = state.get("script_filename", "generated_website.py")
    
    # Get current iteration count
    iteration_count = state.get("iteration_count", 0)
    # Increment counter for this execution
    new_iteration_count = iteration_count + 1
    MAX_ITERATIONS = 3  # Maximum number of coder-tester iterations allowed
    
    server_process = None
    try:
        # Start the server with the generated script and capture stdout/stderr
        server_process = subprocess.Popen(
            ['python', script_filename], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False
        )

        server_up, error_message = wait_for_server(5000, server_process)
        if server_up:
            print("Server is up. Executing the rest of the script.")
            result = asyncio.run(main(state))
            
            # Check if all criteria are met
            all_criteria_met = True
            for test in result:
                if not test["result"]["isCriterionMet"]:
                    all_criteria_met = False
                    break
            
            # Determine whether to end or continue based on criteria and iteration count
            if all_criteria_met or new_iteration_count >= MAX_ITERATIONS:
                # End the loop if criteria met or max iterations reached
                reason = "All criteria met!" if all_criteria_met else f"Max iterations ({MAX_ITERATIONS}) reached!"
                print(f"{reason} Ending after {new_iteration_count} iterations.")
                
                return Command(
                    update={
                        "test_results": [result],
                        "iteration_count": new_iteration_count
                    },
                    goto=END
                )
            else:
                # Continue the loop
                print(f"Criteria not met. Starting iteration {new_iteration_count} of {MAX_ITERATIONS}...")
                return Command(
                    update={
                        "test_results": [result],
                        "iteration_count": new_iteration_count
                    },
                    goto="code_editor"
                )
        else:
            print(f"Server failed to start: {error_message}")
            # Create a single simulated failed test output with the actual error
            simulated_output = [{
                "result": {
                    "isCriterionMet": False,
                    "comments": error_message,
                    "isTestBlocked": True
                },
                "feedback_message": f"Test blocked: Server failed to start. Error: {error_message}"
            }]
            
            # End if max iterations reached, otherwise continue to code editor
            if new_iteration_count >= MAX_ITERATIONS:
                print(f"Max iterations ({MAX_ITERATIONS}) reached! Ending despite server failure.")
                return Command(
                    update={
                        "test_results": [simulated_output],
                        "iteration_count": new_iteration_count
                    },
                    goto=END
                )
            else:
                print(f"Server failed. Starting iteration {new_iteration_count} of {MAX_ITERATIONS}...")
                return Command(
                    update={
                        "test_results": [simulated_output],
                        "iteration_count": new_iteration_count
                    },
                    goto="code_editor"
                )
    finally:
        if server_process:
            terminate_process(server_process)
            print("Server process terminated.")

