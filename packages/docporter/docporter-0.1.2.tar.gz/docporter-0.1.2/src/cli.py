import argparse
from .core import main as core_main

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
    docporter https://github.com/Aatitkarki/docporter.git
  
  Extract from local folder:
    docporter ./my-project --output ./docs

  Default output is [repo_name]-docs in current directory"""
    )
    parser.add_argument(
        "source",
        type=str,
        help="GitHub repository URL (https/ssh format) or path to local folder"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Custom output directory (default: [repo_name]-docs in current dir)"
    )
    
    args = parser.parse_args()
    core_main(args.source, args.output)
