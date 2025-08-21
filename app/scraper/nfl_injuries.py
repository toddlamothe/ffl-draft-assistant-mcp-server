import httpx
from bs4 import BeautifulSoup
from typing import List, Dict

ESPN_INJURIES_URL = "https://www.espn.com/nfl/injuries"

def fetch_nfl_injuries() -> List[Dict]:
    """Fetch and parse NFL injuries from ESPN."""
    response = httpx.get(ESPN_INJURIES_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    teams = []
    for team_section in soup.select(".Table__Title, .Table__Scroller"):
        if 'Table__Title' in team_section.get('class', []):
            team_name = team_section.text.strip()
            current_team = {"team": team_name, "injuries": []}
            teams.append(current_team)
        elif 'Table__Scroller' in team_section.get('class', []):
            for row in team_section.select("tbody tr"):
                cols = [td.text.strip() for td in row.find_all("td")]
                if len(cols) >= 5:
                    player, pos, injury, status, estimated_return = cols[:5]
                    current_team["injuries"].append({
                        "player": player,
                        "position": pos,
                        "injury": injury,
                        "status": status,
                        "estimated_return": estimated_return
                    })
    return teams
