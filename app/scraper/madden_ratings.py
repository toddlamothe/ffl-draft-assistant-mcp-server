import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)

MADDEN_RATINGS_URL = "https://www.ea.com/games/madden-nfl/ratings"


def fetch_madden_ratings() -> List[Dict]:
    """Fetch and parse Madden NFL player ratings from EA's website across all pages."""
    logger.info("Fetching Madden NFL ratings from EA website (all pages)")

    players: List[Dict] = []

    try:
        # Fetch initial/base page first
        base_players = _fetch_madden_ratings_page(None)
        logger.info(f"Base page returned {len(base_players)} players")
        players.extend(base_players)

        # Then iterate subsequent pages using the page query param until no results
        page = 2
        while True:
            page_players = _fetch_madden_ratings_page(page)
            logger.info(f"Page {page} returned {len(page_players)} players")
            if not page_players:
                break
            players.extend(page_players)
            page += 1

        logger.info(f"Successfully extracted {len(players)} total player ratings across pages")
        return players

    except Exception as e:
        logger.error(f"Unexpected error fetching Madden ratings: {e}")
        raise


def _fetch_madden_ratings_page(page: Optional[int]) -> List[Dict]:
    """Fetch a single page of Madden ratings. If page is None, fetch the base page.
    Returns a list of parsed player dicts. Does not raise on HTTP errors; logs and returns [].
    """
    try:
        url = MADDEN_RATINGS_URL if page is None else f"{MADDEN_RATINGS_URL}?page={page}"
        logger.info(f"Fetching Madden ratings page: {url}")
        response = httpx.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        players: List[Dict] = []
        player_rows = soup.find_all("tr", class_="Table_row__eoyUr")
        logger.info(f"Found {len(player_rows)} player rows on current page")

        for row in player_rows:
            try:
                player_data = extract_player_data(row)
                if player_data:
                    players.append(player_data)
            except Exception as e:
                logger.warning(f"Error extracting player data from row: {e}")
                continue

        return players

    except httpx.RequestError as e:
        logger.error(f"Network error fetching Madden ratings page {page}: {e}")
        return []
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching Madden ratings page {page}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching page {page}: {e}")
        return []


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

        if not name or overall is None:
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
