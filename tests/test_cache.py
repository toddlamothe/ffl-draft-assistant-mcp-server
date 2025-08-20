import os
import tempfile
import time
import json
from app.cache import cache

def test_cache_set_and_get(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "nfl_injuries.json")
        monkeypatch.setattr(cache, "CACHE_FILE", cache_file)
        monkeypatch.setattr(cache, "CACHE_TTL", 1)  # 1 second for test
        injuries = [{"team": "Test", "injuries": []}]
        cache.set_cache(injuries)
        assert cache.get_cache() == injuries
        time.sleep(2)
        assert cache.get_cache() is None
