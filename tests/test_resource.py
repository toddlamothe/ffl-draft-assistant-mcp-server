import pytest
from unittest.mock import patch
from app.resources import nfl_injuries_resource

def test_get_all_injuries_cache_hit(monkeypatch):
    monkeypatch.setattr(nfl_injuries_resource, "get_cache", lambda: ["cached"])
    monkeypatch.setattr(nfl_injuries_resource, "fetch_nfl_injuries", lambda: ["fresh"])
    monkeypatch.setattr(nfl_injuries_resource, "set_cache", lambda x: None)
    result = nfl_injuries_resource.get_all_injuries()
    assert result == ["cached"]

def test_get_all_injuries_cache_miss(monkeypatch):
    monkeypatch.setattr(nfl_injuries_resource, "get_cache", lambda: None)
    monkeypatch.setattr(nfl_injuries_resource, "fetch_nfl_injuries", lambda: ["fresh"])
    called = {}
    def fake_set_cache(x):
        called["set"] = x
    monkeypatch.setattr(nfl_injuries_resource, "set_cache", fake_set_cache)
    result = nfl_injuries_resource.get_all_injuries()
    assert result == ["fresh"]
    assert called["set"] == ["fresh"]
