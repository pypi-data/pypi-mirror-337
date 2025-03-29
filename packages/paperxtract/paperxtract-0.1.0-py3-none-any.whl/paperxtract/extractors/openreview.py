"""
OpenReview Paper Extractor

Module for extracting academic paper information from the OpenReview platform
"""

import openreview
import re
import json
import pandas as pd
from typing import Dict, List, Union, Optional
from urllib.parse import urlparse, parse_qs
from datetime import datetime


class OpenReviewExtractor:
    """
    OpenReview Paper Extractor Class
    
    Provides functionality to extract paper information from the OpenReview platform
    """
    
    def __init__(self, username=None, password=None):
        """
        Initialize the OpenReview paper extractor
        
        Args:
            username: OpenReview username (optional)
            password: OpenReview password (optional)
        """
        self.client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=username,
            password=password
        )
        
    def extract_venue_id_from_url(self, url: str) -> str:
        """
        Extract conference ID from an OpenReview URL
        
        Args:
            url: OpenReview web URL
            
        Returns:
            Conference ID string
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        if 'id' in query_params:
            venue_id = query_params['id'][0]
            return venue_id
        
        # Try to extract conference ID from URL path
        match = re.search(r'group\?id=([^&#]+)', url)
        if match:
            return match.group(1)
            
        raise ValueError("Unable to extract conference ID from the provided URL")
    
    def extract_paper_category_from_url(self, url: str) -> Optional[str]:
        """
        Extract paper category (e.g., oral, spotlight, poster) from URL
        
        Args:
            url: OpenReview web URL
            
        Returns:
            Paper category or None
        """
        match = re.search(r'#tab-([^&#]+)', url)
        if match:
            category = match.group(1)
            # Handle common category names
            if 'accept' in category:
                parts = category.split('-')
                if len(parts) > 1:
                    return parts[1]  # For example, accept-oral returns oral
                return 'accepted'
            return category
        return None
    
    def get_accepted_papers(self, venue_id: str, category: Optional[str] = None) -> List[Dict]:
        """
        Get accepted papers for a specific conference
        
        Args:
            venue_id: Conference ID
            category: Paper category (e.g., oral, spotlight, poster)
            
        Returns:
            List of paper information
        """
        try:
            # Get conference group information
            venue_group = self.client.get_group(venue_id)
            
            # Get only accepted papers
            # Directly use venueid field to filter papers for the specified conference
            accepted_papers = self.client.get_all_notes(content={'venueid': venue_id})
            
            # If no papers found, try alternative query methods based on conference structure
            if not accepted_papers:
                try:
                    # Try common accepted paper query methods
                    possible_venues = [
                        {'venueid': f"{venue_id}/Acceptance"},
                        {'venueid': f"{venue_id}/Accepted"},
                        {'venueid': venue_id},
                    ]
                    
                    for venue_query in possible_venues:
                        accepted_papers = self.client.get_all_notes(content=venue_query)
                        if accepted_papers:
                            break
                except Exception as e:
                    print(f"Error while trying alternative query methods: {str(e)}")
            
            # Further filter by category
            if category and category.lower() not in ['accepted', 'all']:
                filtered_papers = []
                for paper in accepted_papers:
                    if 'venue' in paper.content and 'value' in paper.content['venue']:
                        venue_value = paper.content['venue']['value'].lower()
                        if category.lower() in venue_value:
                            filtered_papers.append(paper)
                return filtered_papers
            
            return accepted_papers
            
        except Exception as e:
            print(f"Error while getting papers: {str(e)}")
            return []
    
    def extract_paper_info(self, paper) -> Dict:
        """
        Extract detailed information from a paper
        
        Args:
            paper: OpenReview paper object
            
        Returns:
            Dictionary containing detailed paper information
        """
        # Basic information
        paper_info = {
            'id': paper.id,
            'title': paper.content.get('title', {}).get('value', ''),
            'abstract': paper.content.get('abstract', {}).get('value', ''),
            'keywords': paper.content.get('keywords', {}).get('value', []),
            'tldr': paper.content.get('TLDR', {}).get('value', ''),
            'forum_link': f"https://openreview.net/forum?id={paper.id}",
            'pdf_link': f"https://openreview.net/pdf?id={paper.id}",
        }
        
        # Extract year
        try:
            venue_info = paper.content.get('venue', {}).get('value', '')
            year_match = re.search(r'\b20\d{2}\b', venue_info)
            if year_match:
                paper_info['year'] = year_match.group(0)
            else:
                # Try to extract year from conference ID
                year_match = re.search(r'\b20\d{2}\b', paper.invitations[0])
                paper_info['year'] = year_match.group(0) if year_match else ''
        except:
            paper_info['year'] = ''
        
        # Extract category information using a more general method
        try:
            # First try to extract category information from venue field
            venue_value = paper.content.get('venue', {}).get('value', '').lower()
            
            # Check common category keywords
            common_categories = {
                'oral': ['oral', 'talk', 'presentation'],
                'spotlight': ['spotlight', 'highlight'],
                'poster': ['poster'],
                'workshop': ['workshop'],
                'demo': ['demo', 'demonstration']
            }
            
            category_found = False
            for category, keywords in common_categories.items():
                if any(keyword in venue_value for keyword in keywords):
                    paper_info['category'] = category
                    category_found = True
                    break
            
            # If not found in common categories, extract the last word from venue as a possible category
            if not category_found:
                # Remove year
                venue_without_year = re.sub(r'\b20\d{2}\b', '', venue_value).strip()
                # Extract the last word as a possible category
                parts = venue_without_year.split()
                if parts:
                    paper_info['category'] = parts[-1].strip()
                else:
                    paper_info['category'] = 'accepted'
        except:
            paper_info['category'] = 'accepted'
        
        # Get author information
        try:
            # Try to get author information from content
            paper_info['authors'] = paper.content.get('authors', {}).get('value', [])
        except:
            try:
                # If the above method fails, try to get from signatures
                authors = self.client.get_group(f"{paper.signatures[0]}")
                paper_info['authors'] = authors.members
            except:
                paper_info['authors'] = []
        
        # Convert timestamp to date
        if hasattr(paper, 'cdate'):
            paper_info['creation_date'] = datetime.fromtimestamp(
                paper.cdate / 1000).strftime('%Y-%m-%d')
        
        return paper_info
    
    def get_papers_from_url(self, url: str) -> List[Dict]:
        """
        Get paper information directly from URL
        
        Args:
            url: OpenReview web URL
            
        Returns:
            List of paper information
        """
        venue_id = self.extract_venue_id_from_url(url)
        category = self.extract_paper_category_from_url(url)
        
        papers = self.get_accepted_papers(venue_id, category)
        return [self.extract_paper_info(paper) for paper in papers]
    
    def get_papers_from_venue(self, venue_id: str, category: Optional[str] = None) -> List[Dict]:
        """
        Get paper information from conference ID
        
        Args:
            venue_id: Conference ID
            category: Paper category
            
        Returns:
            List of paper information
        """
        papers = self.get_accepted_papers(venue_id, category)
        return [self.extract_paper_info(paper) for paper in papers]
    
    def save_to_json(self, papers: List[Dict], output_file: str) -> None:
        """
        Save paper information as a JSON file
        
        Args:
            papers: List of paper information
            output_file: Output file path
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
            
    def save_to_csv(self, papers: List[Dict], output_file: str) -> None:
        """
        Save paper information as a CSV file
        
        Args:
            papers: List of paper information
            output_file: Output file path
        """
        df = pd.DataFrame(papers)
        df.to_csv(output_file, index=False, encoding='utf-8') 