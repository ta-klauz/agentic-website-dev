"""
Example of generating a simple website using the agentic website development system.
"""
import sys
import os

# Add parent directory to path for importing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

if __name__ == "__main__":
    # Example website description
    description = "Create a portfolio website for a photographer with a gallery section, about page, and contact form."
    
    # Run the website generation workflow
    result = main(description)
    
    # Access the final state
    print("\nGeneration complete!")
    print(f"Final script: {result.get('script_filename', 'No script generated')}")
    print(f"Iterations: {result.get('iteration_count', 0)}")
    
    if result.get('test_results'):
        print("\nTest Results:")
        test_results = result['test_results'][-1]
        passed = sum(1 for test in test_results if test['result']['isCriterionMet'])
        total = len(test_results)
        print(f"Passed: {passed}/{total} criteria") 