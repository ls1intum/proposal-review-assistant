# Proposal Review Assistant

A tool for academic proposal review and feedback generation using Large Language Models.

## Features

- Automatically analyzes proposal sections (abstract, introduction, problem statement, etc.)
- Provides two types of feedback:
  - Detailed natural language feedback on writing and content
  - Structured feedback with specific issues and suggestions
- Generates a comprehensive summary with key issues and improvement recommendations
- Web-based interface using Gradio for easy proposal upload and feedback review
- Outputs both human-readable Markdown and structured JSON
- Works with PDF proposal documents

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/proposal-assistance.git
cd proposal-assistance
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Set up your environment variables:
```bash
# Copy the example environment file
cp .env.example .env
# Edit with your preferred editor
nano .env  # or vim, VS Code, etc.
```

The project uses a flexible model provider system supporting OpenAI, Azure OpenAI, and Ollama.

## Usage

### Web Interface (Gradio)

The easiest way to use the tool is through the web interface:

```bash
poetry run app
```

This will start a Gradio web application accessible at `http://127.0.0.1:7860`. From there, you can:

1. Upload your proposal PDF
2. View generated feedback in the interface
3. Download structured feedback as JSON or text
4. Copy feedback directly from the interface

If you've set `PLAYGROUND_USERNAME` and `PLAYGROUND_PASSWORD` in your environment, the interface will be password protected.

### Docker Support

You can also run the application using Docker:

```bash
docker compose -f docker/compose.app.yaml up
```

The output will include:
- Detailed feedback on each proposal section
- Structured feedback with specific issues and suggestions
- Priority-based organization of feedback items
- Recommendations for improvement

## Project Structure

- `app/`: Main package containing the application
  - `main.py`: Gradio web interface implementation
  - `pdf_converter.py`: PDF processing and text extraction
  - `settings.py`: Configuration and environment variables
  - `models/`: LLM integration (OpenAI, Azure OpenAI, Ollama)
  - `prompts/`: Directory containing section-specific prompt templates
- `docker/`: Docker configuration files
- `pyproject.toml`: Poetry project definition and dependencies

## Advanced Usage

You can extend the functionality by:

- Creating custom prompt templates for specialized domains
- Adding new section analyzers in the `prompts/` directory
- Integrating alternative LLM providers by extending the models in `app/models/`
- Customizing the feedback display in the Gradio interface
- Setting up Langfuse for tracking and analyzing feedback generations

## Environment Variables

The project supports multiple LLM providers through a flexible configuration system. You can find examples in the `.env.example` file:

### Authentication

- `PLAYGROUND_USERNAME`, `PLAYGROUND_PASSWORD`: Optional credentials for the Gradio interface

### Model Configuration

- `MODEL_NAME`: Main model for proposal analysis (e.g., "azure_openai:o3-mini")
- `IMAGE_MODEL_NAME`: Model for processing figures/diagrams (e.g., "azure_openai:gpt-4o")
- `FORMAT_MODEL_NAME`: Model for formatting output (e.g., "azure_openai:gpt-41-mini")

### OpenAI Configuration

- `OPENAI_API_KEY`: Your OpenAI API key

### Azure OpenAI Configuration

- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `OPENAI_API_VERSION`: API version for Azure OpenAI

### Ollama Configuration

- `OLLAMA_HOST`: Host address for Ollama
- `OLLAMA_BASIC_AUTH_USERNAME`, `OLLAMA_BASIC_AUTH_PASSWORD`: Optional Ollama authentication

### Observability

- `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`: Langfuse configuration for tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License 