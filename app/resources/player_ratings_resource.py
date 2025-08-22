import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.scraper.madden_ratings import fetch_madden_ratings
from app.resources.pff_ratings_resource import get_all_pff_ratings

logger = logging.getLogger(__name__)

# Cache configuration
CACHE_DIR = "/tmp/pigskin-pickem-cache"
MADDEN_CACHE_FILE = os.path.join(CACHE_DIR, "madden_ratings.json")
CACHE_TTL_HOURS = 48

def get_madden_cache() -> Optional[List[Dict]]:
    """Get Madden ratings from cache if available and not expired."""
    try:
        if not os.path.exists(MADDEN_CACHE_FILE):
            logger.info("Madden cache file does not exist")
            return None
        
        # Check file modification time
        file_mtime = datetime.fromtimestamp(os.path.getmtime(MADDEN_CACHE_FILE))
        age = datetime.now() - file_mtime
        
        if age > timedelta(hours=CACHE_TTL_HOURS):
            logger.info(f"Madden cache expired (age: {age})")
            return None
        
        with open(MADDEN_CACHE_FILE, 'r') as f:
            data = json.load(f)
            logger.info(f"Madden cache hit: {len(data)} players")
            return data
            
    except Exception as e:
        logger.error(f"Error reading Madden cache: {e}")
        return None

def set_madden_cache(ratings: List[Dict]) -> None:
    """Cache Madden ratings data."""
    try:
        # Ensure cache directory exists
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        with open(MADDEN_CACHE_FILE, 'w') as f:
            json.dump(ratings, f, indent=2)
        
        logger.info(f"Madden ratings cached: {len(ratings)} players")
        
    except Exception as e:
        logger.error(f"Error caching Madden ratings: {e}")

def get_all_madden_ratings() -> List[Dict]:
    """Get all Madden ratings (cached, refreshed every 48h)."""
    logger.info("Fetching Madden ratings")
    
    # Try to get from cache first
    ratings = get_madden_cache()
    if ratings is not None:
        logger.info("Using cached Madden ratings")
        return ratings
    
    # Cache miss, fetch fresh data
    logger.info("Cache miss, fetching fresh Madden ratings")
    try:
        ratings = fetch_madden_ratings()
        set_madden_cache(ratings)
        logger.info(f"Successfully cached {len(ratings)} Madden ratings")
        return ratings
    except Exception as e:
        logger.error(f"Error fetching Madden ratings: {e}")
        raise

def normalize_player_name(name: str) -> str:
    """Normalize player name for matching across sources."""
    # Remove common suffixes and normalize
    name = name.strip().lower()
    name = name.replace(" iii", "").replace(" ii", "").replace(" jr.", "").replace(" sr.", "")
    name = name.replace("'", "").replace("'", "")  # Handle apostrophes
    return name

def match_players_by_name(madden_players: List[Dict], pff_players: List[Dict]) -> Dict[str, Dict]:
    """Create a mapping of normalized names to player data from both sources."""
    player_map = {}
    
    # Add Madden players
    for player in madden_players:
        normalized_name = normalize_player_name(player.get("name", ""))
        if normalized_name:
            if normalized_name not in player_map:
                player_map[normalized_name] = {"madden": player, "pff": None}
            else:
                player_map[normalized_name]["madden"] = player
    
    # Add PFF players
    for player in pff_players:
        normalized_name = normalize_player_name(player.get("name", ""))
        if normalized_name:
            if normalized_name not in player_map:
                player_map[normalized_name] = {"madden": None, "pff": player}
            else:
                player_map[normalized_name]["pff"] = player
    
    return player_map

def combine_player_ratings() -> List[Dict]:
    """
    Combine Madden and PFF ratings into unified player objects.
    Each player will have ratings from both sources if available.
    """
    logger.info("Combining Madden and PFF ratings")
    
    # Get ratings from both sources
    madden_ratings = get_all_madden_ratings()
    pff_ratings = get_all_pff_ratings()
    
    logger.info(f"Madden ratings: {len(madden_ratings)} players")
    logger.info(f"PFF ratings: {len(pff_ratings)} players")
    
    # Create player mapping
    player_map = match_players_by_name(madden_ratings, pff_ratings)
    
    # Combine into unified format
    combined_players = []
    for normalized_name, sources in player_map.items():
        # Prioritize PFF team data over Madden (since Madden often shows "Unknown")
        team = sources["pff"]["team"] if sources["pff"] and sources["pff"]["team"] != "Unknown" else sources["madden"]["team"] if sources["madden"] else "Unknown"
        
        player_data = {
            "name": sources["madden"]["name"] if sources["madden"] else sources["pff"]["name"],
            "position": sources["madden"]["position"] if sources["madden"] else sources["pff"]["position"],
            "team": team,
            "ratings": []
        }
        
        # Add Madden rating if available
        if sources["madden"]:
            madden_rating = {
                "source": "Madden NFL",
                "overall": sources["madden"].get("overall"),
                "attributes": sources["madden"].get("attributes", {}),
                "position_rank": sources["madden"].get("position_rank")
            }
            player_data["ratings"].append(madden_rating)
        
        # Add PFF rating if available
        if sources["pff"]:
            pff_rating = {
                "source": "Pro Football Focus",
                "overall": sources["pff"].get("overall"),
                "pff_grade": sources["pff"].get("pff_grade"),
                "pff_rank": sources["pff"].get("pff_rank"),
                "overall_rank": sources["pff"].get("overall_rank"),
                "position_rank": sources["pff"].get("position_rank"),
                "projected_points": sources["pff"].get("projected_points"),
                "adp": sources["pff"].get("adp"),
                "auction_value": sources["pff"].get("auction_value"),
                "bye_week": sources["pff"].get("bye_week")
            }
            player_data["ratings"].append(pff_rating)
        
        combined_players.append(player_data)
    
    logger.info(f"Combined ratings: {len(combined_players)} unique players")
    return combined_players

def get_all_player_ratings() -> List[Dict]:
    """
    Get all player ratings from multiple sources (cached, refreshed every 48h).
    Returns unified player objects with ratings from all available sources.
    """
    return combine_player_ratings()

def get_player_ratings_by_source(source: str) -> List[Dict]:
    """
    Get player ratings from a specific source (e.g., 'Madden NFL', 'Pro Football Focus').
    Returns players that have ratings from the specified source.
    """
    all_players = get_all_player_ratings()
    source_lower = source.lower()
    
    filtered_players = []
    for player in all_players:
        for rating in player.get("ratings", []):
            if rating.get("source", "").lower() == source_lower:
                # Create a copy with only the matching source rating
                filtered_player = player.copy()
                filtered_player["ratings"] = [rating]
                filtered_players.append(filtered_player)
                break
    
    return filtered_players

def get_player_ratings_by_position(position: str) -> List[Dict]:
    """
    Get player ratings filtered by position (e.g., 'QB', 'RB', 'WR', 'TE', 'K', 'DEF').
    Returns players at the specified position with ratings from all sources.
    """
    all_players = get_all_player_ratings()
    position_upper = position.upper()
    
    return [
        player for player in all_players 
        if player.get("position", "").upper() == position_upper
    ]

def get_player_ratings_by_team(team: str) -> List[Dict]:
    """
    Get player ratings filtered by team name.
    Returns players on the specified team with ratings from all sources.
    """
    all_players = get_all_player_ratings()
    team_lower = team.lower()
    
    return [
        player for player in all_players 
        if player.get("team", "").lower() == team_lower
    ]

def get_player_by_name(player_name: str) -> Optional[Dict]:
    """
    Get ratings for a specific player by name.
    Returns player data with ratings from all available sources.
    """
    all_players = get_all_player_ratings()
    player_name_lower = player_name.lower()
    
    for player in all_players:
        if player.get("name", "").lower() == player_name_lower:
            return player
    
    return None

def get_player_ratings_stats() -> Dict:
    """
    Get statistics about the combined player ratings dataset.
    """
    all_players = get_all_player_ratings()
    
    if not all_players:
        return {"error": "No player ratings loaded"}
    
    # Basic stats
    total_players = len(all_players)
    
    # Source coverage
    madden_count = sum(1 for p in all_players if any(r.get("source") == "Madden NFL" for r in p.get("ratings", [])))
    pff_count = sum(1 for p in all_players if any(r.get("source") == "Pro Football Focus" for r in p.get("ratings", [])))
    both_sources_count = sum(1 for p in all_players if len(p.get("ratings", [])) >= 2)
    
    # Position distribution
    position_counts = {}
    for player in all_players:
        pos = player.get("position", "Unknown")
        position_counts[pos] = position_counts.get(pos, 0) + 1
    
    # Team distribution
    team_counts = {}
    for player in all_players:
        team = player.get("team", "Unknown")
        team_counts[team] = team_counts.get(team, 0) + 1
    
    return {
        "total_players": total_players,
        "source_coverage": {
            "madden_only": madden_count - both_sources_count,
            "pff_only": pff_count - both_sources_count,
            "both_sources": both_sources_count
        },
        "position_counts": position_counts,
        "team_counts": team_counts
    }
