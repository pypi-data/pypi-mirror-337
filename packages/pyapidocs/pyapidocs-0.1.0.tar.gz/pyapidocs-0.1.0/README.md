# PyDoc

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Generating Documentation](#generating-documentation)
  - [Generating a Readme](#generating-a-readme)
- [Contributing](#contributing)
- [License](#license)

## Overview

PyDoc is a command-line tool designed to automatically generate API documentation and a project README file. It leverages the power of local large language models (LLMs) through the Ollama library to analyze your codebase and produce comprehensive documentation in Markdown format.

## Features

- **Automatic Documentation Generation:** PyDoc can generate API documentation for your code files, saving you time and effort.
- **README Creation:** It can also create a detailed README file for your project, including an overview, features, installation guide, and usage examples.
- **Customizable:** You can specify the language model to use, the file extension to target, and the directory to scan.
- **`.gitignore` Support:** PyDoc respects your `.gitignore` file, ensuring that excluded files are not included in the documentation process.
- **Markdown Output:** The generated documentation is in Markdown format, making it easy to read and integrate into your project.

## Installation

1.  **Install Ollama:** Follow the instructions on the [Ollama website](https://ollama.com/) to install Ollama on your system.
2.  **Install PyDoc:**
    ```bash
    pip install pydoc
    ```

## Usage

### Generating Documentation

To generate API documentation for your project, use the following command:

```bash
pydoc -m <model_name> -e <file_extension> -d <directory> -f <filepath> -i <ignore_path>
```

- `<model_name>`: The name of the Ollama model you want to use (e.g., `llama2`, `mistral`).
- `<file_extension>`: The file extension of the files you want to document (e.g., `py`, `js`).
- `<directory>`: (Optional) The directory to recursively scan for files. If not specified, the current working directory is used, supports multiple paths
- `<file>`: (Optional) The files to generate api documentation for, supports multiple files
- `<ignore>`: (Optional) The directories or files to ignore, supports multiple paths

**Example:**

```bash
pydoc -m llama2 -e py -d src
```
