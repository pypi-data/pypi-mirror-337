# kopipasta

[![Version](https://img.shields.io/pypi/v/kopipasta.svg)](https://pypi.python.org/pypi/kopipasta)
[![Downloads](http://pepy.tech/badge/kopipasta)](http://pepy.tech/project/kopipasta)

Beyond TAB TAB TAB. Giving you full control of the context.

A CLI tool for generating code task prompts with project structure and file contents, using an interactive editor-based workflow. OR a very easy way to give a large context to an LLM.

<img src="kopipasta.jpg" alt="kopipasta" width="300">

- An LLM told me that kopi means Coffee in some languages.. and a Diffusion model then made this delicious soup.

## Installation

You can install kopipasta using pipx (or pip):

```bash
pipx install kopipasta
```

## Usage

To use kopipasta, run the following command in your terminal:

```bash
kopipasta [files_or_directories_or_urls]
```

Replace `[files_or_directories_or_urls]` with the paths to the files or directories you want to include in the prompt, as well as any web URLs you want to fetch content from.

Example input:
```bash
kopipasta src/ config.json https://example.com/api-docs
```

This will guide you through an interactive process to:
1. Select files and directories to include in the prompt
2. Choose between full content, snippets, or patches for large files
3. Fetch and include content from provided URLs
4. Open an editor for you to input the specific task or code generation instructions
5. Generate a comprehensive prompt that includes project structure, selected file contents, and your task instructions

The generated prompt will be displayed in the console and automatically copied to your clipboard, ready to be used with an AI code generation tool.

## Features

- Generates structured prompts with project overview, file contents, web content, and task instructions
- Interactive file selection process with options for full content, snippets, or specific patches
- Fetches and includes content from web URLs
- Opens your preferred editor (configurable via EDITOR environment variable) for task input
- Detects and securely handles environment variables from a `.env` file
- Ignores files and directories based on common .gitignore patterns
- Allows interactive selection of files to include
- Supports various file types with syntax highlighting in the selection process
- Automatically copies the generated prompt to the clipboard

## Real life example

Context:
I had a bug that setup.py did not have all the dependencies. I wanted to make things easier:

1. `kopipasta -t "setup.py should take requirements from requirements.txt" requirements.txt setup.py`
2. Opened the service that provides the best LLM currently.
3. Pasted the prompt to their chat.
4. Reviewed the first message and typed "Proceed".
5. Got back the code that fixed the issue.


