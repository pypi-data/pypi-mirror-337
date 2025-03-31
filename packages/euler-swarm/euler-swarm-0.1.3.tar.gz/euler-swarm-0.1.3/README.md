# euler-swarm

A tool for building dependency graphs and generating code documentation using an agent.

## Installation

Install via pip (after publishing to PyPI) or locally:

```bash
pip install euler
```

## Usage

Before running, set your OpenAI API key as an environment variable:

```bash
set OPENAI_API_KEY=your_openai_api_key   # on Windows
export OPENAI_API_KEY=your_openai_api_key  # on macOS/Linux
```

Then run the tool:

```bash
euler-swarm
```

This will execute the main function in `main.py` and run the magic!