from app.scraper.nfl_injuries import fetch_nfl_injuries
from app.cache.cache import get_cache, set_cache
from typing import List, Dict

def get_all_injuries() -> List[Dict]:
    injuries = get_cache()
    if injuries is not None:
        return injuries
    injuries = fetch_nfl_injuries()
    set_cache(injuries)
    return injuries
