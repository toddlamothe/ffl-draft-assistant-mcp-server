from fastmcp import FastMCP, Context
from app.scraper.nfl_injuries import fetch_nfl_injuries
from app.cache.cache import get_cache, set_cache
from app.resources.player_ratings_resource import (
    get_all_player_ratings, 
    get_player_ratings_by_source as get_ratings_by_source,
    get_player_ratings_by_position as get_ratings_by_position,
    get_player_ratings_by_team as get_ratings_by_team
)
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("FantasyFootballAssistant")

@mcp.tool()
async def get_nfl_injuries(ctx: Context) -> List[Dict]:
    """Get the latest NFL injuries (cached, refreshed every 24h)."""
    logger.info("Tool called: get_nfl_injuries")
    injuries = get_cache()
    if injuries is None:
        logger.info("NFL injuries: CACHE MISS - fetching fresh data from website")
        injuries = fetch_nfl_injuries()
        set_cache(injuries)
        logger.info(f"NFL injuries: CACHE UPDATED - stored {len(injuries)} injury records")
    else:
        logger.info(f"NFL injuries: CACHE HIT - serving {len(injuries)} cached injury records")
    return injuries

@mcp.tool()
async def get_player_ratings(ctx: Context) -> List[Dict]:
    """Get all player ratings from multiple sources (cached, refreshed every 48h)."""
    logger.info("Tool called: get_player_ratings")
    ratings = get_all_player_ratings()
    logger.info(f"Player ratings: served {len(ratings)} ratings (cache status logged by resource)")
    return ratings

@mcp.tool()
async def get_player_ratings_by_source(ctx: Context, source: str) -> List[Dict]:
    """Get player ratings from a specific source (e.g., 'Madden NFL')."""
    logger.info(f"Tool called: get_player_ratings_by_source with source={source}")
    ratings = get_ratings_by_source(source)
    logger.info(f"Player ratings by source '{source}': served {len(ratings)} ratings (cache status logged by resource)")
    return ratings

@mcp.tool()
async def get_player_ratings_by_position(ctx: Context, position: str) -> List[Dict]:
    """Get player ratings filtered by position (e.g., 'QB', 'RB', 'WR', 'TE', 'K', 'DEF')."""
    logger.info(f"Tool called: get_player_ratings_by_position with position={position}")
    ratings = get_ratings_by_position(position)
    logger.info(f"Player ratings by position '{position}': served {len(ratings)} ratings (cache status logged by resource)")
    return ratings

@mcp.tool()
async def get_player_ratings_by_team(ctx: Context, team: str) -> List[Dict]:
    """Get player ratings filtered by team name."""
    logger.info(f"Tool called: get_player_ratings_by_team with team={team}")
    ratings = get_ratings_by_team(team)
    logger.info(f"Player ratings by team '{team}': served {len(ratings)} ratings (cache status logged by resource)")
    return ratings

if __name__ == "__main__":
    mcp.run()
