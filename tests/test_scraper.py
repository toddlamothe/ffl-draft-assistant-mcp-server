import pytest
from unittest.mock import patch
from app.scraper.nfl_injuries import fetch_nfl_injuries

MOCK_HTML = '''<div class="Table__Title">Team A</div><div class="Table__Scroller"><table><tbody><tr><td>Player 1</td><td>QB</td><td>Knee</td><td>Out</td><td>2024-06-01</td></tr></tbody></table></div>'''

@patch("httpx.get")
def test_fetch_nfl_injuries(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = MOCK_HTML
    injuries = fetch_nfl_injuries()
    assert isinstance(injuries, list)
    assert injuries[0]["team"] == "Team A"
    assert injuries[0]["injuries"][0]["player"] == "Player 1"
