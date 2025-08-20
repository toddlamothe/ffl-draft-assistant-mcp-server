import os
import json
import time
from typing import Any, Optional

CACHE_DIR = "/tmp/pigskin-pickem-cache"
INJURIES_CACHE_FILE = os.path.join(CACHE_DIR, "nfl_injuries.json")
RATINGS_CACHE_FILE = os.path.join(CACHE_DIR, "madden_ratings.json")
INJURIES_CACHE_TTL = 60 * 60 * 24  # 24 hours
RATINGS_CACHE_TTL = 60 * 60 * 48  # 48 hours

os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_data(cache_file: str, ttl: int) -> Optional[Any]:
    """Generic cache getter with TTL check."""
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file, "r") as f:
            data = json.load(f)
        if time.time() - data.get("timestamp", 0) > ttl:
            return None
        return data.get("data")
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading cache file {cache_file}: {e}")
        return None

def set_cache_data(data: Any, cache_file: str):
    """Generic cache setter."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump({"timestamp": time.time(), "data": data}, f)
    except IOError as e:
        print(f"Error writing cache file {cache_file}: {e}")

# NFL Injuries cache functions
def get_injuries_cache() -> Optional[Any]:
    """Get cached NFL injuries data."""
    return get_cache_data(INJURIES_CACHE_FILE, INJURIES_CACHE_TTL)

def set_injuries_cache(injuries: Any):
    """Set cached NFL injuries data."""
    set_cache_data(injuries, INJURIES_CACHE_FILE)

# Madden Ratings cache functions  
def get_ratings_cache() -> Optional[Any]:
    """Get cached Madden ratings data."""
    return get_cache_data(RATINGS_CACHE_FILE, RATINGS_CACHE_TTL)

def set_ratings_cache(ratings: Any):
    """Set cached Madden ratings data."""
    set_cache_data(ratings, RATINGS_CACHE_FILE)

# Backward compatibility
def get_cache() -> Optional[Any]:
    """Backward compatibility function for injuries cache."""
    return get_injuries_cache()

def set_cache(injuries: Any):
    """Backward compatibility function for injuries cache."""
    set_injuries_cache(injuries)
