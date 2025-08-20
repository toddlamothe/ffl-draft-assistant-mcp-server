from app.scraper.nfl_injuries import fetch_nfl_injuries
from app.cache.cache import get_injuries_cache, set_injuries_cache
from typing import List, Dict

def get_all_injuries() -> List[Dict]:
    injuries = get_injuries_cache()
    if injuries is not None:
        return injuries
    injuries = fetch_nfl_injuries()
    set_injuries_cache(injuries)
    return injuries
