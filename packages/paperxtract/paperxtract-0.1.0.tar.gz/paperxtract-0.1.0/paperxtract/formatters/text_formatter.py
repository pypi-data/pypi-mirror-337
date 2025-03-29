"""
Paper Text Formatter

Module for converting paper data into text format
"""

import json
import csv
import os
import re
from typing import List, Dict, Union, Optional


class PaperFormatter:
    """
    Paper Formatter Class
    
    Provides functionality to convert paper data into different formats
    """
    
    def __init__(self, input_file: str):
        """
        Initialize the paper formatter
        
        Args:
            input_file: Input file path (JSON or CSV format)
        """
        self.input_file = input_file
        self.papers = self._load_papers()
        
    def _load_papers(self) -> List[Dict]:
        """
        Load paper data based on file extension
        
        Returns:
            List of paper data
        """
        file_ext = os.path.splitext(self.input_file)[1].lower()
        
        if file_ext == '.json':
            return self._load_from_json()
        elif file_ext == '.csv':
            return self._load_from_csv()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Please provide a JSON or CSV file.")
    
    def _load_from_json(self) -> List[Dict]:
        """
        Load paper data from JSON file
        
        Returns:
            List of paper data
        """
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Error loading JSON file: {str(e)}")
    
    def _load_from_csv(self) -> List[Dict]:
        """
        Load paper data from CSV file
        
        Returns:
            List of paper data
        """
        try:
            papers = []
            with open(self.input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Special handling for list fields in CSV
                    if 'keywords' in row and isinstance(row['keywords'], str):
                        try:
                            # Try to convert string to list
                            row['keywords'] = eval(row['keywords'])
                        except:
                            # If failed, split by comma
                            row['keywords'] = [k.strip() for k in row['keywords'].split(',')]
                    
                    if 'authors' in row and isinstance(row['authors'], str):
                        try:
                            row['authors'] = eval(row['authors'])
                        except:
                            row['authors'] = [a.strip() for a in row['authors'].split(',')]
                    
                    papers.append(row)
            return papers
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
    
    def filter_papers_by_category(self, categories: Union[str, List[str]]) -> List[Dict]:
        """
        Filter papers by category
        
        Args:
            categories: Single category or list of categories (e.g., 'oral', ['oral', 'spotlight'])
            
        Returns:
            Filtered list of papers
        """
        if isinstance(categories, str):
            categories = [categories.lower()]
        else:
            categories = [c.lower() for c in categories]
        
        filtered_papers = []
        for paper in self.papers:
            paper_category = paper.get('category', '').lower()
            if paper_category in categories:
                filtered_papers.append(paper)
        
        return filtered_papers
    
    def _extract_conference_info(self) -> Dict:
        """
        Extract conference information from paper data
        
        Returns:
            Conference information dictionary
        """
        # Default values
        conference_info = {
            'name': 'Unknown Conference',
            'year': '',
            'total_papers': len(self.papers)
        }
        
        # Try to extract conference information from papers
        if self.papers:
            # Try to extract conference name and year from the first paper's venue
            venue = self.papers[0].get('forum_link', '')
            venue_match = re.search(r'openreview\.net/group\?id=([^/&#]+)', venue)
            if venue_match:
                conference_id = venue_match.group(1)
                parts = conference_id.split('.')
                if len(parts) >= 2:
                    conference_info['name'] = parts[0]
            
            # Extract year from year field
            year = self.papers[0].get('year', '')
            if year:
                conference_info['year'] = year
        
        return conference_info
    
    def format_papers_to_txt(self, output_file: str, categories: Optional[Union[str, List[str]]] = None) -> None:
        """
        Format papers to TXT file
        
        Args:
            output_file: Output TXT file path
            categories: Optional category filter
        """
        # If category is specified, filter papers first
        papers_to_format = self.papers
        if categories:
            papers_to_format = self.filter_papers_by_category(categories)
            
        # Extract conference information
        conference_info = self._extract_conference_info()
        
        # Format and write to TXT file
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write conference information
            header = f"{conference_info['name']}.{conference_info['year']} - Accept\n"
            header += f"   | Total: {len(papers_to_format)}\n\n"
            f.write(header)
            
            # Write each paper's information
            for i, paper in enumerate(papers_to_format, 1):
                # Title
                title = paper.get('title', 'Untitled Paper')
                f.write(f"#{i} {title}\n")
                
                # Authors
                authors = paper.get('authors', [])
                if authors:
                    authors_str = ', '.join(authors)
                    f.write(f"Authors: {authors_str}\n")
                
                # Keywords
                keywords = paper.get('keywords', [])
                if keywords:
                    if isinstance(keywords, list):
                        keywords_str = ', '.join(keywords)
                    else:
                        keywords_str = keywords
                    f.write(f"Keywords: {keywords_str}\n")
                
                # Abstract
                abstract = paper.get('abstract', '')
                if abstract:
                    f.write(f"Abstract: {abstract}\n")
                
                # Space between papers
                f.write("\n")
    
    @staticmethod
    def get_available_categories(input_file: str) -> List[str]:
        """
        Get all available paper categories in the input file
        
        Args:
            input_file: Input file path (JSON or CSV)
            
        Returns:
            List of available categories
        """
        formatter = PaperFormatter(input_file)
        categories = set()
        
        for paper in formatter.papers:
            category = paper.get('category')
            if category:
                categories.add(category)
        
        return sorted(list(categories))


def convert_papers_to_txt(input_file: str, output_file: str, categories: Optional[Union[str, List[str]]] = None) -> None:
    """
    Convert paper data to TXT format
    
    Args:
        input_file: Input file path (JSON or CSV)
        output_file: Output TXT file path
        categories: Optional category filter
    """
    formatter = PaperFormatter(input_file)
    formatter.format_papers_to_txt(output_file, categories)
    print(f"Paper data has been converted to TXT format and saved to: {output_file}")
    
    # Display category statistics
    if categories:
        if isinstance(categories, str):
            categories = [categories]
        filtered_papers = formatter.filter_papers_by_category(categories)
        print(f"Filtered {len(filtered_papers)} papers (categories: {', '.join(categories)})")
    else:
        print(f"Processed {len(formatter.papers)} papers (all categories)") 