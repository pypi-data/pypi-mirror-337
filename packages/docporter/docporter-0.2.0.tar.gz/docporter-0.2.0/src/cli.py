import argparse
from .core import extract_docs, copy_llm_format

def main():
    parser = argparse.ArgumentParser(
        description="""Documentation Extractor Tool

Extracts documentation files from GitHub repositories or local folders. Supports:
- README files (any case)
- Markdown (.md, .mdx)
- reStructuredText (.rst)
- Plain text (.txt)""",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  Extract from GitHub repo:
    docporter extract https://github.com/Aatitkarki/docporter.git -o ./output-docs
  
  Extract from local folder:
    docporter extract ./my-project --output ./docs

  Default output is [repo_name]-docs in current directory"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # Extract subcommand
    extract_parser = subparsers.add_parser("extract", help="Extract documentation files")
    extract_parser.add_argument(
        "source",
        type=str,
        help="GitHub repository URL (https/ssh format) or path to local folder"
    )
    extract_parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Custom output directory (default: [repo_name]-docs in current dir)"
    )

    # Copy subcommand
    copy_parser = subparsers.add_parser("copy", help="Copy documentation in LLM ingestible format to clipboard")
    copy_parser.add_argument(
        "source",
        type=str,
        help="GitHub repository URL (https/ssh format) or path to local folder"
    )
    
    args = parser.parse_args()

    if args.command == "extract":
        extract_docs(args.source, args.output)
    elif args.command == "copy":
        copy_llm_format(args.source)
