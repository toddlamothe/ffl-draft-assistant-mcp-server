import pytest
from unittest.mock import patch, Mock
from app.scraper.madden_ratings import fetch_madden_ratings, extract_player_data

MOCK_HTML = '''
<tr class="Table_row__eoyUr">
    <td class="Table_cell__qBFwB" data-type="profile">
        <div class="Table_centerCell__Sr9MG">
            <a class="Table_profileCellAnchor__Zj6g4" href="/games/madden-nfl/ratings/player-ratings/devon-witherspoon/23023">
                <div class="Table_profileCell__ZoaSs Table_anchorCell__n9X1R">
                    <div class="Table_profileContent__0t2_u">
                        <span class="Table_profileLabel__tuyG0">Devon Witherspoon</span>
                    </div>
                </div>
            </a>
        </div>
    </td>
    <td class="Table_cell__qBFwB" data-type="profile">
        <a class="Table_centerCell__Sr9MG Table_anchorCell__n9X1R" href="/games/madden-nfl/ratings/positions-ratings/cornerback/CB">
            <span class="Table_tag__vKZKn">CB</span>
        </a>
    </td>
    <td class="Table_cell__qBFwB">
        <a class="Table_centerCell__Sr9MG Table_anchorCell__n9X1R" href="/games/madden-nfl/ratings/teams-ratings/seattle-seahawks/28">
            <img alt="Seattle Seahawks" class="Picture_image__L8suG" src="seahawks.png"/>
        </a>
    </td>
    <td class="Table_cell__qBFwB">
        <div class="Table_centerCell__Sr9MG">
            <div class="Table_statCell__jDTje" data-label="OVR">
                <div class="Table_statCellValueContent__eSIUF">
                    <div class="Table_statCellValueWithLabel__54LUo">
                        <span class="Table_statCellValue__zn5Cx">88</span>
                    </div>
                </div>
            </div>
        </div>
    </td>
</tr>
'''

EMPTY_PAGE_HTML = """<table></table>"""

@patch("httpx.get")
def test_fetch_madden_ratings(mock_get):
    """Test fetching Madden ratings from the website."""
    def side_effect(url, timeout):
        # Return the mock data for the base page, empty for any pagination
        if url.endswith("ratings") and "page=" not in url:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = MOCK_HTML
            mock_response.raise_for_status = Mock()
            return mock_response
        else:
            # Return empty page for any pagination attempts
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = EMPTY_PAGE_HTML
            mock_response.raise_for_status = Mock()
            return mock_response
    
    mock_get.side_effect = side_effect
    
    ratings = fetch_madden_ratings()
    
    assert isinstance(ratings, list)
    assert len(ratings) == 1
    assert ratings[0]["name"] == "Devon Witherspoon"
    assert ratings[0]["position"] == "CB"
    assert ratings[0]["team"] == "Seattle Seahawks"
    assert ratings[0]["overall"] == 88
    assert ratings[0]["source"] == "Madden NFL"

@patch("httpx.get")
def test_fetch_madden_ratings_http_error(mock_get):
    """Test handling of HTTP errors."""
    mock_get.side_effect = Exception("Network error")
    
    # With pagination, errors are caught and return empty results
    ratings = fetch_madden_ratings()
    assert ratings == []

def test_extract_player_data():
    """Test extracting player data from a table row."""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(MOCK_HTML, "html.parser")
    row = soup.find("tr", class_="Table_row__eoyUr")
    
    player_data = extract_player_data(row)
    
    assert player_data is not None
    assert player_data["name"] == "Devon Witherspoon"
    assert player_data["position"] == "CB"
    assert player_data["team"] == "Seattle Seahawks"
    assert player_data["overall"] == 88
    assert player_data["source"] == "Madden NFL"

def test_extract_player_data_invalid_row():
    """Test extracting player data from invalid row."""
    from bs4 import BeautifulSoup
    
    invalid_html = '<tr class="Table_row__eoyUr"><td>No player data</td></tr>'
    soup = BeautifulSoup(invalid_html, "html.parser")
    row = soup.find("tr")
    
    player_data = extract_player_data(row)
    
    assert player_data is None
