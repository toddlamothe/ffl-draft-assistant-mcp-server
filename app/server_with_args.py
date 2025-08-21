from fastmcp import FastMCP, Context
from app.scraper.nfl_injuries import fetch_nfl_injuries
from app.cache.cache import get_cache, set_cache
from app.resources.player_ratings_resource import (
    get_all_player_ratings, 
    get_player_ratings_by_source,
    get_player_ratings_by_position,
    get_player_ratings_by_team
)
from typing import List, Dict
import logging
import argparse
import sys

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
        logger.info("Cache miss, fetching fresh injuries")
        injuries = fetch_nfl_injuries()
        set_cache(injuries)
    return injuries

@mcp.tool()
async def get_player_ratings(ctx: Context) -> List[Dict]:
    """Get all player ratings from multiple sources (cached, refreshed every 48h)."""
    logger.info("Tool called: get_player_ratings")
    return get_all_player_ratings()

@mcp.tool()
async def get_player_ratings_by_source(ctx: Context, source: str) -> List[Dict]:
    """Get player ratings from a specific source (e.g., 'Madden NFL')."""
    logger.info(f"Tool called: get_player_ratings_by_source with source={source}")
    return get_player_ratings_by_source(source)

@mcp.tool()
async def get_player_ratings_by_position(ctx: Context, position: str) -> List[Dict]:
    """Get player ratings filtered by position (e.g., 'QB', 'RB', 'WR', 'TE', 'K', 'DEF')."""
    logger.info(f"Tool called: get_player_ratings_by_position with position={position}")
    return get_player_ratings_by_position(position)

@mcp.tool()
async def get_player_ratings_by_team(ctx: Context, team: str) -> List[Dict]:
    """Get player ratings filtered by team name."""
    logger.info(f"Tool called: get_player_ratings_by_team with team={team}")
    return get_player_ratings_by_team(team)

def parse_arguments():
    """Parse command line arguments, ignoring unknown ones that MCP inspector might pass."""
    parser = argparse.ArgumentParser(description="Fantasy Football MCP Server")
    
    # Add any arguments your server might need
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Parse known args only, ignore unknown ones
    args, unknown = parser.parse_known_args()
    
    if unknown:
        logger.info(f"Ignoring unknown arguments: {unknown}")
    
    return args

if __name__ == "__main__":
    # Parse arguments (ignoring unknown ones)
    args = parse_arguments()
    
    # Set log level based on arguments
    if args.verbose or args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")
    
    logger.info("Starting Fantasy Football MCP Server...")
    logger.info(f"Available tools: {list(mcp.tools.keys())}")
    
    # Run the MCP server
    mcp.run()
