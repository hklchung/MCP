# MCP Demo

This project demonstrates a simple multi-agent workflow for generating marketing blog posts.
It uses Streamlit for a minimal interface and OpenAI LLMs for text generation.

## Requirements
- Python 3.11+
- [Poetry](https://python-poetry.org/)
- [Pre-commit](https://pre-commit.com/)

## Setup
1. Install dependencies:
   ```bash
   poetry install
   ```
2. Copy `.env.example` to `.env` and add your OpenAI API key.
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```
4. Run the application:
   ```bash
   PYTHONPATH=src poetry run streamlit run src/streamlit_app.py --server.port 8000
   ```

## Docker
To build and run using Docker:
```bash
docker build -t mcp-demo .
docker run -p 8000:8000 --env OPENAI_API_KEY=your-key mcp-demo
```

## Usage
Open `http://localhost:8000` in your browser. Submit a brief, choose the desired
OpenAI model, and review the generated draft. Guardrails can be edited on the
"Edit Guardrails" page.
