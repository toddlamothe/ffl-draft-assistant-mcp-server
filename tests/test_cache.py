import os
import tempfile
import time
import json
from app.cache import cache

def test_injuries_cache_set_and_get(monkeypatch):
    """Test setting and getting injuries cache with TTL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "nfl_injuries.json")
        monkeypatch.setattr(cache, "INJURIES_CACHE_FILE", cache_file)
        monkeypatch.setattr(cache, "INJURIES_CACHE_TTL", 1)  # 1 second for test
        
        injuries = [{"team": "Test", "injuries": []}]
        cache.set_injuries_cache(injuries)
        assert cache.get_injuries_cache() == injuries
        
        time.sleep(2)
        assert cache.get_injuries_cache() is None

def test_ratings_cache_set_and_get(monkeypatch):
    """Test setting and getting ratings cache with TTL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "madden_ratings.json")
        monkeypatch.setattr(cache, "RATINGS_CACHE_FILE", cache_file)
        monkeypatch.setattr(cache, "RATINGS_CACHE_TTL", 1)  # 1 second for test
        
        ratings = [{"name": "Test Player", "overall": 85}]
        cache.set_ratings_cache(ratings)
        assert cache.get_ratings_cache() == ratings
        
        time.sleep(2)
        assert cache.get_ratings_cache() is None

def test_generic_cache_functions(monkeypatch):
    """Test the generic cache functions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "test_cache.json")
        ttl = 1  # 1 second for test
        
        test_data = {"test": "data"}
        cache.set_cache_data(test_data, cache_file)
        assert cache.get_cache_data(cache_file, ttl) == test_data
        
        time.sleep(2)
        assert cache.get_cache_data(cache_file, ttl) is None

def test_cache_file_creation(monkeypatch):
    """Test that cache directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = os.path.join(tmpdir, "new_cache_dir")
        cache_file = os.path.join(cache_dir, "test.json")
        
        # Ensure directory doesn't exist
        assert not os.path.exists(cache_dir)
        
        test_data = {"test": "data"}
        cache.set_cache_data(test_data, cache_file)
        
        # Directory should be created
        assert os.path.exists(cache_dir)
        assert os.path.exists(cache_file)

def test_backward_compatibility(monkeypatch):
    """Test backward compatibility functions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "nfl_injuries.json")
        monkeypatch.setattr(cache, "INJURIES_CACHE_FILE", cache_file)
        monkeypatch.setattr(cache, "INJURIES_CACHE_TTL", 1)  # 1 second for test
        
        injuries = [{"team": "Test", "injuries": []}]
        cache.set_cache(injuries)  # Old function name
        assert cache.get_cache() == injuries  # Old function name
