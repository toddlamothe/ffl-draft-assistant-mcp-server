from fastmcp import FastMCP, Context
from app.scraper.nfl_injuries import fetch_nfl_injuries
from app.cache.cache import get_cache, set_cache
from typing import List, Dict

mcp = FastMCP("NFLInjuryServer")

@mcp.tool()
async def get_nfl_injuries(ctx: Context) -> List[Dict]:
    """Get the latest NFL injuries (cached, refreshed every 24h)."""
    injuries = get_cache()
    if injuries is None:
        injuries = fetch_nfl_injuries()
        set_cache(injuries)
    return injuries

if __name__ == "__main__":
    mcp.run()
