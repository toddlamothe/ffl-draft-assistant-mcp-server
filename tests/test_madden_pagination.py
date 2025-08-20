import pytest
from unittest.mock import patch, Mock
from app.scraper.madden_ratings import fetch_madden_ratings

PAGE_BASE_HTML = '''
<table>
  <tr class="Table_row__eoyUr">
    <td>
      <span class="Table_profileLabel__tuyG0">Player One</span>
      <span class="Table_tag__vKZKn">QB</span>
      <img alt="New England Patriots" />
      <span class="Table_statCellValue__zn5Cx">80</span>
    </td>
  </tr>
</table>
'''

PAGE_2_HTML = '''
<table>
  <tr class="Table_row__eoyUr">
    <td>
      <span class="Table_profileLabel__tuyG0">Player Two</span>
      <span class="Table_tag__vKZKn">WR</span>
      <img alt="Kansas City Chiefs" />
      <span class="Table_statCellValue__zn5Cx">90</span>
    </td>
  </tr>
</table>
'''

EMPTY_PAGE_HTML = """<table></table>"""


def _make_response(html: str):
    m = Mock()
    m.status_code = 200
    m.text = html
    m.raise_for_status = Mock()
    return m


@patch("httpx.get")
def test_fetch_madden_ratings_paginates(mock_get):
    def side_effect(url, timeout):
        if url.endswith("ratings"):
            return _make_response(PAGE_BASE_HTML)
        if url.endswith("page=2"):
            return _make_response(PAGE_2_HTML)
        # page=3 or beyond returns empty
        return _make_response(EMPTY_PAGE_HTML)

    mock_get.side_effect = side_effect

    players = fetch_madden_ratings()
    names = {p["name"] for p in players}

    assert "Player One" in names
    assert "Player Two" in names
    assert len(players) == 2
