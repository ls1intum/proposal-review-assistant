# Proposal Review Assistant

A tool for academic proposal review and feedback generation using Large Language Models.

## Features

- Automatically analyzes proposal sections (abstract, introduction, problem statement, etc.)
- Provides two types of feedback:
  - Detailed natural language feedback on writing and content
  - Structured feedback with specific issues and suggestions
- Generates a comprehensive summary with key issues and improvement recommendations
- Simple command-line interface for easy use
- Outputs both human-readable Markdown and structured JSON
- Works with PDF proposal documents

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/proposal-assistance.git
cd proposal-assistance
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Command-Line Interface

The simplest way to use the tool is through the command-line interface:

```bash
python review_proposal.py path/to/your/proposal.pdf --output review_results.md --json-output feedback.json
```

Options:
- `--output`, `-o`: Path to save the review results as Markdown (default: review_results.md)
- `--json-output`: Path to save structured feedback as JSON (default: output/feedback.json)
- `--model`: OpenAI model to use (default: gpt-3.5-turbo, options: o4-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo)
- `--verbose`, `-v`: Show detailed progress

### Example

```bash
python review_proposal.py input/your_proposal.pdf --verbose
```

The output will include:
- Detailed feedback on each section
- Structured feedback with specific issues and suggestions
- An overall assessment with key strengths and weaknesses
- Recommendations for improvement

## Project Structure

- `proposal_reviewer/`: Main package containing proposal review functionality
  - `simple_reviewer.py`: Core reviewer implementation
- `review_proposal.py`: Command-line interface
- `prompts/`: Directory containing section-specific prompt templates
- `requirements.txt`: Required dependencies

## Advanced Usage

You can extend the functionality by:
- Adding custom section extraction patterns for different proposal formats
- Implementing custom feedback strategies for specific domains
- Integrating with other PDF processing tools for improved text extraction

## License

MIT License 