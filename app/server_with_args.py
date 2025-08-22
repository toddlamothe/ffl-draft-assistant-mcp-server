from fastmcp import FastMCP, Context
from app.scraper.nfl_injuries import fetch_nfl_injuries
from app.cache.cache import get_cache, set_cache
from app.resources.player_ratings_resource import (
    get_all_player_ratings, 
    get_player_ratings_by_source,
    get_player_ratings_by_position,
    get_player_ratings_by_team,
    get_player_by_name,
    get_player_ratings_stats
)
from app.resources.ol_rankings_resource import (
    get_all_ol_rankings,
    get_ol_rankings_by_team_cached,
    get_top_ol_rankings_cached,
    get_ol_rankings_by_rank_range_cached,
    get_ol_rankings_stats
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
        logger.info("NFL injuries: CACHE MISS - fetching fresh data from website")
        injuries = fetch_nfl_injuries()
        set_cache(injuries)
        logger.info(f"NFL injuries: CACHE UPDATED - stored {len(injuries)} injury records")
    else:
        logger.info(f"NFL injuries: CACHE HIT - serving {len(injuries)} cached injury records")
    return injuries

@mcp.tool()
async def get_player_ratings(ctx: Context) -> List[Dict]:
    """Get all player ratings from multiple sources (Madden NFL + PFF) with ratings from all available sources for each player."""
    logger.info("Tool called: get_player_ratings")
    ratings = get_all_player_ratings()
    logger.info(f"Player ratings: served {len(ratings)} players with unified ratings from all sources")
    return ratings

@mcp.tool()
async def get_player_ratings_by_source(ctx: Context, source: str) -> List[Dict]:
    """Get player ratings from a specific source (e.g., 'Madden NFL', 'Pro Football Focus')."""
    logger.info(f"Tool called: get_player_ratings_by_source with source={source}")
    ratings = get_player_ratings_by_source(source)
    logger.info(f"Player ratings by source '{source}': served {len(ratings)} players")
    return ratings

@mcp.tool()
async def get_player_ratings_by_position(ctx: Context, position: str) -> List[Dict]:
    """Get player ratings filtered by position (e.g., 'QB', 'RB', 'WR', 'TE', 'K', 'DEF') with ratings from all sources."""
    logger.info(f"Tool called: get_player_ratings_by_position with position={position}")
    ratings = get_player_ratings_by_position(position)
    logger.info(f"Player ratings by position '{position}': served {len(ratings)} players")
    return ratings

@mcp.tool()
async def get_player_ratings_by_team(ctx: Context, team: str) -> List[Dict]:
    """Get player ratings filtered by team name with ratings from all sources."""
    logger.info(f"Tool called: get_player_ratings_by_team with team={team}")
    ratings = get_player_ratings_by_team(team)
    logger.info(f"Player ratings by team '{team}': served {len(ratings)} players")
    return ratings

@mcp.tool()
async def get_player_by_name(ctx: Context, player_name: str) -> Dict:
    """Get ratings for a specific player by name with ratings from all available sources."""
    logger.info(f"Tool called: get_player_by_name with player_name={player_name}")
    player = get_player_by_name(player_name)
    if player:
        logger.info(f"Player '{player_name}': found with {len(player.get('ratings', []))} rating sources")
    else:
        logger.info(f"Player '{player_name}': player not found")
    return player or {"error": f"Player '{player_name}' not found"}

@mcp.tool()
async def get_player_ratings_stats(ctx: Context) -> Dict:
    """Get statistics about the combined player ratings dataset (Madden + PFF)."""
    logger.info("Tool called: get_player_ratings_stats")
    stats = get_player_ratings_stats()
    logger.info("Player ratings stats: served dataset statistics")
    return stats

# Offensive Line Ranking Tools
@mcp.tool()
async def get_ol_rankings(ctx: Context) -> List[Dict]:
    """Get all PFF offensive line rankings (cached, refreshed every 48h)."""
    logger.info("Tool called: get_ol_rankings")
    rankings = get_all_ol_rankings()
    logger.info(f"OL rankings: served {len(rankings)} team rankings (cache status logged by resource)")
    return rankings

@mcp.tool()
async def get_ol_rankings_by_team(ctx: Context, team: str) -> Dict:
    """Get offensive line ranking for a specific team."""
    logger.info(f"Tool called: get_ol_rankings_by_team with team={team}")
    ranking = get_ol_rankings_by_team_cached(team)
    if ranking:
        logger.info(f"OL ranking for '{team}': found (rank {ranking.get('rank', 'N/A')})")
    else:
        logger.info(f"OL ranking for '{team}': team not found")
    return ranking or {"error": f"Team '{team}' not found in OL rankings"}

@mcp.tool()
async def get_top_ol_rankings(ctx: Context, top_n: int = 10) -> List[Dict]:
    """Get top N offensive line rankings (e.g., top_n=10 for top 10 teams)."""
    logger.info(f"Tool called: get_top_ol_rankings with top_n={top_n}")
    rankings = get_top_ol_rankings_cached(top_n)
    logger.info(f"Top {top_n} OL rankings: served {len(rankings)} team rankings")
    return rankings

@mcp.tool()
async def get_ol_rankings_by_rank_range(ctx: Context, min_rank: int, max_rank: int) -> List[Dict]:
    """Get offensive line rankings within a specific rank range (e.g., min_rank=1, max_rank=10)."""
    logger.info(f"Tool called: get_ol_rankings_by_rank_range with range {min_rank}-{max_rank}")
    rankings = get_ol_rankings_by_rank_range_cached(min_rank, max_rank)
    logger.info(f"OL rankings by rank range {min_rank}-{max_rank}: served {len(rankings)} team rankings")
    return rankings

@mcp.tool()
async def get_ol_rankings_stats(ctx: Context) -> Dict:
    """Get statistics about the offensive line rankings dataset."""
    logger.info("Tool called: get_ol_rankings_stats")
    stats = get_ol_rankings_stats()
    logger.info("OL rankings stats: served dataset statistics")
    return stats

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
    logger.info("Available tools: get_nfl_injuries, get_player_ratings, get_player_ratings_by_source, get_player_ratings_by_position, get_player_ratings_by_team, get_player_by_name, get_player_ratings_stats, get_ol_rankings, get_ol_rankings_by_team, get_top_ol_rankings, get_ol_rankings_by_rank_range, get_ol_rankings_stats")
    
    # Run the MCP server
    mcp.run()
