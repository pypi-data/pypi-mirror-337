import argparse
from .core import main as core_main

def main():
    parser = argparse.ArgumentParser(
        description="Extract documentation files from a GitHub repository or local folder."
    )
    parser.add_argument(
        "source",
        type=str,
        help="URL of the GitHub repository or path to local folder containing documentation"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output directory for documentation files (default: [repo_name]-docs)"
    )
    
    args = parser.parse_args()
    core_main(args.source, args.output)