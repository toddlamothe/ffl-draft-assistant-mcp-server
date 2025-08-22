import pandas as pd
import os
from typing import List, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Path to the PFF CSV file
PFF_CSV_PATH = Path(__file__).parent.parent.parent / "data" / "pff_ratings.csv"

def load_pff_ratings() -> List[Dict]:
    """
    Load PFF player ratings from CSV file.
    
    Returns:
        List of dictionaries containing player rating data
    """
    try:
        if not PFF_CSV_PATH.exists():
            logger.error(f"PFF ratings file not found at {PFF_CSV_PATH}")
            logger.info("Please place your PFF ratings CSV file at: data/pff_ratings.csv")
            return []
        
        logger.info(f"Loading PFF ratings from {PFF_CSV_PATH}")
        
        # Read CSV with skiprows=1 to skip the empty first line
        df = pd.read_csv(PFF_CSV_PATH, skiprows=1)
        
        # Convert DataFrame to list of dictionaries
        ratings = []
        for _, row in df.iterrows():
            # Handle the specific column structure of the user's CSV
            rating = {
                "name": row.get("Full Name", row.get("name", row.get("player", row.get("player_name", "")))),
                "position": row.get("Position", row.get("position", row.get("pos", ""))).upper(),
                "team": row.get("Team Abbreviation", row.get("team", row.get("team_name", ""))),
                "overall_rank": row.get("Overall Rank", row.get("overall", row.get("rating", row.get("grade", 0)))),
                "position_rank": row.get("Position Rank", row.get("rank", row.get("position_rank", None))),
                "bye_week": row.get("Bye Week", row.get("bye", None)),
                "adp": row.get("ADP", row.get("adp", None)),
                "projected_points": row.get("Projected Points", row.get("projected_points", row.get("points", None))),
                "auction_value": row.get("Auction Value", row.get("auction_value", row.get("value", None))),
                "source": "Pro Football Focus"
            }
            
            # Clean up the data - remove None values and empty strings
            rating = {k: v for k, v in rating.items() if v is not None and v != "" and v != "null" and v != "N/A"}
            ratings.append(rating)
        
        logger.info(f"Successfully loaded {len(ratings)} PFF ratings")
        return ratings
        
    except Exception as e:
        logger.error(f"Error loading PFF ratings: {e}")
        return []

def get_all_pff_ratings() -> List[Dict]:
    """
    Get all PFF player ratings.
    
    Returns:
        List of all PFF player ratings
    """
    return load_pff_ratings()

def get_pff_ratings_by_position(position: str) -> List[Dict]:
    """
    Get PFF ratings filtered by position.
    
    Args:
        position: Position to filter by (QB, RB, WR, TE, etc.)
        
    Returns:
        List of PFF ratings for the specified position
    """
    ratings = load_pff_ratings()
    position_upper = position.upper()
    return [rating for rating in ratings if rating.get("position") == position_upper]

def get_pff_ratings_by_team(team: str) -> List[Dict]:
    """
    Get PFF ratings filtered by team.
    
    Args:
        team: Team name to filter by
        
    Returns:
        List of PFF ratings for the specified team
    """
    ratings = load_pff_ratings()
    return [rating for rating in ratings if rating.get("team", "").lower() == team.lower()]

def get_pff_ratings_by_rank_range(min_rank: int, max_rank: int) -> List[Dict]:
    """
    Get PFF ratings within a specific overall rank range.
    
    Args:
        min_rank: Minimum overall rank
        max_rank: Maximum overall rank
        
    Returns:
        List of PFF ratings within the rank range
    """
    ratings = load_pff_ratings()
    return [
        rating for rating in ratings 
        if rating.get("overall_rank") is not None 
        and min_rank <= rating["overall_rank"] <= max_rank
    ]

def get_top_pff_ratings_by_position(position: str, top_n: int = 10) -> List[Dict]:
    """
    Get top N PFF ratings for a specific position.
    
    Args:
        position: Position to filter by
        top_n: Number of top players to return
        
    Returns:
        List of top N PFF ratings for the position
    """
    position_ratings = get_pff_ratings_by_position(position)
    
    # Sort by overall rank (lower rank = better)
    def sort_key(rating):
        return rating.get("overall_rank", 999) or 999
    
    sorted_ratings = sorted(position_ratings, key=sort_key)
    return sorted_ratings[:top_n]

def get_pff_player_by_name(player_name: str) -> Optional[Dict]:
    """
    Get PFF rating for a specific player by name.
    
    Args:
        player_name: Name of the player to find
        
    Returns:
        Player rating data or None if not found
    """
    ratings = load_pff_ratings()
    player_name_lower = player_name.lower()
    
    for rating in ratings:
        if rating.get("name", "").lower() == player_name_lower:
            return rating
    
    return None

def get_pff_stats() -> Dict:
    """
    Get statistics about the PFF ratings dataset.
    
    Returns:
        Dictionary with dataset statistics
    """
    ratings = load_pff_ratings()
    
    if not ratings:
        return {"error": "No PFF ratings loaded"}
    
    # Count by position
    position_counts = {}
    for rating in ratings:
        pos = rating.get("position", "Unknown")
        position_counts[pos] = position_counts.get(pos, 0) + 1
    
    # Count by team
    team_counts = {}
    for rating in ratings:
        team = rating.get("team", "Unknown")
        team_counts[team] = team_counts.get(team, 0) + 1
    
    # Rank statistics
    ranks = [r.get("overall_rank") for r in ratings if r.get("overall_rank") is not None]
    rank_stats = {
        "count": len(ranks),
        "min": min(ranks) if ranks else None,
        "max": max(ranks) if ranks else None,
        "avg": sum(ranks) / len(ranks) if ranks else None
    }
    
    # Projected points statistics
    points = [r.get("projected_points") for r in ratings if r.get("projected_points") is not None]
    points_stats = {
        "count": len(points),
        "min": min(points) if points else None,
        "max": max(points) if points else None,
        "avg": sum(points) / len(points) if points else None
    }
    
    return {
        "total_players": len(ratings),
        "position_counts": position_counts,
        "team_counts": team_counts,
        "rank_statistics": rank_stats,
        "projected_points_statistics": points_stats
    }
