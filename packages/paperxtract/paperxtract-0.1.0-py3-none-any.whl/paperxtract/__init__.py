"""
PaperXtract - Paper Extraction and Formatting Tool

A toolkit for extracting paper information from academic platforms and formatting them
"""

__version__ = "0.1.0"

from paperxtract.extractors.openreview import OpenReviewExtractor
from paperxtract.formatters.text_formatter import PaperFormatter, convert_papers_to_txt

__all__ = [
    'OpenReviewExtractor',
    'PaperFormatter',
    'convert_papers_to_txt'
] 