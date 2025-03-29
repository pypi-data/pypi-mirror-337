"""
Command Line Interface

Provides command-line tool functionality for PaperXtract
"""

import argparse
import sys
import os
from typing import List, Optional

from paperxtract.extractors.openreview import OpenReviewExtractor
from paperxtract.formatters.text_formatter import convert_papers_to_txt, PaperFormatter


def extract_command(args):
    """
    Handle paper extraction command
    
    Args:
        args: Command-line arguments
    """
    try:
        extractor = OpenReviewExtractor(username=args.username, password=args.password)
        
        if args.url:
            print(f"Extracting papers from URL: {args.url}")
            papers = extractor.get_papers_from_url(args.url)
        elif args.venue_id:
            print(f"Extracting papers from conference ID: {args.venue_id}")
            papers = extractor.get_papers_from_venue(args.venue_id, args.category)
        else:
            print("Error: Must provide URL or conference ID")
            return 1
        
        # Save extraction results
        if args.output_format.lower() == 'json':
            output_file = args.output or f"{os.path.splitext(os.path.basename(args.url or args.venue_id))[0]}_papers.json"
            extractor.save_to_json(papers, output_file)
        else:
            output_file = args.output or f"{os.path.splitext(os.path.basename(args.url or args.venue_id))[0]}_papers.csv"
            extractor.save_to_csv(papers, output_file)
        
        print(f"Successfully extracted {len(papers)} papers, saved to: {output_file}")
        return 0
    except Exception as e:
        print(f"Error extracting papers: {str(e)}")
        return 1


def format_command(args):
    """
    Handle paper formatting command
    
    Args:
        args: Command-line arguments
    """
    try:
        if args.list_categories:
            categories = PaperFormatter.get_available_categories(args.input_file)
            print(f"Available categories: {', '.join(categories)}")
            return 0
        
        output_file = args.output or f"{os.path.splitext(args.input_file)[0]}.txt"
        convert_papers_to_txt(args.input_file, output_file, args.categories)
        return 0
    except Exception as e:
        print(f"Error formatting papers: {str(e)}")
        return 1


def pipeline_command(args):
    """
    Handle one-step extraction and formatting command
    
    Args:
        args: Command-line arguments
    """
    try:
        # Step 1: Extract papers
        extractor = OpenReviewExtractor(username=args.username, password=args.password)
        
        if args.url:
            print(f"Extracting papers from URL: {args.url}")
            papers = extractor.get_papers_from_url(args.url)
        elif args.venue_id:
            print(f"Extracting papers from conference ID: {args.venue_id}")
            papers = extractor.get_papers_from_venue(args.venue_id, args.category)
        else:
            print("Error: Must provide URL or conference ID")
            return 1
        
        # Save intermediate results
        temp_json = f"{os.path.splitext(args.output)[0]}_temp.json"
        extractor.save_to_json(papers, temp_json)
        print(f"Extracted {len(papers)} papers")
        
        # Step 2: Format papers
        convert_papers_to_txt(temp_json, args.output, args.categories)
        
        # Clean up temporary files
        if args.clean_temp:
            os.remove(temp_json)
            print("Deleted temporary JSON file")
        
        return 0
    except Exception as e:
        print(f"Error processing papers: {str(e)}")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main function for the command-line tool
    
    Args:
        argv: Command-line argument list, defaults to None (uses sys.argv)
        
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="PaperXtract - Paper Extraction and Formatting Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract papers from academic platforms")
    extract_parser.add_argument("--url", help="OpenReview web URL")
    extract_parser.add_argument("--venue-id", help="Conference ID")
    extract_parser.add_argument("--category", help="Paper category (e.g., oral, spotlight, poster)")
    extract_parser.add_argument("--username", help="OpenReview username")
    extract_parser.add_argument("--password", help="OpenReview password")
    extract_parser.add_argument("--output", "-o", help="Output file path")
    extract_parser.add_argument("--output-format", choices=["json", "csv"], default="json", help="Output format (default: json)")
    
    # Format command
    format_parser = subparsers.add_parser("format", help="Format paper data to TXT format")
    format_parser.add_argument("input_file", help="Input file path (JSON or CSV)")
    format_parser.add_argument("--output", "-o", help="Output TXT file path")
    format_parser.add_argument("--categories", nargs="+", help="Filter papers by category (e.g., oral spotlight)")
    format_parser.add_argument("--list-categories", action="store_true", help="List all available categories in the input file")
    
    # Pipeline command
    pipeline_parser = subparsers.add_parser("run", help="One-step extraction and formatting of papers")
    pipeline_parser.add_argument("--url", help="OpenReview web URL")
    pipeline_parser.add_argument("--venue-id", help="Conference ID")
    pipeline_parser.add_argument("--category", help="Paper category (e.g., oral, spotlight, poster)")
    pipeline_parser.add_argument("--username", help="OpenReview username")
    pipeline_parser.add_argument("--password", help="OpenReview password")
    pipeline_parser.add_argument("--output", "-o", required=True, help="Output TXT file path")
    pipeline_parser.add_argument("--categories", nargs="+", help="Filter papers by category (e.g., oral spotlight)")
    pipeline_parser.add_argument("--clean-temp", action="store_true", help="Delete temporary JSON file")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Display version information")
    
    args = parser.parse_args(argv)
    
    if args.command == "extract":
        return extract_command(args)
    elif args.command == "format":
        return format_command(args)
    elif args.command == "run":
        return pipeline_command(args)
    elif args.command == "version":
        from paperxtract import __version__
        print(f"PaperXtract v{__version__}")
        return 0
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main()) 