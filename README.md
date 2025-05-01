# Agentic Website Development System

An AI-powered system for automatically generating and testing 1-page websites based on simple descriptions.

## Overview

This system uses large language models (LLMs) and browser automation to:
1. Generate detailed requirements and acceptance criteria from a simple description
2. Create a complete Flask website implementation based on those requirements
3. Test the website against the acceptance criteria using browser automation
4. Iteratively improve the website until all criteria are met

The system uses a directed graph-based workflow to manage the process, with nodes for requirements generation, script generation, testing, and code editing.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ta-klauz/agentic-website-dev.git
cd agentic-website-dev
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers
```bash
playwright install
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

5. Enable LangSmith tracing (optional but recommended):
```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="<your-langsmith-api-key>"
```
For detailed LangSmith setup instructions, visit the [LangSmith documentation](https://docs.smith.langchain.com/).

## Usage

### Basic Usage

Run the main script with a description of the website you want to create:

```bash
python main.py --description "Create a landing page for a coffee shop with a menu, about section, and contact form"
```

This will generate a complete Flask website with HTML, CSS, and JavaScript, and test it against the automatically generated requirements.

### Running Examples

Example usage is provided in the `examples` directory:

```bash
python examples/simple_website_generation.py
```

## Key Components

- `main.py`: Main entry point for website generation
- `examples/`: Contains example scripts showing how to use the system
- `nodes/`: Individual workflow components (requirements generation, script generation, testing, code editing)

## How It Works

The graph-based workflow consists of the following steps, which are implemented as Langgraph nodes:
1. **Requirements Generation**: Converts a brief description into detailed requirements and acceptance criteria
2. **Script Generation**: Creates a 1-page Flask website implementation
3. **Testing**: Uses browser automation to test the website against each acceptance criteria
4. **Code Editing**: Fixes any issues identified during testing
Steps 3-4 are repeated until all criteria are met or maximum iterations are reached

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Best Practices

When using this system, follow these security guidelines to protect sensitive data and ensure safe execution:

### API Key Management
1. **Never hardcode API keys** in scripts or commit them to version control.
2. Use environment variables to store your API keys:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
3. For production, use secure secret management tools.

### Execution Environment
1. **Run in a sandboxed environment** when possible to isolate the system.
2. Use virtual environments to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```
## Acknowledgments

- LangChain for the LLM integration framework
- LangGraph for the workflow graph structure
- browser_use package for browser automation 