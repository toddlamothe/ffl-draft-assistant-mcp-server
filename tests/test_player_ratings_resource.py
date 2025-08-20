import pytest
from unittest.mock import patch, Mock
from app.resources.player_ratings_resource import (
    get_all_player_ratings,
    get_player_ratings_by_source,
    get_player_ratings_by_position,
    get_player_ratings_by_team
)

MOCK_RATINGS = [
    {
        "name": "Devon Witherspoon",
        "position": "CB",
        "team": "Seattle Seahawks",
        "overall": 88,
        "source": "Madden NFL"
    },
    {
        "name": "Patrick Mahomes",
        "position": "QB",
        "team": "Kansas City Chiefs",
        "overall": 95,
        "source": "Madden NFL"
    },
    {
        "name": "Christian McCaffrey",
        "position": "RB",
        "team": "San Francisco 49ers",
        "overall": 93,
        "source": "Madden NFL"
    }
]

def test_get_all_player_ratings_cache_hit(monkeypatch):
    """Test getting player ratings when cache has data."""
    def mock_get_cache():
        return MOCK_RATINGS
    
    def mock_set_cache(ratings):
        pass
    
    monkeypatch.setattr("app.resources.player_ratings_resource.get_ratings_cache", mock_get_cache)
    monkeypatch.setattr("app.resources.player_ratings_resource.set_ratings_cache", mock_set_cache)
    
    result = get_all_player_ratings()
    assert result == MOCK_RATINGS

def test_get_all_player_ratings_cache_miss(monkeypatch):
    """Test getting player ratings when cache is empty."""
    def mock_get_cache():
        return None
    
    def mock_set_cache(ratings):
        pass
    
    def mock_get_all_madden_ratings():
        return MOCK_RATINGS
    
    monkeypatch.setattr("app.resources.player_ratings_resource.get_ratings_cache", mock_get_cache)
    monkeypatch.setattr("app.resources.player_ratings_resource.set_ratings_cache", mock_set_cache)
    monkeypatch.setattr("app.resources.player_ratings_resource.get_all_madden_ratings", mock_get_all_madden_ratings)
    
    result = get_all_player_ratings()
    assert result == MOCK_RATINGS

def test_get_player_ratings_by_source(monkeypatch):
    """Test filtering player ratings by source."""
    def mock_get_all_ratings():
        return MOCK_RATINGS
    
    monkeypatch.setattr("app.resources.player_ratings_resource.get_all_player_ratings", mock_get_all_ratings)
    
    result = get_player_ratings_by_source("Madden NFL")
    assert len(result) == 3
    assert all(rating["source"] == "Madden NFL" for rating in result)
    
    result = get_player_ratings_by_source("Unknown Source")
    assert len(result) == 0

def test_get_player_ratings_by_position(monkeypatch):
    """Test filtering player ratings by position."""
    def mock_get_all_ratings():
        return MOCK_RATINGS
    
    monkeypatch.setattr("app.resources.player_ratings_resource.get_all_player_ratings", mock_get_all_ratings)
    
    result = get_player_ratings_by_position("QB")
    assert len(result) == 1
    assert result[0]["name"] == "Patrick Mahomes"
    
    result = get_player_ratings_by_position("WR")
    assert len(result) == 0

def test_get_player_ratings_by_team(monkeypatch):
    """Test filtering player ratings by team."""
    def mock_get_all_ratings():
        return MOCK_RATINGS
    
    monkeypatch.setattr("app.resources.player_ratings_resource.get_all_player_ratings", mock_get_all_ratings)
    
    result = get_player_ratings_by_team("Seattle Seahawks")
    assert len(result) == 1
    assert result[0]["name"] == "Devon Witherspoon"
    
    result = get_player_ratings_by_team("Unknown Team")
    assert len(result) == 0
