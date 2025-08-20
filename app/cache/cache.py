import os
import json
import time
from typing import Any, Optional

CACHE_DIR = os.path.join(os.path.dirname(__file__), "data")
CACHE_FILE = os.path.join(CACHE_DIR, "nfl_injuries.json")
CACHE_TTL = 60 * 60 * 24  # 24 hours

os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache() -> Optional[Any]:
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, "r") as f:
        data = json.load(f)
    if time.time() - data.get("timestamp", 0) > CACHE_TTL:
        return None
    return data.get("injuries")

def set_cache(injuries: Any):
    with open(CACHE_FILE, "w") as f:
        json.dump({"timestamp": time.time(), "injuries": injuries}, f)
