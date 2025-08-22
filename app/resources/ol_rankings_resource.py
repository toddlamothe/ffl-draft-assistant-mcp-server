import os
import json
import logging
from typing import List, Dict
from datetime import datetime, timedelta
from app.scraper.pff_ol_rankings import (
    fetch_pff_ol_rankings,
    get_ol_rankings_by_team,
    get_top_ol_rankings,
    get_ol_rankings_by_rank_range
)

logger = logging.getLogger(__name__)

# Cache configuration
CACHE_DIR = "/tmp/pigskin-pickem-cache"
OL_RANKINGS_CACHE_FILE = os.path.join(CACHE_DIR, "pff_ol_rankings.json")
CACHE_TTL_HOURS = 48

def get_ol_rankings_cache() -> List[Dict]:
    """
    Get offensive line rankings from cache if available and not expired.
    
    Returns:
        Cached OL rankings or None if cache miss/expired
    """
    try:
        if not os.path.exists(OL_RANKINGS_CACHE_FILE):
            logger.info("OL rankings cache file does not exist")
            return None
        
        # Check file modification time
        file_mtime = datetime.fromtimestamp(os.path.getmtime(OL_RANKINGS_CACHE_FILE))
        age = datetime.now() - file_mtime
        
        if age > timedelta(hours=CACHE_TTL_HOURS):
            logger.info(f"OL rankings cache expired (age: {age})")
            return None
        
        with open(OL_RANKINGS_CACHE_FILE, 'r') as f:
            data = json.load(f)
            logger.info(f"OL rankings cache hit: {len(data)} teams")
            return data
            
    except Exception as e:
        logger.error(f"Error reading OL rankings cache: {e}")
        return None

def set_ol_rankings_cache(rankings: List[Dict]) -> None:
    """
    Cache offensive line rankings data.
    
    Args:
        rankings: OL rankings data to cache
    """
    try:
        # Ensure cache directory exists
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        with open(OL_RANKINGS_CACHE_FILE, 'w') as f:
            json.dump(rankings, f, indent=2)
        
        logger.info(f"OL rankings cached: {len(rankings)} teams")
        
    except Exception as e:
        logger.error(f"Error caching OL rankings: {e}")

def get_all_ol_rankings() -> List[Dict]:
    """
    Get all offensive line rankings (cached, refreshed every 48h).
    
    Returns:
        List of all team OL rankings
    """
    logger.info("Fetching offensive line rankings")
    
    # Try to get from cache first
    rankings = get_ol_rankings_cache()
    if rankings is not None:
        logger.info("Using cached offensive line rankings")
        return rankings
    
    # Cache miss, fetch fresh data
    logger.info("Cache miss, fetching fresh offensive line rankings")
    try:
        rankings = fetch_pff_ol_rankings()
        set_ol_rankings_cache(rankings)
        logger.info(f"Successfully cached {len(rankings)} team OL rankings")
        return rankings
    except Exception as e:
        logger.error(f"Error fetching offensive line rankings: {e}")
        raise

def get_ol_rankings_by_team_cached(team_name: str) -> Dict:
    """
    Get offensive line ranking for a specific team (cached).
    
    Args:
        team_name: Name of the team to find
        
    Returns:
        Team OL ranking data or empty dict if not found
    """
    all_rankings = get_all_ol_rankings()
    team_name_lower = team_name.lower()
    
    for ranking in all_rankings:
        if ranking.get("team", "").lower() == team_name_lower:
            return ranking
    
    return {}

def get_top_ol_rankings_cached(top_n: int = 10) -> List[Dict]:
    """
    Get top N offensive line rankings (cached).
    
    Args:
        top_n: Number of top teams to return
        
    Returns:
        List of top N OL rankings
    """
    all_rankings = get_all_ol_rankings()
    return all_rankings[:top_n]

def get_ol_rankings_by_rank_range_cached(min_rank: int, max_rank: int) -> List[Dict]:
    """
    Get offensive line rankings within a specific rank range (cached).
    
    Args:
        min_rank: Minimum rank
        max_rank: Maximum rank
        
    Returns:
        List of OL rankings within the range
    """
    all_rankings = get_all_ol_rankings()
    return [
        ranking for ranking in all_rankings 
        if min_rank <= ranking.get("rank", 999) <= max_rank
    ]

def get_ol_rankings_stats() -> Dict:
    """
    Get statistics about the offensive line rankings dataset.
    
    Returns:
        Dictionary with dataset statistics
    """
    rankings = get_all_ol_rankings()
    
    if not rankings:
        return {"error": "No OL rankings loaded"}
    
    # Basic stats
    total_teams = len(rankings)
    
    # Rank distribution
    rank_distribution = {}
    for ranking in rankings:
        rank = ranking.get("rank", 0)
        if rank <= 10:
            rank_distribution["top_10"] = rank_distribution.get("top_10", 0) + 1
        elif rank <= 20:
            rank_distribution["11_20"] = rank_distribution.get("11_20", 0) + 1
        elif rank <= 32:
            rank_distribution["21_32"] = rank_distribution.get("21_32", 0) + 1
    
    # Extract PFF grades if available
    pff_grades = []
    for ranking in rankings:
        key_details = ranking.get("key_details", {})
        if "pff_overall_grade" in key_details:
            pff_grades.append(key_details["pff_overall_grade"])
    
    grade_stats = {}
    if pff_grades:
        grade_stats = {
            "count": len(pff_grades),
            "min": min(pff_grades),
            "max": max(pff_grades),
            "avg": sum(pff_grades) / len(pff_grades)
        }
    
    return {
        "total_teams": total_teams,
        "rank_distribution": rank_distribution,
        "pff_grade_statistics": grade_stats
    }
