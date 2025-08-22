import httpx
import logging
from bs4 import BeautifulSoup
from typing import List, Dict
import re

logger = logging.getLogger(__name__)

def fetch_pff_ol_rankings() -> List[Dict]:
    """
    Scrape PFF offensive line rankings from their website.
    
    Returns:
        List of dictionaries containing team OL rankings and details
    """
    url = "https://www.pff.com/news/nfl-2025-nfl-offensive-line-rankings"
    
    try:
        logger.info(f"Fetching PFF offensive line rankings from {url}")
        
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main content area
        content = soup.find('div', class_='article-content') or soup.find('article') or soup
        
        # Extract team rankings
        teams = []
        
        # Look for numbered sections (1. Team Name, 2. Team Name, etc.)
        # The content structure shows teams as numbered sections
        team_sections = []
        
        # Find all h3 tags that contain team rankings
        for h3 in content.find_all('h3'):
            text = h3.get_text().strip()
            # Look for patterns like "1. Philadelphia Eagles" or "1\. Philadelphia Eagles"
            match = re.match(r'^(\d+)\.\s+(.+)$', text)
            if match:
                rank = int(match.group(1))
                team_name = match.group(2).strip()
                team_sections.append((rank, team_name, h3))
        
        # If we didn't find h3 tags, try h2 tags
        if not team_sections:
            for h2 in content.find_all('h2'):
                text = h2.get_text().strip()
                match = re.match(r'^(\d+)\.\s+(.+)$', text)
                if match:
                    rank = int(match.group(1))
                    team_name = match.group(2).strip()
                    team_sections.append((rank, team_name, h2))
        
        # Sort by rank
        team_sections.sort(key=lambda x: x[0])
        
        for rank, team_name, header in team_sections:
            # Find the description text for this team
            description = ""
            next_element = header.find_next_sibling()
            
            # Collect text until we hit the next team or end
            while next_element and next_element.name not in ['h2', 'h3']:
                if next_element.name in ['p', 'div']:
                    text = next_element.get_text().strip()
                    if text and not text.startswith('Subscribe to PFF+'):
                        description += text + " "
                next_element = next_element.find_next_sibling()
            
            # Clean up the description
            description = re.sub(r'\s+', ' ', description).strip()
            
            # Extract key details using regex patterns
            key_details = {}
            
            # Look for PFF grades
            grade_matches = re.findall(r'(\d+\.\d+)\s+PFF\s+(overall|pass-blocking|run-blocking)\s+grade', description, re.IGNORECASE)
            for grade, grade_type in grade_matches:
                key_details[f"pff_{grade_type.lower().replace('-', '_')}_grade"] = float(grade)
            
            # Look for rankings
            rank_matches = re.findall(r'ranked\s+(\d+)(?:st|nd|rd|th)?\s+(?:among|at)', description, re.IGNORECASE)
            if rank_matches:
                key_details["position_rank"] = int(rank_matches[0])
            
            # Look for pressure stats
            pressure_match = re.search(r'(\d+)\s+pressures?', description)
            if pressure_match:
                key_details["pressures_allowed"] = int(pressure_match.group(1))
            
            # Look for sack stats
            sack_match = re.search(r'(\d+)\s+sacks?', description)
            if sack_match:
                key_details["sacks_allowed"] = int(sack_match.group(1))
            
            # Look for pass-blocking efficiency
            pbe_match = re.search(r'(\d+\.\d+)\s+PFF\s+pass-blocking\s+efficiency', description, re.IGNORECASE)
            if pbe_match:
                key_details["pass_blocking_efficiency"] = float(pbe_match.group(1))
            
            team_data = {
                "rank": rank,
                "team": team_name,
                "description": description,
                "key_details": key_details
            }
            
            teams.append(team_data)
        
        logger.info(f"Successfully scraped {len(teams)} team offensive line rankings")
        return teams
        
    except Exception as e:
        logger.error(f"Error fetching PFF offensive line rankings: {e}")
        return []

def get_ol_rankings_by_team(team_name: str) -> Dict:
    """
    Get offensive line ranking for a specific team.
    
    Args:
        team_name: Name of the team to find
        
    Returns:
        Team OL ranking data or empty dict if not found
    """
    rankings = fetch_pff_ol_rankings()
    team_name_lower = team_name.lower()
    
    for ranking in rankings:
        if ranking.get("team", "").lower() == team_name_lower:
            return ranking
    
    return {}

def get_top_ol_rankings(top_n: int = 10) -> List[Dict]:
    """
    Get top N offensive line rankings.
    
    Args:
        top_n: Number of top teams to return
        
    Returns:
        List of top N OL rankings
    """
    rankings = fetch_pff_ol_rankings()
    return rankings[:top_n]

def get_ol_rankings_by_rank_range(min_rank: int, max_rank: int) -> List[Dict]:
    """
    Get offensive line rankings within a specific rank range.
    
    Args:
        min_rank: Minimum rank
        max_rank: Maximum rank
        
    Returns:
        List of OL rankings within the range
    """
    rankings = fetch_pff_ol_rankings()
    return [
        ranking for ranking in rankings 
        if min_rank <= ranking.get("rank", 999) <= max_rank
    ]
