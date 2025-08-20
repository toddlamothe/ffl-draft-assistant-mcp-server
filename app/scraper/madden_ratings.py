import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)

MADDEN_RATINGS_URL = "https://www.ea.com/games/madden-nfl/ratings"

def fetch_madden_ratings() -> List[Dict]:
    """Fetch and parse Madden NFL player ratings from EA's website."""
    logger.info("Fetching Madden NFL ratings from EA website")
    
    try:
        response = httpx.get(MADDEN_RATINGS_URL, timeout=30)
        response.raise_for_status()
        logger.info("Successfully fetched Madden ratings page")
        
        soup = BeautifulSoup(response.text, "html.parser")
        players = []
        
        # Find all player rows in the table
        player_rows = soup.find_all("tr", class_="Table_row__eoyUr")
        logger.info(f"Found {len(player_rows)} player rows")
        
        for row in player_rows:
            try:
                player_data = extract_player_data(row)
                if player_data:
                    players.append(player_data)
            except Exception as e:
                logger.warning(f"Error extracting player data from row: {e}")
                continue
        
        logger.info(f"Successfully extracted {len(players)} player ratings")
        return players
        
    except httpx.RequestError as e:
        logger.error(f"Network error fetching Madden ratings: {e}")
        raise
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching Madden ratings: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching Madden ratings: {e}")
        raise

def extract_player_data(row) -> Optional[Dict]:
    """Extract player data from a table row."""
    try:
        # Extract player name
        name_element = row.find("span", class_="Table_profileLabel__tuyG0")
        if not name_element:
            return None
        name = name_element.text.strip()
        
        # Extract position
        position_element = row.find("span", class_="Table_tag__vKZKn")
        position = position_element.text.strip() if position_element else "Unknown"
        
        # Extract team (from alt text of team image)
        team_img = row.find("img", alt=re.compile(r".*"))
        team = "Unknown"
        if team_img and team_img.get("alt"):
            alt_text = team_img.get("alt")
            # Extract team name from alt text (e.g., "Buffalo Bills" from alt text)
            team_match = re.search(r"([A-Za-z\s]+(?:Bills|Dolphins|Patriots|Jets|Ravens|Bengals|Browns|Steelers|Texans|Colts|Jaguars|Titans|Broncos|Chiefs|Raiders|Chargers|Cowboys|Giants|Eagles|Commanders|Bears|Lions|Packers|Vikings|Falcons|Panthers|Saints|Buccaneers|Cardinals|Rams|49ers|Seahawks))", alt_text)
            if team_match:
                team = team_match.group(1).strip()
        
        # Extract overall rating (OVR)
        ovr_element = row.find("span", class_="Table_statCellValue__zn5Cx")
        overall = None
        if ovr_element:
            try:
                overall = int(ovr_element.text.strip())
            except ValueError:
                logger.warning(f"Could not parse overall rating for {name}: {ovr_element.text}")
        
        if not name or not overall:
            return None
            
        return {
            "name": name,
            "position": position,
            "team": team,
            "overall": overall,
            "source": "Madden NFL"
        }
        
    except Exception as e:
        logger.warning(f"Error extracting player data: {e}")
        return None

def get_all_madden_ratings() -> List[Dict]:
    """Get all Madden NFL player ratings."""
    return fetch_madden_ratings()
