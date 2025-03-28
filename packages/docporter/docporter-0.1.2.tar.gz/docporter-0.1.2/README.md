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

### From GitHub repository:

```bash
doc-porter https://github.com/user/repo.git -o ./output-docs
```

### From local folder:

```bash
doc-porter /path/to/local/docs -o ./output-docs
```

## Options

- `-o`, `--output`: Specify custom output directory (default: [repo_name]-docs)

## Examples

1. Extract docs from GitHub with default output:

```bash
doc-porter https://github.com/user/repo.git
```

2. Extract docs from local folder with custom output:

```bash
doc-porter ./my-docs -o ./extracted-docs
```

## Development

Run tests:

```bash
pytest
```

## License

MIT
