# Doc Porter

A Python package to extract documentation files from GitHub repositories and local folders.

## Features

- **GitHub Support**:

  - Clones repositories (shallow clone)
  - Handles various GitHub URL formats
  - Automatically cleans up after cloning

- **Local Folder Support**:

  - Processes documentation files from local directories
  - Validates path existence and permissions

- **Documentation Extraction**:

  - Recognizes .md, .mdx, .rst, .txt files
  - Automatically includes README files
  - Preserves directory structure in output

- **CLI Interface**:
  - Simple command-line usage
  - Custom output directory support
  - Help messages and error handling
  - Copies documentation in LLM ingestible format to clipboard

## Installation

Install directly from PyPI:

```bash
pip install docporter
```

Or install from source:

```bash
git clone https://github.com/aatitkarki/docporter
cd docporter
pip install .
```

## Usage

### Extract documentation from GitHub repository:

```bash
docporter extract https://github.com/aatitkarki/docporter.git -o ./output-docs
```

### Extract documentation from local folder:

```bash
docporter extract /path/to/local/docs -o ./output-docs
```

### Copy documentation in LLM ingestible xml format to clipboard:

```bash
docporter copy /path/to/local/docs
```

## Options

- `-o`, `--output`: Specify custom output directory (default: [repo_name]-docs)

## Examples

1.  Extract docs from GitHub with default output:

```bash
docporter extract https://github.com/user/repo.git
```

2.  Extract docs from local folder with custom output:

```bash
docporter extract ./my-docs -o ./extracted-docs
```

## Development

Run tests:

```bash
pytest
```

## License

MIT
