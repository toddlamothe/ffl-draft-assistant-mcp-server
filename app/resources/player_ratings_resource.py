from app.scraper.madden_ratings import get_all_madden_ratings
from app.cache.cache import get_ratings_cache, set_ratings_cache
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def get_all_player_ratings() -> List[Dict]:
    """Get all player ratings from multiple sources (cached, refreshed based on TTL)."""
    logger.info("Fetching player ratings")
    
    # Try to get from cache first
    ratings = get_ratings_cache()
    if ratings is not None:
        logger.info("Using cached player ratings")
        return ratings
    
    # Cache miss, fetch fresh data
    logger.info("Cache miss, fetching fresh player ratings")
    try:
        ratings = get_all_madden_ratings()
        set_ratings_cache(ratings)
        logger.info(f"Successfully cached {len(ratings)} player ratings")
        return ratings
    except Exception as e:
        logger.error(f"Error fetching player ratings: {e}")
        raise

def get_player_ratings_by_source(source: str) -> List[Dict]:
    """Get player ratings from a specific source."""
    all_ratings = get_all_player_ratings()
    return [rating for rating in all_ratings if rating.get("source") == source]

def get_player_ratings_by_position(position: str) -> List[Dict]:
    """Get player ratings filtered by position."""
    all_ratings = get_all_player_ratings()
    return [rating for rating in all_ratings if rating.get("position") == position.upper()]

def get_player_ratings_by_team(team: str) -> List[Dict]:
    """Get player ratings filtered by team."""
    all_ratings = get_all_player_ratings()
    return [rating for rating in all_ratings if rating.get("team") == team]
