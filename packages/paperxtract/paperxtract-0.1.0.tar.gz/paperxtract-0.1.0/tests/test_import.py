"""
Simple import test
"""

def test_import():
    """Test if key modules can be correctly imported"""
    try:
        from paperxtract import OpenReviewExtractor, PaperFormatter, convert_papers_to_txt
        from paperxtract.extractors.openreview import OpenReviewExtractor
        from paperxtract.formatters.text_formatter import PaperFormatter, convert_papers_to_txt
        from paperxtract.cli import main
        print("All modules imported successfully!")
        return True
    except ImportError as e:
        print(f"Import failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_import() 